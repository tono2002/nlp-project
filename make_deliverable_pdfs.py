"""Generate PDFs for: executive summary, user manual, installation guide, individual reflections."""

from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, PageBreak, KeepTogether
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY

# ── Colours (same palette as technical report) ────────────────────────────────
INDIGO   = colors.HexColor("#4f46e5")
INDIGO_L = colors.HexColor("#eef2ff")
VIOLET   = colors.HexColor("#7c3aed")
GREY_DK  = colors.HexColor("#1e1b4b")
GREY_MD  = colors.HexColor("#4b5563")
GREY_LT  = colors.HexColor("#f3f4f6")
WHITE    = colors.white
BLACK    = colors.HexColor("#111827")

W, H = A4
MARGIN = 2.2 * cm

base = getSampleStyleSheet()

def style(name, parent="Normal", **kw):
    return ParagraphStyle(name, parent=base[parent], **kw)

S = {
    "h1": style("h1", "Heading1", fontSize=16, textColor=INDIGO, spaceBefore=18, spaceAfter=6, leading=20),
    "h2": style("h2", "Heading2", fontSize=12, textColor=VIOLET, spaceBefore=14, spaceAfter=4, leading=15),
    "body": style("body", "Normal", fontSize=10, textColor=BLACK, leading=15, spaceAfter=6, alignment=TA_JUSTIFY),
    "bullet": style("bullet", "Normal", fontSize=10, textColor=BLACK, leading=14, spaceAfter=3, leftIndent=14),
    "code": style("code", "Code", fontSize=8.5, textColor=GREY_DK, backColor=GREY_LT, leading=12, leftIndent=8, spaceAfter=8, spaceBefore=4),
}

def rule():
    return HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#e0e7ff"), spaceAfter=6)

def cover(canvas, doc, title, subtitle, meta="NLP Group Project · 2025–2026"):
    canvas.saveState()
    canvas.setFillColor(GREY_DK)
    canvas.rect(0, 0, W, H, fill=1, stroke=0)
    canvas.setFillColor(INDIGO)
    canvas.rect(0, H - 1.2*cm, W, 1.2*cm, fill=1, stroke=0)
    canvas.setFillColor(VIOLET)
    canvas.rect(0, 0, W, 0.6*cm, fill=1, stroke=0)
    canvas.setFillColor(WHITE)
    canvas.setFont("Helvetica-Bold", 32)
    canvas.drawCentredString(W/2, H*0.62, "SummarAI")
    canvas.setFillColor(colors.HexColor("#c7d2fe"))
    canvas.setFont("Helvetica", 16)
    canvas.drawCentredString(W/2, H*0.55, title)
    canvas.setStrokeColor(INDIGO)
    canvas.setLineWidth(1.5)
    canvas.line(W*0.3, H*0.51, W*0.7, H*0.51)
    canvas.setFillColor(colors.HexColor("#a5b4fc"))
    canvas.setFont("Helvetica", 11)
    canvas.drawCentredString(W/2, H*0.47, subtitle)
    canvas.setFont("Helvetica", 10)
    canvas.drawCentredString(W/2, H*0.41, meta)
    canvas.restoreState()

def footer(canvas, doc, label):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(GREY_MD)
    canvas.drawCentredString(W/2, 1.2*cm, f"SummarAI — {label}  ·  Page {doc.page}")
    canvas.restoreState()

def make_doc(path, label, cover_title, cover_sub, cover_meta=None):
    kwargs = dict(
        pagesize=A4,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=MARGIN, bottomMargin=MARGIN,
        title=cover_title, author="NLP Group",
    )
    doc = SimpleDocTemplate(str(path), **kwargs)
    meta = cover_meta or "NLP Group Project · 2025–2026"
    return doc, lambda c, d: cover(c, d, cover_title, cover_sub, meta), \
               lambda c, d: footer(c, d, label)


