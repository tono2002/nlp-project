# User Manual

> **Option 1 deliverable.** How an end user operates the application.

---

## Overview

SummarAI is a meeting summarisation tool. You give it a recorded meeting — as an audio/video file or a plain-text transcript — and it returns three things:

- **Summary** — a concise paragraph capturing what the meeting was about
- **Key takeaways** — the main points and decisions made
- **Action items** — concrete tasks, with the responsible person where identifiable

The language of the output is **your choice**, not the language of the meeting. You can attend an English meeting and receive everything in Spanish, or vice versa.

---

## Getting started

### Option A — Hosted version _(recommended)_

> Live link: _TODO — add URL once deployed._

Open the link in any modern browser (Chrome, Firefox, Safari, Edge). No installation or account needed.

### Option B — Run locally

Follow the [Installation & Execution Guide](installation_guide.md) to set up the project on your machine, then run:

```bash
python src/app.py
```

Open `http://127.0.0.1:7860` in your browser.

---

## Features

### 1. Upload a meeting recording

Drag and drop — or click **Upload file** — to load an audio or video file.

| Supported format | Extension |
|---|---|
| MP4 video | `.mp4` |
| MP3 audio | `.mp3` |
| WAV audio | `.wav` |
| M4A audio | `.m4a` |

SummarAI will automatically transcribe the audio using Whisper before processing it. Transcription runs locally on your machine; your audio is never sent to an external server.

> **File size tip:** Files under 100 MB process fastest. For longer recordings, consider trimming silence at the start and end.

---

### 2. Paste a transcript directly

If you already have the meeting text (e.g. exported from Zoom or Teams), click the **Paste transcript** tab, paste the text, and skip the transcription step entirely. This is faster and avoids any ASR errors.

---

### 3. Choose the output language

Use the **Output language** selector to choose between:

- 🇬🇧 **English**
- 🇪🇸 **Spanish**

This setting controls the language of the summary, takeaways, and action items — independently of the language spoken in the meeting. A meeting conducted in English can produce a Spanish summary, and vice versa.

---

### 4. Run the summarisation

Click **Summarise**. Processing time depends on file length:

| Meeting length | Approximate wait time |
|---|---|
| < 10 minutes | 15–45 seconds |
| 10–30 minutes | 1–3 minutes |
| 30–60 minutes | 3–6 minutes |

While processing, a progress bar shows the current step (Transcribing → Summarising).

---

### 5. Read the results

Results appear in three panels:

**Summary**
A short paragraph (3–5 sentences) describing the meeting's purpose, main discussion points, and outcome.

**Key takeaways**
A bullet list of the most important points and decisions. Typically 4–8 items.

**Action items**
A structured list of tasks agreed during the meeting. Where the recording makes it clear who is responsible, the owner is listed next to the task.

Example output (English meeting → Spanish output):

```
📋 Resumen
El equipo revisó el estado del sprint actual y acordó retrasar el lanzamiento
una semana para completar las pruebas de rendimiento. Se asignaron tareas
específicas para abordar los problemas de latencia identificados.

✅ Puntos clave
• El lanzamiento se pospone al 24 de junio.
• Las pruebas de rendimiento son bloqueantes.
• El equipo de backend priorizará la reducción de latencia esta semana.

📌 Tareas
• Reducir la latencia de la API por debajo de 200 ms — responsable: equipo backend
• Actualizar el documento de release notes — responsable: Ana
• Confirmar la nueva fecha con el cliente — responsable: Marcos
```

---

### 6. Export the results

Click **Copy to clipboard** under any panel to copy the text, or click **Download as .txt** to save all three outputs as a single plain-text file.

---

## Example usage

**Scenario:** You are a Spanish-speaking team lead. Your weekly sync is conducted in English. You want a Spanish action-item list to share with a colleague who was absent.

1. After the meeting, export the recording as an `.mp4` from Zoom (or ask a colleague to send it).
2. Open SummarAI and drag the file onto the upload area.
3. Set **Output language** to **Spanish**.
4. Click **Summarise** and wait ~1 minute.
5. Copy the **Tareas** panel and paste it into your team's Slack or Notion page.

---

## Limitations

SummarAI is a proof-of-concept. The following are known limitations:

| Limitation | Detail |
|---|---|
| **No speaker diarisation** | Whisper does not identify who is speaking. Action-item owners are inferred from the transcript text only (e.g. "John, can you handle this?"). If speakers are not named, the owner field will be empty. |
| **Audio quality matters** | Strong background noise, heavy accents, or overlapping speech degrade transcription accuracy, which propagates to the summary. |
| **No visual content** | Anything shown on screen (slides, diagrams, whiteboard) is not captured. Only spoken content is processed. |
| **Long meetings lose coherence** | For recordings over 60 minutes, the model may lose track of early context. Split very long recordings into segments for best results. |
| **Action items may occasionally be hallucinated** | The model may infer a plausible but unspoken action item. Always review the output before sharing. |
| **Two output languages only** | The current version supports English and Spanish. Other languages are planned for a future release. |