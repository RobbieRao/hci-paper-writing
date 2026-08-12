# Source Integration

Use for `hci-integrate` when turning notes, meeting transcripts, chats, emails,
review comments, lab documents, or other user-provided material into manuscript
content. The central question is not where text can be pasted. It is who owns the
idea, whether the author endorses it, what evidence supports it, and what the
paper is allowed to claim.

## Classify Every Material

| Material | Default treatment |
|---|---|
| author's existing manuscript or notes | author intent, but still check evidence and version |
| coauthor or lab discussion | candidate idea until author endorsement is clear |
| reviewer comment | external concern, not a fact about the paper |
| participant data or quote | research evidence governed by consent, ethics, and de-identification |
| published source | verify source and claim support before citation |
| AI-generated draft or summary | unverified working material, never evidence |

## Endorsement and Provenance Pass

Before editing, record:

| Source ID | Speaker/owner | Proposed claim | Endorsed by author? | Evidence status | Permission/privacy | Intended location |
|---|---|---|---|---|---|---|

Use only material the user explicitly requested or clearly endorsed. Treat
brainstorming, questions, objections, rejected ideas, and another person's
proposal as context unless the author adopts them. If endorsement is ambiguous,
omit the claim from the manuscript and flag the decision.

Do not turn a reviewer request into a new result, a participant quote into a
general prevalence claim, or a meeting hypothesis into a finding.

## Integration Workflow

1. Read the complete supplied material within the authorized privacy boundary.
2. Map claims to speaker, endorsement, evidence, and permission.
3. Select the manuscript location by argumentative function, not keyword match.
4. Draft in the paper's established voice, terminology, and epistemic strength.
5. Preserve dissent or uncertainty when it matters; do not manufacture a cleaner
   consensus than the source contains.
6. Update `.hci-paper/sources.csv` and the relevant claim or revision ledger.
7. Recheck adjacent paragraphs, abstract, contributions, figures, discussion,
   and limitations for drift.
8. For substantive LaTeX edits, compile with the project's documented command
   when the toolchain is available. Report success or the first unresolved error.

## Citation Boundary

Conversation and internal notes can establish author intent but usually cannot
substitute for scholarly evidence. Search and verify a citable primary source
when the integrated claim needs literature support. Record whether the full
source, abstract, or metadata was inspected; do not create BibTeX from memory.

## Privacy Boundary

Keep unpublished materials local unless the user has authorized an external
service and its data handling is acceptable. Do not place private transcripts,
review text, participant data, or the `.hci-paper/` workspace in a public issue
or repository without explicit rights and de-identification checks.

## Return

Report what was integrated, what was omitted, ambiguous endorsement decisions,
new or changed claims, evidence still required, manuscript locations touched,
ledger updates, and compile or audit status.
