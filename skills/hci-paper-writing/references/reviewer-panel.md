# HCI Reviewer Panel

Use this protocol for `hci-panel`, high-stakes red-teaming, or a final review.
The goal is to expose instability across justified readings, not manufacture
consensus or imitate a program committee decision.

## Independence Boundary

When the platform and user permit independent agents, give each reviewer only
the shared intake and manuscript, collect their reports, then synthesize. Do not
show one reviewer's conclusion to another before collection.

When independent execution is unavailable, run the lenses sequentially and say
that the passes are role-separated but not statistically independent. Never
describe sequential simulation as multiple human reviewers.

## Core Panel

1. **Contribution reviewer**: thesis, originality claim, HCI knowledge gain,
   significance, and closest-work positioning.
2. **Method-tradition reviewer**: fit among claims, context, population,
   artifact, method, analysis, and epistemic tradition.
3. **Reader and venue reviewer**: contribution recoverability, narrative,
   figures, track fit, and presentation risks.

Add an **ethics, accessibility, and deployment reviewer** when the work involves
human subjects, sensitive data, disability, vulnerable groups, automated
decisions, or real-world deployment. Add a domain expert only when the domain is
material to validity.

Do not add generic reviewers whose checklists do not fit the paper. For example,
do not demand ablations from an interpretivist field study or saturation from a
controlled interaction-technique experiment.

## Per-Reviewer Contract

```text
reviewer_id:
lens and relevant expertise:
artifacts read:
one-sentence interpretation of the paper:
strongest defensible contribution:
major concerns:
  - concern_id:
    manuscript evidence:
    consequence:
    severity: blocking / major / moderate / minor
    repair or decision-changing evidence:
missing information:
champion sentence:
killer concern:
confidence boundary:
```

Every concern must cite manuscript evidence or say `insufficient evidence` and
name what is missing. Do not output an acceptance probability. If a venue uses a
score, reproduce it only when the user asks and the current official review form
has been verified.

## Meta-Review

Synthesize by concern, not by averaging reviewer sentiment:

| Concern | Reviewers | Shared evidence | Disagreement | Severity | Repair | Verification |
|---|---|---|---|---|---|---|

Then report:

- stable strengths that survived the skeptical lenses;
- stable risks found by more than one lens;
- lens-specific risks that should not be averaged away;
- disagreements caused by different readings or standards;
- missing evidence that prevents resolution;
- the next three highest-leverage actions.

Agreement is evidence that a reading is stable under this panel. It is not proof
that the claim is true or that reviewers at the venue will agree.

## Machine-Readable Shape

When the user requests JSON, return an object with `schema_version`, `paper_id`,
`privacy_boundary`, `reviewers`, `concerns`, `agreements`, `disagreements`,
`missing_evidence`, and `next_actions`. Keep stable concern IDs so later revisions
can be compared without fuzzy matching.
