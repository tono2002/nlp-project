# Executive Summary

> **One page max. Written for a non-technical reader.** No jargon — explain what the app does, why it matters, and what we found.

---

## What we built

SummarAI is an AI-powered meeting assistant that turns a recorded meeting into a structured written record. Upload the audio or video of any English-language meeting and, within minutes, the app returns a plain-language summary, a list of the main decisions made, and a clear set of action items showing who is responsible for what.

The system is designed for English input and produces all output in English. It targets a gap left by tools such as Otter.ai or the built-in assistants in Zoom and Microsoft Teams: rather than surfacing a raw transcript, SummarAI interprets the conversation and distils it into three immediately useful artefacts — a concise summary, a decision log, and a task list with owners.

---

## Why it matters

Unproductive meetings cost U.S. businesses an estimated $259 billion per year, according to a 2024 London School of Economics report. A large part of that cost is not the meetings themselves but what happens afterwards: decisions get forgotten, action items go unrecorded, and absent team members miss critical information. Studies show that 54% of employees regularly leave meetings without a clear understanding of the next steps.

SummarAI addresses this directly: it automates the capture of meeting decisions and action items so that nothing important slips through the cracks after the call ends.

---

## What we found

We tested SummarAI on 40 meeting transcripts spanning English-only. The system performed well on its core task: summaries were consistently coherent and action items were correctly identified in the large majority of cases.

The main limitation we identified is owner attribution — correctly identifying who is responsible for each action item. When speakers are named explicitly in the conversation ("Ana, can you handle this?"), attribution is reliable. When responsibility is implied rather than stated, the system sometimes leaves the owner blank or makes an incorrect inference. This is a known limitation of working with audio transcripts that do not label speakers, and it is the clearest direction for future improvement.

---

## Bottom line

SummarAI demonstrates that a focused AI pipeline can meaningfully reduce the administrative burden of meetings — capturing decisions and tasks automatically from any English-language recording. The proof of concept is functional, the core task is working well, and the failure modes are well-understood and addressable. The most immediate next step is adding speaker identification so that action-item ownership can be assigned reliably without depending on participants being named out loud.
