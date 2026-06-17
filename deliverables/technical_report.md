# Technical Report

> Final deliverable: export to **PDF** before submission. Length appropriate to the project.

## 1. Introduction
_TODO_

## 2. Justification of need
_Why is this application needed? Where would it be applied? What do existing approaches lack that ours provides?_

## 3. Field review
_Trends, challenges, major players, and existing solutions in the industry where the system operates._

## 4. System description
_Architecture, NLP methods/models used, and the core functionalities of the POC._

### 4.1 Two-stage NLP pipeline
The system chains two NLP models: (1) **speech-to-text** via Whisper (`faster-whisper`, local CPU) and (2) **summarization + information extraction** via Claude Haiku 4.5 with a strict JSON schema. The web app is only the interface; the intelligence is in these two stages.

### 4.2 Performance optimization (empirical finding)
While testing the POC we observed that **latency is almost entirely in transcription, not summarization** — the LLM (Haiku 4.5, already the fastest/cheapest Claude model) returns in seconds, whereas Whisper dominated total runtime. We therefore optimized the transcription stage only, applying four zero-cost changes:

1. **English-only model** — switched from the multilingual `base` model to `base.en` (faster and more accurate for English).
2. **Greedy decoding** — `beam_size=1` instead of the library default of 5 (~2× faster for negligible accuracy loss).
3. **Full CPU parallelism** — set `cpu_threads` to all available cores.
4. **Skipped language detection** — passed `language="en"` to avoid the automatic detection pass.

**Measured result (same 20-minute `.m4a`, same hardware):**

| Configuration | Transcription + analysis time | Transcript length |
|---|---|---|
| Original (`base`, beam 5, auto-detect) | **7 min 50 s** | 36,702 chars |
| Optimized (`base.en`, greedy, multithread) | **2 min 12 s** | 36,620 chars |

This is a **~3.5× speedup (≈72% reduction) at zero additional cost**, with no measurable loss in transcript quality (near-identical character counts; unchanged downstream summary). 

**What we learned:** the intuition that "use a bigger/slower model for safety" was wrong for our use case — the cost-accuracy frontier favored the smaller English-specialized model, and the default beam search was paying for accuracy we did not need. The trade-off is that the system now assumes **English-spoken audio**; non-English meetings would transcribe poorly. This is consistent with our decision to scope the product to English. The Whisper model size is configurable via the `WHISPER_MODEL` environment variable (e.g. `tiny.en` for an even faster live demo at some accuracy cost).

## 5. Custom evaluation
_Our own test set (30–50 examples) with expected outputs. Quantitative results (accuracy / F1 / BLEU / task-appropriate metric). Methodology for building the set._

## 6. Failure mode analysis
_5–10 documented cases where the system fails or behaves unexpectedly, with hypotheses about why._

## 7. Future directions
_Unrealized features, grounded in what we built._

## 8. Use of AI tools
_How LLMs were used throughout the project (brainstorming, debugging, drafting, etc.)._

## 9. Conclusion
_TODO_

## References
_TODO_
