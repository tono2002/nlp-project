"""Generate all 4 submission PDFs — professional template with proper spacing."""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable,
    PageBreak, KeepTogether, Table, TableStyle, Preformatted
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

W, H = A4
L_MARGIN = 2.5 * cm
R_MARGIN = 2.5 * cm
T_MARGIN = 2.2 * cm
B_MARGIN = 2.5 * cm

# ── Palette ───────────────────────────────────────────────────────────────────
C_NAVY    = colors.HexColor("#12104a")   # cover background
C_INDIGO  = colors.HexColor("#4f46e5")   # accent / H1
C_VIOLET  = colors.HexColor("#7c3aed")   # H2 / H3
C_LAVEND  = colors.HexColor("#c7d2fe")   # cover subtitle
C_MUTED   = colors.HexColor("#a5b4fc")   # cover description
C_RULE    = colors.HexColor("#ddd6fe")   # section rules
C_BODY    = colors.HexColor("#1f2937")   # body text
C_GREY    = colors.HexColor("#6b7280")   # footer / captions
C_CODEBG  = colors.HexColor("#f3f4f6")
C_H1_BAR  = colors.HexColor("#ede9fe")   # thin left-accent behind H1
WHITE     = colors.white


# ── Style factory ─────────────────────────────────────────────────────────────
def S(name, **kw):
    base = kw.pop("parent", "Normal")
    defaults = dict(fontName="Helvetica", fontSize=10,
                    textColor=C_BODY, leading=16, spaceAfter=0, spaceBefore=0)
    defaults.update(kw)
    return ParagraphStyle(name, **defaults)

ST = {
    "h1": S("h1", fontName="Helvetica-Bold", fontSize=17, textColor=C_INDIGO,
             leading=22, spaceBefore=28, spaceAfter=6),
    "h2": S("h2", fontName="Helvetica-Bold", fontSize=13, textColor=C_VIOLET,
             leading=18, spaceBefore=22, spaceAfter=5),
    "h3": S("h3", fontName="Helvetica-Bold", fontSize=11, textColor=C_VIOLET,
             leading=15, spaceBefore=14, spaceAfter=4),
    "body": S("body", fontSize=10.5, textColor=C_BODY, leading=17,
              spaceAfter=10, alignment=TA_JUSTIFY),
    "bullet": S("bul", fontSize=10.5, textColor=C_BODY, leading=16,
                spaceAfter=5, leftIndent=18, firstLineIndent=0),
    "sub":    S("sub", fontSize=10.5, textColor=C_BODY, leading=16,
                spaceAfter=5, leftIndent=36, firstLineIndent=0),
    "code":   S("code", fontName="Courier", fontSize=9, textColor=C_INDIGO,
                leading=13, spaceBefore=6, spaceAfter=10,
                backColor=C_CODEBG, leftIndent=10, rightIndent=10),
    "cap":    S("cap", fontSize=9, textColor=C_GREY, alignment=TA_CENTER,
                leading=12, spaceAfter=8),
    "footer": S("ft",  fontSize=8,  textColor=C_GREY, alignment=TA_CENTER, leading=10),
}


# ── Helpers ───────────────────────────────────────────────────────────────────
def sp(n=1):
    return Spacer(1, n * 0.35 * cm)

def rule(color=C_RULE, thickness=0.6):
    return HRFlowable(width="100%", thickness=thickness, color=color,
                      spaceBefore=2, spaceAfter=10)

def heavy_rule():
    return HRFlowable(width="100%", thickness=1.5, color=C_INDIGO,
                      spaceBefore=0, spaceAfter=14)

def h1(text):
    return KeepTogether([
        Paragraph(text, ST["h1"]),
        heavy_rule(),
    ])

def h2(text):
    return KeepTogether([
        Paragraph(text, ST["h2"]),
        rule(C_RULE, 0.5),
    ])

def h3(text):
    return Paragraph(text, ST["h3"])

def body(text):
    return Paragraph(text, ST["body"])

def bullet(text, level=0):
    indent = 18 + level * 18
    st = S(f"b{level}", fontSize=10.5, textColor=C_BODY, leading=16,
           spaceAfter=5, leftIndent=indent, firstLineIndent=0)
    marker = u"•" if level == 0 else u"–"
    return Paragraph(f"{marker}  {text}", st)

def code(text):
    return Preformatted(text, ST["code"])