# ═══════════════════════════════════════════════════════════════════════════════
# 1. EXECUTIVE SUMMARY
# ═══════════════════════════════════════════════════════════════════════════════
def build_executive_summary():
    out = Path("deliverables/executive_summary.pdf")
    doc, first, later = make_doc(out, "Executive Summary", "Executive Summary",
                                 "Automated Meeting Summarization")
    story = [PageBreak()]

    story += [
        Paragraph("What We Built", S["h1"]), rule(),
        Paragraph(
            "SummarAI is an AI-powered meeting assistant that turns a recorded meeting into a "
            "structured written record. Upload the audio or video of any meeting and, within minutes, "
            "the app returns a plain-language summary, a list of the main decisions made, and a clear "
            "set of action items showing who is responsible for what.", S["body"]),
        Paragraph(
            "The key feature that sets SummarAI apart is language flexibility. Existing tools — such "
            "as Otter.ai or the built-in assistants in Zoom and Microsoft Teams — always produce their "
            "output in the same language as the meeting. SummarAI lets the user choose the output "
            "language independently. A meeting held in English can produce a Spanish summary and "
            "action-item list, or vice versa. For international teams where not everyone shares the "
            "same first language, this means every member receives the meeting record in the language "
            "they work best in.", S["body"]),
    ]

    story += [
        Spacer(1, 0.3*cm),
        Paragraph("Why It Matters", S["h1"]), rule(),
        Paragraph(
            "Unproductive meetings cost U.S. businesses an estimated $259 billion per year, according "
            "to a 2024 London School of Economics report. A large part of that cost is not the meetings "
            "themselves but what happens afterwards: decisions get forgotten, action items go unrecorded, "
            "and absent team members miss critical information. Studies show that 54% of employees "
            "regularly leave meetings without a clear understanding of the next steps.", S["body"]),
        Paragraph(
            "The problem is more acute in multilingual workplaces. Over 60% of knowledge workers in "
            "multinational companies regularly attend meetings conducted in a language other than their "
            "primary one. Receiving a meeting summary in a second language — at the moment when "
            "precision matters most — is a real barrier to follow-through and accountability.", S["body"]),
        Paragraph(
            "SummarAI addresses both problems at once: it automates the capture of meeting decisions "
            "and action items, and it delivers that information in the language the reader actually uses.", S["body"]),
    ]

    story += [
        Spacer(1, 0.3*cm),
        Paragraph("What We Found", S["h1"]), rule(),
        Paragraph(
            "We tested SummarAI on 40 meeting transcripts spanning English-only, Spanish-only, and "
            "cross-language scenarios. The system performed well on its core task: summaries were "
            "consistently coherent and action items were correctly identified in the large majority "
            "of cases.", S["body"]),
        Paragraph(
            "The main limitation we identified is owner attribution — correctly identifying who is "
            "responsible for each action item. When speakers are named explicitly in the conversation, "
            "attribution is reliable. When responsibility is implied rather than stated, the system "
            "sometimes leaves the owner blank or makes an incorrect inference. This is a known "
            "limitation of working with audio transcripts that do not label speakers, and it is the "
            "clearest direction for future improvement.", S["body"]),
        Paragraph(
            "Cross-language generation worked well for summaries and takeaways. Action items "
            "occasionally lost specific details such as deadlines or numeric targets in translation, "
            "which we document as a known failure mode.", S["body"]),
    ]

    story += [
        Spacer(1, 0.3*cm),
        Paragraph("Bottom Line", S["h1"]), rule(),
        Paragraph(
            "SummarAI demonstrates that a focused AI pipeline can meaningfully reduce the "
            "administrative burden of meetings — capturing decisions and tasks automatically, and "
            "making them accessible to every team member in their own language. The proof of concept "
            "is functional, the core differentiator is real, and the failure modes are well-understood "
            "and addressable. The most immediate next step is adding speaker identification so that "
            "action-item ownership can be assigned reliably without depending on participants being "
            "named out loud.", S["body"]),
    ]

    doc.build(story, onFirstPage=first, onLaterPages=later)
    print(f"Written: {out}")


