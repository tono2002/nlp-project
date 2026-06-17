# SummarAI: One-Day Finish Roadmap

**Goal:** complete every deliverable in one day. Two tracks run in **parallel** so nobody is blocked.

**Team split:**
- 🛠️ **Technical**: Antonio, Martí, Bojana
- ✍️ **Content**: Jo, Smaragda
- 👥 **Everyone**: shared tasks (labeling, reflections, rehearsal)

> The single most important output is the **custom evaluation** (Phase 2). It carries the grade. Protect that time.

---

## Phase 0: Kickoff (30 min · everyone)

- [ ] Pull latest `main`, confirm the app runs locally (`uvicorn src.app:app`).
- [ ] Agree on the **action-item matching rule** for scoring (e.g. a predicted action "counts" if task meaning matches a gold action AND owner matches). This is a *team decision*, write it down, you must defend it in Q&A.
- [ ] Confirm everyone can open the app and produce a summary.

---

## Phase 1: Build the gold test set (morning · EVERYONE, ~1.5h)

The "intellectual" core the rubric rewards, must be the team's own work.

- [ ] Each person creates **8–10 short meeting transcripts** (≈ 45 total) → exceeds the 30–50 requirement.
  - Mix: standups, planning, sales, project syncs; include 2–3 tricky ones (no action items, ambiguous owners, overlapping speakers).
  - Realistic, messy text is good, that's what stresses the model.
- [ ] For **each** transcript, hand-label the **expected action items** (`task`, `owner`, `deadline`) → this is the gold standard.
- [ ] Save everything in one file: `data/eval/eval_set.jsonl` (one JSON object per line: `{"id", "transcript", "expected_action_items": [...]}`).

**Owners:** all 5 (≈ 9 each). Jo & Smaragda can also pull realistic transcripts from public meeting minutes and label them.

---

## Phase 2: TECHNICAL TRACK 🛠️ (Antonio · Martí · Bojana)

### 2A. Evaluation harness (Martí + Bojana, ~2–3h): CRITICAL PATH
- [ ] `data/eval/evaluate.py`: load `eval_set.jsonl`, call the app on each transcript, compare predicted vs gold action items using the agreed matching rule.
- [ ] Compute **precision / recall / F1** for action-item extraction; also report % takeaways correctly typed (decision/note).
- [ ] Output a results table + save raw predictions to `data/eval/results.json`.
- [ ] **Run it** on the full set → record the numbers.

### 2B. App + repro polish (Antonio, ~2h)
- [ ] Document the real system prompt + JSON schema in `prompts/` (`prompts/system_prompt.md`).
- [ ] Finish `docs/installation_guide.md` (exact steps: venv, `pip install -r requirements.txt`, `.env`, run, install `faster-whisper`).
- [ ] Quick code cleanup; confirm `requirements.txt` is complete.
- [ ] *(Optional, only if time)* deploy to Render/Railway (not Vercel, local Whisper) and add the link.

### 2C. Failure-mode analysis (whoever finishes first, ~1h)
- [ ] From the eval misses, document **5–10 failure cases** with hypotheses. Seed examples we already have:
  - Whisper mishears proper names (e.g. *Bojana → "Janna"*) → wrong action-item owner.
  - Non-meeting input (podcast) correctly yields **zero** action items (good behavior, note why).
  - Long meetings: transcription latency (~8 min for 20 min audio).
- [ ] Save as `data/eval/failure_analysis.md`.

---

## Phase 3: CONTENT TRACK ✍️ (Jo · Smaragda): runs in parallel with Phase 2

### 3A. Field review (Jo, ~2–3h)
- [ ] Research the meeting-AI / transcription industry: Otter, Fireflies, Zoom AI Companion, Fathom, tl;dv.
- [ ] Write trends, major players, gaps, and what SummarAI does differently (typed takeaways, owned action items, project memory).
- [ ] Drop into the report's Field Review section + cite 4–6 sources (Google Scholar / arXiv / Papers with Code).

### 3B. Executive summary + manuals (Smaragda, ~2–3h)
- [ ] `deliverables/executive_summary.md`, 1 page, non-technical: what it does, why it matters, what we found (add the eval numbers once Phase 2 finishes).
- [ ] Finish `docs/user_manual.md`, how an end user operates the app (screenshots from the running app help a lot).
- [ ] Start the **slides** outline in `deliverables/slides.md`.

---

## Phase 4: Assemble the report & slides (afternoon · everyone, ~2h)

Wait for Phase 2 numbers, then merge everything.

- [ ] **Technical report**: reconcile `deliverables/technical_report.md` with the existing PDF; plug in: justification, field review (Jo), system description (Antonio), **evaluation results** (Martí/Bojana), **failure analysis**, future directions, and the required **"Use of AI tools"** section.
- [ ] **Slides** (20 min): problem → field review → live demo → eval method + results → failure cases → future work → Q&A. (Jo + Smaragda build, technical team supplies the numbers/figures.)
- [ ] Export the report to **PDF**.

---

## Phase 5: Reflections, integration & rehearsal (evening · everyone, ~1.5h)

- [ ] **Each member** writes their own ~1-page reflection (`deliverables/reflections/<name>.md`): your specific contributions + what you learned.
- [ ] Final check against the deliverables table in the README, everything ✅.
- [ ] **Rehearse the presentation once** end-to-end. Make sure **each person can defend any choice** (matching rule, model choice, Whisper limits, why English-only).
- [ ] Commit & push everything.

---

## Deliverables checklist (Option 1)

- [ ] Technical report (PDF) with "Use of AI tools" section
- [ ] One-page executive summary
- [ ] Slides
- [ ] Code repo (✅ already done)
- [ ] Supporting artifacts: `eval_set.jsonl`, `evaluate.py`, `results.json`, `prompts/`
- [ ] 5 individual reflections
- [ ] User manual + installation guide
- [ ] (Optional) hosted app link

---

### Quick owner map

| Person | Primary | Secondary |
|---|---|---|
| **Antonio** 🛠️ | App/repro polish, prompts doc, install guide, (deploy) | Report: system description |
| **Martí** 🛠️ | Eval harness `evaluate.py` + run it | Report: evaluation results |
| **Bojana** 🛠️ | Eval harness (matching/metrics) + failure analysis | Report: failure modes |
| **Jo** ✍️ | Field review + slides | Label transcripts |
| **Smaragda** ✍️ | Executive summary + user manual + slides | Label transcripts |
| **Everyone** 👥 | ~9 labeled transcripts each, own reflection, rehearsal |, |