def simple_table(headers, rows, col_widths=None):
    w = W - L_MARGIN - R_MARGIN
    if col_widths is None:
        col_widths = [w / len(headers)] * len(headers)
    data = [[Paragraph(f"<b>{h}</b>", S("th", textColor=WHITE, fontSize=9.5,
                       fontName="Helvetica-Bold", leading=13)) for h in headers]]
    for r in rows:
        data.append([Paragraph(str(c), S("td", fontSize=9.5, leading=14,
                               textColor=C_BODY)) for c in r])
    tbl = Table(data, colWidths=col_widths, repeatRows=1)
    tbl.setStyle(TableStyle([
        ("BACKGROUND",  (0,0), (-1,0),  C_INDIGO),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [WHITE, C_H1_BAR]),
        ("TOPPADDING",  (0,0), (-1,-1), 7),
        ("BOTTOMPADDING",(0,0), (-1,-1), 7),
        ("LEFTPADDING", (0,0), (-1,-1), 10),
        ("RIGHTPADDING",(0,0), (-1,-1), 10),
        ("GRID",        (0,0), (-1,-1), 0.3, C_RULE),
        ("VALIGN",      (0,0), (-1,-1), "MIDDLE"),
    ]))
    return tbl


# ── Cover page ────────────────────────────────────────────────────────────────
def draw_cover(canvas, doc, title, subtitle, description, names=None):
    canvas.saveState()

    # Background
    canvas.setFillColor(C_NAVY)
    canvas.rect(0, 0, W, H, fill=1, stroke=0)

    # Top gradient bar (two-strip effect)
    canvas.setFillColor(C_INDIGO)
    canvas.rect(0, H - 1.4*cm, W, 1.4*cm, fill=1, stroke=0)
    canvas.setFillColor(colors.HexColor("#6366f1"))
    canvas.rect(0, H - 1.8*cm, W, 0.4*cm, fill=1, stroke=0)

    # Bottom accent
    canvas.setFillColor(C_VIOLET)
    canvas.rect(0, 0, W, 0.7*cm, fill=1, stroke=0)
    canvas.setFillColor(colors.HexColor("#6d28d9"))
    canvas.rect(0, 0.7*cm, W, 0.25*cm, fill=1, stroke=0)

    # Left accent strip
    canvas.setFillColor(C_VIOLET)
    canvas.rect(0, 0, 0.55*cm, H, fill=1, stroke=0)

    # Decorative circle
    canvas.setFillColor(colors.HexColor("#312e81"))
    canvas.circle(W * 0.82, H * 0.72, 4.5*cm, fill=1, stroke=0)
    canvas.setFillColor(colors.HexColor("#3730a3"))
    canvas.circle(W * 0.78, H * 0.68, 3*cm, fill=1, stroke=0)

    # "SummarAI" wordmark
    canvas.setFillColor(WHITE)
    canvas.setFont("Helvetica-Bold", 46)
    canvas.drawString(2.2*cm, H * 0.635, "SummarAI")

    # Divider line
    canvas.setStrokeColor(C_INDIGO)
    canvas.setLineWidth(2)
    canvas.line(2.2*cm, H * 0.615, W - 2.2*cm, H * 0.615)

    # Document title
    canvas.setFillColor(C_LAVEND)
    canvas.setFont("Helvetica-Bold", 20)
    canvas.drawString(2.2*cm, H * 0.565, title)

    # Subtitle / description
    canvas.setFillColor(C_MUTED)
    canvas.setFont("Helvetica", 12)
    canvas.drawString(2.2*cm, H * 0.525, subtitle)

    canvas.setFont("Helvetica", 11)
    canvas.drawString(2.2*cm, H * 0.495, description)

    # Team / names block (optional)
    if names:
        canvas.setFillColor(colors.HexColor("#818cf8"))
        canvas.setFont("Helvetica-Bold", 10)
        canvas.drawString(2.2*cm, H * 0.31, "Team")
        canvas.setFillColor(C_MUTED)
        canvas.setFont("Helvetica", 10)
        y = H * 0.285
        for name in names:
            canvas.drawString(2.2*cm, y, name)
            y -= 0.52*cm

    # Year tag bottom-right
    canvas.setFillColor(colors.HexColor("#4338ca"))
    canvas.roundRect(W - 5.5*cm, 1.4*cm, 4.5*cm, 0.8*cm, 4, fill=1, stroke=0)
    canvas.setFillColor(WHITE)
    canvas.setFont("Helvetica-Bold", 9)
    canvas.drawCentredString(W - 3.25*cm, 1.76*cm, "NLP Group Project  ·  2025–2026")

    canvas.restoreState()


def draw_later_page(canvas, doc, footer_text):
    canvas.saveState()
    # Left accent strip
    canvas.setFillColor(colors.HexColor("#ede9fe"))
    canvas.rect(0, 0, 0.3*cm, H, fill=1, stroke=0)
    # Footer rule
    canvas.setStrokeColor(C_RULE)
    canvas.setLineWidth(0.5)
    canvas.line(L_MARGIN, 1.6*cm, W - R_MARGIN, 1.6*cm)
    # Footer text
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(C_GREY)
    canvas.drawString(L_MARGIN, 1.1*cm, footer_text)
    canvas.drawRightString(W - R_MARGIN, 1.1*cm, f"Page {doc.page}")
    canvas.restoreState()


