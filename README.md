<p align="center">
  <img src="assets/hci-paper-coach-hero.png" alt="HCI Paper Coach — Make the contribution undeniable" width="100%">
</p>

<p align="center">
  <a href="README.md">English</a> · <a href="README.zh-CN.md">简体中文</a>
</p>

<p align="center">
  <a href="https://github.com/RobbieRao/hci-paper-writing/actions/workflows/ci.yml"><img src="https://github.com/RobbieRao/hci-paper-writing/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-34d399.svg" alt="MIT License"></a>
  <a href="skills/hci-paper-writing/SKILL.md"><img src="https://img.shields.io/badge/Agent%20Skill-open%20standard-8b5cf6.svg" alt="Agent Skill"></a>
  <img src="https://img.shields.io/badge/preflight-local%20%26%20read--only-22d3ee.svg" alt="Local and read-only preflight">
</p>

<p align="center">
  <strong>Stop polishing sentences while the argument is still broken.</strong><br>
  An open-source agent skill that diagnoses HCI contributions, traces claims to
  evidence, and red-teams manuscripts before reviewers do.
</p>

---

Most academic writing tools optimize prose. **HCI Paper Coach audits the thing
reviewers actually have to believe:** that the paper makes a clear HCI
contribution and supports it with the right kind of evidence.

It is built for authors working toward **CHI, CSCW, DIS, UIST, TOCHI, and
adjacent HCI venues**. It understands that a qualitative inquiry, an interaction
technique, a field deployment, and a research-through-design paper should not be
judged with one generic rubric.

> [!IMPORTANT]
> This is an author-side reasoning and revision tool—not an acceptance predictor,
> citation generator, or substitute for research judgment.

## Three workflows that earn their place in your repo

| Workflow | What it does | What you get |
|---|---|---|
| **`hci-diagnose`** | Reconstructs the paper's thesis, contribution type, and evidence chain | Contribution diagnosis, claim-evidence matrix, top risks |
| **`hci-red-team`** | Reviews through contribution, method, and reader/venue lenses | Consolidated major risks, champion sentence, killer concern |
| **`hci-revision`** | Turns reviews or diagnosis into ordered work | Revision ledger with evidence needs and verification tests |

Also included: planning, section revision, study reporting, interaction-figure
guidance, LLM-system reporting, privacy guardrails, and live venue-policy checks.

## 30-second install

### Codex and Agent Skills-compatible tools

```bash
git clone https://github.com/RobbieRao/hci-paper-writing.git
cd hci-paper-writing
./install.sh codex
```

### Claude Code

```bash
git clone https://github.com/RobbieRao/hci-paper-writing.git
cd hci-paper-writing
./install.sh claude
```

The installer creates a symlink so `git pull` updates the installed skill. It
refuses to overwrite an existing installation.

Then ask your agent:

```text
Use $hci-paper-writing in hci-diagnose mode on my abstract and contributions.
```

Or:

```text
Use $hci-paper-writing to red-team this draft for CHI 2027.
Separate contribution, method, and reader/venue risks.
```

## Local manuscript preflight

Before semantic review, run a deterministic scan:

```bash
python3 skills/hci-paper-writing/scripts/manuscript_audit.py paper.tex
```

It detects:

- paper structure and missing common headings;
- explicit RQ and contribution markers;
- strong constructs such as trust, understanding, agency, and usefulness;
- common study, ethics, and limitations markers;
- unfinished text such as `TODO`, `TBD`, and `FIXME`.

The scanner is Python-standard-library only, read-only, and makes **zero network
requests**. It produces review leads—not fake quality scores.

<details>
<summary><strong>See an example preflight</strong></summary>

```text
# Local Manuscript Preflight

- File: synthetic-paper.md
- Sections detected: 6
- Privacy: local read-only scan; no network requests

## Contribution Candidates
- We introduce TraceLens and use it as a research artifact...

## Review Leads
- Strong-claim term detected: usefulness
- Verify that each construct is operationalized or carefully bounded
```

