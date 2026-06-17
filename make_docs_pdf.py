"""Generate all 4 submission PDFs matching the SummarAI template."""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable,
    PageBreak, KeepTogether, Preformatted
)

W, H = A4
MARGIN = 2.2 * cm

# ── Palette ───────────────────────────────────────────────────────────────────
C_BG      = colors.HexColor("#1e1b4b")
C_INDIGO  = colors.HexColor("#4f46e5")
C_VIOLET  = colors.HexColor("#7c3aed")
C_LAVEND  = colors.HexColor("#c7d2fe")
C_MUTED   = colors.HexColor("#a5b4fc")
C_BODY    = colors.HexColor("#111827")
C_GREY    = colors.HexColor("#6b7280")
C_CODE_BG = colors.HexColor("#f3f4f6")
C_CODE_BD = colors.HexColor("#e5e7eb")
C_H1      = colors.HexColor("#3730a3")
C_H2      = colors.HexColor("#6d28d9")
C_H3      = colors.HexColor("#7c3aed")
WHITE     = colors.white

# ── Styles ────────────────────────────────────────────────────────────────────
def S(name, parent="Normal", **kw):
    return ParagraphStyle(name, parent=getSampleStyleSheet()[parent], **kw)

STYLES = {
    "h1":     S("h1",  "Heading1", fontSize=16, textColor=C_H1,    spaceBefore=20, spaceAfter=4,  leading=20),
    "h2":     S("h2",  "Heading2", fontSize=13, textColor=C_H2,    spaceBefore=16, spaceAfter=4,  leading=16),
    "h3":     S("h3",  "Heading3", fontSize=11, textColor=C_H3,    spaceBefore=12, spaceAfter=3,  leading=14),
    "body":   S("body","Normal",   fontSize=10, textColor=C_BODY,  leading=15, spaceAfter=6,  alignment=TA_JUSTIFY),
    "bullet": S("bul", "Normal",   fontSize=10, textColor=C_BODY,  leading=14, spaceAfter=3,  leftIndent=14),
    "sub":    S("sub", "Normal",   fontSize=10, textColor=C_BODY,  leading=14, spaceAfter=3,  leftIndent=28, firstLineIndent=0),
    "footer": S("ft",  "Normal",   fontSize=8,  textColor=C_GREY,  alignment=TA_CENTER),
}

def rule():
    return HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#e0e7ff"), spaceAfter=8, spaceBefore=2)

def h1(text):
    return KeepTogether([Paragraph(text, STYLES["h1"]), rule()])

def h2(text):
    return KeepTogether([Paragraph(text, STYLES["h2"]), rule()])

def h3(text):
    return Paragraph(text, STYLES["h3"])

def body(text):
    return Paragraph(text, STYLES["body"])

def bullet(text):
    return Paragraph(u"• " + text, STYLES["bullet"])

def sub(text):
    return Paragraph(text, STYLES["sub"])

def code(text):
    return Preformatted(
        text,
        ParagraphStyle("code", fontName="Courier", fontSize=8.5, textColor=C_H1,
                       backColor=C_CODE_BG, leading=12, leftIndent=8, rightIndent=8,
                       spaceBefore=4, spaceAfter=8, borderPad=4,
                       borderColor=C_CODE_BD, borderWidth=0.5, borderRadius=4)
    )

def sp(n=1):
    return Spacer(1, n * 0.25 * cm)


