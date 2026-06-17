# Custom Evaluation Set

Our evaluation measures **action-item extraction** — the system's core, objectively-scorable task — on **30 real meeting recordings** (~32 min each). Gold labels are the team's own work (the rubric's "primary evidence").

## Files & workflow

| File | What it is |
|---|---|
| `transcribe_all.py` | Transcribes the 30 `.wav` recordings → `transcripts/*.txt` (run once) |
| `transcripts/` | Whisper transcripts (committed; the raw audio is **not** in the repo — too large) |
| `build_template.py` | Builds `eval_set.jsonl` + `gold_template.csv` from the transcripts |
| `gold_template.csv` | **Team fills this** — the expected action items per meeting |
| `gold_action_items.csv` | The finished gold labels (rename the template to this) |
| `evaluate.py` | Runs the real system on each transcript, scores **precision / recall / F1** |
| `results.json` | Output numbers (goes in the report) |

## Steps

1. `python data/eval/transcribe_all.py` → produces `transcripts/`  ✅ (running/done)
2. `python data/eval/build_template.py` → produces `gold_template.csv`
3. **Label** — for each meeting, add a row per expected action item (`meeting_id, task, owner, deadline`). A meeting with no action items = leave it with no item rows. Save as `gold_action_items.csv`.
4. `python data/eval/evaluate.py` → prints precision/recall/F1, writes `results.json`.

## How to label (for everyone)

Open `gold_template.csv` in Excel / Google Sheets. For each meeting, write down the action items a human would extract — a concrete task someone committed to, plus the owner and deadline **only if actually stated**. Be consistent; this is the gold standard we score against, so the team must agree on what counts as an action item (write that rule down — you defend it in Q&A).

## Matching rule (documented decision)

A predicted action item counts as correct if, for the same meeting, it matches a gold item on **owner** (equal or empty) and **task text similarity ≥ 0.6**. Greedy one-to-one. See the docstring in `evaluate.py`.
