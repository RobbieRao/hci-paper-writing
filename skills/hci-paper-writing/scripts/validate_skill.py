#!/usr/bin/env python3
"""Validate the public HCI skill package with Python's standard library."""

from __future__ import annotations

import argparse
import py_compile
import re
import sys
from pathlib import Path


NAME_PATTERN = re.compile(r"^[a-z0-9-]{1,63}$")
REFERENCE_PATTERN = re.compile(r"references/[A-Za-z0-9._-]+\.md")


def validate(skill_dir: Path) -> list[str]:
    errors: list[str] = []
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.is_file():
        return ["Missing SKILL.md"]

    text = skill_file.read_text(encoding="utf-8")
    match = re.match(r"\A---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if not match:
        return ["SKILL.md must begin with YAML frontmatter"]
    frontmatter = match.group(1)
    keys = re.findall(r"(?m)^([A-Za-z][A-Za-z0-9_-]*):", frontmatter)
    if sorted(keys) != ["description", "name"]:
        errors.append(f"Frontmatter must contain only name and description; found {keys}")
    name_match = re.search(r"(?m)^name:\s*([^\n]+)$", frontmatter)
    name = name_match.group(1).strip() if name_match else ""
    if not NAME_PATTERN.fullmatch(name):
        errors.append(f"Invalid skill name: {name!r}")
    if name != skill_dir.name:
        errors.append(f"Skill name {name!r} must match directory {skill_dir.name!r}")
    if not re.search(r"(?m)^description:\s*>?\s*$", frontmatter):
        errors.append("Description must use a YAML block scalar")

    referenced = set(REFERENCE_PATTERN.findall(text))
    available = {str(path.relative_to(skill_dir)) for path in (skill_dir / "references").glob("*.md")}
    missing = sorted(referenced - available)
    unreferenced = sorted(available - referenced)
    if missing:
        errors.append(f"Missing referenced files: {', '.join(missing)}")
    if unreferenced:
        errors.append(f"Unreferenced files: {', '.join(unreferenced)}")

    openai_yaml = skill_dir / "agents" / "openai.yaml"
    if not openai_yaml.is_file():
        errors.append("Missing agents/openai.yaml")
    else:
        ui_text = openai_yaml.read_text(encoding="utf-8")
        for field in ("display_name", "short_description", "default_prompt"):
            if not re.search(rf"(?m)^\s+{field}:", ui_text):
                errors.append(f"agents/openai.yaml missing {field}")

    for script in (skill_dir / "scripts").glob("*.py"):
        try:
            py_compile.compile(str(script), doraise=True)
        except py_compile.PyCompileError as exc:
            errors.append(f"Python compile failed for {script.name}: {exc.msg}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "skill_dir",
        nargs="?",
        type=Path,
        default=Path(__file__).resolve().parents[1],
    )
    args = parser.parse_args()
    errors = validate(args.skill_dir.resolve())
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"Skill is valid: {args.skill_dir.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