Try it on the intentionally synthetic [example paper](examples/synthetic-paper.md).
</details>

## Why this is different

### Contribution first, prose second

The skill refuses to treat “we conducted a user study” as a contribution. It
asks what the study reveals, validates, enables, or changes for HCI.

### Method-aware, not method-dogmatic

It selects among qualitative, quantitative, design-research, systems,
field/CSCW, and mixed-method lenses. It does not demand an experiment merely
because an experiment is familiar.

### Evidence before confidence

Every major criticism must point to manuscript evidence, explain why it matters,
and propose a minimum credible repair. Every strong author claim must map to
evidence, a citation, or narrower wording.

### Current policy, not cached folklore

Venue rules change. The skill requires agents to verify deadlines, length,
anonymization, accessibility, ethics, AI-use disclosure, and supplementary
material rules from current official sources at run time.

### Privacy that is stated, not implied

The local scanner never sends a manuscript anywhere. The skill also reminds
users that the surrounding AI platform—not this repository—controls model-side
data handling. Never upload a confidential paper you are reviewing without
explicit authorization and policy support.

## What's inside

```text
skills/hci-paper-writing/
├── SKILL.md                         # Router, guardrails, output contracts
├── agents/openai.yaml               # Discoverable UI metadata
├── assets/                          # Intake and revision templates
├── scripts/
│   ├── manuscript_audit.py          # Local deterministic preflight
│   └── validate_skill.py            # Zero-dependency package validator
└── references/
    ├── contribution-types.md
    ├── workflows.md
    ├── method-lenses.md
    ├── study-evidence.md
    ├── section-patterns.md
    ├── reviewer-checklist.md
    ├── llm-systems.md
    └── policy-and-privacy.md
```

## Design principles

1. **Author retains judgment.** The agent scaffolds critique; it does not decide
   what the research should claim.
2. **No fabricated authority.** No invented citations, participants, policies,
   statistics, or reviewer consensus.
3. **No acceptance theater.** Research strength and venue fit are separated; no
   numerical acceptance probability is invented.
4. **Epistemic pluralism.** Rigor is evaluated within the paper's research
   tradition.
5. **Actionable or omitted.** Feedback needs evidence, severity, repair, and a
   verification step.

## Roadmap

- [x] Contribution diagnosis and claim-evidence workflow
- [x] Three-lens HCI red-team
- [x] Local Markdown/LaTeX/text preflight
- [x] Qualitative, quantitative, design, systems, field, and mixed-method lenses
- [x] Privacy and live-policy guardrails
- [ ] Public benchmark using synthetic and author-consented manuscripts
- [ ] Structured LaTeX cross-section consistency checks
- [ ] Subcommunity packs for CSCW, DIS, UIST, accessibility, and health HCI
- [ ] Bilingual Chinese/English report templates
- [ ] Reviewer-feedback comparison and revision tracking

## Contributing

The fastest way to improve this project is to contribute a **method-specific
failure case**, a **synthetic test manuscript**, or a **public official policy
source**. See [CONTRIBUTING.md](CONTRIBUTING.md).

If this saves you one avoidable review cycle, consider starring the repo. It
helps other HCI researchers find a tool that critiques the argument—not just the
grammar.

## Responsible use

- Use the project for formative author feedback, not automated peer-review
  gatekeeping.
- Verify citations and venue policies yourself.
- Follow your venue's AI-use disclosure policy.
- Do not submit confidential manuscripts belonging to others to third-party
  models.
- The project is not affiliated with or endorsed by ACM, SIGCHI, CHI, CSCW, DIS,
  UIST, or any other venue.

## License and provenance

MIT licensed. See [LICENSE](LICENSE) and [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

The project is independently authored and informed by public HCI submission
guidance and open academic-writing workflows. No third-party source code is
vendored.
