# 👋 Teammate Guide — Working on SummarAI with Claude Code

Read this once. It shows you how to clone the repo, get Claude Code up to speed on our project, and finish your part of the deliverables **fast but well** — so we're done by tomorrow.

---

## 1. Get set up (5 minutes)

1. Install **Claude Code** (the terminal tool) and have a **Claude.ai** account open in your browser too — you'll use both.
2. Clone the project:
   ```
   git clone https://github.com/tono2002/nlp-project.git
   cd nlp-project
   ```
3. Open the folder in your terminal and start Claude Code by typing:
   ```
   claude
   ```
4. **Before anything else, pull the latest** so you're not working on old files:
   ```
   git pull
   ```

---

## 2. ⭐ The golden rule: give Claude the context FIRST

Claude Code starts each session knowing *nothing* about our project. Don't just ask it to "write the slides." First, make it read our repo. Paste this as your **first message** every session:

> Read `README.md`, `ROADMAP.md`, and `PROJECT_PLAN.md` in this repo. Also read `Group_Assignment_NLP.pdf` if it's here, or ask me for the assignment criteria. Then tell me in 5 bullet points: what SummarAI is, what's already done, what's left, and the grading criteria. I'm **[your name]** and I'm working on **[your task]**.

Now Claude understands the project, the app, what's done, and how we're graded — and everything it writes will fit our actual project instead of generic filler.

**Key context files already in the repo:**
- `README.md` — what the app is, the tech, the project status (done vs to-do)
- `ROADMAP.md` — who does what, the one-day plan
- `PROJECT_PLAN.md` — the simple explanation of the whole assignment
- `deliverables/technical_report.md` — the report skeleton (already has a real "Performance" finding written in §4.2)

---

## 3. Find your job

Open `ROADMAP.md` → "Quick owner map" and find your name. In short:

| You | Your main deliverable |
|---|---|
| **Antonio** | App polish, prompts doc, install guide |
| **Martí** | Build & run the evaluation script |
| **Bojana** | Evaluation metrics + failure analysis |
| **Jo** | Field review + slides |
| **Smaragda** | Executive summary + user manual + slides |
| **Everyone** | ~9 labeled transcripts each + your own reflection |

---

## 4. How to work fast but good (the loop)

For whatever you're writing, repeat this with Claude Code:

1. **Point it at the repo context** (golden rule above).
2. **Ask for a draft** of your specific deliverable, telling it to base everything on our actual project — not invent things.
3. **Read what it wrote.** Fix anything wrong or generic. *You* own the ideas — the rubric says you must be able to defend every choice in Q&A.
4. **Tell it to save the file** in the right place (e.g. "save this to `deliverables/executive_summary.md`").
5. **Commit and push** so the team has it (see §6).

⏱️ **Don't aim for perfect — aim for done and correct.** One solid pass per deliverable beats endless polishing.

---

## 5. Claude Code vs. Claude.ai — use the right one

- **Claude Code (terminal)** → working *inside the repo*: reading our files, writing the markdown deliverables, running the app, the eval script, screenshots. **Use it for anything that touches the repo.**
- **Claude.ai (browser chat)** → making **polished documents**: it can generate real **Word (.docx)**, **PowerPoint (.pptx)**, and **PDF** files directly. Great for the final report PDF, the slide deck, and the executive summary if you want it nicely formatted.

**Workflow that works best:** draft the *content* in Claude Code (so it's grounded in our repo), then paste that content into Claude.ai and ask it to turn it into a clean .pptx / .docx / .pdf. Best of both.

---

## 6. ⚠️ Limits of Claude Code — know these

- **It doesn't make pretty PDFs or slides.** It writes the *text/markdown*. For a polished **PDF report** or **slide deck**, take the content to **Claude.ai** (it has document-creation skills) or build slides in **Google Slides / PowerPoint / Canva**.
- **It can READ a PDF** (like the assignment brief) but you may need to point it at the file.
- **It works on your computer only** — your changes aren't shared until you **push** (see below).
- **It can't invent our results.** Do **not** let it make up evaluation numbers, accuracy scores, or fake quotes. Use the **real numbers** from `evaluate.py` once Martí/Bojana run it. Made-up data is the fastest way to fail the project.
- **For the field review**, Claude can structure and draft, but **check the sources it cites are real** (use Google Scholar / arXiv). Don't submit citations you haven't verified.

---

## 7. 🔀 Git etiquette — so we don't overwrite each other

We already hit merge conflicts once. Avoid them:

- **`git pull` before you start** and again before you push.
- **Work on YOUR file** (your section / your reflection). Two people editing the same file = conflict.
- **Commit small and push often.** After finishing a section:
  ```
  git add .
  git commit -m "short description of what you did"
  git pull
  git push
  ```
- **Tell the group chat when you push** something big.
- If git shows a **conflict**, don't panic — paste the message to Claude Code and ask it to resolve it.

---

## 8. ❌ Don'ts

- Don't fabricate data, results, or sources.
- Don't rewrite a teammate's file without telling them.
- Don't submit anything you can't explain — each of us must defend our part in the 20-min presentation + 5-min Q&A.
- Don't forget the report needs a **"Use of AI tools"** section (how we used Claude). Be honest there — it's required and graded.

---

## 9. ✅ Definition of done (check the README table)

We're finished when every row in the README "Deliverables" table is ✅:
- Technical report (PDF) with "Use of AI tools" section
- One-page executive summary
- Slides (20-min talk)
- Code repo ✅ (already done)
- Supporting artifacts: eval set + script + results, prompts
- 5 individual reflections (one each)
- User manual + installation guide

When your part is done, tick it off and help whoever's behind. The two things that move the grade most are the **evaluation** and the **failure analysis** — if you finish early, help there.

**You've got this. Context first, one clean pass, push often. 🚀**
