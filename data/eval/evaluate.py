"""Evaluate SummarAI's action-item extraction against the team's gold labels.

Runs the REAL system (reuses src.app.analyze — same model + prompt) on each
transcript, then scores predicted action items vs the hand-labeled gold set.

Matching rule (the team's documented decision — defend this in Q&A):
  A predicted action item is a TRUE POSITIVE if there is an unmatched gold item
  for the same meeting where:
    - task text similarity >= TASK_THRESHOLD (difflib ratio on normalized text), AND
    - owners match (normalized equal, or both empty/unspecified).
  Matching is greedy and one-to-one. Leftover predictions = false positives;
  leftover gold = false negatives.

Outputs precision / recall / F1 (micro), a per-meeting table, and results.json.

Run after labeling:  .venv/bin/python data/eval/evaluate.py
"""

import csv
import json
import sys
from difflib import SequenceMatcher
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT))

from src.app import analyze  # noqa: E402  (reuse the real pipeline)

GOLD = HERE / "gold_action_items.csv"
EVAL_SET = HERE / "eval_set.jsonl"
TASK_THRESHOLD = 0.6


def norm(s: str) -> str:
    return " ".join((s or "").lower().split())


def owners_match(a: str, b: str) -> bool:
    a, b = norm(a), norm(b)
    if not a and not b:
        return True
    return a == b or a in b or b in a


def task_sim(a: str, b: str) -> float:
    return SequenceMatcher(None, norm(a), norm(b)).ratio()


def match(pred: list[dict], gold: list[dict]) -> tuple[int, int, int]:
    """Return (true_positives, false_positives, false_negatives) for one meeting."""
    used = set()
    tp = 0
    for p in pred:
        best_j, best_score = -1, 0.0
        for j, g in enumerate(gold):
            if j in used:
                continue
            if not owners_match(p.get("owner") or "", g.get("owner") or ""):
                continue
            s = task_sim(p.get("task") or "", g.get("task") or "")
            if s > best_score:
                best_j, best_score = j, s
        if best_j >= 0 and best_score >= TASK_THRESHOLD:
            used.add(best_j)
            tp += 1
    fp = len(pred) - tp
    fn = len(gold) - len(used)
    return tp, fp, fn


def load_gold() -> dict[str, list[dict]]:
    gold: dict[str, list[dict]] = {}
    with GOLD.open(encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            mid = (row.get("meeting_id") or "").strip()
            task = (row.get("task") or "").strip()
            if not mid or not task:  # blank template rows / no-action meetings
                gold.setdefault(mid, [])
                continue
            gold.setdefault(mid, []).append(
                {"task": task, "owner": (row.get("owner") or "").strip(),
                 "deadline": (row.get("deadline") or "").strip()}
            )
    return gold


def main() -> None:
    if not GOLD.exists():
        print(f"Missing {GOLD.name}. Fill gold_template.csv and save it as gold_action_items.csv.")
        return
    transcripts = {json.loads(line)["id"]: json.loads(line)["transcript"]
                   for line in EVAL_SET.read_text(encoding="utf-8").splitlines() if line.strip()}
    gold = load_gold()

    rows, TP, FP, FN = [], 0, 0, 0
    for mid in sorted(transcripts, key=lambda x: (len(x), x)):
        result = analyze(transcripts[mid])
        pred = result.get("action_items", [])
        tp, fp, fn = match(pred, gold.get(mid, []))
        TP, FP, FN = TP + tp, FP + fp, FN + fn
        rows.append({"meeting": mid, "pred": len(pred), "gold": len(gold.get(mid, [])),
                     "tp": tp, "fp": fp, "fn": fn})
        print(f"  {mid:<14} pred={len(pred):>2} gold={len(gold.get(mid, [])):>2} "
              f"TP={tp} FP={fp} FN={fn}", flush=True)

    precision = TP / (TP + FP) if TP + FP else 0.0
    recall = TP / (TP + FN) if TP + FN else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0

    summary = {"meetings": len(rows), "TP": TP, "FP": FP, "FN": FN,
               "precision": round(precision, 3), "recall": round(recall, 3), "f1": round(f1, 3)}
    (HERE / "results.json").write_text(json.dumps({"summary": summary, "per_meeting": rows}, indent=2))

    print("\n" + "=" * 48)
    print(f"  Meetings : {len(rows)}")
    print(f"  Precision: {precision:.3f}")
    print(f"  Recall   : {recall:.3f}")
    print(f"  F1       : {f1:.3f}")
    print("=" * 48)
    print("Saved results.json")


if __name__ == "__main__":
    main()
