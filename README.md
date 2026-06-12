# NLP Group Project

Repository for the **NLP course group assignment**. This is the main project of the course: a substantial piece of NLP work demonstrating technical competence, critical thinking, and original analysis, culminating in a **20-minute in-class presentation + 5 minutes of Q&A**.

> Core expectation across all options: produce **evidence and analysis that are genuinely our own**, grounded in primary work carried out by the team.

**Team:** Antonio · Martí · Bojana · Smaragda · Jo

---

## 1. Project options (choose one)

All three are equivalent in expected effort and weight. **The topic must be approved by the professor before starting.**

| Option | What we build | Best fit for |
|---|---|---|
| **1. Application Development** | A functioning NLP-powered application with a custom evaluation harness and real user feedback | Teams that want to ship something concrete |
| **2. System Audit** | A structured audit of a deployed NLP system, with a custom probe set and a failure taxonomy | Teams that want to deeply understand existing systems |
| **3. Replication & Extension** | Reproduction of a recent paper plus our own extension experiment | Teams that want a research-flavored project |

When choosing a topic, consider: **relevance** (current trends, real-world applications), **feasibility** (think big, start small), **originality** (not a replica of a lab exercise), and **team commitment** (everyone invested).

### Option 1 — Application Development

Build a working NLP application for a real-world use case. A clear proof of concept is sufficient (no need for production-grade); unrealized features are presented as future directions.

Required components:
- **Justification of need** — why the app is needed, where it applies, what it brings that existing approaches lack.
- **Field review** — concise but substantive review of the industry: trends, challenges, major players, existing solutions.
- **Functional system** — working demo/POC exhibiting the core functionalities.
- **Custom evaluation** — our own test set of **30–50 examples** with expected outputs, reporting quantitative results (accuracy, F1, BLEU, etc.). Off-the-shelf benchmarks alone are not sufficient.
- **Failure mode analysis** — **5–10 documented failure cases** with hypotheses about why.
- **Reproducible repository** — clean code, clear README, requirements file.

*Advice: aspire to a substantial problem but commit to a modest, demonstrable POC. Focus is NLP technical competence, not marketability.*

### Option 2 — System Audit

Pick a real, deployed NLP system (chatbot, translation service, content moderator, voice assistant, search, recommender) and audit its behavior. The output should let someone considering deploying that system make an informed decision. A purely descriptive review does not meet the bar — we must build substantial new evidence.

Required components:
- **System characterization** — what it does, features, where it sits among similar technologies.
- **Custom probe set** — **~150–300 items** structured around hypotheses about likely weaknesses (edge cases, bias, robustness, compositionality, multilingual handling…), with documented design rationale.
- **Empirical findings** — run probes, document outputs with evidence (screenshots, transcripts, logs), quantify failure rates by category.
- **Failure taxonomy** — coherent taxonomy with definitions and representative examples.
- **Comparison** — at least **one comparable alternative system** evaluated on the same probe set.
- **Technical context** — underlying technologies and methods, connected to academic literature.
- **Mitigations and future directions** — specific proposals based on findings + literature.

*Advice: choose a system we can probe extensively — open-weight local models, free public APIs, or generous trial tiers. Rate limits and paywalls become bottlenecks.*

### Option 3 — Replication & Extension Study

Pick a recent NLP paper (last ~3 years, reputable venue, public code) and reproduce + extend it.

Required components:
- **Paper selection** — justify the choice: why interesting, what it claims, how influential.
- **Replication** — reproduce the main result; document deviations, undocumented assumptions, implementation issues; compare our numbers vs. published ones.
- **Extension experiment** — one **substantive** extension beyond the original (different language, domain, model size, eval set, or a new ablation). A one-line change is not sufficient.
- **Mini-survey** — focused literature survey anchored in the paper: what came before and after.
- **Critical assessment** — what holds up, what is brittle, what remains open.
- **Open question** — a concrete research direction grounded in our empirical observations.

*Advice: choose a paper whose code actually runs — check the GitHub issues before committing. Code availability matters more than prestige.*

---

## 2. Deliverables (submitted via the course platform)

- [ ] **Technical report (PDF)** — length appropriate to the project.
- [ ] **One-page executive summary** — written for a non-technical reader.
- [ ] **Presentation slides** — used in the in-class presentation.
- [ ] **Code repository (link)** — this repo. Option 1: full system · Option 2: probe set + analysis scripts · Option 3: replication + extension code.
- [ ] **Supporting artifacts** — datasets, probe sets, prompts, anything referenced in the report.
- [ ] **Individual reflections** — ~1 page per team member: specific contributions and what was learned.
- [ ] **Option 1 only:** user manual + installation/execution guide (and a hosting link if the app is online).

The report must include a short **“Use of AI tools”** section describing how LLMs were used.

---

## 3. Evaluation criteria

1. **Technical execution and rigor** — correct methodology, sound experimental design, quality of code and artifacts.
2. **Empirical evidence and depth of analysis** — conclusions grounded in our own data and measurements, not restated from external sources.
3. **Originality and critical thinking** — going beyond the obvious, surfacing non-trivial insights.
4. **Communication** — clarity and structure of report and presentation.
5. **Reproducibility and quality of deliverables** — a reader should be able to follow and reproduce the work.

Individual grades may differ from the team grade if contributions are clearly uneven.

---

## 4. Use of LLMs / AI assistance

LLMs **may and should** be used: brainstorming, debugging, drafting prose, literature exploration, boilerplate code, paper summaries. However:

- Substantive intellectual decisions (problem framing, methodology, test set design, label definitions, error interpretation, conclusions) **must come from the team**.
- The final report must include the **“Use of AI tools”** section.
- During Q&A, **every team member must be able to defend any choice** in the work.

---

## 5. Recommended workflow

| Phase | Focus |
|---|---|
| **Early** | Finalize topic and scope (get professor approval), agree on roles, initial scan of literature/system landscape |
| **Middle** | Core empirical work: build / audit / replicate |
| **Late** | Analysis, report writing, slides, internal rehearsal of the presentation |

Pace the work and surface problems early.

---

## 6. Useful research repositories

- [Google Scholar](https://scholar.google.es/) — broad academic search
- [arXiv](https://arxiv.org/) — open-access pre-prints (NLP/ML)
- [ACL Anthology](https://aclanthology.org/) — canonical NLP repository (focus on 2015+)
- [IEEE Xplore](https://ieeexplore.ieee.org/) — engineering and CS literature
- [Semantic Scholar](https://www.semanticscholar.org/) — AI-powered scientific search
- [Papers with Code](https://paperswithcode.com/) — papers + implementations (especially for Option 3)

---

*“The strongest projects are not necessarily the most technically ambitious. They are the ones whose authors can articulate, with concrete observations from their own work, what they learned and why it matters.”*
