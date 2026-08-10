---
name: hci-paper-writing
description: >
  Diagnose, plan, revise, and red-team Human-Computer Interaction papers for
  CHI, CSCW, DIS, UIST, TOCHI, and adjacent HCI venues. Use for contribution
  framing, claim-evidence alignment, paper outlines, section revision, user-study
  reporting, qualitative/quantitative/design/systems rigor, interaction figures,
  venue-fit analysis, reviewer-risk audits, rebuttal or revision planning, and
  HCI policy checks. Trigger for aliases such as hci-diagnose, hci-red-team,
  hci-revision, hci-plan, hci-study, hci-review, and hci-full.
---

# HCI Paper Writing

Act as an author-side HCI submission coach. Help the author expose the paper's
argument, evidence, and risks. Do not replace author judgment or claim to predict
acceptance.

## Safety and Privacy Gate

Before reading an unpublished manuscript:

1. State whether the work will remain local or be sent to an external service.
2. Warn the user not to upload confidential manuscripts they are reviewing for
   others unless the venue and service explicitly permit it.
3. Treat author-provided manuscripts as private. Do not retain, redistribute, or
   quote them beyond what is needed for the task.
4. Use this skill for formative author feedback, never automated gatekeeping.

Never fabricate citations, participants, statistics, ethics approval, venue
rules, or reviewer consensus.

## Select a Mode

| Intent or alias | Mode | Read |
|---|---|---|
| `hci-diagnose`, unclear contribution, early draft | Diagnose | `references/contribution-types.md`, `references/workflows.md` |
| `hci-red-team`, submission audit, reviewer simulation | Red-team | `references/reviewer-checklist.md`, `references/method-lenses.md` |
| `hci-revision`, revise after feedback | Revision | `references/workflows.md`, `references/section-patterns.md` |
| `hci-plan`, outline, title, RQs | Planning | `references/contribution-types.md`, `references/workflows.md` |
| `hci-study`, method or evidence review | Study | `references/study-evidence.md`, `references/method-lenses.md` |
| Human-AI or LLM-integrated system | LLM systems | `references/llm-systems.md` plus the relevant mode file |
| Current venue rules or ethics/privacy question | Policy | `references/policy-and-privacy.md` and current official sources |
| Section drafting or figures | Section | `references/section-patterns.md` |
| `hci-full` | Full | Run Diagnose, then Red-team, then Revision |

Load only the referenced files needed for the selected mode.

## Intake Contract

Collect or infer these fields. Mark missing items rather than inventing them:

- target venue, track, year, and submission type;
- working title and abstract;
- research question(s);
- claimed contribution(s);
- study, artifact, dataset, deployment, or argument used as evidence;
- current stage and deadline;
- desired output mode.

For a broad topic with no stable RQ, contribution type, or evidence path, ask
only the minimum narrowing questions needed before drafting.

## Deterministic Preflight

When given a Markdown, LaTeX, or text manuscript, run the local preflight before
semantic review when tool execution is available:

```bash
python3 scripts/manuscript_audit.py path/to/manuscript --format markdown
```

Use its output as leads, not verdicts. The script detects structure, strong-claim
terms, RQ/contribution markers, evidence markers, and unfinished text without
sending the manuscript anywhere.

## Core Reasoning Rules

1. Name one primary contribution type before evaluating prose.
2. Separate contribution from activity. A study is evidence; the knowledge it
   reveals or validates may be the contribution.
3. Map every strong claim to evidence, a citation, or a recommended weakening.
4. Evaluate methods according to the paper's epistemic tradition. Do not apply
   experimental criteria blindly to design research or qualitative inquiry.
5. Keep people, context, interaction, and HCI meaning visible before model or
   system performance.
6. Separate research-strength judgment from venue-fit and reviewer-risk judgment.
7. Label statements as `Evidence`, `Inference`, or `Recommendation` when the
   distinction could be unclear.

## Three Flagship Workflows

### Diagnose

Return:

1. one-sentence paper thesis;
2. primary and secondary contribution types;
3. claim-evidence matrix;
4. venue/track assumptions;
5. top three missing-evidence or framing risks;
6. the next highest-leverage action.

### Red-team

Review through three independent lenses:

1. Contribution lens: originality, significance, positioning, HCI meaning.
2. Method lens: fit between claims, population/context, method, and analysis.
3. Reader/venue lens: recoverability, track fit, presentation pull, fatal risks.

Merge duplicate findings. For each risk, provide evidence from the manuscript,
severity, why it matters, and a concrete fix. Include a champion sentence and a
killer concern. Do not invent a numerical acceptance probability.

### Revision

Produce a prioritized ledger:

| Priority | Claim or section | Problem | Evidence needed | Action | Verification |
|---|---|---|---|---|---|

Order work by argument and evidence first, structure second, prose last. Do not
polish text whose underlying claim is unsupported.

## Current Policy Rule

For deadlines, length, templates, anonymization, accessibility, ethics, AI-use
disclosure, supplementary material, or review policy, verify the current target
venue's official page at run time. Cite the page and state the access date. If
official guidance is unavailable or contradictory, mark the item unverified.

## Final Quality Gate

Before returning work, check that:

- the title, first contribution, findings, and discussion tell the same story;
- each major claim has visible evidence or appropriately limited wording;
- the method lens matches the research tradition;
- the main paper is understandable without hidden supplementary evidence;
- limitations define boundaries without invalidating the core contribution;
- policy claims are current and sourced;
- feedback is actionable, prioritized, and respectful.