# ── Cover builder ─────────────────────────────────────────────────────────────
def make_cover(canvas, doc, title, subtitle, description):
    canvas.saveState()
    canvas.setFillColor(C_BG)
    canvas.rect(0, 0, W, H, fill=1, stroke=0)
    canvas.setFillColor(C_INDIGO)
    canvas.rect(0, H - 1.1*cm, W, 1.1*cm, fill=1, stroke=0)
    canvas.setFillColor(C_VIOLET)
    canvas.rect(0, 0, W, 0.55*cm, fill=1, stroke=0)

    canvas.setFillColor(WHITE)
    canvas.setFont("Helvetica-Bold", 38)
    canvas.drawCentredString(W/2, H * 0.60, "SummarAI")

    canvas.setFillColor(C_LAVEND)
    canvas.setFont("Helvetica", 17)
    canvas.drawCentredString(W/2, H * 0.53, title)

    canvas.setStrokeColor(C_INDIGO)
    canvas.setLineWidth(1.5)
    canvas.line(W*0.28, H*0.49, W*0.72, H*0.49)

    canvas.setFillColor(C_MUTED)
    canvas.setFont("Helvetica", 11)
    canvas.drawCentredString(W/2, H * 0.45, subtitle)

    canvas.setFont("Helvetica", 10)
    canvas.drawCentredString(W/2, H * 0.39, description)
    canvas.restoreState()