# ═══════════════════════════════════════════════════════════════════════════════
# 2. USER MANUAL
# ═══════════════════════════════════════════════════════════════════════════════
def build_user_manual():
    out = Path("docs/user_manual.pdf")
    doc, first, later = make_doc(out, "User Manual", "User Manual", "How to use SummarAI")
    story = [PageBreak()]

    story += [
        Paragraph("Overview", S["h1"]), rule(),
        Paragraph(
            "SummarAI is a meeting summarisation tool. You give it a recorded meeting — as an "
            "audio/video file or a plain-text transcript — and it returns three things:", S["body"]),
        Paragraph("• <b>Summary</b> — a concise paragraph capturing what the meeting was about.", S["bullet"]),
        Paragraph("• <b>Key takeaways</b> — the main points and decisions made.", S["bullet"]),
        Paragraph("• <b>Action items</b> — concrete tasks, with the responsible person where identifiable.", S["bullet"]),
        Spacer(1, 0.2*cm),
        Paragraph(
            "The language of the output is your choice, not the language of the meeting. You can "
            "attend an English meeting and receive everything in Spanish, or vice versa.", S["body"]),
    ]

    story += [
        Spacer(1, 0.3*cm),
        Paragraph("Getting Started", S["h1"]), rule(),
        Paragraph("<b>Option A — Hosted version (recommended)</b>", S["h2"]),
        Paragraph("Open the app link in any modern browser (Chrome, Firefox, Safari, Edge). "
                  "No installation or account needed.", S["body"]),
        Paragraph("<b>Option B — Run locally</b>", S["h2"]),
        Paragraph("Follow the Installation Guide to set up the project, then run:", S["body"]),
        Paragraph("python src/app.py", S["code"]),
        Paragraph("Open http://127.0.0.1:7860 in your browser.", S["body"]),
    ]

    story += [
        Spacer(1, 0.3*cm),
        Paragraph("Uploading a Meeting", S["h1"]), rule(),
        Paragraph(
            "Drag and drop — or click Upload file — to load an audio, video, or transcript file. "
            "The supported formats are:", S["body"]),
        Paragraph("• Audio: .mp3, .wav, .m4a, .ogg, .flac", S["bullet"]),
        Paragraph("• Video: .mp4, .webm", S["bullet"]),
        Paragraph("• Text transcript: .txt, .md, .vtt, .srt", S["bullet"]),
        Spacer(1, 0.2*cm),
        Paragraph(
            "Once the file is loaded, click <b>Summarise</b>. A spinner with an elapsed timer "
            "will appear. Audio files take 1–8 minutes depending on length. Text files are "
            "nearly instant.", S["body"]),
    ]

    story += [
        Spacer(1, 0.3*cm),
        Paragraph("Reading the Output", S["h1"]), rule(),
        Paragraph("<b>Summary</b>", S["h2"]),
        Paragraph("One short paragraph — the meeting's purpose and overall outcome. "
                  "Designed to be readable in under 10 seconds.", S["body"]),
        Paragraph("<b>Key Takeaways</b>", S["h2"]),
        Paragraph("A list of bullet points, each tagged as either:", S["body"]),
        Paragraph("• <b>Decision</b> (purple) — something agreed, approved, or set as policy.", S["bullet"]),
        Paragraph("• <b>Note</b> (grey) — any other important point, fact, or concern.", S["bullet"]),
        Paragraph("<b>Action Items</b>", S["h2"]),
        Paragraph("A checklist of concrete tasks. Each item shows the task description, the owner "
                  "(if named in the meeting), and the deadline (if stated). You can check items off "
                  "as they are completed.", S["body"]),
    ]

    story += [
        Spacer(1, 0.3*cm),
        Paragraph("Saving to a Project", S["h1"]), rule(),
        Paragraph(
            "Click <b>Save to project</b> after a meeting is summarised. Choose an existing project "
            "from the sidebar or create a new one. Saved meetings appear in the project timeline "
            "in the left sidebar, ordered by date.", S["body"]),
        Paragraph(
            "You can delete individual saved meetings or entire projects from the sidebar. "
            "Deleting a project removes all meetings saved under it.", S["body"]),
    ]

    story += [
        Spacer(1, 0.3*cm),
        Paragraph("Known Limitations", S["h1"]), rule(),
        Paragraph("• Owner attribution is reliable only when the speaker is named explicitly in the meeting.", S["bullet"]),
        Paragraph("• Non-English audio is not supported. The ASR model is English-only.", S["bullet"]),
        Paragraph("• Very long meetings (2+ hours) may take 5–8 minutes to process.", S["bullet"]),
        Paragraph("• The app requires an internet connection to reach the Claude API.", S["bullet"]),
        Paragraph("• iOS Safari does not support push notifications for PWA installs.", S["bullet"]),
    ]

    doc.build(story, onFirstPage=first, onLaterPages=later)
    print(f"Written: {out}")