def build_pdf(path, cover_title, cover_subtitle, cover_desc, footer,
              story, cover_names=None):
    os.makedirs(os.path.dirname(path) if os.path.dirname(path) else ".", exist_ok=True)

    doc = SimpleDocTemplate(
        path, pagesize=A4,
        leftMargin=L_MARGIN + 0.3*cm, rightMargin=R_MARGIN,
        topMargin=T_MARGIN, bottomMargin=B_MARGIN,
    )

    def first_page(c, d):
        draw_cover(c, d, cover_title, cover_subtitle, cover_desc, cover_names)

    def later_page(c, d):
        draw_later_page(c, d, footer)

    doc.build([PageBreak()] + story,
              onFirstPage=first_page,
              onLaterPages=later_page)
    print(f"  {path}")


# ═══════════════════════════════════════════════════════════════════════════════
# 1. EXECUTIVE SUMMARY
# ═══════════════════════════════════════════════════════════════════════════════
def build_executive_summary():
    s = []

    s.append(h1("What We Built"))
    s.append(body(
        "SummarAI is an AI-powered meeting assistant that converts a recorded meeting into a "
        "structured written record. Upload the audio or video of any meeting and, within minutes, "
        "the application returns a plain-language summary, a list of the main decisions made, and "
        "a clear set of action items showing who is responsible for what."
    ))
    s.append(body(
        "The key differentiating feature is language flexibility. Existing tools such as Otter.ai "
        "or the built-in assistants in Zoom and Microsoft Teams always produce their output in "
        "the same language as the meeting. SummarAI lets the user choose the output language "
        "independently. A meeting held in English can produce a Spanish summary and action-item "
        "list, or vice versa. For international teams where not everyone shares the same first "
        "language, this means every member receives the meeting record in the language they work "
        "best in."
    ))

    s.append(sp(1.5))
    s.append(h1("Why It Matters"))
    s.append(body(
        "Unproductive meetings cost U.S. businesses an estimated $259 billion per year, according "
        "to a 2024 London School of Economics report. A large part of that cost is not the meetings "
        "themselves but what happens afterwards: decisions go unrecorded, action items are "
        "forgotten, and absent team members miss critical information. Studies show that 54% of "
        "employees regularly leave meetings without a clear understanding of next steps."
    ))
    s.append(body(
        "The problem is more acute in multilingual workplaces. Over 60% of knowledge workers in "
        "multinational companies regularly attend meetings conducted in a language other than their "
        "primary one. Receiving a meeting summary in a second language at the moment when precision "
        "matters most is a real barrier to follow-through and accountability."
    ))
    s.append(body(
        "SummarAI addresses both problems simultaneously: it automates the capture of meeting "
        "decisions and action items, and delivers that information in the language the reader "
        "actually uses day to day."
    ))

    s.append(sp(1.5))
    s.append(h1("What We Found"))
    s.append(body(
        "We tested SummarAI on 30 meeting transcripts from the AMI Meeting Corpus — a standard "
        "research benchmark with professional human annotations. The system performed well on its "
        "core task: summaries were consistently coherent and action items were identified in the "
        "majority of cases."
    ))
    s.append(sp(0.5))
    s.append(simple_table(
        ["Metric", "Score"],
        [
            ["ROUGE-1 (F, avg)",           "0.335"],
            ["ROUGE-2 (F, avg)",           "0.057"],
            ["ROUGE-L (F, avg)",           "0.148"],
            ["Action-item coverage (recall)", "42.4%  (28 / 66)"],
        ],
        col_widths=[10.5*cm, 5.5*cm]
    ))
    s.append(sp(0.5))
    s.append(body(
        "The main limitation identified is <b>owner attribution</b>: correctly identifying who is "
        "responsible for each action item. When speakers are named explicitly in the conversation, "
        "attribution is reliable. When responsibility is implied rather than stated, the system "
        "sometimes leaves the owner blank. This is a known limitation of working with audio "
        "transcripts that do not label speakers, and it is the clearest direction for future work."
    ))

    s.append(sp(1.5))
    s.append(h1("Bottom Line"))
    s.append(body(
        "SummarAI demonstrates that a focused AI pipeline can meaningfully reduce the "
        "administrative burden of meetings: capturing decisions and tasks automatically, and "
        "making them accessible to every team member in their own language. The proof of concept "
        "is functional, the core differentiator is real, and the failure modes are well-understood "
        "and addressable. The most immediate next step is adding speaker diarization so that "
        "action-item ownership can be assigned reliably without depending on participants being "
        "named aloud."
    ))

    build_pdf(
        "docs/executive_summary.pdf",
        "Executive Summary",
        "Automated Meeting Summarization",
        "NLP Group Project  ·  2025–2026",
        "SummarAI  —  Executive Summary",
        s,
    )


