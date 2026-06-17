# SummarAI: Meeting Summarizer

An NLP-powered web app that turns a meeting recording (or transcript) into a **2-sentence summary**, a set of **typed key-takeaway bullets** (decision / note), and **action items** (task · owner · deadline). Summaries can be organised into **projects** and saved.

**Course:** NLP, Group Assignment · **Option 1: Application Development**
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
   - **action items**: who has to do what, by when (owner/deadline only when actually stated).
3. Optionally **saves** the result to a **project** (persisted in Supabase) and shows it in a timeline.

## 2. Where the NLP is

The web app is just the interface. The intelligence is in two NLP stages:

| Stage | NLP task | How |
|---|---|---|
| Audio → text | **Speech-to-text (ASR)** | `faster-whisper` (`base.en` model), local CPU. Skipped for `txt` input. |
| Text → insights | **Summarization + information extraction** | Claude **Haiku 4.5** with a strict JSON schema → summary, typed takeaways, action items. |

## 3. Justification of need

Meetings are everywhere and most of their value is lost: people forget decisions, action items slip, and nobody re-watches a one-hour recording. Existing tools (Otter, Fireflies, Zoom AI Companion) are paid, closed, and not always good at pulling **clear, owned action items**. SummarAI focuses on turning talk into a concrete, owned to-do list, separates **decisions from notes**, and keeps a per-project memory of past meetings.

_(Full justification + field review go in the technical report.)_

## 4. Evaluation

We evaluate the **summarization** stage on **30 real meetings from the AMI Meeting Corpus**, using AMI's **human-written summaries** as the ground truth. There is no manual labeling: we reuse the professional human annotations that ship with the corpus and compare the app's output against them automatically.

- **ROUGE-1 / 2 / L** measure how close our output is to the human reference summary.
- **Action-item coverage** measures how many of the human-annotated action items the app recovers.

Result (30 meetings): **ROUGE-1 0.34**, and the system recovers about **42% of the human action items** working end to end from audio. The methodology, script, and full per-meeting results are in [data/eval/](data/eval/).

## 5. Tech stack (built)

- **Backend:** Python + **FastAPI** ([src/app.py](src/app.py)), endpoints for processing, projects, and saved summarizations.
- **Transcription:** [`faster-whisper`](https://github.com/SYSTRAN/faster-whisper) `base.en` model, local, int8.
- **Analysis:** **Claude Haiku 4.5** via the Anthropic SDK, structured JSON output.
- **Frontend:** single-page vanilla JS + CSS ([src/static/index.html](src/static/index.html)), midnight-indigo theme, drag-and-drop, typed takeaway bubbles, action checklist, **collapsible sidebar**, **iPhone-responsive**.
- **Persistence:** **Supabase** (Postgres), `projects` + `summarizations` tables ([supabase_schema.sql](supabase_schema.sql)).
- Run it: see [docs/installation_guide.md](docs/installation_guide.md).

---

## 6. Project status

### ✅ Done
- [x] Functional POC: upload → transcribe → summary + typed takeaways + action items
- [x] Whisper transcription verified on real meeting audio; transcription sped up ~3.5x
- [x] Project management + Supabase persistence + timeline view
- [x] English-only output, 2-sentence summary, decision/note bubbles
- [x] Responsive (iPhone) layout + collapsible projects sidebar
- [x] Custom evaluation on 30 AMI meetings (ROUGE + action-item coverage)
- [x] Failure-mode analysis (in the technical report)
- [x] Technical report, executive summary, user manual, installation guide, prompt documentation

### 🔲 To do
1. Export the technical report to a fresh **PDF** from the corrected markdown.
2. Build the **presentation slides**.
3. Each member writes their **individual reflection**.
4. (Optional) **Deploy**: local Whisper rules out Vercel serverless; Render / Railway / Fly.io fit a long-running FastAPI app.

---

## 7. Deliverables (Option 1)

| # | Deliverable | File | Status |
|---|---|---|---|
| 1 | Technical report (PDF) | [.md](deliverables/technical_report.md) | 🟡 content done, export PDF |
| 2 | One-page executive summary | [deliverables/executive_summary.md](deliverables/executive_summary.md) | ✅ |
| 3 | Presentation slides | [deliverables/slides.md](deliverables/slides.md) | 🔲 to build |
| 4 | Code repository | this repo · [src/](src/) | ✅ |
| 5 | Supporting artifacts (eval set, prompts) | [data/eval/](data/eval/) · [prompts/](prompts/) | ✅ |
| 6 | Individual reflections (1 per member) | [deliverables/reflections/](deliverables/reflections/) | 🔲 each member |
| 7 | User manual *(Option 1)* | [docs/user_manual.md](docs/user_manual.md) | ✅ |
| 8 | Installation / execution guide *(Option 1)* | [docs/installation_guide.md](docs/installation_guide.md) | ✅ |

The report includes the required **"Use of AI tools"** section (Section 8).

## 8. Required components (Option 1)

- **Justification of need**: why SummarAI is needed and what existing tools lack. ✅
- **Field review**: the meeting-AI / transcription industry, trends, players, gaps. ✅
- **Functional system**: a working web app demo (POC). ✅
- **Custom evaluation**: 30 AMI meetings with quantitative results (ROUGE + action-item coverage). ✅
- **Failure mode analysis**: documented cases with hypotheses. ✅
- **Reproducible repository**: clean code, clear README, requirements file. ✅

## 9. Evaluation criteria (rubric)

1. **Technical execution and rigor**: sound methodology, quality code and artifacts.
2. **Empirical evidence and depth of analysis**: conclusions grounded in our own measurements. ← biggest one
3. **Originality and critical thinking**: non-trivial insights beyond the obvious.
4. **Communication**: clear report and presentation.
5. **Reproducibility and quality of deliverables**: others can follow and reproduce our work.

⚠️ Presentation: **20 min + 5 min Q&A.** Every team member must be able to defend any choice made in the project.

---

## 10. Useful research repositories

- [Google Scholar](https://scholar.google.es/) · [arXiv](https://arxiv.org/) · [ACL Anthology](https://aclanthology.org/) · [IEEE Xplore](https://ieeexplore.ieee.org/) · [Semantic Scholar](https://www.semanticscholar.org/) · [Papers with Code](https://paperswithcode.com/)

---

*"The strongest projects are the ones whose authors can articulate, with concrete observations from their own work, what they learned and why it matters."*
