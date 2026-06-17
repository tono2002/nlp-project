# Project Plan (simple)

**The project in one line:** build a small web app that does something smart with language, **prove how well it works with our own tests**, then present it.

---

## Part 1: What we do (the work)

1. **Pick & get approval**: choose the idea. ⚠️ The professor must approve the topic *before* we start.
2. **Research the field**: who else does this, what tools exist, what they get wrong. (Becomes a report section.)
3. **Build the app (POC)**: a simple working web app: paste text in → get a smart result out. Doesn't need to be pretty or production-ready, just work.
4. **Build the test set** ⭐ *most important*, create **30–50 examples** by hand: each one is an input + the correct answer *we* decided.
5. **Measure it**: run the app on all 30–50, count how many it gets right (e.g. "38/50"). This is our proof.
6. **Analyze failures**: pick **5–10 wrong cases** and explain *why* they failed.
7. **Write & present**: write it up, make slides, present in class (**20 min + 5 min Q&A**).

---

## Part 2: What we deliver (the submission)

| # | Deliverable | Plain meaning | File in repo |
|---|---|---|---|
| 1 | Technical report (PDF) | Full write-up: need, research, how it works, results, failures | `deliverables/technical_report.md` |
| 2 | Executive summary (1 page) | Same thing for a non-technical reader | `deliverables/executive_summary.md` |
| 3 | Slides | What we show in class | `deliverables/slides.md` |
| 4 | Code repo | This GitHub repo (app + test set) | `src/` |
| 5 | Supporting files | Test set, prompts, data | `data/eval/`, `prompts/` |
| 6 | Individual reflections | 1 page from each of the 5 of us | `deliverables/reflections/` |
| 7 | User manual *(Option 1)* | How to use the app | `docs/user_manual.md` |
| 8 | Installation guide *(Option 1)* | How to run the app | `docs/installation_guide.md` |

Plus a short **"Use of AI tools"** section inside the report (how we used LLMs).

---

## Part 3: What they grade

1. Is the work technically sound?
2. **Did we measure it with our OWN data?** ← biggest one
3. Is it original / did we think critically?
4. Is the report + presentation clear?
5. Could someone else reproduce it?

⚠️ In the Q&A, **each of the 5 of us must be able to defend any choice.** Don't let one person do everything.

---

## The simplest way to remember it

> **Build a language tool → test it with 30–50 of our own examples → explain where it breaks → write it up → present it.**

Everything else supports that core loop.

---

**Team:** Antonio · Martí · Bojana · Smaragda · Jo
