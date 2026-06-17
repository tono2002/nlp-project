"""Generate SummarAI_Technical_Report.pdf from technical_report.md"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import Flowable

# ── Colours ──────────────────────────────────────────────────────────────────
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

# ── Styles ────────────────────────────────────────────────────────────────────
base = getSampleStyleSheet()

def style(name, parent="Normal", **kw):
    s = ParagraphStyle(name, parent=base[parent], **kw)
    return s

S = {
    "cover_title": style("cover_title", "Title",
        fontSize=28, textColor=WHITE, alignment=TA_CENTER,
        spaceAfter=6, leading=34),
    "cover_sub": style("cover_sub", "Normal",
        fontSize=13, textColor=colors.HexColor("#c7d2fe"),
        alignment=TA_CENTER, spaceAfter=4),
    "cover_meta": style("cover_meta", "Normal",
        fontSize=10, textColor=colors.HexColor("#a5b4fc"),
        alignment=TA_CENTER, spaceAfter=2),

    "h1": style("h1", "Heading1",
        fontSize=16, textColor=INDIGO, spaceBefore=18, spaceAfter=6,
        borderPad=0, leading=20),
    "h2": style("h2", "Heading2",
        fontSize=12, textColor=VIOLET, spaceBefore=14, spaceAfter=4,
        leading=15),
    "body": style("body", "Normal",
        fontSize=10, textColor=BLACK, leading=15, spaceAfter=6,
        alignment=TA_JUSTIFY),
    "bullet": style("bullet", "Normal",
        fontSize=10, textColor=BLACK, leading=14, spaceAfter=3,
        leftIndent=14, firstLineIndent=0),
    "code": style("code", "Code",
        fontSize=8.5, textColor=colors.HexColor("#1e1b4b"),
        backColor=GREY_LT, leading=12, leftIndent=8, rightIndent=8,
        spaceAfter=8, spaceBefore=4),
    "ref": style("ref", "Normal",
        fontSize=8.5, textColor=GREY_MD, leading=13, spaceAfter=3,
        leftIndent=14, firstLineIndent=-14),
    "caption": style("caption", "Normal",
        fontSize=8, textColor=GREY_MD, alignment=TA_CENTER, spaceAfter=6),
    "tbl_hdr": style("tbl_hdr", "Normal",
        fontSize=9, textColor=WHITE, leading=12, alignment=TA_CENTER),
    "tbl_cell": style("tbl_cell", "Normal",
        fontSize=9, textColor=BLACK, leading=12),
    "tbl_cell_c": style("tbl_cell_c", "Normal",
        fontSize=9, textColor=BLACK, leading=12, alignment=TA_CENTER),
}


# ── Table helper ──────────────────────────────────────────────────────────────
def make_table(header, rows, col_widths=None):
    usable = W - 2 * MARGIN
    if col_widths is None:
        n = len(header)
        col_widths = [usable / n] * n

    hdr_row = [Paragraph(h, S["tbl_hdr"]) for h in header]
    data = [hdr_row]
    for row in rows:
        data.append([Paragraph(str(c), S["tbl_cell"]) for c in row])

    t = Table(data, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND",  (0,0), (-1,0),  INDIGO),
        ("BACKGROUND",  (0,1), (-1,-1), WHITE),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [WHITE, INDIGO_L]),
        ("GRID",        (0,0), (-1,-1), 0.4, colors.HexColor("#e0e7ff")),
        ("TOPPADDING",  (0,0), (-1,-1), 5),
        ("BOTTOMPADDING",(0,0),(-1,-1), 5),
        ("LEFTPADDING", (0,0), (-1,-1), 7),
        ("RIGHTPADDING",(0,0), (-1,-1), 7),
        ("VALIGN",      (0,0), (-1,-1), "MIDDLE"),
    ]))
    return t


def rule():
    return HRFlowable(width="100%", thickness=0.5,
                      color=colors.HexColor("#e0e7ff"), spaceAfter=6)


# ── Cover page ────────────────────────────────────────────────────────────────
class CoverPage(Flowable):
    def __init__(self):
        super().__init__()
        self.width  = W
        self.height = H

    def draw(self):
        c = self.canv
        # Background gradient-ish rectangle
        c.setFillColor(GREY_DK)
        c.rect(0, 0, W, H, fill=1, stroke=0)
        # Accent bar top
        c.setFillColor(INDIGO)
        c.rect(0, H - 1.2*cm, W, 1.2*cm, fill=1, stroke=0)
        # Accent bar bottom
        c.setFillColor(VIOLET)
        c.rect(0, 0, W, 0.6*cm, fill=1, stroke=0)

        # Title
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 36)
        c.drawCentredString(W/2, H*0.62, "SummarAI")

        c.setFillColor(colors.HexColor("#c7d2fe"))
        c.setFont("Helvetica", 16)
        c.drawCentredString(W/2, H*0.55, "Technical Report")

        # Divider
        c.setStrokeColor(INDIGO)
        c.setLineWidth(1.5)
        c.line(W*0.3, H*0.51, W*0.7, H*0.51)

        c.setFillColor(colors.HexColor("#a5b4fc"))
        c.setFont("Helvetica", 11)
        c.drawCentredString(W/2, H*0.47, "Automated Meeting Summarization using Whisper + Claude")

        c.setFont("Helvetica", 10)
        c.drawCentredString(W/2, H*0.41, "NLP Group Project  ·  2025–2026")

        c.setFont("Helvetica", 9)
        c.drawCentredString(W/2, H*0.36,
            "Antonio · Bojana · Jo · Marti · Smaragda")


# ── Build document ────────────────────────────────────────────────────────────
def build():
    out = "docs/SummarAI_Technical_Report.pdf"
    doc = SimpleDocTemplate(
        out, pagesize=A4,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=MARGIN, bottomMargin=MARGIN,
        title="SummarAI Technical Report",
        author="NLP Group",
    )

    story = []
    story.append(PageBreak())  # cover is drawn via onFirstPage callback, this skips to page 2

    # ── 1. Introduction ────────────────────────────────────────────────────
    story.append(Paragraph("1. Introduction", S["h1"]))
    story.append(rule())
    story.append(Paragraph(
        "Meetings generate decisions and commitments, but most of that information is lost shortly "
        "after the call ends. People rely on informal notes, fragmented memory, or re-watching "
        "recordings — none of which scale. <b>SummarAI</b> is a web application that automates "
        "this capture: upload an English-language meeting recording and, within minutes, receive a "
        "concise written record structured around two outputs: a short prose summary and a set of "
        "bullet points covering key takeaways and action items.", S["body"]))
    story.append(Paragraph(
        "The system chains two NLP components. First, a local speech recognition model (Whisper) "
        "converts audio to text. Second, a large language model (Claude Haiku 4.5) reads that "
        "transcript and produces structured output through a strict JSON schema. The web interface "
        "is minimal by design — the value is in the NLP pipeline, not the UI.", S["body"]))
    story.append(Paragraph(
        "This report describes the motivation, the technical design, an empirical evaluation, and "
        "the failure modes documented during development.", S["body"]))

    # ── 2. Justification of need ───────────────────────────────────────────
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph("2. Justification of Need", S["h1"]))
    story.append(rule())
    story.append(Paragraph(
        "Meetings consume a large share of knowledge workers' time, yet much of their value is lost "
        "once the call ends. The problem is rarely the discussion itself but the follow-through: "
        "decisions made verbally go unrecorded, action items are forgotten, and participants who "
        "were absent have no reliable way to catch up. A written record fixes this, but taking "
        "accurate minutes by hand is tedious and routinely skipped.", S["body"]))
    story.append(Paragraph(
        "Several tools exist to address this — Otter.ai, Fireflies.ai, Zoom AI Companion, and "
        "Microsoft Teams Copilot all offer some form of meeting transcription and summary. Their "
        "limitations are relevant to this project:", S["body"]))
    for bullet in [
        "<b>Cost and access:</b> all major tools require paid subscriptions; several are tied to specific video-conferencing platforms.",
        "<b>Output quality:</b> most tools produce a raw transcript or a continuous prose summary. They rarely separate <i>decisions</i> from <i>notes</i>, and action-item extraction is either absent or unreliable when responsibility is only implied.",
        "<b>Closed systems:</b> none of these tools expose the underlying model or prompt, making it impossible to understand or modify their behaviour.",
    ]:
        story.append(Paragraph("• " + bullet, S["bullet"]))
    story.append(Spacer(1, 0.2*cm))
    story.append(Paragraph(
        "SummarAI addresses the output-quality gap specifically. Its two-output design — a 2-sentence "
        "summary plus typed bullet points (decision / note / action item) — forces the model to make "
        "an explicit distinction that conversational summaries routinely blur.", S["body"]))

    # ── 3. Field review ────────────────────────────────────────────────────
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph("3. Field Review", S["h1"]))
    story.append(rule())

    story.append(Paragraph("3.1 Automatic Speech Recognition (ASR)", S["h2"]))
    story.append(Paragraph(
        "The dominant open-source ASR model at the time of writing is OpenAI Whisper (Radford et al., 2022). "
        "Whisper is an encoder-decoder transformer trained on 680,000 hours of web audio, achieving "
        "near-human accuracy on clean English speech and robust performance on accented or lightly "
        "noisy audio. Its English-only variants (<i>tiny.en</i>, <i>base.en</i>, <i>small.en</i>) "
        "outperform the corresponding multilingual models on English audio while being faster.", S["body"]))
    story.append(Paragraph(
        "<i>faster-whisper</i> is a community re-implementation of Whisper using the CTranslate2 "
        "inference library. It achieves the same output as the original at 2–4× lower memory usage "
        "and measurably faster runtime, making it practical for a local CPU deployment without a GPU.", S["body"]))
    story.append(Paragraph(
        "Commercial ASR alternatives (AssemblyAI, AWS Transcribe, Azure Cognitive Services) offer "
        "higher accuracy on telephony-quality audio and built-in speaker diarization, at per-minute "
        "costs that make them unsuitable for a course prototype.", S["body"]))

    story.append(Paragraph("3.2 Meeting Summarization and Information Extraction", S["h2"]))
    story.append(Paragraph(
        "LLM-based summarization has largely displaced earlier extractive and abstractive approaches "
        "(TextRank, BART, PEGASUS) for long-document tasks. Instruction-tuned models handle long, "
        "noisy meeting transcripts better than task-specific fine-tuned models, primarily because "
        "they can follow complex, multi-part instructions about output format.", S["body"]))
    story.append(Paragraph(
        "Structured output — enforcing a JSON schema at the API level rather than prompt-engineering "
        "the model to emit valid JSON — eliminates parsing failures caused by model deviation from "
        "the expected format. Claude Haiku 4.5 was selected for this project on cost grounds: it is "
        "the fastest and cheapest model in the Claude 4 family while still following complex "
        "structured instructions reliably.", S["body"]))

    # ── 4. System description ──────────────────────────────────────────────
    story.append(PageBreak())
    story.append(Paragraph("4. System Description", S["h1"]))
    story.append(rule())

    story.append(Paragraph("4.1 Architecture", S["h2"]))
    story.append(Paragraph(
        "SummarAI is a single-server web application. The backend is a Python FastAPI app "
        "(<i>src/app.py</i>). The frontend is a single-page vanilla JavaScript application "
        "(<i>src/static/index.html</i>). Meeting results can optionally be saved to a Supabase "
        "(PostgreSQL) database for project-level persistence and timeline views.", S["body"]))

    # Input formats table
    story.append(Spacer(1, 0.2*cm))
    story.append(make_table(
        ["Category", "Supported Extensions"],
        [
            ["Audio / Video", ".mp4  ·  .mp3  ·  .wav  ·  .m4a  ·  .webm  ·  .ogg  ·  .flac"],
            ["Text (skip ASR)", ".txt  ·  .md  ·  .vtt  ·  .srt"],
        ],
        col_widths=[(W-2*MARGIN)*0.28, (W-2*MARGIN)*0.72]
    ))
    story.append(Spacer(1, 0.2*cm))

    story.append(Paragraph("4.2 Two-Stage NLP Pipeline", S["h2"]))
    story.append(Paragraph(
        "<b>Stage 1 — Speech-to-text.</b> <i>faster-whisper</i> runs locally on CPU using the "
        "<i>base.en</i> model in int8 quantization. Voice activity detection "
        "(<i>vad_filter=True</i>) strips silence before transcription. The output is a plain "
        "string of the full meeting speech.", S["body"]))
    story.append(Paragraph(
        "<b>Stage 2 — Summarization and information extraction.</b> The transcript is sent to "
        "Claude Haiku 4.5 with a system prompt that instructs the model to produce exactly "
        "three structured fields:", S["body"]))
    for item in [
        "<b>summary</b> — at most 2 short sentences stating the meeting's purpose and overall outcome.",
        "<b>key_takeaways</b> — an array of bullet objects, each with a <i>text</i> field (≤14 words) and a <i>type</i> field: <i>\"decision\"</i> (something agreed or set as policy) or <i>\"note\"</i> (any other important point). The instruction to be comprehensive is deliberate: the 2-sentence summary omits detail by design, so takeaways carry all substantive information.",
        "<b>action_items</b> — concrete tasks with <i>owner</i> and <i>deadline</i> populated only when actually stated; never inferred.",
    ]:
        story.append(Paragraph("• " + item, S["bullet"]))

    story.append(Paragraph("4.3 Performance Optimization", S["h2"]))
    story.append(Paragraph(
        "During development we measured end-to-end processing time on a 20-minute .m4a file on a "
        "standard laptop CPU. Latency was almost entirely in the ASR stage — Claude Haiku 4.5 "
        "returned in 3–6 seconds regardless of transcript length. We applied four zero-cost "
        "changes to the transcription stage:", S["body"]))

    story.append(make_table(
        ["Change", "Rationale"],
        [
            ["base.en instead of multilingual base", "English-only model is faster and more accurate for English audio"],
            ["beam_size=1 (greedy decoding)", "Removes beam search overhead (~2× faster) with negligible accuracy loss"],
            ["cpu_threads=os.cpu_count()", "Uses all available cores instead of the library default"],
            ["language=\"en\"", "Skips the automatic language-detection pass"],
        ],
        col_widths=[(W-2*MARGIN)*0.38, (W-2*MARGIN)*0.62]
    ))
    story.append(Spacer(1, 0.3*cm))

    story.append(make_table(
        ["Configuration", "Total Time", "Transcript Length"],
        [
            ["Original (base, beam 5, auto-detect)", "7 min 50 s", "36,702 chars"],
            ["Optimized (base.en, greedy, multithread)", "2 min 12 s", "36,620 chars"],
        ],
        col_widths=[(W-2*MARGIN)*0.5, (W-2*MARGIN)*0.25, (W-2*MARGIN)*0.25]
    ))
    story.append(Spacer(1, 0.2*cm))
    story.append(Paragraph(
        "This represents a <b>3.5× speedup (≈72% reduction) at zero additional cost</b>, with no "
        "measurable effect on downstream summary quality.", S["body"]))

    # ── 5. Custom evaluation ───────────────────────────────────────────────
    story.append(PageBreak())
    story.append(Paragraph("5. Custom Evaluation", S["h1"]))
    story.append(rule())

    story.append(Paragraph("5.1 Methodology", S["h2"]))
    story.append(Paragraph(
        "Our test set is <b>30 meetings from the AMI Meeting Corpus</b> (Carletta et al., 2006), "
        "a widely used research dataset of recorded meetings. AMI is annotated with human-written "
        "abstractive summaries, each split into ABSTRACT, DECISIONS, and ACTIONS sections. We use "
        "those human annotations as ground truth, avoiding the circularity of grading an LLM "
        "against answers we wrote ourselves.", S["body"]))
    story.append(Paragraph(
        "We feed our own Whisper transcripts (not AMI's clean reference transcripts) as input, so "
        "scores reflect the full audio-to-summary path, including transcription noise. Two metrics "
        "are reported:", S["body"]))
    for item in [
        "<b>ROUGE-1 / 2 / L (F-measure):</b> our full output against the human reference. ROUGE is the standard meeting-summarization metric.",
        "<b>Action-item coverage (recall):</b> the fraction of human ACTIONS sentences that a predicted action item covers, counting a match when ROUGE-L F ≥ 0.30.",
    ]:
        story.append(Paragraph("• " + item, S["bullet"]))

    story.append(Paragraph("5.2 Results", S["h2"]))
    story.append(make_table(
        ["Metric", "Score"],
        [
            ["ROUGE-1 (F, avg)", "0.335"],
            ["ROUGE-2 (F, avg)", "0.057"],
            ["ROUGE-L (F, avg)", "0.148"],
            ["Action-item coverage (recall)", "0.424  (28 / 66)"],
        ],
        col_widths=[(W-2*MARGIN)*0.6, (W-2*MARGIN)*0.4]
    ))
    story.append(Spacer(1, 0.2*cm))
    story.append(Paragraph(
        "The summaries are coherent and stay on topic. ROUGE figures are modest primarily due to a "
        "deliberate <b>format mismatch</b>: our summary is two sentences by design, whereas an AMI "
        "reference is a ~200-word multi-section document. ROUGE rewards n-gram overlap, so a "
        "deliberately compressed output is penalised on form even when its content is accurate. "
        "A ROUGE-1 of 0.34 means our output shares roughly a third of its unigrams with a much "
        "longer human summary — a reasonable result for an output that is an order of magnitude "
        "shorter.", S["body"]))
    story.append(Paragraph(
        "The most informative number is the <b>42% action-item coverage</b>: working end to end "
        "from raw audio, the system recovers roughly four of every ten action items a human "
        "annotator recorded.", S["body"]))

    story.append(Paragraph("5.3 Error Analysis", S["h2"]))
    story.append(Paragraph(
        "Two systematic factors explain most missed action items:", S["body"]))
    for item in [
        '<b>Representation gap.</b> AMI annotates actions by <i>role</i> (&ldquo;the industrial designer will work on the design&rdquo;), while SummarAI extracts them by <i>name</i>. The surface forms differ enough to fall below the overlap threshold.',
        "<b>Owner attribution / speaker identity.</b> Whisper produces no speaker labels. When responsibility is implied rather than named, the model leaves owner null rather than guessing — conservative and arguably correct, but it counts as an incomplete action item.",
    ]:
        story.append(Paragraph("• " + item, S["bullet"]))

    # ── 6. Failure mode analysis ───────────────────────────────────────────
    story.append(PageBreak())
    story.append(Paragraph("6. Failure Mode Analysis", S["h1"]))
    story.append(rule())
    story.append(Paragraph(
        "The following cases were documented during development and evaluation.", S["body"]))

    failures = [
        ("1. Implied speaker identity",
         "When responsibility is suggested rather than stated (&ldquo;we should look into this&rdquo;), "
         "the model correctly produces an action item with owner: null. This limits the "
         "utility of the action-item list for follow-up."),
        ("2. Whisper mishearing proper nouns",
         "Names uncommon in Whisper's training data are occasionally transcribed incorrectly "
         "(e.g. Bojana transcribed as Janna). This propagates directly into incorrect "
         "owner attribution downstream."),
        ("3. Off-topic or non-meeting audio",
         "Podcast-style recordings, long monologues, and panel discussions produce coherent "
         "summaries but correctly yield zero action items. Users uploading non-meeting content "
         "may be confused by the empty action-item list."),
        ("4. Heavily overlapping or noisy audio",
         "Whisper's VAD filter removes silence effectively but does not separate overlapping "
         "speakers. In meetings where multiple participants speak simultaneously, the transcript "
         "can contain garbled sentences. Summary quality degrades noticeably."),
        ("5. Very long meetings near the character limit",
         "Processing time scales linearly with transcript length. A 2-hour meeting can take "
         "4–5 minutes on modest hardware. The LLM context window is not a bottleneck at "
         "current meeting lengths."),
        ("6. Implicit decisions",
         "When a decision emerges through consensus rather than an explicit statement, the model "
         "sometimes tags it as note rather than decision. The distinction is genuinely ambiguous "
         "in natural speech."),
        ("7. Repetitive or circular discussions",
         "In meetings where the same point is debated multiple times, the model sometimes "
         "produces duplicate or near-duplicate takeaways. The system prompt instructs "
         "comprehensiveness, which can work against deduplication."),
    ]
    for title, body in failures:
        story.append(KeepTogether([
            Paragraph(f"<b>{title}</b>", S["body"]),
            Paragraph(body, S["bullet"]),
            Spacer(1, 0.15*cm),
        ]))

    # ── 7. Future directions ───────────────────────────────────────────────
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph("7. Future Directions", S["h1"]))
    story.append(rule())
    directions = [
        ("<b>Speaker diarization.</b>",
         "Integrating automatic speaker labelling would directly solve the owner attribution "
         "problem. Libraries such as pyannote.audio provide open-source diarization that could "
         "be inserted between the Whisper ASR stage and the LLM stage."),
        ("<b>Larger Whisper models.</b>",
         "The base.en model was chosen for speed. On hardware with more RAM, small.en or "
         "medium.en would improve accuracy on accented speech, domain-specific vocabulary, "
         "and noisy audio."),
        ("<b>Confidence and uncertainty signals.</b>",
         "The current system does not communicate uncertainty. A useful extension would flag "
         "action items or decisions where the model's confidence is low."),
        ("<b>Persistent project search.</b>",
         "Adding full-text search over saved summaries and takeaways would make the meeting "
         "archive genuinely useful as an organizational memory tool."),
        ("<b>Deployment.</b>",
         "The local Whisper model rules out serverless hosting (Vercel, Lambda) due to memory "
         "and runtime constraints. A long-running FastAPI server on Render, Railway, or Fly.io "
         "would work without changes to the application code."),
    ]
    for heading, body in directions:
        story.append(Paragraph(f"{heading} {body}", S["bullet"]))
        story.append(Spacer(1, 0.15*cm))

    # ── 8. Use of AI tools ─────────────────────────────────────────────────
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph("8. Use of AI Tools", S["h1"]))
    story.append(rule())
    story.append(Paragraph(
        "Claude (Anthropic) was used throughout the project in several capacities:", S["body"]))
    for item in [
        "<b>Code generation and debugging:</b> the FastAPI backend, structured output schema, and Supabase integration were iteratively developed with Claude assistance.",
        "<b>System prompt engineering:</b> the system prompt was drafted collaboratively — initial versions generated by Claude Sonnet and refined through iterative testing on real transcripts.",
        "<b>Documentation:</b> sections of this report, the user manual, and the installation guide were drafted with Claude assistance and then reviewed and edited by team members.",
        "<b>Transcription (Whisper):</b> the ASR component is itself an AI model, used as a fixed inference component rather than interactively.",
    ]:
        story.append(Paragraph("• " + item, S["bullet"]))
    story.append(Spacer(1, 0.2*cm))
    story.append(Paragraph(
        "All code, prompts, and documentation were reviewed and edited by team members. "
        "No output was used without human review.", S["body"]))

    # ── 9. Conclusion ──────────────────────────────────────────────────────
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph("9. Conclusion", S["h1"]))
    story.append(rule())
    story.append(Paragraph(
        "SummarAI demonstrates that a two-stage NLP pipeline — local ASR followed by a structured "
        "LLM call — can reliably transform an English meeting recording into an actionable written "
        "record. The system is functional, reproducible, and fast enough for practical use on "
        "consumer hardware.", S["body"]))
    story.append(Paragraph(
        "The key finding from development was empirical: latency is dominated by transcription, "
        "not by the LLM, and a set of zero-cost Whisper optimizations reduced total processing "
        "time by 72% with no measurable loss in output quality. The key limitation is owner "
        "attribution, a problem that speaker diarization would directly address.", S["body"]))
    story.append(Paragraph(
        "The two-output design (summary + bullets) proved to be the right abstraction. The "
        "2-sentence summary is useful for quick orientation; the typed bullet list carries the "
        "substance. Separating decisions from notes forces the model to make a distinction that "
        "is genuinely useful for follow-up and accountability.", S["body"]))

    # ── References ─────────────────────────────────────────────────────────
    story.append(PageBreak())
    story.append(Paragraph("References", S["h1"]))
    story.append(rule())
    refs = [
        "Carletta, J., et al. (2006). <i>The AMI meeting corpus: A pre-announcement.</i> Machine Learning for Multimodal Interaction (MLMI), 28–39.",
        "Lewis, M., et al. (2020). <i>BART: Denoising sequence-to-sequence pre-training for natural language generation, translation, and comprehension.</i> Proceedings of ACL 2020.",
        "Radford, A., et al. (2022). <i>Robust speech recognition via large-scale weak supervision.</i> arXiv preprint arXiv:2212.04356.",
        "See, A., Liu, P. J., & Manning, C. D. (2017). <i>Get to the point: Summarization with pointer-generator networks.</i> Proceedings of ACL 2017.",
        "SYSTRAN. (2023). <i>faster-whisper</i> [Computer software]. GitHub. https://github.com/SYSTRAN/faster-whisper",
        "Vaswani, A., et al. (2017). <i>Attention is all you need.</i> Advances in Neural Information Processing Systems, 30.",
    ]
    for r in refs:
        story.append(Paragraph(r, S["ref"]))
        story.append(Spacer(1, 0.1*cm))

    # ── Page callbacks ─────────────────────────────────────────────────────
    def first_page(canvas, doc):
        # Draw full-bleed cover
        canvas.saveState()
        canvas.setFillColor(GREY_DK)
        canvas.rect(0, 0, W, H, fill=1, stroke=0)
        canvas.setFillColor(INDIGO)
        canvas.rect(0, H - 1.2*cm, W, 1.2*cm, fill=1, stroke=0)
        canvas.setFillColor(VIOLET)
        canvas.rect(0, 0, W, 0.6*cm, fill=1, stroke=0)
        canvas.setFillColor(WHITE)
        canvas.setFont("Helvetica-Bold", 36)
        canvas.drawCentredString(W/2, H*0.62, "SummarAI")
        canvas.setFillColor(colors.HexColor("#c7d2fe"))
        canvas.setFont("Helvetica", 16)
        canvas.drawCentredString(W/2, H*0.55, "Technical Report")
        canvas.setStrokeColor(INDIGO)
        canvas.setLineWidth(1.5)
        canvas.line(W*0.3, H*0.51, W*0.7, H*0.51)
        canvas.setFillColor(colors.HexColor("#a5b4fc"))
        canvas.setFont("Helvetica", 11)
        canvas.drawCentredString(W/2, H*0.47, "Automated Meeting Summarization using Whisper + Claude")
        canvas.setFont("Helvetica", 10)
        canvas.drawCentredString(W/2, H*0.41, "NLP Group Project  .  2025-2026")
        canvas.setFont("Helvetica", 9)
        canvas.drawCentredString(W/2, H*0.36, "Antonio  .  Bojana  .  Jo  .  Marti  .  Smaragda")
        canvas.restoreState()

    def later_pages(canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(GREY_MD)
        canvas.drawCentredString(W/2, 1.2*cm, f"SummarAI Technical Report  .  Page {doc.page}")
        canvas.restoreState()

    doc.build(story, onFirstPage=first_page, onLaterPages=later_pages)
    print(f"PDF written: {out}")


if __name__ == "__main__":
    build()