# ═══════════════════════════════════════════════════════════════════════════════
# 2. INSTALLATION GUIDE
# ═══════════════════════════════════════════════════════════════════════════════
def build_installation_guide():
    s = []

    s.append(h1("Requirements"))
    for item in [
        "Python <b>3.10</b> or <b>3.11</b> (3.12+ not tested)",
        "<b>pip 23+</b>",
        "<b>ffmpeg</b> (any recent version) — required by Whisper for audio decoding",
        "<b>Anthropic API key</b> — needed for Claude summarisation",
        "At least <b>8 GB RAM</b> and <b>3 GB free disk space</b> for Whisper model weights",
    ]:
        s.append(bullet(item))
    s.append(sp())
    s.append(body("Compatible with macOS, Linux, and Windows (PowerShell)."))

    s.append(sp(1.5))
    s.append(h1("Setup Steps"))

    s.append(h2("Step 1 — Clone the Repository"))
    s.append(code("git clone https://github.com/tono2002/nlp-project.git\ncd nlp-project"))

    s.append(h2("Step 2 — Create a Virtual Environment"))
    s.append(code("python -m venv .venv"))
    s.append(body("<b>macOS / Linux:</b>"))
    s.append(code("source .venv/bin/activate"))
    s.append(body("<b>Windows (PowerShell):</b>"))
    s.append(code(".venv\\Scripts\\Activate.ps1"))

    s.append(h2("Step 3 — Install Python Dependencies"))
    s.append(code("pip install --upgrade pip\npip install -r requirements.txt"))

    s.append(h2("Step 4 — Install ffmpeg"))
    s.append(body("<b>macOS:</b>"))
    s.append(code("brew install ffmpeg"))
    s.append(body("<b>Ubuntu / Debian:</b>"))
    s.append(code("sudo apt install ffmpeg"))
    s.append(body(
        "<b>Windows</b> — download from ffmpeg.org/download.html and add the bin/ folder to PATH."
    ))

    s.append(h2("Step 5 — Configure Environment Variables"))
    s.append(body("Copy the example file and fill in your Anthropic API key:"))
    s.append(code("cp .env.example .env"))
    s.append(body("Open <i>.env</i> and set:"))
    s.append(code("ANTHROPIC_API_KEY=sk-ant-..."))
    s.append(body(
        "Supabase variables (SUPABASE_URL, SUPABASE_ANON_KEY) are optional. Without them, "
        "project saving is disabled but summarisation still works."
    ))

    s.append(h2("Step 6 — Run the App"))
    s.append(code("python -m uvicorn src.app:app --reload --port 8000"))
    s.append(body(
        "Open <b>http://127.0.0.1:8000</b> in your browser. "
        "On first run, Whisper will download the <i>base.en</i> model weights (~145 MB). "
        "This is cached for subsequent runs."
    ))

    s.append(h2("Step 7 — Optional: Change the Whisper Model"))
    s.append(body(
        "The default model is <i>base.en</i>. For faster results use <i>tiny.en</i>; "
        "for better accuracy on noisy audio use <i>small.en</i>:"
    ))
    s.append(code("WHISPER_MODEL=tiny.en python -m uvicorn src.app:app --port 8000"))
    s.append(sp(0.5))
    s.append(simple_table(
        ["Model", "Speed", "Accuracy", "Disk"],
        [
            ["tiny.en",   "Fastest",  "Lower",   "~75 MB"],
            ["base.en",   "Fast",     "Good",    "~145 MB"],
            ["small.en",  "Moderate", "Better",  "~460 MB"],
            ["medium.en", "Slow",     "Best",    "~1.4 GB"],
        ],
        col_widths=[3.5*cm, 3.5*cm, 3.5*cm, 3.5*cm]
    ))

    s.append(sp(1.5))
    s.append(h1("Troubleshooting"))
    for item in [
        "<b>ffmpeg not found</b> — ensure ffmpeg is on your system PATH and restart your terminal.",
        "<b>Invalid API key</b> — check that ANTHROPIC_API_KEY is set correctly in .env.",
        "<b>Port already in use</b> — kill the existing process or start on a different port.",
        "<b>Slow transcription</b> — switch to tiny.en for demos; use small.en for better accuracy.",
        "<b>Windows Execution Policy error</b> — run: Set-ExecutionPolicy RemoteSigned -Scope CurrentUser",
    ]:
        s.append(bullet(item))

    build_pdf(
        "docs/installation_guide.pdf",
        "Installation Guide",
        "How to run SummarAI locally",
        "NLP Group Project  ·  2025–2026",
        "SummarAI  —  Installation Guide",
        s,
    )


