#!/usr/bin/env python3
"""Create a local, versionable HCI paper state directory without overwriting files."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


FILES = {
    "context.md": """# Paper Context

- Working title:
- Target venue, year, track:
- Submission type:
- Deadline:
- Primary contribution type:
- Research question(s):
- Method tradition:
- Manuscript path:
- Privacy boundary:
- Current stage:

## One-sentence thesis


## Evidence currently available


## Known boundaries and unresolved decisions

""",
    "claims.csv": "claim_id,claim,contribution_type,evidence,source_location,status,scope_note\n",
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
}


def plan_workspace(project_dir: Path) -> dict[str, object]:
    workspace = project_dir / ".hci-paper"
    return {
        "schema_version": "0.2.0",
        "workspace": str(workspace),
        "files": sorted(FILES) + ["manifest.json"],
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
    return manifest


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project_dir", type=Path, help="Existing paper project directory")
    parser.add_argument("--manuscript", default="", help="Optional manuscript path to record")
    parser.add_argument("--dry-run", action="store_true", help="Show the plan without writing files")
    parser.add_argument("--json", action="store_true", help="Print machine-readable output")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    project_dir = args.project_dir.resolve()
    result = plan_workspace(project_dir) if args.dry_run else create_workspace(project_dir, args.manuscript)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        action = "Would create" if args.dry_run else "Created"
        print(f"{action} {result['workspace']}")
        for filename in result["files"]:
            print(f"- {filename}")
        print("- runs/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