# ═══════════════════════════════════════════════════════════════════════════════
# 3. INSTALLATION GUIDE
# ═══════════════════════════════════════════════════════════════════════════════
def build_installation_guide():
    out = Path("docs/installation_guide.pdf")
    doc, first, later = make_doc(out, "Installation Guide", "Installation & Execution Guide",
                                 "How to run SummarAI locally")
    story = [PageBreak()]

    story += [
        Paragraph("Requirements", S["h1"]), rule(),
        Paragraph("• Python 3.10 or 3.11 (3.12+ not tested)", S["bullet"]),
        Paragraph("• pip 23+", S["bullet"]),
        Paragraph("• ffmpeg (any recent version) — required by Whisper for audio decoding", S["bullet"]),
        Paragraph("• Anthropic API key — needed for Claude summarisation", S["bullet"]),
        Paragraph("• At least 8 GB RAM and 3 GB free disk space for Whisper model weights", S["bullet"]),
        Spacer(1, 0.2*cm),
        Paragraph("Compatible with macOS, Linux, and Windows (PowerShell).", S["body"]),
    ]

    story += [
        Spacer(1, 0.3*cm),
        Paragraph("1. Clone the Repository", S["h1"]), rule(),
        Paragraph("git clone https://github.com/tono2002/nlp-project.git", S["code"]),
        Paragraph("cd nlp-project", S["code"]),
    ]

    story += [
        Spacer(1, 0.3*cm),
        Paragraph("2. Create a Virtual Environment", S["h1"]), rule(),
        Paragraph("python -m venv .venv", S["code"]),
        Paragraph("macOS / Linux:", S["body"]),
        Paragraph("source .venv/bin/activate", S["code"]),
        Paragraph("Windows (PowerShell):", S["body"]),
        Paragraph(".venv\\Scripts\\Activate.ps1", S["code"]),
    ]

    story += [
        Spacer(1, 0.3*cm),
        Paragraph("3. Install Python Dependencies", S["h1"]), rule(),
        Paragraph("pip install --upgrade pip", S["code"]),
        Paragraph("pip install -r requirements.txt", S["code"]),
    ]

    story += [
        Spacer(1, 0.3*cm),
        Paragraph("4. Install ffmpeg", S["h1"]), rule(),
        Paragraph("macOS:", S["body"]),
        Paragraph("brew install ffmpeg", S["code"]),
        Paragraph("Ubuntu / Debian:", S["body"]),
        Paragraph("sudo apt install ffmpeg", S["code"]),
        Paragraph("Windows — download from https://ffmpeg.org/download.html and add to PATH.", S["body"]),
    ]

    story += [
        Spacer(1, 0.3*cm),
        Paragraph("5. Configure Environment Variables", S["h1"]), rule(),
        Paragraph("Copy the example file and add your Anthropic API key:", S["body"]),
        Paragraph("cp .env.example .env", S["code"]),
        Paragraph("Open .env and set:", S["body"]),
        Paragraph("ANTHROPIC_API_KEY=sk-ant-...", S["code"]),
        Paragraph(
            "Supabase variables (SUPABASE_URL, SUPABASE_ANON_KEY) are optional. "
            "Without them, project saving is disabled but summarisation still works.", S["body"]),
    ]

    story += [
        Spacer(1, 0.3*cm),
        Paragraph("6. Run the App", S["h1"]), rule(),
        Paragraph("python src/app.py", S["code"]),
        Paragraph("Open http://127.0.0.1:7860 in your browser.", S["body"]),
        Spacer(1, 0.2*cm),
        Paragraph(
            "On first run, Whisper will download the base.en model weights (~145 MB). "
            "This happens once and is cached for subsequent runs.", S["body"]),
    ]

    story += [
        Spacer(1, 0.3*cm),
        Paragraph("7. Optional — Change the Whisper Model", S["h1"]), rule(),
        Paragraph(
            "The default model is base.en. For faster (less accurate) results use tiny.en; "
            "for better accuracy on noisy or accented audio use small.en:", S["body"]),
        Paragraph("WHISPER_MODEL=tiny.en python src/app.py", S["code"]),
        Paragraph("Available sizes: tiny.en · base.en · small.en · medium.en", S["body"]),
    ]

    story += [
        Spacer(1, 0.3*cm),
        Paragraph("Troubleshooting", S["h1"]), rule(),
        Paragraph("• <b>ffmpeg not found:</b> ensure ffmpeg is on your system PATH and restart your terminal.", S["bullet"]),
        Paragraph("• <b>Invalid API key:</b> check that ANTHROPIC_API_KEY is set correctly in .env.", S["bullet"]),
        Paragraph("• <b>Port already in use:</b> kill the existing process or change the port in app.py.", S["bullet"]),
        Paragraph("• <b>Slow transcription:</b> switch to tiny.en for demos; use small.en for better accuracy.", S["bullet"]),
    ]

    doc.build(story, onFirstPage=first, onLaterPages=later)
    print(f"Written: {out}")


