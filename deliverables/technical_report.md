# Technical Report — SummarAI

> Final deliverable: export to **PDF** before submission.

---

## 1. Introduction

Meetings generate decisions and commitments, but most of that information is lost shortly after the call ends. People rely on informal notes, fragmented memory, or re-watching recordings — none of which scale. SummarAI is a web application that automates this capture: upload an English-language meeting recording and, within minutes, receive a concise written record structured around two outputs: a short prose summary and a set of bullet points covering key takeaways and action items.

The system chains two NLP components. First, a local speech recognition model (Whisper) converts audio to text. Second, a large language model (Claude Haiku 4.5) reads that transcript and produces structured output through a strict JSON schema. The web interface is minimal by design — the value is in the NLP pipeline, not the UI.

This report describes the motivation, the technical design, an empirical evaluation, and the failure modes we documented during development.

---

## 2. Justification of need

Unproductive or poorly followed-up meetings cost U.S. businesses an estimated $259 billion per year (London School of Economics, 2024). A large share of that cost is post-meeting: decisions made verbally go unrecorded, action items are forgotten, and absent participants have no reliable way to catch up. Studies consistently show that a majority of employees leave meetings without a clear understanding of the next steps.

Several tools exist to address this — Otter.ai, Fireflies.ai, Zoom AI Companion, and Microsoft Teams Copilot all offer some form of meeting transcription and summary. Their limitations are relevant to this project:

- **Cost and access**: all major tools require paid subscriptions; several are tied to specific video-conferencing platforms.
- **Output quality**: most tools produce a raw transcript or a continuous prose summary. They rarely separate *decisions* from *notes*, and action-item extraction is either absent or unreliable when responsibility is only implied rather than explicitly assigned.
- **Closed systems**: none of these tools expose the underlying model or prompt, making it impossible to understand or modify their behaviour.

SummarAI addresses the output-quality gap specifically. Its two-output design — a 2-sentence summary plus typed bullet points (decision / note / action item) — forces the model to make an explicit distinction that conversational summaries routinely blur.

---

## 3. Field review

### 3.1 Automatic speech recognition (ASR)

The dominant open-source ASR model at the time of writing is OpenAI Whisper (Radford et al., 2022). Whisper is an encoder-decoder transformer trained on 680,000 hours of web audio, achieving near-human accuracy on clean English speech and robust performance on accented or lightly noisy audio. Its English-only variants (`tiny.en`, `base.en`, `small.en`, …) outperform the corresponding multilingual models on English audio while being faster.

`faster-whisper` is a community re-implementation of Whisper using the CTranslate2 inference library. It achieves the same output as the original at 2–4× lower memory usage and measurably faster runtime, which makes it practical for a local CPU deployment without a GPU.

Commercial ASR alternatives (AssemblyAI, AWS Transcribe, Azure Cognitive Services) offer higher accuracy on telephony-quality audio and built-in speaker diarization, at per-minute costs that make them unsuitable for a course prototype that needs to run cheaply at demo scale.

### 3.2 Meeting summarization and information extraction

LLM-based summarization has largely displaced earlier extractive and abstractive approaches (TextRank, BART, PEGASUS) for long-document tasks. Instruction-tuned models handle long, noisy meeting transcripts better than task-specific fine-tuned models, primarily because they can follow complex, multi-part instructions about output format.

Structured output — enforcing a JSON schema at the API level rather than prompt-engineering the model to emit valid JSON — is a significant recent development. It eliminates parsing failures caused by the model deviating from the expected format, which was a common failure mode in earlier tool-calling approaches.

The dominant commercial players (OpenAI GPT-4o, Google Gemini, Anthropic Claude) all now support structured output. Claude Haiku 4.5 was selected for this project on cost grounds: it is the fastest and cheapest model in the Claude 4 family while still following complex structured instructions reliably.

---

## 4. System description

### 4.1 Architecture

SummarAI is a single-server web application. The backend is a Python FastAPI app (`src/app.py`). The frontend is a single-page vanilla JavaScript application (`src/static/index.html`). Meeting results can optionally be saved to a Supabase (PostgreSQL) database for project-level persistence and timeline views.

The processing pipeline is strictly sequential:

```
User uploads file
        │
        ▼
 Audio/video? ──Yes──► Whisper (faster-whisper, base.en, local CPU)
        │                       │
        No                      ▼
        │               Plain-text transcript
        └──────────────────────►│
                                ▼
                     Claude Haiku 4.5 (JSON schema)
                                │
                    ┌───────────┴────────────┐
                    ▼                        ▼
              Summary (≤ 2 sentences)   Bullet points
                                     (key takeaways + action items)
```

Supported input formats:

| Category | Extensions |
|---|---|
| Audio / video | `.mp4`, `.mp3`, `.wav`, `.m4a`, `.webm`, `.ogg`, `.flac` |
| Text (skip ASR) | `.txt`, `.md`, `.vtt`, `.srt` |

The 300,000-character transcript limit corresponds to roughly 3–4 hours of dense meeting speech — well beyond the practical use case of a single meeting.

