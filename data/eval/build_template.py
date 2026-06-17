"""Build the labeling artifacts once transcripts exist.

Generates:
  - eval_set.jsonl       : {id, transcript} per meeting (canonical eval input)
  - gold_template.csv    : meeting_id, task, owner, deadline  (team fills this in)

The team hand-labels the EXPECTED action items in gold_template.csv (rename to
gold_action_items.csv when done). A meeting with no action items = no rows for it.

Run after transcription:  .venv/bin/python data/eval/build_template.py
"""

import csv
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
TRANSCRIPTS = HERE / "transcripts"


def natural_key(p: Path) -> int:
    nums = re.findall(r"\d+", p.name)
    return int(nums[0]) if nums else 0


def main() -> None:
    files = sorted(TRANSCRIPTS.glob("*.txt"), key=natural_key)
    if not files:
        print("No transcripts yet. Run transcribe_all.py first.")
        return

    # 1) canonical eval input
    with (HERE / "eval_set.jsonl").open("w", encoding="utf-8") as fh:
        for f in files:
            fh.write(json.dumps({"id": f.stem, "transcript": f.read_text(encoding="utf-8")}) + "\n")

    # 2) labeling template (one example blank row per meeting)
    with (HERE / "gold_template.csv").open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["meeting_id", "task", "owner", "deadline"])
        for f in files:
            w.writerow([f.stem, "", "", ""])  # team fills task/owner/deadline; add rows as needed

    print(f"Wrote eval_set.jsonl and gold_template.csv for {len(files)} meetings.")
    print("→ Team: fill expected action items in gold_template.csv, then save it as gold_action_items.csv")


if __name__ == "__main__":
    main()
