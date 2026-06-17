# Executive Summary

> **One page max. Written for a non-technical reader.** No jargon — explain what the app does, why it matters, and what we found.

---

## What we built

SummarAI is an AI-powered meeting assistant that turns a recorded meeting into a structured written record. Upload the audio or video of any meeting and, within minutes, the app returns a plain-language summary, a list of the main decisions made, and a clear set of action items showing who is responsible for what.

The key feature that sets SummarAI apart is language flexibility. Existing tools — such as Otter.ai or the built-in assistants in Zoom and Microsoft Teams — always produce their output in the same language as the meeting. SummarAI lets the user choose the output language independently. A meeting held in English can produce a Spanish summary and action-item list, or vice versa. For international teams where not everyone shares the same first language, this means every member receives the meeting record in the language they work best in.

---

## Why it matters

Unproductive meetings cost U.S. businesses an estimated $259 billion per year, according to a 2024 London School of Economics report. A large part of that cost is not the meetings themselves but what happens afterwards: decisions get forgotten, action items go unrecorded, and absent team members miss critical information. Studies show that 54% of employees regularly leave meetings without a clear understanding of the next steps.

The problem is more acute in multilingual workplaces. Over 60% of knowledge workers in multinational companies regularly attend meetings conducted in a language other than their primary one. Receiving a meeting summary in a second language — at the moment when precision matters most — is a real barrier to follow-through and accountability.

SummarAI addresses both problems at once: it automates the capture of meeting decisions and action items, and it delivers that information in the language the reader actually uses.

---

## What we found

We tested SummarAI on 40 meeting transcripts spanning English-only, Spanish-only, and cross-language scenarios. The system performed well on its core task: summaries were consistently coherent and action items were correctly identified in the large majority of cases.

The main limitation we identified is owner attribution — correctly identifying who is responsible for each action item. When speakers are named explicitly in the conversation ("Ana, can you handle this?"), attribution is reliable. When responsibility is implied rather than stated, the system sometimes leaves the owner blank or makes an incorrect inference. This is a known limitation of working with audio transcripts that do not label speakers, and it is the clearest direction for future improvement.

Cross-language generation — producing Spanish output from an English meeting — worked well for summaries and takeaways. Action items occasionally lost specific details such as deadlines or numeric targets in the translation, which we document as a known failure mode.

---

## Bottom line

SummarAI demonstrates that a focused AI pipeline can meaningfully reduce the administrative burden of meetings — capturing decisions and tasks automatically, and making them accessible to every team member in their own language. The proof of concept is functional, the core differentiator is real, and the failure modes are well-understood and addressable. The most immediate next step is adding speaker identification so that action-item ownership can be assigned reliably without depending on participants being named out loud.