### 4.2 Two-stage NLP pipeline

**Stage 1 — Speech-to-text.** `faster-whisper` runs locally on CPU using the `base.en` model in `int8` quantization. Voice activity detection (`vad_filter=True`) strips silence before transcription, which both speeds up processing and avoids spurious text segments from quiet segments. The output is a plain string of the full meeting speech.

**Stage 2 — Summarization and information extraction.** The transcript is sent to Claude Haiku 4.5 with a system prompt that instructs the model to produce exactly three fields:

1. **`summary`** — at most 2 short sentences stating the meeting's purpose and overall outcome.
2. **`key_takeaways`** — an array of bullet objects, each with a `text` field (≤14 words) and a `type` field: `"decision"` (something agreed or set as policy) or `"note"` (any other important point, fact, or concern). The instruction to be *comprehensive* here is deliberate: the 2-sentence summary omits detail by design, so the takeaways carry all substantive information.
3. **`action_items`** — concrete tasks with `owner` and `deadline` populated only when actually stated in the meeting; never inferred.

The output schema is enforced at the API level using Claude's `json_schema` output format, which guarantees that every response parses correctly without defensive handling.

### 4.3 Performance optimization

During development we measured end-to-end processing time on a 20-minute `.m4a` file on a standard laptop CPU. Latency was almost entirely in the ASR stage — Claude Haiku 4.5 returned in 3–6 seconds regardless of transcript length, while Whisper dominated total runtime. We applied four zero-cost changes to the transcription stage only:

| Change | Rationale |
|---|---|
| `base.en` instead of multilingual `base` | English-only model is faster and more accurate for English audio |
| `beam_size=1` (greedy decoding) | Removes beam search overhead (~2× faster) with negligible accuracy loss |
| `cpu_threads=os.cpu_count()` | Uses all available cores instead of the library default |
| `language="en"` | Skips the automatic language-detection pass |

**Measured result (same file, same hardware):**

| Configuration | Total time | Transcript length |
|---|---|---|
| Original (`base`, beam 5, auto-detect) | 7 min 50 s | 36,702 chars |
| Optimized (`base.en`, greedy, multithread) | 2 min 12 s | 36,620 chars |

This is a **3.5× speedup (≈72% reduction) at zero additional cost**, with no measurable effect on downstream summary quality (near-identical transcript character counts; unchanged model output).

The Whisper model is configurable via the `WHISPER_MODEL` environment variable — `tiny.en` offers even faster throughput at some accuracy cost for live demos on constrained hardware.

---

## 5. Custom evaluation

### 5.1 Methodology

We built a custom test set of 40 English-language meeting transcripts. Each example was annotated with a reference set of ground-truth action items (task description + owner, where stated). Transcripts were sourced from publicly available meeting recordings and internally produced test conversations designed to cover a range of meeting types: project standups, planning sessions, and decision-heavy strategic calls.

Evaluation focused on **action-item extraction**, the output field most amenable to precise measurement. We applied standard information-retrieval metrics:

- **Precision**: fraction of extracted action items that match a ground-truth item.
- **Recall**: fraction of ground-truth items successfully extracted.
- **F1**: harmonic mean of precision and recall.

Matching was done with a combination of exact string overlap (for owner and deadline) and semantic similarity threshold (for task text), since paraphrase is expected between the reference and the model output.

Secondary evaluation covered **takeaway type accuracy** (decision vs. note classification) and **summary quality** assessed qualitatively, as automated metrics like ROUGE correlate poorly with human judgement on short, abstractive summaries.

### 5.2 Results

The system performed well on its core task. Summaries were consistently coherent and accurately reflected the meeting's main purpose and outcome. Action items were correctly identified in the large majority of test cases, with higher precision than recall — the model rarely invented false action items, but occasionally missed implicit commitments.

Takeaway type accuracy was high when the distinction was unambiguous (explicit votes or approvals → decision; factual updates → note) and lower on borderline cases where participants framed decisions as suggestions.

### 5.3 Main limitation identified

Owner attribution was the clearest failure mode. When a speaker's name was explicitly mentioned in the meeting ("Ana, can you handle this?"), the model correctly assigned ownership. When responsibility was implied or distributed, the model frequently left the `owner` field null rather than guessing — which is the conservative and correct behaviour, but results in incomplete action items. This is a fundamental limitation of working with transcripts that do not label speakers by name.

---

## 6. Failure mode analysis

The following cases were documented during development and evaluation.

**1. Implied speaker identity.** When responsibility is suggested rather than stated ("we should look into this"), the model correctly produces an action item with `owner: null`. This is not wrong behaviour, but it limits the utility of the action-item list for follow-up.

**2. Whisper mishearing proper nouns.** Names that are uncommon in Whisper's training data are occasionally transcribed incorrectly (e.g. "Bojana" transcribed as "Janna"). Since action-item owners depend on accurate name transcription, this propagates directly into incorrect attribution downstream.

**3. Off-topic or non-meeting audio.** Podcast-style recordings — long monologues, panel discussions, interviews — produce coherent summaries and takeaways but correctly yield zero action items. The system behaves as designed, but users uploading non-meeting content may be confused by the empty action-item list.

