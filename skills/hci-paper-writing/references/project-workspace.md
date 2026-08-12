# Project Workspace

Use a `.hci-paper/` directory when the work will span more than one pass, more
than one reviewer, or more than one session. It is a memory aid and audit trail,
not a source of truth. The manuscript and underlying research artifacts remain
authoritative.

## Initialize

When tool execution and a local project directory are available, run:

```bash
python3 scripts/project_workspace.py /path/to/paper --manuscript paper.tex
```

Use `--dry-run` before writing when the target directory is uncertain. The script
never overwrites an existing `.hci-paper/` directory and makes no network
requests.

## State Files

| File | Purpose |
|---|---|
| `context.md` | Stable thesis, venue, method tradition, privacy boundary, stage |
| `claims.csv` | Claims, evidence, locations, scope, and support status |
| `sources.csv` | Material owner/speaker, endorsement, permission, and claim support |
| `figures.csv` | Figure purpose, supported claim, source, reference, caption/alt text |
| `reviewer-comments.csv` | Normalized concerns before response drafting |
| `revision-ledger.csv` | Concrete changes and verification tests |
| `policy-snapshot.md` | Current rules with official URL and access date |
| `state.json` | Ordered lifecycle stage and evidence note for each transition |
| `handoff.md` | Minimal cold-resume context, blockers, and next action |
| `runs/` | Dated or named reports; never silently treated as current truth |

## State Discipline

1. Read `context.md` and the relevant ledger before a new pass.
2. Do not infer that a blank cell means `no`; it means `not recorded`.
3. Give every major claim, reviewer comment, and revision action a stable ID.
4. Mark an action `done` only after checking the specified manuscript location.
5. Preserve disagreements and unresolved evidence. Do not overwrite them with a
   cleaner narrative.
6. Refresh venue rules from official sources; a policy snapshot is a dated
   record, not permanent guidance.
7. Keep private drafts and reviews out of public version control unless the
   author has deliberately cleared them.

## Lifecycle Gates

Use these stages in order:

```text
framing -> study-ready -> evidence-frozen -> claim-locked -> drafted -> reviewed
-> response-ready -> submission-ready
```

- `study-ready`: RQs, contribution axes, method rationale, ethics, and data plan
  are reviewable before collection.
- `evidence-frozen`: the evidence version used for claims is identified; known
  exclusions and deviations are recorded.
- `claim-locked`: every central claim has evidence or a declared boundary.
- `drafted`: all load-bearing sections and primary figures exist.
- `reviewed`: method-matched and reader/venue passes are recorded.
- `response-ready`: reviewer concerns or internal risks have dispositions and
  feasible revision actions.
- `submission-ready`: deterministic integrity checks pass and current official
  venue requirements have been verified.

After checking the relevant gate, advance exactly one stage and record the
evidence for the decision:

```bash
python3 scripts/project_workspace.py /path/to/paper \
  --advance study-ready --note "RQs, ethics, and study plan reviewed"
```

Read status with `--status`. The script prevents skipped stages but cannot prove
research quality; the note and underlying artifacts remain the audit trail.

## Run Record

For a consequential pass, save a compact report under `runs/` containing:

```text
mode:
manuscript version or commit:
artifacts read:
artifacts missing:
privacy boundary:
findings added or changed:
remaining uncertainty:
```

If file writing is unavailable, return the same structure in the response and
tell the author it has not been persisted.