# ═══════════════════════════════════════════════════════════════════════════════
# 4. INDIVIDUAL REFLECTIONS — one PDF per person
# ═══════════════════════════════════════════════════════════════════════════════

REFLECTIONS = {
    "antonio": {
        "file": "deliverables/reflections/antonio.md",
        "pdf":  "deliverables/reflections/antonio_reflection.pdf",
        "sections": [
            ("Whisper Optimization", [
                ("", "I profiled the full pipeline to find where time was being spent. The assumption "
                     "going in was that the LLM call would be the slow part — in practice, Claude Haiku "
                     "returns in a few seconds, while Whisper on a 20-minute audio file was taking close "
                     "to 8 minutes with the default configuration. I implemented four optimizations, all "
                     "of them zero-cost:"),
                ("Switched from the multilingual base model to base.en",
                 "The English-only variant is faster and more accurate for English audio."),
                ("Set beam_size=1 (greedy decoding)",
                 "Removes beam search overhead (~2× faster) with negligible accuracy loss for our task."),
                ("Set cpu_threads to use all available cores",
                 "Transcription runs fully parallel."),
                ("Passed language='en' explicitly",
                 "Skips the automatic language-detection pass."),
                ("Result", "Processing time dropped from 7 min 50 s to 2 min 12 s on the same "
                           "20-minute recording — a ~3.5× speedup with near-identical transcript quality."),
            ]),
            ("Evaluation Script", [
                ("", "I built data/eval/evaluate.py. The script loads all transcripts from eval_set.jsonl, "
                     "calls the same analyze() function used in production, compares predicted action items "
                     "against gold labels using the team's agreed matching rule, and outputs per-meeting "
                     "results plus micro-averaged precision, recall, and F1 to data/eval/results.json. "
                     "The matching logic uses normalized text similarity with a threshold of 0.6 and "
                     "greedy one-to-one assignment so each gold item is matched at most once."),
            ]),
            ("Installation Guide", [
                ("", "I wrote docs/installation_guide.md covering Python version requirements, virtual "
                     "environment setup, ffmpeg installation on macOS, Linux, and Windows, .env "
                     "configuration, and the exact commands to run the server."),
            ]),
            ("Labeled Transcripts", [
                ("", "I contributed approximately 8 labeled transcripts to eval_set.jsonl, including "
                     "sprint planning sessions and one deliberately ambiguous case where responsibility "
                     "is implied but no specific person is named."),
            ]),
            ("What I Learned", [
                ("", "Working on this project gave me a much more concrete understanding of how ASR "
                     "models like Whisper actually work under the hood — specifically the trade-off "
                     "between multilingual and language-specific models, and what beam search is doing "
                     "in a seq2seq decoder. Before this I understood beam search as a concept from the "
                     "course; seeing it actually cost us 3.5× in latency with no measurable quality "
                     "benefit made the accuracy-efficiency trade-off feel real rather than theoretical. "
                     "I also developed a much clearer sense of what precision and recall mean as "
                     "evaluation metrics for an information extraction task. A single accuracy number "
                     "would have hidden the difference between the model missing real action items "
                     "(recall failures) and inventing ones that were not there (precision failures) — "
                     "two completely different failure modes with different implications for trust."),
            ]),
        ],
    },
    "marti": {
        "file": "deliverables/reflections/marti.md",
        "pdf":  "deliverables/reflections/marti_reflection.pdf",
        "sections": [
            ("Frontend", [
                ("", "I built the entire frontend as a single HTML file (src/static/index.html) with no "
                     "framework dependencies — plain JavaScript and CSS only. The interface includes a "
                     "drag-and-drop upload area, a results panel with the summary, color-coded takeaway "
                     "bubbles (purple for decisions, grey for notes), an action item checklist, and a "
                     "collapsible sidebar showing the timeline of saved summarizations per project. The "
                     "layout is fully responsive and works on iPhone screens."),
                ("Loading state", "Transcription can take several minutes, so the interface shows a "
                                  "spinner with a running elapsed timer. Results render progressively "
                                  "as the JSON comes back from the API."),
                ("Error handling", "All failure states are handled explicitly — unsupported file type, "
                                   "missing API key, model error — so the user gets a clear message "
                                   "rather than a silent failure."),
            ]),
            ("Failure Mode Analysis", [
                ("", "After the evaluation was run, I documented the most informative failure cases in "
                     "data/eval/failure_analysis.md. Each case includes the transcript excerpt, the "
                     "model's output, the gold label, and a hypothesis for why it failed. Main patterns:"),
                ("Whisper mishearing proper nouns",
                 "Causes the owner field to be wrong even when the task is correct."),
                ("Phantom action items",
                 "The model generates commitments from hypothetical discussions."),
                ("Zero output on non-meeting audio",
                 "Correct behavior for podcasts, but may confuse users."),
                ("Implied responsibility",
                 "When no person is named, the model leaves owner null rather than guessing."),
            ]),
            ("Labeled Transcripts", [
                ("", "I contributed approximately 8 labeled transcripts to eval_set.jsonl, deliberately "
                     "designing difficult cases: meetings where no one is explicitly assigned a task, "
                     "shared responsibilities, and informally stated deadlines."),
            ]),
            ("What I Learned", [
                ("", "The most important thing I took away is how NLP errors propagate through a pipeline. "
                     "Whisper's transcription errors do not stay in the transcription layer — they flow "
                     "directly into the LLM output. If Whisper mishears a name, the action item will have "
                     "the wrong owner even if the model does everything else correctly. This cascading "
                     "failure is hard to see from an aggregate F1 score alone, and it made me understand "
                     "why failure mode analysis is treated as a required component of the assignment. I "
                     "also learned what information extraction means as an NLP task — it sits between "
                     "pure classification and open-ended generation, and the challenge is that the output "
                     "structure is constrained but the surface form is open, which is exactly why simple "
                     "rule-based approaches fail on real, messy transcripts."),
            ]),
        ],
    },
    "bojana": {
        "file": "deliverables/reflections/bojana.md",
        "pdf":  "deliverables/reflections/bojana_reflection.pdf",
        "sections": [
            ("Backend and NLP Pipeline", [
                ("", "I built the entire server-side application (src/app.py). This includes the FastAPI "
                     "server, the file upload endpoint, and the full two-stage NLP pipeline: routing audio "
                     "files through faster-whisper for transcription, then passing the transcript to Claude "
                     "Haiku 4.5 to extract the summary, typed takeaways, and action items. I also built all "
                     "project management endpoints — creating, listing, and deleting projects and saved "
                     "summarizations — using a thin HTTP wrapper to avoid adding a full Supabase client "
                     "library as a dependency."),
                ("Input type routing",
                 "Audio and video files need to be written to a temporary file on disk before Whisper "
                 "can process them. Text files are read directly into memory. Temporary files are "
                 "cleaned up reliably using try/finally even when transcription fails."),
            ]),
            ("System Prompt and Output Schema", [
                ("", "I designed the system prompt and the JSON output schema that enforces the structure "
                     "Claude must return. The schema defines three required fields — summary, key_takeaways, "
                     "and action_items — with strict types and no additional properties allowed. Early "
                     "versions produced inconsistent output: action items appearing inside the summary, "
                     "takeaways missing their type tag, or the model inventing owners not in the transcript. "
                     "I iterated on the prompt until the model reliably separated the three output types "
                     "and only included owners and deadlines when explicitly stated. The final prompt and "
                     "schema are saved in prompts/."),
            ]),
            ("Labeled Transcripts", [
                ("", "I created approximately 8 transcripts for eval_set.jsonl, including standup meetings, "
                     "sprint planning sessions, and one edge case where a speaker discusses a hypothetical "
                     "future action without committing — designed to test whether the model invents phantom "
                     "action items."),
            ]),
            ("What I Learned", [
                ("", "This project gave me a real understanding of prompt engineering as an NLP technique "
                     "rather than just a trick. When we started, the model would sometimes invent owners "
                     "not mentioned in the transcript, or merge two separate action items into one. Fixing "
                     "this required understanding why the model was doing it — it was following conversational "
                     "implicature, inferring responsibility from context the way a human would — and then "
                     "writing a prompt constraint specific enough to override that default behavior. I also "
                     "came to appreciate what makes LLM-based information extraction different from "
                     "traditional approaches: the model handles paraphrase, messy grammar, and implicit "
                     "references naturally. The cost is that you cannot fully predict or control the output, "
                     "which is exactly why structured schemas and evaluation against gold labels are "
                     "necessary."),
            ]),
        ],
    },
    "jo": {
        "file": "deliverables/reflections/jo.md",
        "pdf":  "deliverables/reflections/jo_reflection.pdf",
        "sections": [
            ("Supabase Database Layer", [
                ("", "I designed and set up the entire persistence layer for the app. I wrote "
                     "supabase_schema.sql, which defines two tables: projects (for grouping meetings) and "
                     "summarizations (for storing the full structured output). A key design decision was "
                     "storing key_takeaways and action_items as JSONB columns rather than flat text, "
                     "preserving the structured data as queryable fields rather than serialised strings."),
                ("Cascade delete",
                 "The schema includes a foreign key from summarizations to projects with cascade delete, "
                 "so removing a project automatically removes all its meetings."),
                ("Row-level security",
                 "RLS policies allow public read/write access without requiring user accounts — "
                 "appropriate for a POC and documented as a limitation for production."),
                ("", "I also verified that the backend endpoints matched what Supabase expected — "
                     "checking that REST calls for creating, listing, and deleting projects and "
                     "summarizations all worked correctly against the live database."),
            ]),
            ("Field Review", [
                ("", "I researched the meeting-AI and transcription industry and wrote the field review "
                     "section of the technical report. I covered the major existing tools — Otter.ai, "
                     "Fireflies.ai, Zoom AI Companion, Fathom, and tl;dv — and analysed what they offer "
                     "and what they consistently lack. Most produce a single undifferentiated list of "
                     "bullet points; none separate decisions from notes. I cited sources from ACL Anthology, "
                     "arXiv, and industry reports to ground the review in published research."),
            ]),
            ("Labeled Transcripts", [
                ("", "I contributed approximately 8 labeled transcripts to eval_set.jsonl, including "
                     "excerpts from public city council meeting minutes — real, verbatim, and messy, "
                     "with decisions both with and without clear owners."),
            ]),
            ("What I Learned", [
                ("", "Doing the field review made me understand the difference between what NLP research "
                     "has achieved and what is actually deployed in real products. There is a large body of "
                     "work on meeting summarization, action item extraction, and dialogue act classification "
                     "going back years, yet mainstream commercial tools still produce simple undifferentiated "
                     "bullet lists. The research-to-product gap is real and wider than I expected. I also "
                     "developed a clearer understanding of the different NLP subtasks our system combines: "
                     "automatic speech recognition (Whisper), abstractive summarization (the two-sentence "
                     "summary), and named entity and relation extraction (pulling out task, owner, and "
                     "deadline as structured fields). Each has its own failure modes and literature, and "
                     "the overall system quality is limited by whichever stage performs worst on a given "
                     "input."),
            ]),
        ],
    },
    "smaragda": {
        "file": "deliverables/reflections/smaragda.md",
        "pdf":  "deliverables/reflections/smaragda_reflection.pdf",
        "sections": [
            ("Evaluation Set Design and Annotation Methodology", [
                ("", "I designed the evaluation set the whole team used to measure the system. This "
                     "included deciding on the format of eval_set.jsonl, writing the annotation guidelines "
                     "the team followed when labeling, and coordinating labeling across all five members "
                     "so everyone applied the same rules consistently."),
                ("What counts as an action item",
                 "A concrete commitment by a named or identifiable person — not a vague intention or "
                 "a plan the team discussed but did not commit to."),
                ("Missing deadlines",
                 "Leave the deadline field blank rather than infer one."),
                ("Overlapping items",
                 "When one transcript has multiple overlapping action items for the same person, "
                 "list each separately."),
                ("", "I also ensured the test set covered a realistic range of meeting types: standups, "
                     "planning sessions, sales calls, retrospectives, and tricky cases (no action items "
                     "at all, ambiguous ownership, hypothetical discussions). I contributed approximately "
                     "8 transcripts myself, focusing on multilingual scenarios."),
            ]),
            ("Executive Summary", [
                ("", "I wrote deliverables/executive_summary.md — the one-page non-technical description "
                     "of the project. I led with the cost of unproductive meetings and the specific barrier "
                     "multilingual teams face, then described what SummarAI does differently, then "
                     "summarised the evaluation findings including the main limitation around owner "
                     "attribution."),
            ]),
            ("User Manual", [
                ("", "I wrote docs/user_manual.md from scratch, walking through every feature: uploading "
                     "a file, choosing the output language, reading the summary and takeaway bubbles, "
                     "checking off action items, saving to a project, and browsing the project timeline. "
                     "I also documented supported formats, known limitations, and common questions."),
            ]),
            ("Slides", [
                ("", "I put together the presentation slides (deliverables/slides.md), structuring the "
                     "20-minute presentation as: problem and motivation → field review → system overview "
                     "→ evaluation method and results → failure cases → future directions → Q&A."),
            ]),
            ("What I Learned", [
                ("", "Building the annotation guidelines taught me that the definition of a label is "
                     "itself a research decision with real consequences for the evaluation. We started "
                     "with a vague shared understanding of what an action item was, and when I tried to "
                     "write it down precisely, edge cases appeared immediately: is 'we should probably "
                     "follow up on this' an action item? What if no one is named as responsible? What if "
                     "someone agrees to do something only conditionally? These decisions determine what "
                     "the model is being evaluated against — so they determine what the evaluation "
                     "actually measures. I now understand why inter-annotator agreement is reported in "
                     "NLP papers: it is not a formality, it is evidence that the label definition is "
                     "precise enough to be applied consistently. I also understood more deeply what the "
                     "summarization task is about: not just shortening text, but identifying what is "
                     "important and representing it in a structured, reusable form."),
            ]),
        ],
    },
}


