#!/usr/bin/env python3
"""Create a local, versionable HCI paper state directory without overwriting files."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path


FILES = {
    "context.md": """# Paper Context

- Working title:
- Target venue, year, track:
- Submission type:
- Deadline:
- Primary contribution form:
- Secondary contribution form (optional):
- Research area:
- Research question(s):
- Research tradition:
- Manuscript path:
- Privacy boundary:
- Current stage:

## One-sentence thesis


## Evidence currently available


## Known boundaries and unresolved decisions

""",
    "claims.csv": "claim_id,claim,contribution_type,evidence,source_location,status,scope_note\n",
    "sources.csv": "source_id,source_type,owner_or_speaker,endorsement_status,claim_supported,location,permission_or_license,verification_status\n",
    "figures.csv": "figure_id,purpose,claim_supported,evidence_shown,source_file,text_reference,caption_alt_text,status\n",
    "reviewer-comments.csv": "comment_id,source,concern_type,concern,evidence_basis,severity,response_strategy,status\n",
    "revision-ledger.csv": "item_id,comment_id,claim_or_section,problem,evidence_needed,action,location,verification,status\n",
    "policy-snapshot.md": """# Venue Policy Snapshot

Record only rules checked against current official sources.

| Item | Verified rule | Official URL | Access date | Status |
|---|---|---|---|---|
| Deadline | | | | unverified |
| Length and format | | | | unverified |
| Anonymization | | | | unverified |
| Accessibility | | | | unverified |
| Ethics and AI disclosure | | | | unverified |
| Supplementary material | | | | unverified |
""",
    "handoff.md": """# Cold-Resume Handoff

- Current manuscript version or commit:
- Current stage:
- Last completed action:
- Next highest-leverage action:
- Open blockers:
- Decisions that must not be silently reopened:
- Files to read first:
- Privacy boundary:
""",
}

STAGES = (
    "framing",
    "study-ready",
    "evidence-frozen",
    "claim-locked",
    "drafted",
    "reviewed",
    "response-ready",
    "submission-ready",
)


def initial_state() -> dict[str, object]:
    return {
        "schema_version": "0.3.0",
        "current_stage": STAGES[0],
        "history": [{"stage": STAGES[0], "note": "workspace initialized"}],
    }


def plan_workspace(project_dir: Path) -> dict[str, object]:
    workspace = project_dir / ".hci-paper"
    return {
        "schema_version": "0.3.0",
        "workspace": str(workspace),
        "files": sorted(FILES) + ["manifest.json", "state.json"],
        "directories": ["runs"],
        "privacy": "local files only; no network requests",
    }


def create_workspace(project_dir: Path, manuscript: str = "") -> dict[str, object]:
    if not project_dir.is_dir():
        raise ValueError(f"Project directory does not exist: {project_dir}")
    workspace = project_dir / ".hci-paper"
    if workspace.exists():
        raise FileExistsError(
            f"Refusing to overwrite existing workspace: {workspace}. "
            "Rename or back it up before creating a new one."
        )

    workspace.mkdir()
    (workspace / "runs").mkdir()
    for filename, content in FILES.items():
        if filename == "context.md" and manuscript:
            content = content.replace("- Manuscript path:\n", f"- Manuscript path: {manuscript}\n")
        (workspace / filename).write_text(content, encoding="utf-8")
    manifest = plan_workspace(project_dir)
    (workspace / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (workspace / "state.json").write_text(
        json.dumps(initial_state(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return manifest


def read_state(project_dir: Path) -> dict[str, object]:
    state_path = project_dir / ".hci-paper" / "state.json"
    if not state_path.is_file():
        raise FileNotFoundError(f"Missing workspace state: {state_path}")
    state = json.loads(state_path.read_text(encoding="utf-8"))
    if state.get("current_stage") not in STAGES:
        raise ValueError(f"Unknown current stage: {state.get('current_stage')!r}")
    return state


def advance_state(project_dir: Path, target: str, note: str) -> dict[str, object]:
    if target not in STAGES:
        raise ValueError(f"Unknown target stage: {target}. Choose from: {', '.join(STAGES)}")
    if not note.strip():
        raise ValueError("--note is required when advancing state")
    state = read_state(project_dir)
    current = str(state["current_stage"])
    expected_index = STAGES.index(current) + 1
    if expected_index >= len(STAGES):
        raise ValueError("Workspace is already at submission-ready")
    expected = STAGES[expected_index]
    if target != expected:
        raise ValueError(f"Cannot advance from {current} to {target}; next stage is {expected}")
    state["current_stage"] = target
    history = list(state.get("history", []))
    history.append(
        {
            "stage": target,
            "note": note.strip(),
            "recorded_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        }
    )
    state["history"] = history
    state_path = project_dir / ".hci-paper" / "state.json"
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return state


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project_dir", type=Path, help="Existing paper project directory")
    parser.add_argument("--manuscript", default="", help="Optional manuscript path to record")
    parser.add_argument("--dry-run", action="store_true", help="Show the plan without writing files")
    parser.add_argument("--json", action="store_true", help="Print machine-readable output")
    parser.add_argument("--status", action="store_true", help="Read the current workspace stage")
    parser.add_argument("--advance", choices=STAGES, help="Advance exactly one lifecycle stage")
    parser.add_argument("--note", default="", help="Evidence or decision recorded with --advance")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    project_dir = args.project_dir.resolve()
    if args.status and args.advance:
        raise SystemExit("Choose only one of --status and --advance")
    if args.status:
        result = read_state(project_dir)
    elif args.advance:
        result = advance_state(project_dir, args.advance, args.note)
    else:
        result = plan_workspace(project_dir) if args.dry_run else create_workspace(project_dir, args.manuscript)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.status or args.advance:
        print(f"Current stage: {result['current_stage']}")
    else:
        action = "Would create" if args.dry_run else "Created"
        print(f"{action} {result['workspace']}")
        for filename in result["files"]:
            print(f"- {filename}")
        print("- runs/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
