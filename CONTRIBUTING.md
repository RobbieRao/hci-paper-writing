# Contributing

Contributions are welcome, especially from researchers who can strengthen the
project's methodological range without collapsing HCI into one review tradition.

## High-value contributions

- a synthetic manuscript that exposes a real failure mode;
- a method-lens correction grounded in public methodological guidance;
- a deterministic check with unit tests;
- a synthetic reviewer-panel or rebuttal case with stable concern IDs;
- a figure/text, terminology, or numeric-consistency fixture;
- a DOCX, anonymization, LaTeX dependency, or citation-integrity fixture;
- a source-integration case that distinguishes speaker, endorsement, evidence,
  and permission without exposing private material;
- a current official venue-policy source;
- an accessibility or privacy improvement;
- a clearer output contract or reproducible example.

## Benchmark contributions

The HCI Paper Coach Benchmark is in active development. Useful contributions
include:

- reproducible metadata or embedding pipelines for the most recent five years of
  CHI papers;
- expert-authored synthetic failure cases and annotation protocols;
- evaluation code for issue detection, false positives, evidence traceability,
  method fit, actionability, and calibration;
- an accepted or rejected submission journey when the contributor has the rights
  and permissions needed to share the manuscript, reviews, rebuttal, decision,
  and revisions;
- de-identification, licensing, consent, and dataset-governance expertise.

Benchmark contributors will receive priority invitations to the private beta,
subject to capacity and completion of applicable rights, privacy, and consent
checks. A contribution does not guarantee inclusion in a public dataset.

**Do not upload manuscript or review content to a public issue or pull request.**
Open an issue containing only a high-level description of the proposed
contribution so maintainers can arrange an appropriate review path.

Do not submit confidential manuscripts, private peer reviews, fabricated studies,
personal data, or copyrighted text you are not authorized to redistribute. An
author's permission to share a manuscript does not automatically establish the
right to publish reviewer-authored text; review and clear each artifact
separately.

## Development

```bash
git clone https://github.com/RobbieRao/hci-paper-writing.git
cd hci-paper-writing
make validate
make test
make guard
```

To exercise the safe workspace initializer without writing files:

```bash
python3 skills/hci-paper-writing/scripts/project_workspace.py . --dry-run
```

Keep the core `SKILL.md` concise. Put method-specific knowledge in a directly
linked file under `references/`. Scripts must use deterministic behavior where
possible and include tests. Avoid claims about acceptance-rate improvement unless
they are backed by a public, reproducible evaluation.

Before opening a pull request, run `make guard`. Keep unpublished manuscripts,
review text, credentials, private research infrastructure, and generated local
artifacts outside this repository. Contribute only public or clean-room
synthetic regression cases, never raw private outputs.

By contributing, you agree that your contribution is licensed under the MIT
License of this repository.

If a contribution adapts an external project, name the source and license in the
pull request. Do not copy from noncommercial or unlicensed projects. Compatible
open-source inspiration still needs attribution when its expression or code is
reused.
