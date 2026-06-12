# SummarAI — Meeting Summarizer

An NLP-powered **bilingual (English / Spanish)** web app that turns a meeting recording (or transcript) into a **summary**, a list of **key takeaways**, and a set of **actionable insights / action items** — in the language the user chooses, regardless of the meeting's original language.

**Course:** NLP — Group Assignment · **Option 1: Application Development**
**Team:** Antonio · Martí · Bojana · Smaragda · Jo

> See [PROJECT_PLAN.md](PROJECT_PLAN.md) for the simple step-by-step plan.

---

## 1. The idea

```
INPUT (mp4 or txt)  →  transcribe to text  →  ┌─ Summary
                                              ├─ Key takeaways
                                              └─ Actionable insights / plans
```

You upload a meeting (audio/video file, or paste an existing transcript) and pick your output language (**English or Spanish**). SummarAI:
1. **Transcribes** the audio into text (speech-to-text).
2. **Reads** the transcript and produces, **in the chosen language**:
   - a concise **summary** of the meeting,
   - the **key takeaways** (main points/decisions),
   - the **action items** — who has to do what, by when.

**Bilingual / cross-lingual:** the meeting can be in English and a Spanish user can still get the summary, takeaways, and actions in Spanish (and vice versa). The output language is independent of the meeting's language.

## 2. Where the NLP is

The web app is just the interface. The intelligence is in two NLP stages:

| Stage | NLP task | Notes |
|---|---|---|
| Audio → text | **Speech-to-text (ASR)** | Uses an existing engine (e.g. Whisper). Skipped if the input is already `txt`. |
| Text → insights | **Summarization + information extraction** | The core of the project: condense the transcript and pull out takeaways and action items. |
| Output language | **Cross-lingual generation / translation** | Produce the insights in the user's chosen language (EN/ES) even when the meeting is in the other one, preserving meaning. |

## 3. Justification of need

Meetings are everywhere and most of their value is lost: people forget decisions, action items slip, and nobody re-watches a one-hour recording. Existing tools (Otter, Fireflies, Zoom AI Companion, etc.) exist but are paid, closed, and not always good at pulling **clear, owned action items**. They are also mostly **monolingual** — a Spanish speaker in an English meeting gets an English summary. SummarAI focuses on turning talk into a concrete to-do list **and delivering it in the user's own language (EN/ES)**.

_(Full justification + field review go in the technical report.)_

## 4. Evaluation focus — the part that gets graded

We must test the system on our **own 30–50 example test set** and report a real score.

- **Primary, measurable target: action-item extraction.** Each test transcript has a known list of "true" action items (task + owner). We measure **precision/recall**: did the app catch the real actions, miss any, or invent fake ones?
- **Cross-lingual check:** test set includes English meetings with **Spanish** expected outputs (and vice versa) to verify the action items survive the language switch with the same meaning.
- Summary and key takeaways are evaluated more qualitatively (and/or with ROUGE), since "a good summary" is subjective.

This is where the marks live — see [data/eval/](data/eval/).

## 5. Tech (planned)

- **Frontend/web app:** _TODO_
- **Transcription:** _TODO (e.g. OpenAI Whisper)_
- **Summarization / extraction:** _TODO (LLM API or open model)_
- See [docs/installation_guide.md](docs/installation_guide.md) to run it.

---

## 6. Deliverables (Option 1)

All submitted via the course platform. Placeholders already exist in this repo.

| # | Deliverable | File |
|---|---|---|
| 1 | Technical report (PDF) | [deliverables/technical_report.md](deliverables/technical_report.md) |
| 2 | One-page executive summary (non-technical) | [deliverables/executive_summary.md](deliverables/executive_summary.md) |
| 3 | Presentation slides | [deliverables/slides.md](deliverables/slides.md) |
| 4 | Code repository | this repo · [src/](src/) |
| 5 | Supporting artifacts (test set, prompts) | [data/eval/](data/eval/) · [prompts/](prompts/) |
| 6 | Individual reflections (1 per member) | [deliverables/reflections/](deliverables/reflections/) |
| 7 | User manual *(Option 1)* | [docs/user_manual.md](docs/user_manual.md) |
| 8 | Installation / execution guide *(Option 1)* | [docs/installation_guide.md](docs/installation_guide.md) |

The report must include a **"Use of AI tools"** section describing how we used LLMs.

## 7. Required components (Option 1)

- **Justification of need** — why SummarAI is needed and what existing tools lack.
- **Field review** — the meeting-AI / transcription industry: trends, players, gaps.
- **Functional system** — a working web app demo (POC).
- **Custom evaluation** — our 30–50 example test set + quantitative results.
- **Failure mode analysis** — 5–10 documented cases where it fails, with hypotheses.
- **Reproducible repository** — clean code, clear README, requirements file.

## 8. Process / workflow

| Phase | Focus |
|---|---|
| **Early** | Finalize scope, **get professor approval**, agree on roles, scan existing tools |
| **Middle** | Build the app (transcription + summarization + extraction) and the test set |
| **Late** | Run the evaluation, analyze failures, write report, make slides, rehearse |

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
