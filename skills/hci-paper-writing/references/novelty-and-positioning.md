# Novelty and Positioning

Use for `hci-positioning`, titles, introductions, contribution lists, related
work, and novelty challenges. Positioning is an evidence-backed comparison, not
a search for impressive adjectives.

## The Four-Part Argument

Build the argument in this order:

1. **Importance**: name the people, interaction, practice, setting, or
   sociotechnical consequence that makes the question worth answering.
2. **Unresolved question**: state what the closest work does not yet explain,
   compare, enable, or test. Cite the comparison.
3. **Delta**: state exactly what this paper adds and at what scope.
4. **Evidence**: name the study, artifact, analysis, corpus, or argument that can
   establish that delta.

A real gap can still be unimportant. Establish the HCI stake before claiming
novelty.

## Contribution Nouns Are Review Contracts

The contribution noun selects the questions a skeptical reader will ask:

| Noun | Contract it creates |
|---|---|
| empirical finding or account | credible sampling, analysis, context, and bounded inference |
| system, artifact, or technique | nontrivial interaction capability, design rationale, and appropriate evaluation |
| method | reproducible steps, need relative to alternatives, validation, and limits |
| framework, model, or theory | defined constructs, explanatory or generative value, grounding, and scope |
| dataset or benchmark | provenance, governance, documentation, validity, reuse, and bias analysis |
| design knowledge | traceable design process, alternatives, reflection, and transferable insight |

Choose the smallest noun the evidence can defend. An artifact used to run a
study need not be the primary contribution. A framework claim should not be used
as a flattering synonym for a diagram or checklist.

## Defensible Novelty Shapes

- a consequential question not yet answered;
- a direct comparison not yet made;
- a boundary condition, population, setting, or failure mode not yet tested;
- a new interaction capability whose mechanism and value are demonstrated;
- a method that changes what HCI researchers or designers can do;
- a synthesis or conceptualization that reorganizes evidence and supports new
  analysis or design;
- a replication, negative result, or counterexample that changes confidence in
  prior knowledge.

Weak shapes include `first to combine X, Y, and Z`, `no one has studied this`
based on a shallow search, and `novel framework` without a framework-level
evaluation. Translate a component combination into the HCI question or
capability that the combination makes answerable, then evaluate that claim.

## Closest-Work Table

Compare the strongest neighbors rather than a convenient set of distant papers:

| Work | Problem and people/context | Contribution | Method/evidence | What overlaps | Exact remaining delta | Source status |
|---|---|---|---|---|---|---|

Mark each row `full text inspected`, `metadata only`, or `unverified`. Do not
claim a delta from an abstract, snippet, or embedding neighbor alone.

## Related Work as an Argument

Organize by research conversation or mechanism. Each subsection should:

1. synthesize what the line of work establishes;
2. surface a supported tension, boundary, or open question;
3. state how that point connects to the present paper.

Give the closest and most threatening work the most precise treatment. Hiding it
weakens the novelty argument more than acknowledging overlap.

## Non-Defensive Register

State scope and limitations directly. Remove prose that argues with an imagined
reviewer, advertises the author's rigor, or denies an accusation nobody made.

Prefer:

```text
The study examines short-term use by novice participants in a laboratory task;
longitudinal adoption remains outside its evidence boundary.
```

Avoid adding `deliberately`, `carefully`, `to be clear`, `we do not claim`, or
`X, not Y` unless the contrast is genuinely necessary to interpret the result.
Concede a real limitation once, then carry its boundary consistently into the
abstract, findings, and discussion.

## Output Contract

Return the importance statement, unresolved question, primary contribution noun,
smallest defensible delta, closest-work table, evidence path, and any wording that
must be weakened or verified.