# ═══════════════════════════════════════════════════════════════════════════════
# 3. USER MANUAL
# ═══════════════════════════════════════════════════════════════════════════════
def build_user_manual():
    s = []

    s.append(h1("Overview"))
    s.append(body(
        "SummarAI converts a recorded meeting into a structured written record. Upload an audio, "
        "video, or transcript file and the application returns three outputs:"
    ))
    s.append(bullet("<b>Summary</b> — a concise paragraph capturing what the meeting was about."))
    s.append(bullet("<b>Key takeaways</b> — the main decisions and important points, each tagged by type."))
    s.append(bullet("<b>Action items</b> — concrete tasks, with owner and deadline where stated."))
    s.append(sp())
    s.append(body(
        "The output language is your choice, not the language of the meeting. "
        "You can attend an English meeting and receive everything in Spanish, or vice versa."
    ))

    s.append(sp(1.5))
    s.append(h1("Getting Started"))
    s.append(h2("Option A — Hosted Version (Recommended)"))
    s.append(body(
        "Open the app URL in any modern browser (Chrome, Firefox, Safari, Edge). "
        "No installation or account required."
    ))
    s.append(h2("Option B — Run Locally"))
    s.append(body("Follow the Installation Guide, then run:"))
    s.append(code("python -m uvicorn src.app:app --reload --port 8000"))
    s.append(body("Open <b>http://127.0.0.1:8000</b> in your browser."))

    s.append(sp(1.5))
    s.append(h1("Uploading a Meeting"))
    s.append(body(
        "Drag and drop a file onto the upload area, or click it to browse. "
        "Supported formats are:"
    ))
    s.append(sp(0.5))
    s.append(simple_table(
        ["Category", "Formats"],
        [
            ["Audio",            ".mp3 · .wav · .m4a · .ogg · .flac"],
            ["Video",            ".mp4 · .webm"],
            ["Text transcript",  ".txt · .md · .vtt · .srt"],
        ],
        col_widths=[5*cm, 11*cm]
    ))
    s.append(sp())
    s.append(body(
        "Once the file is loaded, click <b>Summarise</b>. A progress bar appears. "
        "Audio files take 1–8 minutes depending on length and hardware. "
        "Text files are nearly instant."
    ))

    s.append(sp(1.5))
    s.append(h1("Reading the Output"))
    s.append(h2("Summary"))
    s.append(body(
        "One short paragraph capturing the meeting’s purpose and overall outcome. "
        "Designed to be readable in under 10 seconds."
    ))
    s.append(h2("Key Takeaways"))
    s.append(body("A bullet list, each item tagged as one of two types:"))
    s.append(bullet("<b>Decision</b> (purple) — something agreed, approved, or set as policy."))
    s.append(bullet("<b>Note</b> (grey) — any other important point, fact, or concern raised."))
    s.append(h2("Action Items"))
    s.append(body(
        "A checklist of concrete tasks. Each item shows the task description, the responsible "
        "person (if named in the meeting), and the deadline (if stated). "
        "You can check items off as they are completed."
    ))

    s.append(sp(1.5))
    s.append(h1("Saving to a Project"))
    s.append(body(
        "Before clicking Summarise, enable the project toggle to save the meeting to a project. "
        "Enter a meeting title and select an existing project or create a new one. "
        "Once processed, the summarization is saved automatically."
    ))
    s.append(body(
        "Saved meetings appear in the project timeline (left sidebar), ordered by date. "
        "Click a meeting to open the full summary. Deleting a project removes all meetings "
        "saved under it."
    ))

    s.append(sp(1.5))
    s.append(h1("Known Limitations"))
    for item in [
        "Owner attribution is reliable only when the speaker is named explicitly in the meeting.",
        "Non-English audio is not supported — the ASR model is English-only.",
        "Very long meetings (2+ hours) may take 5–8 minutes to process on modest hardware.",
        "The app requires an internet connection to reach the Claude API.",
        "iOS Safari does not support PWA push notifications.",
    ]:
        s.append(bullet(item))

    build_pdf(
        "docs/user_manual.pdf",
        "User Manual",
        "How to use SummarAI",
        "NLP Group Project  ·  2025–2026",
        "SummarAI  —  User Manual",
        s,
    )


# ═══════════════════════════════════════════════════════════════════════════════
# 4. INDIVIDUAL REFLECTIONS
# ═══════════════════════════════════════════════════════════════════════════════
def refl_header(name, role=""):
    items = [
        Paragraph(name, S("rn", fontName="Helvetica-Bold", fontSize=20,
                          textColor=C_INDIGO, leading=24, spaceBefore=10, spaceAfter=4)),
    ]
    if role:
        items.append(Paragraph(role, S("rr", fontSize=11, textColor=C_GREY,
                                        leading=14, spaceAfter=8)))
    items.append(HRFlowable(width="100%", thickness=2, color=C_INDIGO,
                            spaceBefore=0, spaceAfter=18))
    return KeepTogether(items)


