# HCI Paper Workflows

## Diagnose

1. Reconstruct the paper in one sentence: problem, intervention or inquiry,
   evidence, and HCI value.
2. Record contribution form, research area, research tradition, and venue/track
   separately; assign a primary and optional secondary contribution form.
3. Extract explicit and implicit claims.
4. Build the claim-evidence matrix.
5. Test title-contribution-evidence-discussion alignment.
6. Report only the three highest-leverage risks before smaller issues.

Use this output:

```markdown
## Paper Thesis
...

## Contribution Diagnosis
- Primary:
- Secondary:
- Research area:
- Research tradition:
- Why:

## Claim-Evidence Matrix
| Claim | Evidence | Status | Repair |
|---|---|---|---|

## Venue Assumptions
...

## Top Risks
1. [severity] Risk — manuscript evidence — repair

## Next Action
...
```

## Red-team

Run the three lenses independently before merging findings. A criticism must
quote or precisely locate manuscript evidence. Do not reward verbosity or punish
non-experimental traditions for lacking experimental conventions.

Severity:

- `Critical`: threatens the central contribution or makes the work unreviewable.
- `Major`: materially weakens confidence, significance, or interpretability.
- `Minor`: local clarity, completeness, or presentation problem.

Use this output:

```markdown
## Overall Read
- Research strength:
- Venue/track fit:

## Contribution Lens
...

## Method Lens
...

## Reader/Venue Lens
...

## Consolidated Risks
| Severity | Risk | Evidence | Why it matters | Fix |
|---|---|---|---|---|

## Champion / Killer
- Champion sentence:
- Killer concern:
```

## Revision

Convert diagnosis, external reviews, or a red-team report into a revision ledger.

1. Resolve contradictory reviewer requests against the paper's actual
   contribution and method tradition.
2. Separate changes requiring new evidence from changes solvable by reframing.
3. Protect accurate limitations; do not hide weaknesses to game a score.
4. Define a verification test for every revision item.
5. Re-run the claim-evidence matrix after major edits.

## Planning

Before drafting prose, produce:

- working title;
- one-sentence contribution;
- RQs;
- primary contribution type;
- target audience and venue assumptions;
- claim-evidence matrix;
- section-to-claim map;
- fatal risks and evidence still needed.
