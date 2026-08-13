# Evidence and Corpus Grounding

Use this protocol when the task asks what recent CHI papers do, requests nearby
work, compares a manuscript with a paper corpus, or evaluates this skill.

## Source hierarchy

Prefer sources in this order:

1. the user's manuscript and explicitly supplied artifacts;
2. current official venue policy pages for rules;
3. publisher records and openly accessible paper versions for paper claims;
4. bibliographic indexes for discovery and metadata;
5. authorized, rights-cleared review and rebuttal records;
6. secondary summaries only when primary material is unavailable.

Never imply that this skill was trained on, evaluated on, or has access to a
private CHI corpus unless the current runtime provides verifiable evidence.

## Retrieval protocol

1. Define the comparison target: contribution, construct, method, population,
   context, system, or venue practice.
2. Record the corpus name, covered years, indexed fields, query, filters, result
   count, and access date.
3. Search separately for the target's problem, claimed contribution, method,
   findings, and limitations. Include same-problem/different-method and
   same-method/different-problem contrasts.
4. Repeat the search with meaning-preserving wording variants, including the
   author's language and a bilingual variant when relevant. Record material
   changes in the candidate set as a coverage limitation.
5. Inspect the source text before describing a candidate. Do not infer a paper's
   contribution or findings from search proximity alone.
6. Cite each factual source claim. Separate exact source content from the
   analyst's synthesis.
7. State missing years, inaccessible text, selection effects, and other coverage
   limitations.

A whole-document ranking is not a substitute for these facet-specific
comparisons. Give special attention to candidates that appear under only one
facet or wording; disagreement is an inspection lead, not noise to hide.

Use this compact provenance block:

```markdown
## Corpus Provenance
- Corpus and version:
- Coverage:
- Indexed fields:
- Query and filters:
- Candidates inspected:
- Access date:
- Known gaps:
```

## Comparison rules

- Treat accepted papers as positive examples of published practice, not causal
  evidence of acceptance criteria.
- Do not treat frequency as a quality rule. A rare method or contribution can be
  rigorous and valuable.
- Do not equate semantic similarity with novelty overlap. Verify shared claims,
  mechanisms, evidence, and scope directly.
- Compare within relevant subcommunities and epistemic traditions before making
  cross-CHI generalizations.
- When review text is available, distinguish the reviewer's opinion from the
  eventual decision and from the analyst's judgment.
- Never produce an acceptance probability from corpus neighbors or review
  language.

## Evaluation protocol

Evaluate the skill on observable tasks rather than a single opaque score:

| Dimension | Question |
|---|---|
| Issue detection | Does it recover expert-annotated major risks? |
| False positives | Does it invent problems unsupported by the manuscript? |
| Evidence traceability | Can each criticism be located in manuscript or source evidence? |
| Method fit | Does it use the appropriate epistemic and methodological lens? |
| Actionability | Is the proposed repair specific and feasible? |
| Prioritization | Are contribution-threatening issues ranked before prose polish? |
| Policy accuracy | Are current rules verified from official sources? |
| Calibration | Does it express uncertainty and corpus limitations honestly? |
| Retrieval stability | Do meaning-preserving and bilingual queries recover a stable threat set? |
| Threatening-neighbor recall | Does it surface the strongest same-problem, same-method, and same-contribution comparators? |
| Similarity discipline | Does it avoid converting semantic proximity into novelty or quality judgment? |

Report per-dimension results, annotator instructions, disagreements, data splits,
and known limitations. Keep synthetic, public-paper, and author-consented data as
separate strata so their results cannot be silently pooled.

## Public discovery starting points

- CHI proceedings and author pages: use current official ACM/SIGCHI sources, such
  as https://chi2026.acm.org/authors/papers/ and
  https://doi.org/10.1145/3772318.
- CHI review-process aggregates: use for process context, not review-text labels;
  see https://chi2023.acm.org/2023/01/05/investigating-the-quality-of-reviews-reviewers-and-their-expertise-for-chi2023/.
- DBLP CHI index: https://dblp.org/db/conf/chi/index
- Semantic Scholar Open Data Platform and OpenAlex: use for metadata discovery,
  subject to current terms and coverage; see https://arxiv.org/abs/2301.10140 and
  https://docs.openalex.org/.
- PeerRead and OpenReview-derived datasets: use only as explicitly labeled
  out-of-domain auxiliary evaluation data, not as CHI ground truth; see
  https://arxiv.org/abs/1804.09635 and
  https://huggingface.co/datasets/Samarth0710/reviewarena.

Verify current terms, licenses, and access rules before downloading, indexing,
redistributing, or releasing any content.
