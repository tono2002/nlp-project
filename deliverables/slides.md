# SummarAI: Presentation Slides

20-minute talk plus 5 minutes of Q&A. Every team member must be able to defend any choice. This file is the slide-by-slide content; build the actual deck (Google Slides / PowerPoint / Canva) from it and add the link below.

**Deck link:** _TODO_

Suggested split for delivery: rotate speakers so each person presents the part they worked on.

---

## Slide 1: Title

**SummarAI**
Turning meeting recordings into a usable written record.

NLP Group Assignment, Option 1. Team: Antonio, Martí, Bojana, Smaragda, Jo.

---

## Slide 2: The problem

- Meetings take up a big part of every team's week, but most of their value disappears once the call ends.
- Decisions get misremembered, action items are never written down, and people who missed the meeting have no fast way to catch up.
- The cost is not the meeting itself, it is the follow-through that never happens.

*Speaker note: keep this human and short. Everyone has lived this.*

---

## Slide 3: What SummarAI does

Upload a recording (or a transcript), get back three things:

1. A **summary** in two sentences.
2. **Key takeaways**, each tagged as a **decision** or a **note**.
3. **Action items**: the task, who owns it, and any deadline.

Results can be saved into **projects**, so a team keeps a searchable history.

*Add a screenshot of the results screen here.*

---

## Slide 4: Where the NLP is

The web page is just the interface. The intelligence is two NLP stages:

```
Audio  →  [ Speech-to-text: Whisper ]  →  text  →  [ Summarize + extract: Claude ]  →  summary, takeaways, action items
```

- Stage 1 turns speech into text.
- Stage 2 reads the text and pulls out the parts people actually need.

If you upload a text transcript, stage 1 is skipped.

---

## Slide 5: The field, and the gap we target

- Tools already exist: Otter.ai, Fireflies.ai, Zoom AI Companion, Microsoft Teams Copilot.
- They are paid, tied to specific platforms, and closed (you cannot see or change how they work).
- Most give you a raw transcript or a flowing paragraph. They rarely separate **decisions** from ordinary notes, and they are unreliable at saying **who owns** each task.
- SummarAI focuses on that gap: a clear, owned to-do list, with decisions kept separate from notes.

---

## Slide 6: Live demo

*Run the app on a real meeting recording. Show: upload, the progress bar, then the summary, the decision/note bubbles, and the action items with owners. Save it to a project to show the history view.*

Backup plan if the demo fails: a recorded screen capture or screenshots on the next hidden slide.

---

## Slide 7: How we evaluated it

- We used **30 real meetings from the AMI Meeting Corpus**, a public research dataset of recorded meetings.
- AMI ships with **summaries written by professional human annotators**, including a list of action items per meeting.
- We compared SummarAI's output against those human summaries **automatically**, with no hand-labeling.
- Why this is honest: we did not write the "correct" answers ourselves, so we are not grading the AI against an AI.

*Speaker note: be ready to explain why we separate transcription from summarization in the evaluation.*

---

## Slide 8: Results

Across the 30 meetings:

| Metric | Score |
|---|---|
| ROUGE-1 | 0.34 |
| ROUGE-2 | 0.06 |
| ROUGE-L | 0.15 |
| Action items recovered (recall) | 42% (28 of 66) |

The headline: working end to end from raw audio, the system recovers about **four in ten** of the action items a human annotator recorded.

---

## Slide 9: Reading the numbers honestly

The ROUGE scores look modest, and there are clear reasons:

- Our summary is **two sentences by design**; the human reference is a 200-word document. ROUGE rewards word overlap, so it penalizes our output for being short, not for being wrong.
- We fed **real transcription output**, which contains errors, not clean text.
- The model is used **out of the box**, with no training on this dataset.

*Speaker note: the point is that we understand our own numbers. That is what the rubric rewards.*

---

## Slide 10: Where it fails, and why

- **Who owns the task.** The transcription does not label who is speaking. When nobody is named ("can you handle that?"), the system leaves the owner blank instead of guessing.
- **Role vs name.** The human annotations say "the industrial designer will...", while our app extracts the person's actual name. Same task, different wording, so some correct answers look like misses.
- **Misheard names.** Whisper sometimes mishears uncommon names (it turned "Bojana" into "Janna"), which then attaches a task to the wrong person.
- **Non-meeting audio.** A podcast or monologue correctly produces zero action items, by design.

---

## Slide 11: A finding from building it

- The slow part of the pipeline is **transcription**, not the language model.
- By switching to an English-tuned model and simpler decoding settings (all free changes), we cut processing of a 20-minute meeting from **about 8 minutes to about 2**, with no loss in quality.
- Lesson: the obvious instinct ("use a bigger, slower model to be safe") was wrong here. Measuring told us where the time actually went.

---

## Slide 12: Future directions

- **Speaker identification**, the single most useful next step. It would fix the owner-attribution problem directly.
- A larger transcription model on stronger hardware, for noisy or accented audio.
- Flagging low-confidence items so users know what to double-check.
- Search across the saved project history.

---

## Slide 13: How we used AI tools

- We used Claude to help write code, draft text, and refine the prompt, then reviewed and edited everything ourselves.
- The decisions that matter (what to build, how to evaluate, what counts as an action item, how to read the results) were ours.
- Whisper, the transcription model, is itself an AI component used as a fixed building block.

---

## Slide 14: Closing and Q&A

- SummarAI is a working proof of concept that turns a recording into a summary, decisions, and owned action items.
- The weak spots are understood, not mysterious, and the most useful fix is clear.

Questions.
