# SummarAI: Executive Summary

## What we built

SummarAI is a web application that turns a meeting recording into a usable written record. You upload an audio file (or paste a transcript), and within a few minutes the app returns three things: a short summary of what the meeting was about, a list of the key points and decisions, and a set of action items showing the task, who owns it, and any deadline that was mentioned.

The aim was not to produce another transcript. Plenty of tools already do that. SummarAI reads the conversation and pulls out the parts people actually need afterwards, the decisions and the to-dos, and presents them in a form you can drop straight into a project tracker. Summaries can be saved and organised into projects, so a team keeps a searchable history of what was agreed across many meetings.

## Why it matters

Meetings take up a large share of any team's week, but most of their value leaks away once the call ends. Decisions get misremembered, action items are never written down, and people who missed the meeting have no quick way to catch up. The cost is rarely the meeting itself; it is the follow-through that doesn't happen. SummarAI targets that gap by capturing the decisions and tasks automatically, so the record exists without anyone having to take minutes by hand.

## What we found

We evaluated the system on 30 real meetings from the AMI Meeting Corpus, a widely used research dataset of recorded meetings that comes with summaries written by professional human annotators. This let us compare SummarAI's output against a human-made reference for the same meetings, rather than against answers we wrote ourselves.

The summaries it produced were coherent and stayed on topic. On the action items, the feature we care about most, the system recovered roughly four out of every ten that the human annotators recorded (28 of 66 across the 30 meetings), working end to end from raw audio.

The clearest weakness is figuring out *who* owns each task. When a name is said out loud ("Ana, can you take that?"), attribution is reliable. When responsibility is only implied, the system either leaves the owner blank or guesses. This traces back to a known limitation of the underlying transcription, which converts speech to text but does not label who is speaking. It is the single most valuable thing to fix next.

On speed, an early version transcribed a 20-minute meeting in about eight minutes; after tuning the transcription settings we brought that down to roughly two minutes, with no measurable loss in quality.

## Where it stands

SummarAI is a working proof of concept. It does its core job, turning a recording into a summary, decisions, and owned action items, and the places where it falls short are understood rather than mysterious. The most direct next step is adding speaker identification, which would let the system assign ownership reliably without depending on people naming each other out loud.
