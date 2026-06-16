# SummarAI — Meeting Summarizer

An NLP-powered web app that turns a meeting recording (or transcript) into a **2-sentence summary**, a set of **typed key-takeaway bullets** (decision / note), and **action items** (task · owner · deadline). Summaries can be organised into **projects** and saved.

**Course:** NLP — Group Assignment · **Option 1: Application Development**
**Team:** Antonio · Martí · Bojana · Smaragda · Jo

> See [PROJECT_PLAN.md](PROJECT_PLAN.md) for the simple step-by-step plan.

---

## 1. The idea

```
INPUT (mp4/mp3/wav/m4a or txt) → transcribe → analyse → ┌─ Summary (≤ 2 sentences)
                                                        ├─ Key takeaways (decision / note bubbles)
                                                        └─ Action items (task · owner · deadline)
```

You upload a meeting (audio/video file, or an existing transcript). SummarAI:
1. **Transcribes** audio into text with Whisper (skipped if the input is already text).
2. **Analyses** the transcript with an LLM and returns, in English:
   - a tight **summary** (max 2 sentences),
   - **key takeaways** as short, scannable bullets, each tagged **decision** or **note**,
   - **action items** — who has to do what, by when (owner/deadline only when actually stated).
3. Optionally **saves** the result to a **project** (persisted in Supabase) and shows it in a timeline.

## 2. Where the NLP is

The web app is just the interface. The intelligence is in two NLP stages:

| Stage | NLP task | How |
|---|---|---|
| Audio → text | **Speech-to-text (ASR)** | `faster-whisper` (`base` model), local CPU. Skipped for `txt` input. |
| Text → insights | **Summarization + information extraction** | Claude **Haiku 4.5** with a strict JSON schema → summary, typed takeaways, action items. |

## 3. Justification of need

Meetings are everywhere and most of their value is lost: people forget decisions, action items slip, and nobody re-watches a one-hour recording. Existing tools (Otter, Fireflies, Zoom AI Companion) are paid, closed, and not always good at pulling **clear, owned action items**. SummarAI focuses on turning talk into a concrete, owned to-do list, separates **decisions from notes**, and keeps a per-project memory of past meetings.

_(Full justification + field review go in the technical report.)_

## 4. Evaluation focus — the part that gets graded ⚠️

We must test the system on our **own 30–50 example test set** and report a real score. **This is the biggest open task** (see status below).

- **Primary, measurable target: action-item extraction.** Each test transcript has a known list of "true" action items (task + owner). We measure **precision / recall**: did the app catch the real actions, miss any, or invent fake ones?
- Secondary: takeaway **type** accuracy (decision vs note) and summary quality (qualitative / ROUGE).

Test set, expected outputs, and the eval script live in [data/eval/](data/eval/).

## 5. Tech stack (built)

- **Backend:** Python + **FastAPI** ([src/app.py](src/app.py)) — endpoints for processing, projects, and saved summarizations.
- **Transcription:** [`faster-whisper`](https://github.com/SYSTRAN/faster-whisper) `base` model, local, int8.
- **Analysis:** **Claude Haiku 4.5** via the Anthropic SDK, structured JSON output.
- **Frontend:** single-page vanilla JS + CSS ([src/static/index.html](src/static/index.html)) — midnight-indigo theme, drag-and-drop, typed takeaway bubbles, action checklist, **collapsible sidebar**, **iPhone-responsive**.
- **Persistence:** **Supabase** (Postgres) — `projects` + `summarizations` tables ([supabase_schema.sql](supabase_schema.sql)).
- Run it: see [docs/installation_guide.md](docs/installation_guide.md).

---

## 6. Project status

### ✅ Done
- [x] Functional POC: upload → transcribe → summary + typed takeaways + action items
- [x] Whisper transcription verified on a real ~20-min `m4a`
- [x] Project management + Supabase persistence + timeline view
- [x] English-only output, 2-sentence summary, decision/note bubbles
- [x] Responsive (iPhone) layout + collapsible projects sidebar
- [x] Technical Report drafted as PDF ([docs/SummarAI_Technical_Report.pdf](docs/SummarAI_Technical_Report.pdf))

### 🔲 To do (priority order)
1. **Custom evaluation set** (30–50 transcripts + expected action items) and an **eval script** that reports precision/recall → [data/eval/](data/eval/). *Highest impact on the grade.*
2. **Failure-mode analysis** — document 5–10 cases with hypotheses (e.g. Whisper mishears names like *Bojana → "Janna"*; podcast input correctly yields zero action items).
3. **Field review** of the meeting-AI / transcription industry (for the report).
4. Fill the remaining deliverables: **executive summary**, **slides**, reconcile **technical_report.md** with the PDF, **5 individual reflections**, finish **user manual** & **install guide**.
5. Document the actual system prompt in [prompts/](prompts/).
6. (Optional) **Deploy** — local Whisper rules out Vercel serverless; Render / Railway / Fly.io fit a long-running FastAPI app.

---

## 7. Deliverables (Option 1)

| # | Deliverable | File | Status |
|---|---|---|---|
| 1 | Technical report (PDF) | [docs/SummarAI_Technical_Report.pdf](docs/SummarAI_Technical_Report.pdf) · [.md](deliverables/technical_report.md) | 🟡 PDF drafted |
| 2 | One-page executive summary | [deliverables/executive_summary.md](deliverables/executive_summary.md) | 🔲 |
| 3 | Presentation slides | [deliverables/slides.md](deliverables/slides.md) | 🔲 |
| 4 | Code repository | this repo · [src/](src/) | ✅ |
| 5 | Supporting artifacts (test set, prompts) | [data/eval/](data/eval/) · [prompts/](prompts/) | 🔲 |
| 6 | Individual reflections (1 per member) | [deliverables/reflections/](deliverables/reflections/) | 🔲 |
| 7 | User manual *(Option 1)* | [docs/user_manual.md](docs/user_manual.md) | 🟡 partial |
| 8 | Installation / execution guide *(Option 1)* | [docs/installation_guide.md](docs/installation_guide.md) | 🟡 partial |

The report must include a **"Use of AI tools"** section describing how we used LLMs.

## 8. Required components (Option 1)

- **Justification of need** — why SummarAI is needed and what existing tools lack. 🟡
- **Field review** — the meeting-AI / transcription industry: trends, players, gaps. 🔲
- **Functional system** — a working web app demo (POC). ✅
- **Custom evaluation** — our 30–50 example test set + quantitative results. 🔲
- **Failure mode analysis** — 5–10 documented cases where it fails, with hypotheses. 🔲
- **Reproducible repository** — clean code, clear README, requirements file. ✅

## 9. Evaluation criteria (rubric)

1. **Technical execution and rigor** — sound methodology, quality code and artifacts.
2. **Empirical evidence and depth of analysis** — conclusions grounded in our own measurements. ← biggest one
3. **Originality and critical thinking** — non-trivial insights beyond the obvious.
4. **Communication** — clear report and presentation.
5. **Reproducibility and quality of deliverables** — others can follow and reproduce our work.

⚠️ Presentation: **20 min + 5 min Q&A.** Every team member must be able to defend any choice made in the project.

---

## 10. Useful research repositories

- [Google Scholar](https://scholar.google.es/) · [arXiv](https://arxiv.org/) · [ACL Anthology](https://aclanthology.org/) · [IEEE Xplore](https://ieeexplore.ieee.org/) · [Semantic Scholar](https://www.semanticscholar.org/) · [Papers with Code](https://paperswithcode.com/)

---

*"The strongest projects are the ones whose authors can articulate, with concrete observations from their own work, what they learned and why it matters."*
