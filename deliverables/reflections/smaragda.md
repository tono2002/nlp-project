# Individual Reflection: Smaragda

## My contributions

### Evaluation set design and annotation methodology
I designed the evaluation set that the whole team used to measure the system. This included deciding on the format of `eval_set.jsonl` (one JSON object per line, each with a unique meeting ID, the raw transcript text, and a matching entry in `gold_action_items.csv` with the expected task, owner, and deadline), writing the annotation guidelines the team followed when labeling, and coordinating the labeling across all five members so that everyone applied the same rules consistently.

The annotation guidelines required real thought. The main decisions I had to make were: what counts as an action item versus a note (we defined it as a concrete commitment by a named or identifiable person, not a vague intention or a plan the team discussed but did not commit to); what to write when no deadline is mentioned (leave blank rather than infer); and how to handle cases where one transcript contains multiple overlapping action items for the same person. Writing these rules down before anyone started labeling prevented the inconsistencies that would have made the evaluation results uninterpretable.

I also ensured the test set covered a realistic range of meeting types: daily standups, project planning sessions, sales calls, retrospectives, and a few deliberately tricky cases (no action items at all, ambiguous ownership, hypothetical discussions that look like commitments). I contributed approximately 8 transcripts myself, focusing on multilingual scenarios where speakers switch languages mid-meeting.

### Executive summary
I wrote `deliverables/executive_summary.md`, the one-page non-technical description of the project. The challenge here was ordering the argument correctly: the instinct when you have built something technical is to start with how it works, but a non-technical reader needs to understand the problem first. I led with the cost of unproductive meetings and the specific barrier multilingual teams face, then described what SummarAI does differently, then summarised the evaluation findings — including the main limitation around owner attribution when responsibility is implied rather than stated.

### User manual
I wrote `docs/user_manual.md` from scratch, walking through every feature of the app: uploading a file, choosing the output language, reading the summary and takeaway bubbles, checking off action items, saving a meeting to a project, and browsing the project timeline. I also documented the supported file formats, known limitations, and answers to the questions a first-time user is most likely to ask.

### Slides
I put together the presentation slides (`deliverables/slides.md`), structuring the 20-minute presentation as: problem and motivation → field review → system overview → evaluation method and results → failure cases → future directions → Q&A. I coordinated with Martí for the evaluation numbers and with Bojana for the failure case examples to make sure the slides reflected the actual findings rather than our expectations going in.

## What I learned

Building the annotation guidelines taught me that the definition of a label is itself a research decision with real consequences for the evaluation. We started with a vague shared understanding of what an action item was, and when I tried to write it down precisely, the edge cases appeared immediately: is "we should probably follow up on this" an action item? What if no one is named as responsible? What if someone agrees to do something but only conditionally? These decisions determine what the model is being evaluated against, so they determine what the evaluation actually measures. I now understand why inter-annotator agreement is reported in NLP papers — it is not a formality, it is evidence that the label definition is precise enough to be applied consistently. I also understood more deeply what the summarization task is about: it is not just shortening text, it is identifying what is important and representing it in a structured, reusable form — which is a much harder and more interesting problem than it first appears.