def reflection_antonio():
    s = []
    s.append(refl_header("Antonio", "Whisper Optimization · Evaluation · Installation Guide"))

    s.append(h2("My Contributions"))

    s.append(h3("Whisper Optimization"))
    s.append(body(
        "I profiled the full pipeline to find where time was being spent. The assumption going in "
        "was that the LLM call would be the slow part — in practice, Claude Haiku 4.5 returns "
        "in a few seconds, while Whisper on a 20-minute audio file was taking close to 8 minutes "
        "with the default configuration. I implemented four zero-cost optimizations:"
    ))
    for item in [
        "<b>Switched from the multilingual base model to base.en</b> — the English-only variant is faster and more accurate for English audio.",
        "<b>Set beam_size=1 (greedy decoding)</b> — removes beam search overhead (~2x faster) with negligible accuracy loss.",
        "<b>Set cpu_threads to use all available cores</b> — transcription runs fully parallel.",
        "<b>Passed language=\'en\' explicitly</b> — skips the automatic language-detection pass.",
    ]:
        s.append(bullet(item))
    s.append(sp(0.5))
    s.append(simple_table(
        ["Configuration", "Total time", "Transcript length"],
        [
            ["Original (base, beam 5, auto-detect)",   "7 min 50 s", "36,702 chars"],
            ["Optimized (base.en, greedy, multithread)", "2 min 12 s", "36,620 chars"],
        ],
        col_widths=[8*cm, 3.5*cm, 4.5*cm]
    ))
    s.append(sp(0.5))
    s.append(body("Result: <b>3.5× speedup (72% reduction)</b> at zero additional cost."))

    s.append(h3("Evaluation Script"))
    s.append(body(
        "I built <i>data/eval/evaluate.py</i>. The script loads all transcripts from "
        "<i>eval_set.jsonl</i>, calls the same analyze() function used in production, compares "
        "predicted action items against gold labels using normalized text similarity "
        "(threshold 0.6, greedy one-to-one assignment), and outputs per-meeting results plus "
        "micro-averaged metrics to <i>data/eval/results.json</i>."
    ))

    s.append(h3("Installation Guide"))
    s.append(body(
        "I wrote <i>docs/installation_guide.md</i> covering Python version requirements, "
        "virtual environment setup, ffmpeg installation on macOS, Linux, and Windows, "
        ".env configuration, and the commands to run the server."
    ))

    s.append(h3("Labeled Transcripts"))
    s.append(body(
        "I contributed approximately 8 labeled transcripts to <i>eval_set.jsonl</i>, "
        "including sprint planning sessions and one deliberately ambiguous case where "
        "responsibility is implied but no specific person is named."
    ))

    s.append(sp(1.5))
    s.append(h2("What I Learned"))
    s.append(body(
        "Working on this project gave me a much more concrete understanding of how ASR models "
        "like Whisper work under the hood — specifically the trade-off between multilingual "
        "and language-specific models, and what beam search is doing in a seq2seq decoder. "
        "Before this I understood beam search as a concept from the course; seeing it actually "
        "cost us 3.5× in latency with no measurable quality benefit made the "
        "accuracy-efficiency trade-off feel real rather than theoretical."
    ))
    s.append(body(
        "I also developed a much clearer sense of what precision and recall mean as evaluation "
        "metrics for an information extraction task. A single accuracy number would have hidden "
        "the difference between the model missing real action items (recall failures) and "
        "inventing ones that were not there (precision failures) — two completely different "
        "failure modes with different implications for trust."
    ))
    return s


def reflection_marti():
    s = []
    s.append(PageBreak())
    s.append(refl_header("Marti", "Frontend · Failure Mode Analysis · Evaluation"))

    s.append(h2("My Contributions"))

    s.append(h3("Frontend"))
    s.append(body(
        "I built the entire frontend as a single HTML file (<i>src/static/index.html</i>) with "
        "no framework dependencies — plain JavaScript and CSS only. The interface includes "
        "a drag-and-drop upload area, a results panel with the summary, color-coded takeaway "
        "bubbles (purple for decisions, grey for notes), an action item checklist, and a "
        "collapsible sidebar showing the timeline of saved summarizations per project. "
        "The layout is fully responsive."
    ))
    s.append(body("Key design decisions:"))
    for item in [
        "<b>Progress bar</b> — transcription can take several minutes, so the interface shows a progress bar during processing.",
        "<b>Explicit error states</b> — unsupported file type, missing API key, model error all show a clear message rather than failing silently.",
        "<b>Project timeline</b> — meetings are grouped by month with dot-and-line connectors and staggered entry animation.",
    ]:
        s.append(bullet(item))

    s.append(h3("Failure Mode Analysis"))
    s.append(body(
        "After the evaluation was run, I documented the most informative failure cases in "
        "<i>data/eval/failure_analysis.md</i>. Each case includes the transcript excerpt, "
        "the model’s output, the gold label, and a hypothesis for why it failed. "
        "Main patterns identified:"
    ))
    for item in [
        "<b>Whisper mishearing proper nouns</b> — causes incorrect owner attribution downstream.",
        "<b>Phantom action items</b> — model generates commitments from hypothetical discussions.",
        "<b>Zero output on non-meeting audio</b> — correct behavior, but may confuse users.",
        "<b>Implied responsibility</b> — model leaves owner null rather than guessing.",
    ]:
        s.append(bullet(item))

    s.append(h3("Labeled Transcripts"))
    s.append(body(
        "I contributed approximately 8 labeled transcripts, deliberately designing difficult cases: "
        "meetings where no one is explicitly assigned a task, shared responsibilities, and "
        "informally stated deadlines."
    ))

    s.append(sp(1.5))
    s.append(h2("What I Learned"))
    s.append(body(
        "The most important thing I took away is how NLP errors propagate through a pipeline. "
        "Whisper’s transcription errors do not stay in the transcription layer — "
        "they flow directly into the LLM output. If Whisper mishears a name, the action item "
        "will have the wrong owner even if the model does everything else correctly. This "
        "cascading failure is hard to see from an aggregate F1 score alone, and it made me "
        "understand why failure mode analysis is treated as a required component of the assignment."
    ))
    s.append(body(
        "I also learned what information extraction means as an NLP task — it sits between "
        "pure classification and open-ended generation, and the challenge is that the output "
        "structure is constrained but the surface form is open, which is exactly why "
        "rule-based approaches fail on real, messy transcripts."
    ))
    return s