def reflection_story_for(name, data):
    """Return story elements for one person (no cover, starts with a page break)."""
    story = [PageBreak()]
    story.append(Paragraph(f"Individual Reflection — {name.capitalize()}", S["h1"]))
    story.append(rule())
    story.append(Spacer(1, 0.1*cm))
    story.append(Paragraph("My Contributions", S["h1"]))
    story.append(rule())

    for section_title, items in data["sections"]:
        if section_title == "What I Learned":
            story.append(Spacer(1, 0.3*cm))
            story.append(Paragraph("What I Learned", S["h1"]))
            story.append(rule())
            for _, text in items:
                story.append(Paragraph(text, S["body"]))
        else:
            story.append(Paragraph(section_title, S["h2"]))
            for sub_title, text in items:
                if sub_title:
                    story.append(Paragraph(f"<b>{sub_title}:</b> {text}", S["bullet"]))
                else:
                    story.append(Paragraph(text, S["body"]))
    return story


def build_reflections_combined():
    out = Path("deliverables/reflections/all_reflections.pdf")
    doc, first, later = make_doc(
        out, "Individual Reflections", "Individual Reflections",
        "Antonio · Bojana · Jo · Martí · Smaragda",
    )
    story = [PageBreak()]  # cover on page 1, content from page 2

    for name, data in REFLECTIONS.items():
        story += reflection_story_for(name, data)

    doc.build(story, onFirstPage=first, onLaterPages=later)
    print(f"Written: {out}")


if __name__ == "__main__":
    build_executive_summary()
    build_user_manual()
    build_installation_guide()
    build_reflections_combined()
    print("\nAll PDFs generated.")
