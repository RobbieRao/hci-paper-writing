#!/usr/bin/env python3
"""Fail a public release when tracked files contain common private artifacts.

This is a defensive release check, not a substitute for keeping private
research infrastructure and evaluation runs physically outside the public
repository. It reads local files only and never prints their contents.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
import re
import subprocess
import sys


MAX_FILE_BYTES = 2 * 1024 * 1024

FORBIDDEN_SUFFIXES = {
    ".arrow", ".bin", ".ckpt", ".db", ".faiss", ".gguf", ".index",
    ".jsonl", ".log", ".npy", ".npz", ".onnx", ".parquet", ".pickle",
    ".pkl", ".pt", ".pth", ".safetensors", ".sqlite",
}

FORBIDDEN_PARTS = {
    ".private", "adapter", "adapters",
    "checkpoints", "embeddings", "indexes", "mlruns", "models",
    "vector_store", "wandb", "weights",
}

FORBIDDEN_FILENAMES = {".env", "id_dsa", "id_ecdsa", "id_ed25519", "id_rsa"}

TEXT_PATTERNS = (
    ("private-key material", re.compile(r"BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY")),
    ("macOS/Linux user path", re.compile("/" + r"(?:Users|home|media)/[^\s<>'\"]+")),
    ("Windows user path", re.compile(r"[A-Za-z]:\\Users\\[^\s<>'\"]+")),
    ("OpenAI-style secret", re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b")),
    ("GitHub token", re.compile(r"\b(?:ghp_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,})\b")),
    ("AWS access key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
)


@dataclass(frozen=True)
class Finding:
    path: str
    reason: str


def tracked_paths(root: Path) -> list[Path]:
    """Return paths currently tracked by Git, including staged additions."""
    process = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=root,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if process.returncode:
        raise RuntimeError("git ls-files failed; run the guard inside a Git repository")
    return [root / item.decode("utf-8", "surrogateescape")
            for item in process.stdout.split(b"\0") if item]


def require_index_matches_worktree(root: Path) -> None:
    """Refuse to scan when a tracked working file differs from its staged blob.

    The guard reads working-tree bytes. Requiring them to match the Git index
    prevents a sensitive staged version from being hidden by an unstaged edit.
    """
    process = subprocess.run(
        ["git", "diff", "--quiet", "--ignore-submodules", "--"],
        cwd=root,
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
    )
    if process.returncode == 1:
        raise RuntimeError(
            "tracked files have unstaged changes; stage them before running the guard"
        )
    if process.returncode:
        raise RuntimeError("git diff failed; run the guard inside a Git repository")


def _inside(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def _scan_text(path: Path, relative: str) -> list[Finding]:
    try:
        raw = path.read_bytes()
    except OSError:
        return [Finding(relative, "cannot read tracked file")]
    if b"\0" in raw[:8192]:
        return []
    text = raw.decode("utf-8", "replace")
    findings: list[Finding] = []
    for label, pattern in TEXT_PATTERNS:
        if pattern.search(text):
            findings.append(Finding(relative, label))
    return findings


def scan_paths(root: Path, paths: list[Path], *, max_file_bytes: int = MAX_FILE_BYTES) -> list[Finding]:
    # Keep the lexical root for classifying the repository entry itself. On
    # macOS, resolving /var to /private/var before comparing an unresolved
    # candidate would incorrectly classify every temporary test file as being
    # outside its repository. Resolve only symlink targets below.
    root = root.absolute()
    resolved_root = root.resolve()
    findings: list[Finding] = []
    for candidate in paths:
        path = candidate if candidate.is_absolute() else root / candidate
        try:
            relative_path = path.relative_to(root)
        except ValueError:
            findings.append(Finding(str(path), "path is outside repository"))
            continue
        relative = relative_path.as_posix()
        parts = set(relative_path.parts)

        if path.is_symlink():
            try:
                target = path.resolve(strict=False)
            except OSError:
                findings.append(Finding(relative, "unresolvable symlink"))
                continue
            if not _inside(target, resolved_root):
                findings.append(Finding(relative, "symlink target is outside repository"))
            continue

        if not path.is_file():
            findings.append(Finding(relative, "tracked path is not a regular file"))
            continue
        if path.name in FORBIDDEN_FILENAMES or path.name.startswith(".env."):
            findings.append(Finding(relative, "credential/config filename is forbidden"))
        if parts & FORBIDDEN_PARTS:
            findings.append(Finding(relative, "private artifact directory is forbidden"))
        if path.suffix.casefold() in FORBIDDEN_SUFFIXES:
            findings.append(Finding(relative, f"private artifact suffix {path.suffix.casefold()} is forbidden"))
        try:
            size = path.stat().st_size
        except OSError:
            findings.append(Finding(relative, "cannot stat tracked file"))
            continue
        if size > max_file_bytes:
            findings.append(Finding(relative, f"file exceeds release size limit ({max_file_bytes} bytes)"))
            continue
        findings.extend(_scan_text(path, relative))

    return sorted(set(findings), key=lambda item: (item.path, item.reason))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="Git repository root")
    parser.add_argument("--max-file-bytes", type=int, default=MAX_FILE_BYTES)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = args.root.resolve()
    if args.max_file_bytes < 1:
        print("error: --max-file-bytes must be positive", file=sys.stderr)
        return 2
    try:
        require_index_matches_worktree(root)
        paths = tracked_paths(root)
        findings = scan_paths(root, paths, max_file_bytes=args.max_file_bytes)
    except RuntimeError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    if findings:
        print("Release guard blocked these tracked files:", file=sys.stderr)
        for finding in findings:
            print(f"- {finding.path}: {finding.reason}", file=sys.stderr)
        return 1
    print(f"Release guard passed: {len(paths)} tracked files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