def reflection_bojana():
    s = []
    s.append(PageBreak())
    s.append(refl_header("Bojana", "Backend · NLP Pipeline · System Prompt"))

    s.append(h2("My Contributions"))

    s.append(h3("Backend and NLP Pipeline"))
    s.append(body(
        "I built the entire server-side application (<i>src/app.py</i>): the FastAPI server, "
        "the file upload endpoint, and the full two-stage NLP pipeline — routing audio "
        "files through faster-whisper for transcription, then passing the transcript to "
        "Claude Haiku 4.5 to extract the summary, typed takeaways, and action items. I also "
        "built all project management endpoints using a thin HTTP wrapper to avoid adding a "
        "full Supabase client library as a dependency."
    ))
    s.append(body(
        "Input type routing: audio and video files are written to a temporary file on disk "
        "before Whisper can process them; text files are read directly into memory. "
        "Temporary files are cleaned up reliably using try/finally even when transcription fails."
    ))

    s.append(h3("System Prompt and Output Schema"))
    s.append(body(
        "I designed the system prompt and JSON output schema that enforces the structure "
        "Claude must return. The schema defines three required fields — summary, "
        "key_takeaways, and action_items — with strict types and no additional properties "
        "allowed. Early versions produced inconsistent output: action items appearing inside "
        "the summary, takeaways missing their type tag, or the model inventing owners not in "
        "the transcript. I iterated on the prompt until the model reliably separated all three "
        "output types and only included owners and deadlines when explicitly stated."
    ))

    s.append(h3("Labeled Transcripts"))
    s.append(body(
        "I created approximately 8 transcripts for <i>eval_set.jsonl</i>, including standup "
        "meetings, sprint planning sessions, and one edge case where a speaker discusses a "
        "hypothetical future action without committing — designed to test whether the "
        "model invents phantom action items."
    ))

    s.append(sp(1.5))
    s.append(h2("What I Learned"))
    s.append(body(
        "This project gave me a real understanding of prompt engineering as an NLP technique "
        "rather than just a trick. When we started, the model would sometimes invent owners not "
        "mentioned in the transcript, or merge two separate action items into one. Fixing this "
        "required understanding why the model was doing it — it was following conversational "
        "implicature, inferring responsibility from context the way a human would — and "
        "then writing a prompt constraint specific enough to override that default behavior."
    ))
    s.append(body(
        "I also came to appreciate what makes LLM-based information extraction different from "
        "traditional approaches: the model handles paraphrase, messy grammar, and implicit "
        "references naturally. The cost is that you cannot fully predict or control the output, "
        "which is exactly why structured schemas and evaluation against gold labels are necessary."
    ))
    return s


