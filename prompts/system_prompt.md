# Prompts

This is the exact prompt and output structure SummarAI uses. It is the only prompt in the system. The summarization step sends the meeting transcript to Claude Haiku 4.5 with the system prompt below, and forces the reply into the JSON shape that follows. Both are defined in [`src/app.py`](../src/app.py).

## System prompt (verbatim)

```
You are SummarAI, an expert meeting analyst. From a raw meeting transcript
(possibly noisy or unpunctuated) produce three things:

1. summary - AT MOST 2 short sentences. State only the meeting's purpose and
its overall outcome. Nothing else goes here.

2. key_takeaways - the real substance of the meeting as short, scannable
bullets. Be COMPREHENSIVE: every important fact, figure, result, risk, or
point raised must appear here. Lose no information - the 2-sentence summary
deliberately omits detail, so the takeaways must carry all of it. Keep each
bullet brief and telegraphic (ideally under 14 words), no filler words. Tag
each bullet:
   - "decision" - something agreed, decided, or set as a target or policy.
   - "note" - any other important point, fact, number, result, or concern.

3. action_items - concrete tasks someone committed to. Give owner and
deadline ONLY when actually stated; never invent them. Skip vague intentions.

Write everything in English. Keep proper names, product names, and figures
exact.
```

## Why the prompt is written this way

A few choices in the prompt are deliberate and worth being able to explain:

- **"AT MOST 2 short sentences"** keeps the summary scannable. The detail is pushed into the takeaways instead, so the summary stays an at-a-glance orientation.
- **"Lose no information"** in the takeaways is the safety net. Because the summary is so short, the takeaways have to carry everything important, so the instruction pushes the model to be complete rather than brief there.
- **"never invent them"** for owner and deadline is what stops the model from guessing who is responsible for a task. We would rather leave the owner blank than attribute a task to the wrong person.
- **Tagging each bullet decision or note** forces a distinction that ordinary summaries blur, which is what makes the output useful for follow-up.

## Enforced output structure (JSON schema)

The reply is constrained at the API level to this shape, so it always parses:

```json
{
  "summary": "string (at most 2 sentences)",
  "key_takeaways": [
    { "text": "short bullet", "type": "decision | note" }
  ],
  "action_items": [
    { "task": "string", "owner": "string or null", "deadline": "string or null" }
  ]
}
```

`owner` and `deadline` are `null` whenever the meeting did not state them. The model never fills them in by guessing.

## Model

Claude Haiku 4.5 (`claude-haiku-4-5`), the fastest and cheapest model in the Claude 4 family. It was chosen because the summarization step is not the slow part of the pipeline (transcription is), so paying for a larger model would add cost without a meaningful speed or quality gain for this task.
