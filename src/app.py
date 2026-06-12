"""SummarAI — bilingual (EN/ES) meeting summarizer.

Pipeline: audio/video or transcript → Whisper (if audio) → Claude → summary,
key takeaways, and action items in the user's chosen language.
"""

import json
import os
import tempfile
from pathlib import Path

import anthropic
from dotenv import load_dotenv
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

app = FastAPI(title="SummarAI")

STATIC_DIR = Path(__file__).resolve().parent / "static"

AUDIO_EXTENSIONS = {".mp4", ".mp3", ".wav", ".m4a", ".webm", ".ogg", ".flac"}
TEXT_EXTENSIONS = {".txt", ".md", ".vtt", ".srt"}
MAX_TRANSCRIPT_CHARS = 300_000  # ~75K tokens, well within the context window

LANGUAGE_NAMES = {"en": "English", "es": "Spanish"}

OUTPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "summary": {
            "type": "string",
            "description": "Concise summary of the meeting (2-4 paragraphs).",
        },
        "key_takeaways": {
            "type": "array",
            "items": {"type": "string"},
            "description": "The main points and decisions, one per item.",
        },
        "action_items": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "task": {"type": "string"},
                    "owner": {
                        "type": ["string", "null"],
                        "description": "Person responsible, null if not stated.",
                    },
                    "deadline": {
                        "type": ["string", "null"],
                        "description": "Deadline as stated in the meeting, null if none.",
                    },
                },
                "required": ["task", "owner", "deadline"],
                "additionalProperties": False,
            },
        },
        "detected_language": {
            "type": "string",
            "description": "Main language of the source transcript.",
        },
    },
    "required": ["summary", "key_takeaways", "action_items", "detected_language"],
    "additionalProperties": False,
}

SYSTEM_PROMPT = """\
You are SummarAI, an expert meeting analyst. You receive a raw meeting \
transcript (possibly noisy, unpunctuated, or mixing languages) and produce:
1. A concise summary capturing purpose, discussion, and outcomes.
2. Key takeaways: the decisions and main points, each standing on its own.
3. Action items: concrete tasks someone committed to. Extract the owner and \
deadline only when actually stated — never invent them. Do not list vague \
intentions ("we should think about X") as action items.

Write ALL output in {language}, regardless of the transcript's language. \
Keep proper names, product names, and quoted terms in their original form."""

_whisper_model = None


def transcribe(path: str) -> str:
    """Transcribe an audio/video file with local Whisper (lazy-loaded)."""
    global _whisper_model
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        raise HTTPException(
            status_code=500,
            detail="Audio transcription requires faster-whisper. "
            "Install it with: pip install faster-whisper",
        )
    if _whisper_model is None:
        _whisper_model = WhisperModel("base", compute_type="int8")
    segments, _info = _whisper_model.transcribe(path, vad_filter=True)
    return " ".join(segment.text.strip() for segment in segments)


def analyze(transcript: str, language: str) -> dict:
    """Send the transcript to Claude and get structured insights back."""
    client = anthropic.Anthropic()
    response = client.messages.create(
        model="claude-haiku-4-5",  # cheapest model — summarization doesn't need more
        max_tokens=8192,
        system=SYSTEM_PROMPT.format(language=LANGUAGE_NAMES[language]),
        messages=[{"role": "user", "content": f"<transcript>\n{transcript}\n</transcript>"}],
        output_config={"format": {"type": "json_schema", "schema": OUTPUT_SCHEMA}},
    )
    text = next(block.text for block in response.content if block.type == "text")
    return json.loads(text)


@app.get("/")
def index():
    return FileResponse(STATIC_DIR / "index.html")


@app.post("/api/process")
async def process(file: UploadFile = File(...), language: str = Form("en")):
    if language not in LANGUAGE_NAMES:
        raise HTTPException(status_code=400, detail="Language must be 'en' or 'es'.")
    if not os.environ.get("ANTHROPIC_API_KEY"):
        raise HTTPException(
            status_code=500,
            detail="ANTHROPIC_API_KEY is not set. Copy .env.example to .env and add your key.",
        )

    extension = Path(file.filename or "").suffix.lower()
    if extension in TEXT_EXTENSIONS:
        raw = await file.read()
        transcript = raw.decode("utf-8", errors="replace")
    elif extension in AUDIO_EXTENSIONS:
        with tempfile.NamedTemporaryFile(suffix=extension, delete=False) as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name
        try:
            transcript = transcribe(tmp_path)
        finally:
            os.unlink(tmp_path)
    else:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type '{extension}'. "
            f"Use audio/video ({', '.join(sorted(AUDIO_EXTENSIONS))}) "
            f"or text ({', '.join(sorted(TEXT_EXTENSIONS))}).",
        )

    transcript = transcript.strip()
    if not transcript:
        raise HTTPException(status_code=400, detail="The file contains no usable text.")
    if len(transcript) > MAX_TRANSCRIPT_CHARS:
        raise HTTPException(
            status_code=400,
            detail="Transcript is too long for the POC (max ~300K characters). "
            "Split the meeting into parts.",
        )

    try:
        result = analyze(transcript, language)
    except anthropic.AuthenticationError:
        raise HTTPException(status_code=500, detail="Invalid Anthropic API key.")
    except anthropic.APIError as exc:
        raise HTTPException(status_code=502, detail=f"Claude API error: {exc.message}")
    except (json.JSONDecodeError, StopIteration):
        raise HTTPException(status_code=502, detail="Model returned a malformed response. Try again.")

    result["transcript_chars"] = len(transcript)
    return result


app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
