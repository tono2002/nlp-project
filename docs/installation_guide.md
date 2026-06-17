## Installation & Execution Guide

> **Option 1 deliverable.** A reader should be able to run the project from scratch following this guide.

---

## Requirements

| Requirement | Version | Notes |
|---|---|---|
| Python | 3.10 or 3.11 | 3.12+ not tested |
| pip | 23+ | comes with Python |
| ffmpeg | any recent | required by Whisper for audio decoding |
| Anthropic API key | — | needed for Claude summarisation |
| RAM | ≥ 8 GB | Whisper `small` fits comfortably; `medium` needs ~12 GB |
| Disk space | ≥ 3 GB | for Whisper model weights |

> **OS:** macOS, Linux, or Windows (PowerShell). All commands below are cross-platform unless noted.

---

## Setup

```bash
# 1. Clone the repository
git clone https://github.com/tono2002/nlp-project.git
cd nlp-project

# 2. Create and activate a virtual environment
python -m venv .venv

# macOS / Linux
source .venv/bin/activate

# Windows (PowerShell)
.venv\Scripts\Activate.ps1

# 3. Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### Install ffmpeg

ffmpeg is required by Whisper to decode audio and video files.

```bash
# macOS (Homebrew)
brew install ffmpeg

# Ubuntu / Debian
sudo apt update && sudo apt install ffmpeg

# Windows — download from https://ffmpeg.org/download.html
# and add the bin/ folder to your PATH
```

Verify the installation:

```bash
ffmpeg -version
```

---

## Configuration

Copy the example environment file and fill in your API key:

```bash
cp .env.example .env
```

Open `.env` and set your Anthropic API key:

```
ANTHROPIC_API_KEY=sk-ant-...
```

> The key is only used for the Claude summarisation step. Whisper transcription runs fully locally.
> Never commit your `.env` file — it is already listed in `.gitignore`.

---

## Running the app

```bash
python src/app.py
```

The Gradio interface will start and print a local URL:

```
Running on local URL: http://127.0.0.1:7860
```

Open that URL in your browser. You will see three input options:

1. **Upload a file** — drag and drop an audio or video file (`.mp3`, `.mp4`, `.wav`, `.m4a`). Whisper will transcribe it automatically.
2. **Paste a transcript** — if you already have the text, paste it directly to skip the ASR step.
3. **Output language** — select `English` or `Spanish`. SummarAI will generate the summary, key takeaways, and action items in the chosen language regardless of the meeting's source language.

Click **Summarise** and wait. Transcription typically takes 1–3× real-time on CPU (e.g. a 10-minute meeting takes 10–30 seconds). Claude generation adds a further 5–10 seconds.

---

## Hosted version

> Live link: _TODO — add Hugging Face Spaces or similar URL once deployed._

---

## Running the evaluation

The evaluation pipeline reproduces the results reported in Section 5.3 of the technical report.

```bash
# Make sure you are in the repo root with the virtual environment active

# 1. Run the pipeline on the test set
python evaluation/run_eval.py \
    --test-set data/eval/test_set.csv \
    --output-dir data/eval/results/

# 2. Compute metrics (ROUGE-L, BERTScore, action-item F1)
python evaluation/compute_metrics.py \
    --results-dir data/eval/results/ \
    --output data/eval/metrics_summary.csv

# 3. Inspect results
cat data/eval/metrics_summary.csv
```

The test set CSV lives at `data/eval/test_set.csv`. Each row contains:

| Column | Description |
|---|---|
| `audio_id` | Filename (without extension) |
| `transcript` | Full meeting transcript text |
| `ref_summary` | Human-written reference summary |
| `ref_takeaways` | Semicolon-separated reference takeaways |
| `ref_actions` | Semicolon-separated reference action items (`task\|owner`) |
| `language_in` | Source language of the meeting (`en` / `es`) |
| `language_out` | Target output language for evaluation (`en` / `es`) |

See `evaluation/README.md` for details on the annotation methodology and inter-annotator agreement.

---

## Project structure

```
nlp-project/
├── src/
│   ├── app.py              # Gradio UI — entry point
│   ├── transcriber.py      # Whisper ASR wrapper
│   ├── summariser.py       # Claude API calls (summary, takeaways, actions)
│   └── prompts/            # Versioned system prompts
├── evaluation/
│   ├── run_eval.py         # Runs the pipeline on the test set
│   ├── compute_metrics.py  # ROUGE-L, BERTScore, action-item F1
│   └── README.md           # Annotation guide
├── data/
│   ├── eval/
│   │   ├── test_set.csv    # 40 annotated transcripts
│   │   └── results/        # Pipeline outputs (gitignored)
│   └── samples/            # Example audio files for quick testing
├── deliverables/
│   ├── technical_report.pdf
│   ├── user_manual.md
│   └── installation_guide.md   ← you are here
├── docs/
├── .env.example
├── requirements.txt
└── README.md
```

---

## Troubleshooting

**`ModuleNotFoundError: No module named 'whisper'`**
Make sure your virtual environment is active (`source .venv/bin/activate` or `.venv\Scripts\Activate.ps1`) before running any commands.

**`FileNotFoundError: ffmpeg not found`**
ffmpeg is not installed or not on your PATH. Follow the ffmpeg installation steps above and restart your terminal.

**`anthropic.AuthenticationError`**
Your `ANTHROPIC_API_KEY` in `.env` is missing or invalid. Double-check the key at console.anthropic.com.

**Whisper is very slow**
By default the app uses the `small` model. You can switch to `tiny` for faster (lower accuracy) transcription by setting `WHISPER_MODEL=tiny` in your `.env`. For GPU acceleration, make sure `torch` is installed with CUDA support.

**Out of memory error with Whisper**
Try setting `WHISPER_MODEL=tiny` or `WHISPER_MODEL=base` in `.env`.
