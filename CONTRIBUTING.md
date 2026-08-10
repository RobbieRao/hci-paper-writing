# Contributing

Contributions are welcome, especially from researchers who can strengthen the
project's methodological range without collapsing HCI into one review tradition.

## High-value contributions

- a synthetic manuscript that exposes a real failure mode;
- a method-lens correction grounded in public methodological guidance;
- a deterministic check with unit tests;
- a current official venue-policy source;
- an accessibility or privacy improvement;
- a clearer output contract or reproducible example.

Do not submit confidential manuscripts, private peer reviews, fabricated studies,
or copyrighted paper text you are not authorized to redistribute.

## Development

```bash
git clone https://github.com/RobbieRao/hci-paper-writing.git
cd hci-paper-writing
make validate
make test
```

Keep the core `SKILL.md` concise. Put method-specific knowledge in a directly
linked file under `references/`. Scripts must use deterministic behavior where
possible and include tests. Avoid claims about acceptance-rate improvement unless
they are backed by a public, reproducible evaluation.

By contributing, you agree that your contribution is licensed under the MIT
License of this repository.

