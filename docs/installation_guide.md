# SummarAI: Installation & Execution Guide

This guide takes you from a fresh clone to a running app. It assumes you are comfortable in a terminal.

## Requirements

| Requirement | Notes |
|---|---|
| Python 3.9+ | Developed and tested on 3.9 |
| An Anthropic API key | Used for the summarisation step ([console.anthropic.com](https://console.anthropic.com)) |
| ~1 GB free disk | For the Whisper transcription model, downloaded on first use |

You do **not** need to install ffmpeg separately, audio decoding is handled by a library bundled with the transcription engine.

## Setup

```bash
# 1. Clone and enter the project
git clone https://github.com/tono2002/nlp-project.git
cd nlp-project

# 2. Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate          # macOS / Linux
# .venv\Scripts\Activate.ps1        # Windows (PowerShell)

# 3. Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

## Configuration

Copy the example environment file and add your Anthropic key:

```bash
cp .env.example .env
```

Then open `.env` and set:

```
ANTHROPIC_API_KEY=sk-ant-...
```

That is the only value you need to run the app. (The Supabase variables are optional, they enable saving meetings into projects, and the project ships with working defaults.) Your `.env` is already git-ignored, so the key won't be committed.

## Running the app

```bash
uvicorn src.app:app --reload
```

Uvicorn prints a local URL, open it in a browser:

```
Uvicorn running on http://127.0.0.1:8000
```

You'll see the upload area. Drop in an audio file (`.mp4`, `.mp3`, `.wav`, `.m4a`, …) or a text transcript (`.txt`, `.vtt`, …) and click **Summarise**.

A few notes on first use:

- The first time you process **audio**, the app downloads the Whisper `base.en` model (~150 MB). This happens once; later runs reuse it.
- Transcription runs on the CPU and takes roughly a tenth of the recording's length (a 20-minute meeting transcribes in about two minutes). Text transcripts skip this step entirely.
- To trade accuracy for speed, set `WHISPER_MODEL=tiny.en` in `.env`.

## Project structure

```
nlp-project/
├── src/
│   ├── app.py              # FastAPI app: endpoints, Whisper transcription, Claude summarisation
│   └── static/
│       └── index.html      # Single-page front end
├── data/eval/
│   ├── transcribe_all.py   # Batch-transcribes the evaluation recordings
│   ├── evaluate_rouge.py   # Scores summaries against AMI human references
│   ├── _match.py           # Maps recordings to AMI meeting IDs
│   ├── transcripts/        # Whisper transcripts of the 30 eval meetings
│   └── results.json        # Evaluation results
├── docs/                   # User manual, this guide
├── deliverables/           # Report, executive summary, slides, reflections
├── requirements.txt
├── .env.example
└── README.md
```

## Reproducing the evaluation

The numbers in the technical report come from `data/eval/`. To regenerate them:

```bash
# 1. Download the AMI human annotations (~23 MB, not committed)
mkdir -p data/eval/ami_raw && cd data/eval/ami_raw
curl -sO https://groups.inf.ed.ac.uk/ami/AMICorpusAnnotations/ami_public_manual_1.6.2.zip
unzip -q ami_public_manual_1.6.2.zip && cd -

# 2. Run the evaluation (uses the committed transcripts in data/eval/transcripts/)
python data/eval/evaluate_rouge.py
```

This runs SummarAI on the 30 evaluation transcripts and prints ROUGE scores plus action-item coverage, writing the full breakdown to `data/eval/results.json`. See [`data/eval/README.md`](../data/eval/README.md) for the methodology.

## Troubleshooting

**`anthropic.AuthenticationError`**: the key in `.env` is missing or wrong. Check it at console.anthropic.com.

**`ANTHROPIC_API_KEY is not set`**: you started the server before creating `.env`, or in a different shell. Confirm `.env` exists in the project root and restart.

**First audio upload hangs for a minute**: it's downloading the Whisper model. Watch the terminal; it only happens once.

**Transcription feels slow**: set `WHISPER_MODEL=tiny.en` in `.env` for a faster (slightly less accurate) model.