def later_page(footer_text):
    def fn(canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(C_GREY)
        canvas.drawCentredString(W/2, 1.1*cm, f"{footer_text}  .  Page {doc.page}")
        canvas.restoreState()
    return fn


def build_pdf(path, cover_title, cover_subtitle, cover_desc, footer, story):
    out_dir = os.path.dirname(path)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    doc = SimpleDocTemplate(
        path, pagesize=A4,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=MARGIN, bottomMargin=MARGIN + 0.4*cm,
    )

    first_cover = [None]
    def first_page(canvas, doc):
        make_cover(canvas, doc, cover_title, cover_subtitle, cover_desc)
        first_cover[0] = (cover_title, cover_subtitle, cover_desc)

    doc.build([PageBreak()] + story,
              onFirstPage=first_page,
              onLaterPages=later_page(footer))
    print(f"  wrote {path}")


# ═══════════════════════════════════════════════════════════════════════════════
# 1. EXECUTIVE SUMMARY
# ═══════════════════════════════════════════════════════════════════════════════
def build_executive_summary():
    story = []

    story.append(h1("What We Built"))
    story.append(body(
        "SummarAI is an AI-powered meeting assistant that turns a recorded meeting into a structured "
        "written record. Upload the audio or video of any meeting and, within minutes, the app returns "
        "a plain-language summary, a list of the main decisions made, and a clear set of action items "
        "showing who is responsible for what."
    ))
    story.append(body(
        "The key feature that sets SummarAI apart is language flexibility. Existing tools "
        "such as Otter.ai or the built-in assistants in Zoom and Microsoft Teams "
        "always produce their output in the same language as the meeting. SummarAI lets "
        "the user choose the output language independently. A meeting held in English can produce "
        "a Spanish summary and action-item list, or vice versa. For international teams where not "
        "everyone shares the same first language, this means every member receives the meeting "
        "record in the language they work best in."
    ))

    story.append(sp())
    story.append(h1("Why It Matters"))
    story.append(body(
        "Unproductive meetings cost U.S. businesses an estimated $259 billion per year, according "
        "to a 2024 London School of Economics report. A large part of that cost is not the meetings "
        "themselves but what happens afterwards: decisions get forgotten, action items go unrecorded, "
        "and absent team members miss critical information. Studies show that 54% of employees "
        "regularly leave meetings without a clear understanding of the next steps."
    ))
    story.append(body(
        "The problem is more acute in multilingual workplaces. Over 60% of knowledge workers in "
        "multinational companies regularly attend meetings conducted in a language other than their "
        "primary one. Receiving a meeting summary in a second language at the moment when precision "
        "matters most is a real barrier to follow-through and accountability."
    ))
    story.append(body(
        "SummarAI addresses both problems at once: it automates the capture of meeting decisions "
        "and action items, and it delivers that information in the language the reader actually uses."
    ))

    story.append(sp())
    story.append(h1("What We Found"))
    story.append(body(
        "We tested SummarAI on 40 meeting transcripts spanning English-only, Spanish-only, and "
        "cross-language scenarios. The system performed well on its core task: summaries were "
        "consistently coherent and action items were correctly identified in the large majority of cases."
    ))
    story.append(body(
        "The main limitation we identified is owner attribution: correctly identifying who is responsible "
        "for each action item. When speakers are named explicitly in the conversation, attribution is "
        "reliable. When responsibility is implied rather than stated, the system sometimes leaves the "
        "owner blank or makes an incorrect inference. This is a known limitation of working with audio "
        "transcripts that do not label speakers, and it is the clearest direction for future improvement."
    ))
    story.append(body(
        "Cross-language generation worked well for summaries and takeaways. Action items occasionally "
        "lost specific details such as deadlines or numeric targets in translation, which we document "
        "as a known failure mode."
    ))

    story.append(sp())
    story.append(h1("Bottom Line"))
    story.append(body(
        "SummarAI demonstrates that a focused AI pipeline can meaningfully reduce the administrative "
        "burden of meetings: capturing decisions and tasks automatically, and making them accessible "
        "to every team member in their own language. The proof of concept is functional, the core "
        "differentiator is real, and the failure modes are well-understood and addressable. The most "
        "immediate next step is adding speaker identification so that action-item ownership can be "
        "assigned reliably without depending on participants being named out loud."
    ))

    build_pdf(
        "docs/executive_summary.pdf",
        "Executive Summary",
        "Automated Meeting Summarization",
        "NLP Group Project . 2025-2026",
        "SummarAI - Executive Summary",
        story,
    )


# ═══════════════════════════════════════════════════════════════════════════════
# 2. INSTALLATION GUIDE
# ═══════════════════════════════════════════════════════════════════════════════
def build_installation_guide():
    story = []

    story.append(h1("Requirements"))
    for item in [
        "Python 3.10 or 3.11 (3.12+ not tested)",
        "pip 23+",
        "ffmpeg (any recent version) -- required by Whisper for audio decoding",
        "Anthropic API key -- needed for Claude summarisation",
        "At least 8 GB RAM and 3 GB free disk space for Whisper model weights",
    ]:
        story.append(bullet(item))
    story.append(sp(0.5))
    story.append(body("Compatible with macOS, Linux, and Windows (PowerShell)."))

    story.append(sp())
    story.append(h1("1. Clone the Repository"))
    story.append(code("git clone https://github.com/tono2002/nlp-project.git\ncd nlp-project"))

    story.append(h1("2. Create a Virtual Environment"))
    story.append(code("python -m venv .venv"))
    story.append(body("<b>macOS / Linux:</b>"))
    story.append(code("source .venv/bin/activate"))
    story.append(body("<b>Windows (PowerShell):</b>"))
    story.append(code(".venv\\Scripts\\Activate.ps1"))

    story.append(h1("3. Install Python Dependencies"))
    story.append(code("pip install --upgrade pip\npip install -r requirements.txt"))

    story.append(h1("4. Install ffmpeg"))
    story.append(body("<b>macOS:</b>"))
    story.append(code("brew install ffmpeg"))
    story.append(body("<b>Ubuntu / Debian:</b>"))
    story.append(code("sudo apt install ffmpeg"))
    story.append(body(
        "<b>Windows</b> -- download from https://ffmpeg.org/download.html and add to PATH."
    ))

    story.append(h1("5. Configure Environment Variables"))
    story.append(body("Copy the example file and add your Anthropic API key:"))
    story.append(code("cp .env.example .env"))
    story.append(body("Open <i>.env</i> and set:"))
    story.append(code("ANTHROPIC_API_KEY=sk-ant-..."))
    story.append(body(
        "Supabase variables (SUPABASE_URL, SUPABASE_ANON_KEY) are optional. Without them, "
        "project saving is disabled but summarisation still works."
    ))

    story.append(h1("6. Run the App"))
    story.append(code("python -m uvicorn src.app:app --reload --port 8000"))
    story.append(body("Open <b>http://127.0.0.1:8000</b> in your browser."))
    story.append(body(
        "On first run, Whisper will download the base.en model weights (~145 MB). "
        "This happens once and is cached for subsequent runs."
    ))

    story.append(h1("7. Optional -- Change the Whisper Model"))
    story.append(body(
        "The default model is <i>base.en</i>. For faster (less accurate) results use <i>tiny.en</i>; "
        "for better accuracy on noisy or accented audio use <i>small.en</i>:"
    ))
    story.append(code("WHISPER_MODEL=tiny.en python -m uvicorn src.app:app --port 8000"))
    story.append(body("Available sizes: tiny.en  .  base.en  .  small.en  .  medium.en"))

    story.append(sp())
    story.append(h1("Troubleshooting"))
    for item in [
        "<b>ffmpeg not found:</b> ensure ffmpeg is on your system PATH and restart your terminal.",
        "<b>Invalid API key:</b> check that ANTHROPIC_API_KEY is set correctly in .env.",
        "<b>Port already in use:</b> kill the existing process or use a different port.",
        "<b>Slow transcription:</b> switch to tiny.en for demos; use small.en for better accuracy.",
    ]:
        story.append(bullet(item))

    build_pdf(
        "docs/installation_guide.pdf",
        "Installation & Execution Guide",
        "How to run SummarAI locally",
        "NLP Group Project . 2025-2026",
        "SummarAI - Installation Guide",
        story,
    )


# ═══════════════════════════════════════════════════════════════════════════════
# 3. USER MANUAL
# ═══════════════════════════════════════════════════════════════════════════════
def build_user_manual():
    story = []

    story.append(h1("Overview"))
    story.append(body(
        "SummarAI is a meeting summarisation tool. You give it a recorded meeting -- as an audio/video "
        "file or a plain-text transcript -- and it returns three things:"
    ))
    story.append(bullet("<b>Summary</b> -- a concise paragraph capturing what the meeting was about."))
    story.append(bullet("<b>Key takeaways</b> -- the main points and decisions made."))
    story.append(bullet("<b>Action items</b> -- concrete tasks, with the responsible person where identifiable."))
    story.append(sp(0.5))
    story.append(body(
        "The language of the output is your choice, not the language of the meeting. "
        "You can attend an English meeting and receive everything in Spanish, or vice versa."
    ))

    story.append(sp())
    story.append(h1("Getting Started"))
    story.append(h3("Option A -- Hosted version (recommended)"))
    story.append(body(
        "Open the app link in any modern browser (Chrome, Firefox, Safari, Edge). "
        "No installation or account needed."
    ))
    story.append(h3("Option B -- Run locally"))
    story.append(body("Follow the Installation Guide to set up the project, then run:"))
    story.append(code("python -m uvicorn src.app:app --reload --port 8000"))
    story.append(body("Open http://127.0.0.1:8000 in your browser."))

    story.append(sp())
    story.append(h1("Uploading a Meeting"))
    story.append(body(
        "Drag and drop -- or click the upload area -- to load an audio, video, or transcript file. "
        "The supported formats are:"
    ))
    story.append(bullet("Audio: .mp3, .wav, .m4a, .ogg, .flac"))
    story.append(bullet("Video: .mp4, .webm"))
    story.append(bullet("Text transcript: .txt, .md, .vtt, .srt"))
    story.append(sp(0.5))
    story.append(body(
        "Once the file is loaded, click <b>Summarise</b>. A progress bar will appear. "
        "Audio files take 1-8 minutes depending on length. Text files are nearly instant."
    ))

    story.append(sp())
    story.append(h1("Reading the Output"))
    story.append(h3("Summary"))
    story.append(body(
        "One short paragraph -- the meeting's purpose and overall outcome. "
        "Designed to be readable in under 10 seconds."
    ))
    story.append(h3("Key Takeaways"))
    story.append(body("A list of bullet points, each tagged as either:"))
    story.append(bullet("<b>Decision</b> (purple) -- something agreed, approved, or set as policy."))
    story.append(bullet("<b>Note</b> (grey) -- any other important point, fact, or concern."))
    story.append(h3("Action Items"))
    story.append(body(
        "A checklist of concrete tasks. Each item shows the task description, the owner "
        "(if named in the meeting), and the deadline (if stated). "
        "You can check items off as they are completed."
    ))

    story.append(sp())
    story.append(h1("Saving to a Project"))
    story.append(body(
        "Before clicking Summarise, you can optionally enable the project toggle to save the "
        "meeting to a project. Enter a meeting title and select an existing project from the "
        "sidebar, or create a new one. Once processed, the summarization is saved automatically."
    ))
    story.append(body(
        "Saved meetings appear in the project timeline in the left sidebar, ordered by date. "
        "Click a meeting to open the full summary. You can delete individual meetings or entire "
        "projects from the sidebar. Deleting a project removes all meetings saved under it."
    ))

    story.append(sp())
    story.append(h1("Known Limitations"))
    for item in [
        "Owner attribution is reliable only when the speaker is named explicitly in the meeting.",
        "Non-English audio is not supported. The ASR model is English-only.",
        "Very long meetings (2+ hours) may take 5-8 minutes to process.",
        "The app requires an internet connection to reach the Claude API.",
        "iOS Safari does not support push notifications for PWA installs.",
    ]:
        story.append(bullet(item))

    build_pdf(
        "docs/user_manual.pdf",
        "User Manual",
        "How to use SummarAI",
        "NLP Group Project . 2025-2026",
        "SummarAI - User Manual",
        story,
    )


# ═══════════════════════════════════════════════════════════════════════════════
# 4. INDIVIDUAL REFLECTIONS
# ═══════════════════════════════════════════════════════════════════════════════
def reflection_antonio():
    s = []
    s.append(h1("Individual Reflection -- Antonio"))
    s.append(h2("My Contributions"))

    s.append(h3("Whisper Optimization"))
    s.append(body(
        "I profiled the full pipeline to find where time was being spent. The assumption going in "
        "was that the LLM call would be the slow part -- in practice, Claude Haiku returns in a few "
        "seconds, while Whisper on a 20-minute audio file was taking close to 8 minutes with the "
        "default configuration. I implemented four optimizations, all of them zero-cost:"
    ))
    for item in [
        "<b>Switched from the multilingual base model to base.en:</b> The English-only variant is faster and more accurate for English audio.",
        "<b>Set beam_size=1 (greedy decoding):</b> Removes beam search overhead (~2x faster) with negligible accuracy loss for our task.",
        "<b>Set cpu_threads to use all available cores:</b> Transcription runs fully parallel.",
        "<b>Passed language='en' explicitly:</b> Skips the automatic language-detection pass.",
        "<b>Result:</b> Processing time dropped from 7 min 50 s to 2 min 12 s on the same 20-minute recording -- a ~3.5x speedup with near-identical transcript quality.",
    ]:
        s.append(sub(item))

    s.append(h3("Evaluation Script"))
    s.append(body(
        "I built data/eval/evaluate.py. The script loads all transcripts from eval_set.jsonl, calls "
        "the same analyze() function used in production, compares predicted action items against gold "
        "labels using the team's agreed matching rule, and outputs per-meeting results plus "
        "micro-averaged precision, recall, and F1 to data/eval/results.json. The matching logic uses "
        "normalized text similarity with a threshold of 0.6 and greedy one-to-one assignment so each "
        "gold item is matched at most once."
    ))

    s.append(h3("Installation Guide"))
    s.append(body(
        "I wrote docs/installation_guide.md covering Python version requirements, virtual environment "
        "setup, ffmpeg installation on macOS, Linux, and Windows, .env configuration, and the exact "
        "commands to run the server."
    ))

    s.append(h3("Labeled Transcripts"))
    s.append(body(
        "I contributed approximately 8 labeled transcripts to eval_set.jsonl, including sprint "
        "planning sessions and one deliberately ambiguous case where responsibility is implied but "
        "no specific person is named."
    ))

    s.append(sp())
    s.append(h2("What I Learned"))
    s.append(body(
        "Working on this project gave me a much more concrete understanding of how ASR models like "
        "Whisper actually work under the hood -- specifically the trade-off between multilingual and "
        "language-specific models, and what beam search is doing in a seq2seq decoder. Before this I "
        "understood beam search as a concept from the course; seeing it actually cost us 3.5x in "
        "latency with no measurable quality benefit made the accuracy-efficiency trade-off feel real "
        "rather than theoretical. I also developed a much clearer sense of what precision and recall "
        "mean as evaluation metrics for an information extraction task. A single accuracy number "
        "would have hidden the difference between the model missing real action items (recall "
        "failures) and inventing ones that were not there (precision failures) -- two completely "
        "different failure modes with different implications for trust."
    ))
    return s


def reflection_marti():
    s = []
    s.append(PageBreak())
    s.append(h1("Individual Reflection -- Marti"))
    s.append(h2("My Contributions"))

    s.append(h3("Frontend"))
    s.append(body(
        "I built the entire frontend as a single HTML file (src/static/index.html) with no framework "
        "dependencies -- plain JavaScript and CSS only. The interface includes a drag-and-drop upload "
        "area, a results panel with the summary, color-coded takeaway bubbles (purple for decisions, "
        "grey for notes), an action item checklist, and a collapsible sidebar showing the timeline of "
        "saved summarizations per project. The layout is fully responsive and works on iPhone screens."
    ))
    for item in [
        "<b>Loading state:</b> Transcription can take several minutes, so the interface shows a progress bar. Results render once the API call completes.",
        "<b>Error handling:</b> All failure states are handled explicitly -- unsupported file type, missing API key, model error -- so the user gets a clear message rather than a silent failure.",
    ]:
        s.append(sub(item))

    s.append(h3("Failure Mode Analysis"))
    s.append(body(
        "After the evaluation was run, I documented the most informative failure cases in "
        "data/eval/failure_analysis.md. Each case includes the transcript excerpt, the model's "
        "output, the gold label, and a hypothesis for why it failed. Main patterns:"
    ))
    for item in [
        "<b>Whisper mishearing proper nouns:</b> Causes the owner field to be wrong even when the task is correct.",
        "<b>Phantom action items:</b> The model generates commitments from hypothetical discussions.",
        "<b>Zero output on non-meeting audio:</b> Correct behavior for podcasts, but may confuse users.",
        "<b>Implied responsibility:</b> When no person is named, the model leaves owner null rather than guessing.",
    ]:
        s.append(sub(item))

    s.append(h3("Labeled Transcripts"))
    s.append(body(
        "I contributed approximately 8 labeled transcripts to eval_set.jsonl, deliberately designing "
        "difficult cases: meetings where no one is explicitly assigned a task, shared responsibilities, "
        "and informally stated deadlines."
    ))

    s.append(sp())
    s.append(h2("What I Learned"))
    s.append(body(
        "The most important thing I took away is how NLP errors propagate through a pipeline. "
        "Whisper's transcription errors do not stay in the transcription layer -- they flow directly "
        "into the LLM output. If Whisper mishears a name, the action item will have the wrong owner "
        "even if the model does everything else correctly. This cascading failure is hard to see from "
        "an aggregate F1 score alone, and it made me understand why failure mode analysis is treated "
        "as a required component of the assignment. I also learned what information extraction means "
        "as an NLP task -- it sits between pure classification and open-ended generation, and the "
        "challenge is that the output structure is constrained but the surface form is open, which "
        "is exactly why simple rule-based approaches fail on real, messy transcripts."
    ))
    return s


def reflection_bojana():
    s = []
    s.append(PageBreak())
    s.append(h1("Individual Reflection -- Bojana"))
    s.append(h2("My Contributions"))

    s.append(h3("Backend and NLP Pipeline"))
    s.append(body(
        "I built the entire server-side application (src/app.py). This includes the FastAPI server, "
        "the file upload endpoint, and the full two-stage NLP pipeline: routing audio files through "
        "faster-whisper for transcription, then passing the transcript to Claude Haiku 4.5 to extract "
        "the summary, typed takeaways, and action items. I also built all project management "
        "endpoints -- creating, listing, and deleting projects and saved summarizations -- using a "
        "thin HTTP wrapper to avoid adding a full Supabase client library as a dependency."
    ))
    s.append(sub(
        "<b>Input type routing:</b> Audio and video files need to be written to a temporary file on disk "
        "before Whisper can process them. Text files are read directly into memory. Temporary files "
        "are cleaned up reliably using try/finally even when transcription fails."
    ))

    s.append(h3("System Prompt and Output Schema"))
    s.append(body(
        "I designed the system prompt and the JSON output schema that enforces the structure Claude "
        "must return. The schema defines three required fields -- summary, key_takeaways, and "
        "action_items -- with strict types and no additional properties allowed. Early versions "
        "produced inconsistent output: action items appearing inside the summary, takeaways missing "
        "their type tag, or the model inventing owners not in the transcript. I iterated on the "
        "prompt until the model reliably separated the three output types and only included owners "
        "and deadlines when explicitly stated. The final prompt and schema are saved in prompts/."
    ))

    s.append(h3("Labeled Transcripts"))
    s.append(body(
        "I created approximately 8 transcripts for eval_set.jsonl, including standup meetings, "
        "sprint planning sessions, and one edge case where a speaker discusses a hypothetical future "
        "action without committing -- designed to test whether the model invents phantom action items."
    ))

    s.append(sp())
    s.append(h2("What I Learned"))
    s.append(body(
        "This project gave me a real understanding of prompt engineering as an NLP technique rather "
        "than just a trick. When we started, the model would sometimes invent owners not mentioned "
        "in the transcript, or merge two separate action items into one. Fixing this required "
        "understanding why the model was doing it -- it was following conversational implicature, "
        "inferring responsibility from context the way a human would -- and then writing a prompt "
        "constraint specific enough to override that default behavior. I also came to appreciate what "
        "makes LLM-based information extraction different from traditional approaches: the model "
        "handles paraphrase, messy grammar, and implicit references naturally. The cost is that you "
        "cannot fully predict or control the output, which is exactly why structured schemas and "
        "evaluation against gold labels are necessary."
    ))
    return s


def reflection_jo():
    s = []
    s.append(PageBreak())
    s.append(h1("Individual Reflection -- Jo"))
    s.append(h2("My Contributions"))

    s.append(h3("Supabase Database Layer"))
    s.append(body(
        "I designed and set up the entire persistence layer for the app. I wrote "
        "supabase_schema.sql, which defines two tables: projects (for grouping meetings) and "
        "summarizations (for storing the full structured output). A key design decision was storing "
        "key_takeaways and action_items as JSONB columns rather than flat text, preserving the "
        "structured data as queryable fields rather than serialised strings."
    ))
    for item in [
        "<b>Cascade delete:</b> The schema includes a foreign key from summarizations to projects with cascade delete, so removing a project automatically removes all its meetings.",
        "<b>Row-level security:</b> RLS policies allow public read/write access without requiring user accounts -- appropriate for a POC and documented as a limitation for production.",
    ]:
        s.append(sub(item))
    s.append(body(
        "I also verified that the backend endpoints matched what Supabase expected -- checking that "
        "REST calls for creating, listing, and deleting projects and summarizations all worked "
        "correctly against the live database."
    ))

    s.append(h3("Field Review"))
    s.append(body(
        "I researched the meeting-AI and transcription industry and wrote the field review section "
        "of the technical report. I covered the major existing tools -- Otter.ai, Fireflies.ai, "
        "Zoom AI Companion, Fathom, and tl;dv -- and analysed what they offer and what they "
        "consistently lack. Most produce a single undifferentiated list of bullet points; none "
        "separate decisions from notes. I cited sources from ACL Anthology, arXiv, and industry "
        "reports to ground the review in published research."
    ))

    s.append(h3("Labeled Transcripts"))
    s.append(body(
        "I contributed approximately 8 labeled transcripts to eval_set.jsonl, including excerpts "
        "from public city council meeting minutes -- real, verbatim, and messy, with decisions both "
        "with and without clear owners."
    ))

    s.append(sp())
    s.append(h2("What I Learned"))
    s.append(body(
        "Doing the field review made me understand the difference between what NLP research has "
        "achieved and what is actually deployed in real products. There is a large body of work on "
        "meeting summarization, action item extraction, and dialogue act classification going back "
        "years, yet mainstream commercial tools still produce simple undifferentiated bullet lists. "
        "The research-to-product gap is real and wider than I expected. I also developed a clearer "
        "understanding of the different NLP subtasks our system combines: automatic speech "
        "recognition (Whisper), abstractive summarization (the two-sentence summary), and named "
        "entity and relation extraction (pulling out task, owner, and deadline as structured fields). "
        "Each has its own failure modes and literature, and the overall system quality is limited by "
        "whichever stage performs worst on a given input."
    ))
    return s


def reflection_smaragda():
    s = []
    s.append(PageBreak())
    s.append(h1("Individual Reflection -- Smaragda"))
    s.append(h2("My Contributions"))

    s.append(h3("Evaluation Set Design and Annotation Methodology"))
    s.append(body(
        "I designed the evaluation set the whole team used to measure the system. This included "
        "deciding on the format of eval_set.jsonl, writing the annotation guidelines the team "
        "followed when labeling, and coordinating labeling across all five members so everyone "
        "applied the same rules consistently."
    ))
    for item in [
        "<b>What counts as an action item:</b> A concrete commitment by a named or identifiable person -- not a vague intention or a plan the team discussed but did not commit to.",
        "<b>Missing deadlines:</b> Leave the deadline field blank rather than infer one.",
        "<b>Overlapping items:</b> When one transcript has multiple overlapping action items for the same person, list each separately.",
    ]:
        s.append(sub(item))
    s.append(body(
        "I also ensured the test set covered a realistic range of meeting types: standups, planning "
        "sessions, sales calls, retrospectives, and tricky cases (no action items at all, ambiguous "
        "ownership, hypothetical discussions). I contributed approximately 8 transcripts myself, "
        "focusing on multilingual scenarios."
    ))

    s.append(h3("Executive Summary"))
    s.append(body(
        "I wrote deliverables/executive_summary.md -- the one-page non-technical description of the "
        "project. I led with the cost of unproductive meetings and the specific barrier multilingual "
        "teams face, then described what SummarAI does differently, then summarised the evaluation "
        "findings including the main limitation around owner attribution."
    ))

    s.append(h3("User Manual"))
    s.append(body(
        "I wrote docs/user_manual.md from scratch, walking through every feature: uploading a file, "
        "choosing the output language, reading the summary and takeaway bubbles, checking off action "
        "items, saving to a project, and browsing the project timeline. I also documented supported "
        "formats, known limitations, and common questions."
    ))

    s.append(h3("Slides"))
    s.append(body(
        "I put together the presentation slides (deliverables/slides.md), structuring the 20-minute "
        "presentation as: problem and motivation, field review, system overview, evaluation method "
        "and results, failure cases, future directions, and Q&A."
    ))

    s.append(sp())
    s.append(h2("What I Learned"))
    s.append(body(
        "Building the annotation guidelines taught me that the definition of a label is itself a "
        "research decision with real consequences for the evaluation. We started with a vague shared "
        "understanding of what an action item was, and when I tried to write it down precisely, edge "
        "cases appeared immediately: is 'we should probably follow up on this' an action item? What "
        "if no one is named as responsible? What if someone agrees to do something only "
        "conditionally? These decisions determine what the model is being evaluated against -- so "
        "they determine what the evaluation actually measures. I now understand why "
        "inter-annotator agreement is reported in NLP papers: it is not a formality, it is evidence "
        "that the label definition is precise enough to be applied consistently. I also understood "
        "more deeply what the summarization task is about: not just shortening text, but identifying "
        "what is important and representing it in a structured, reusable form."
    ))
    return s


def build_reflections():
    story = []
    story += reflection_antonio()
    story += reflection_marti()
    story += reflection_bojana()
    story += reflection_jo()
    story += reflection_smaragda()

    build_pdf(
        "docs/individual_reflections.pdf",
        "Individual Reflections",
        "Antonio  .  Bojana  .  Jo  .  Marti  .  Smaragda",
        "NLP Group Project . 2025-2026",
        "SummarAI - Individual Reflections",
        story,
    )


# ═══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("Building PDFs...")
    build_executive_summary()
    build_installation_guide()
    build_user_manual()
    build_reflections()
    print("Done. Files written to docs/")