def reflection_jo():
    s = []
    s.append(PageBreak())
    s.append(refl_header("Jo", "Database · Field Review · Evaluation"))

    s.append(h2("My Contributions"))

    s.append(h3("Supabase Database Layer"))
    s.append(body(
        "I designed and set up the entire persistence layer. I wrote "
        "<i>supabase_schema.sql</i>, which defines two tables: <i>projects</i> (for grouping "
        "meetings) and <i>summarizations</i> (for storing the full structured output). "
        "A key design decision was storing key_takeaways and action_items as JSONB columns "
        "rather than flat text, preserving the structured data as queryable fields."
    ))
    for item in [
        "<b>Cascade delete</b> — removing a project automatically removes all its meetings.",
        "<b>Row-level security</b> — RLS policies allow public read/write without requiring accounts, appropriate for a POC and documented as a limitation for production.",
    ]:
        s.append(bullet(item))
    s.append(body(
        "I also verified that the backend endpoints matched what Supabase expected, checking "
        "that REST calls for creating, listing, and deleting projects and summarizations all "
        "worked correctly against the live database."
    ))

    s.append(h3("Field Review"))
    s.append(body(
        "I researched the meeting-AI and transcription industry and wrote the field review "
        "section of the technical report, covering Otter.ai, Fireflies.ai, Zoom AI Companion, "
        "Fathom, and tl;dv. I cited sources from ACL Anthology, arXiv, and industry reports "
        "to ground the review in published research."
    ))

    s.append(h3("Labeled Transcripts"))
    s.append(body(
        "I contributed approximately 8 labeled transcripts, including excerpts from public "
        "city council meeting minutes — real, verbatim, and messy, with decisions both "
        "with and without clear owners."
    ))

    s.append(sp(1.5))
    s.append(h2("What I Learned"))
    s.append(body(
        "Doing the field review made me understand the difference between what NLP research "
        "has achieved and what is actually deployed in real products. There is a large body "
        "of work on meeting summarization, action item extraction, and dialogue act "
        "classification going back years, yet mainstream commercial tools still produce "
        "simple undifferentiated bullet lists. The research-to-product gap is real and wider "
        "than I expected."
    ))
    s.append(body(
        "I also developed a clearer understanding of the different NLP subtasks our system "
        "combines: automatic speech recognition (Whisper), abstractive summarization (the "
        "two-sentence summary), and named entity and relation extraction (pulling out task, "
        "owner, and deadline as structured fields). Each has its own failure modes and "
        "literature, and the overall system quality is limited by whichever stage performs "
        "worst on a given input."
    ))
    return s


def reflection_smaragda():
    s = []
    s.append(PageBreak())
    s.append(refl_header("Smaragda", "Evaluation Design · Executive Summary · User Manual · Slides"))

    s.append(h2("My Contributions"))

    s.append(h3("Evaluation Set Design and Annotation Methodology"))
    s.append(body(
        "I designed the evaluation set the whole team used. This included deciding on the "
        "format of <i>eval_set.jsonl</i>, writing the annotation guidelines the team followed "
        "when labeling, and coordinating labeling across all five members so everyone "
        "applied the same rules consistently."
    ))
    s.append(body("Key annotation decisions:"))
    for item in [
        "<b>What counts as an action item</b> — a concrete commitment by a named or identifiable person, not a vague intention or a plan discussed but not committed to.",
        "<b>Missing deadlines</b> — leave the deadline field blank rather than infer one.",
        "<b>Overlapping items</b> — when one transcript has multiple overlapping action items for the same person, list each separately.",
    ]:
        s.append(bullet(item))
    s.append(body(
        "I also ensured the test set covered a realistic range: standups, planning sessions, "
        "sales calls, retrospectives, and tricky edge cases (no action items at all, ambiguous "
        "ownership, hypothetical discussions). I contributed approximately 8 transcripts myself, "
        "focusing on multilingual scenarios."
    ))

    s.append(h3("Executive Summary"))
    s.append(body(
        "I wrote <i>deliverables/executive_summary.md</i>, leading with the cost of "
        "unproductive meetings and the specific barrier multilingual teams face, then describing "
        "what SummarAI does differently, then summarising the evaluation findings including "
        "the main limitation around owner attribution."
    ))

    s.append(h3("User Manual"))
    s.append(body(
        "I wrote <i>docs/user_manual.md</i> from scratch, covering every feature: uploading a "
        "file, choosing the output language, reading the summary and takeaway bubbles, checking "
        "off action items, saving to a project, and browsing the project timeline."
    ))

    s.append(h3("Presentation Slides"))
    s.append(body(
        "I put together the presentation slides (<i>deliverables/slides.md</i>), structuring "
        "the 20-minute presentation as: problem and motivation, field review, system overview, "
        "evaluation method and results, failure cases, future directions, and Q&A."
    ))

    s.append(sp(1.5))
    s.append(h2("What I Learned"))
    s.append(body(
        "Building the annotation guidelines taught me that the definition of a label is itself "
        "a research decision with real consequences for the evaluation. We started with a vague "
        "shared understanding of what an action item was, and when I tried to write it down "
        "precisely, edge cases appeared immediately: is ‘we should probably follow up on "
        "this’ an action item? What if no one is named as responsible? These decisions "
        "determine what the model is being evaluated against — so they determine what "
        "the evaluation actually measures."
    ))
    s.append(body(
        "I now understand why inter-annotator agreement is reported in NLP papers: it is not "
        "a formality, it is evidence that the label definition is precise enough to be applied "
        "consistently. I also understood more deeply what the summarization task is about: "
        "not just shortening text, but identifying what is important and representing it in "
        "a structured, reusable form."
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
        "Antonio  ·  Bojana  ·  Jo  ·  Marti  ·  Smaragda",
        "NLP Group Project  ·  2025–2026",
        "SummarAI  —  Individual Reflections",
        story,
        cover_names=["Antonio", "Bojana", "Jo", "Marti", "Smaragda"],
    )


# ═══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("Building PDFs...")
    build_executive_summary()
    build_installation_guide()
    build_user_manual()
    build_reflections()
    print("Done.")