**4. Heavily overlapping or noisy audio.** Whisper's VAD filter removes silence effectively, but it does not separate overlapping speakers. In meetings where multiple participants speak simultaneously, the transcript can contain garbled or incomplete sentences, which the LLM then has to interpret from context. Summary quality degrades noticeably in these cases.

**5. Very long meetings near the character limit.** The 300,000-character cap (≈3–4 hours of dense speech) is far above typical meeting length, but processing time scales linearly with transcript length. A 2-hour meeting can take 4–5 minutes on modest hardware. The LLM context window (handled by Claude) is not a bottleneck at current meeting lengths.

**6. Implicit decisions.** When a decision emerges through consensus rather than an explicit statement, the model sometimes tags it as `note` rather than `decision`. The distinction is genuinely ambiguous in natural speech, and the system's conservative tagging is reasonable but imperfect.

**7. Repetitive or circular discussions.** In meetings where the same point is debated multiple times, the model sometimes produces duplicate or near-duplicate takeaways. The system prompt instructs comprehensiveness, which can work against deduplication.

---

## 7. Future directions

**Speaker diarization.** The highest-impact improvement would be integrating speaker diarization — automatic labelling of who says what in the transcript. This would directly solve the owner attribution problem and allow the model to assign action items reliably without depending on names being spoken aloud. Libraries such as `pyannote.audio` provide open-source diarization that could be inserted between the Whisper ASR stage and the LLM stage.

**Larger Whisper models.** The `base.en` model was chosen for speed. On hardware with more RAM, `small.en` or `medium.en` would improve accuracy on accented speech, domain-specific vocabulary, and noisy audio with minimal changes to the pipeline.

**Confidence and uncertainty signals.** The current system does not communicate uncertainty. A useful extension would be flagging action items or decisions where the model's confidence is low — for example, items extracted from a single ambiguous sentence rather than a clear explicit commitment.

**Persistent project search.** The current Supabase persistence layer stores full JSON blobs. Adding full-text search over saved summaries and takeaways would make the meeting archive genuinely useful as an organizational memory tool.

**Deployment.** The local Whisper model rules out serverless hosting (Vercel, Lambda) due to memory and runtime constraints. A long-running FastAPI server on Render, Railway, or Fly.io would work without changes to the application code.

---

## 8. Use of AI tools

Claude (Anthropic) was used throughout the project in several capacities:

- **Code generation and debugging**: the FastAPI backend, the structured output schema, and the Supabase integration were iteratively developed with Claude assistance. Claude was particularly useful for generating correct Pydantic models and for debugging JSON schema validation errors.
- **System prompt engineering**: the system prompt that instructs Claude Haiku was drafted collaboratively — initial versions were generated by Claude Sonnet and then refined through iterative testing on real transcripts. The final decision/note distinction and the instruction to "lose no information" in takeaways emerged from this process.
- **Documentation**: sections of this report, the user manual, and the installation guide were drafted with Claude assistance and then reviewed and edited by team members.
- **Transcription** (Whisper): the ASR component is itself an AI model, though it is used as a fixed inference component rather than interactively.

All code, prompts, and documentation were reviewed and edited by team members. No output was used without human review.

---

## 9. Conclusion

SummarAI demonstrates that a two-stage NLP pipeline — local ASR followed by a structured LLM call — can reliably transform an English meeting recording into an actionable written record. The system is functional, reproducible, and fast enough for practical use on consumer hardware.

The key finding from development was empirical: latency is dominated by transcription, not by the LLM, and a set of zero-cost Whisper optimizations reduced total processing time by 72% with no measurable loss in output quality. The key limitation is owner attribution, which depends on speakers being named explicitly in the meeting — a problem that speaker diarization would directly address.

The two-output design (summary + bullets) proved to be the right abstraction. The 2-sentence summary is useful for quick orientation; the typed bullet list carries the substance. Separating decisions from notes forces the model to make a distinction that is genuinely useful for follow-up and accountability, even if that distinction is occasionally ambiguous in natural speech.

---

## References

Radford, A., Kim, J. W., Xu, T., Brockman, G., McLeavey, C., & Sutskever, I. (2022). *Robust speech recognition via large-scale weak supervision*. arXiv preprint arXiv:2212.04356.

Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., Kaiser, L., & Polosukhin, I. (2017). *Attention is all you need*. Advances in Neural Information Processing Systems, 30.

See, A., Liu, P. J., & Manning, C. D. (2017). *Get to the point: Summarization with pointer-generator networks*. Proceedings of ACL 2017.

Lewis, M., Liu, Y., Goyal, N., Ghahraman, M., Mohamed, A., Levy, O., Stoyanov, V., & Zettlemoyer, L. (2020). *BART: Denoising sequence-to-sequence pre-training for natural language generation, translation, and comprehension*. Proceedings of ACL 2020.

Platek, B., & Polak, P. (2023). *faster-whisper*. GitHub repository. https://github.com/SYSTRAN/faster-whisper
