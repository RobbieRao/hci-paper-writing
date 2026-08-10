#!/usr/bin/env python3
"""Local, deterministic preflight for HCI manuscripts.

This script makes no network requests and does not modify the input file. Its
findings are review leads, not judgments about research quality.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any


STRONG_CLAIMS = {
    "trust": r"\btrust(?:ed|ing|worthy)?\b",
    "understanding": r"\bunderstand(?:s|ing|able)?\b|\bcomprehension\b",
    "usability": r"\busab(?:le|ility)\b",
    "usefulness": r"\buseful(?:ness)?\b|\butility\b",
    "interpretability": r"\binterpretab(?:le|ility)\b|\bexplainab(?:le|ility)\b",
    "transparency": r"\btransparen(?:t|cy)\b",
    "collaboration": r"\bcollaborat(?:e|es|ed|ing|ion|ive)\b",
    "engagement": r"\bengag(?:e|es|ed|ing|ement)\b",
    "agency": r"\bagency\b|\bautonomy\b",
    "workload": r"\bworkload\b|\bcognitive load\b",
    "fairness": r"\bfair(?:ness)?\b|\bbias(?:ed)?\b",
    "safety": r"\bsafe(?:ty)?\b|\bharm(?:ful|s)?\b",
    "accessibility": r"\baccessib(?:le|ility)\b",
    "adoption": r"\badopt(?:s|ed|ing|ion)\b",
    "improvement": r"\bimprov(?:e|es|ed|ing|ement)\b|\boutperform(?:s|ed|ing)?\b",
}

EVIDENCE_MARKERS = {
    "participants": ("participant", "respondent", "interviewee", "recruit"),
    "qualitative": ("interview", "thematic", "coding", "fieldnote", "observation"),
    "quantitative": ("experiment", "condition", "effect size", "confidence interval", "p ="),
    "deployment": ("deployment", "field study", "in the wild", "log data"),
    "design": ("prototype", "design process", "research through design", "artifact"),
    "ethics": ("ethics", "irb", "institutional review", "informed consent"),
    "limitations": ("limitation", "boundary", "generalizability", "transferability"),
}

CONTRIBUTION_PATTERN = re.compile(
    r"\bwe\s+(?:propose|introduce|present|develop|design|build|identify|"
    r"characteri[sz]e|demonstrate|contribute|offer|release|show|find)\b",
    re.IGNORECASE,
)

RQ_PATTERN = re.compile(r"\bRQ\s*[-:]?\s*\d+[A-Za-z]?\b|\bresearch questions?\b", re.IGNORECASE)
TODO_PATTERN = re.compile(r"\b(?:TODO|TBD|FIXME|XXX)\b|\[\?\]|\\todo\b", re.IGNORECASE)
FLOAT_REF_PATTERN = re.compile(
    r"\\(?:ref|autoref|cref|Cref)\*?\{([^{}]+)\}", re.IGNORECASE
)


def read_manuscript(path: Path) -> str:
    if path.suffix.lower() not in {".md", ".markdown", ".tex", ".txt"}:
        raise ValueError("Supported inputs are .md, .markdown, .tex, and .txt")
    return path.read_text(encoding="utf-8")


def visible_text(raw: str, suffix: str) -> str:
    text = raw
    if suffix.lower() == ".tex":
        text = re.sub(r"(?m)(?<!\\)%.*$", "", text)
        text = re.sub(r"\\(?:cite|ref|label|url|href)\*?(?:\[[^]]*\])?\{[^{}]*\}", " ", text)
        text = re.sub(r"\\[A-Za-z@]+\*?(?:\[[^]]*\])?", " ", text)
        text = text.replace("{", " ").replace("}", " ")
    paragraphs: list[str] = []
    current: list[str] = []

    def flush() -> None:
        if current:
            paragraphs.append(" ".join(current))
            current.clear()

    for raw_line in text.splitlines():
        line = re.sub(r"[ \t]+", " ", raw_line).strip()
        if not line:
            flush()
            continue
        if re.match(r"^#{1,6}\s+", line):
            flush()
            paragraphs.append(re.sub(r"^#{1,6}\s+", "", line))
            continue
        current.append(line)
    flush()
    return "\n".join(paragraphs)


def extract_sections(raw: str) -> list[str]:
    markdown = [m.group(2).strip() for m in re.finditer(r"(?m)^(#{1,6})\s+(.+?)\s*$", raw)]
    latex = [
        m.group(1).strip()
        for m in re.finditer(r"\\(?:sub)*section\*?\{([^{}]+)\}", raw, re.IGNORECASE)
    ]
    sections: list[str] = []
    for name in markdown + latex:
        if name and name not in sections:
            sections.append(name)
    return sections


def extract_section_blocks(raw: str, suffix: str) -> list[dict[str, str]]:
    """Return a compact reverse outline without trying to parse all Markdown/LaTeX."""
    if suffix.lower() == ".tex":
        pattern = re.compile(
            r"\\(?:section|subsection|subsubsection)\*?\{([^{}]+)\}", re.IGNORECASE
        )
    else:
        pattern = re.compile(r"(?m)^#{1,6}\s+(.+?)\s*$")

    matches = list(pattern.finditer(raw))
    outline: list[dict[str, str]] = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(raw)
        body = visible_text(raw[match.end() : end], suffix)
        sentences = split_sentences(body)
        outline.append(
            {
                "section": match.group(1).strip(),
                "opening_move": sentences[0] if sentences else "",
            }
        )
    return outline


def extract_float_integrity(raw: str, suffix: str) -> dict[str, Any]:
    """Inventory figure/table definitions and references using conservative patterns."""
    if suffix.lower() == ".tex":
        float_pattern = re.compile(
            r"\\begin\{(figure|table)\*?\}(.*?)\\end\{\1\*?\}",
            re.IGNORECASE | re.DOTALL,
        )
        definitions: list[dict[str, str]] = []
        labels: set[str] = set()
        for kind, body in float_pattern.findall(raw):
            label_match = re.search(r"\\label\{([^{}]+)\}", body)
            caption_match = re.search(r"\\caption(?:\[[^]]*\])?\{([^{}]*)\}", body, re.DOTALL)
            label = label_match.group(1).strip() if label_match else ""
            caption = re.sub(r"\s+", " ", caption_match.group(1)).strip() if caption_match else ""
            if label:
                labels.add(label)
            definitions.append({"kind": kind.lower(), "label": label, "caption": caption})

        references = {
            key.strip()
            for group in FLOAT_REF_PATTERN.findall(raw)
            for key in group.split(",")
            if key.strip()
        }
        float_like_references = {
            key for key in references if re.match(r"^(?:fig|figure|tab|table)[:._-]", key, re.I)
        }
        return {
            "definitions": definitions,
            "defined_labels": sorted(labels),
            "referenced_labels": sorted(references & labels),
            "unreferenced_labels": sorted(labels - references),
            "undefined_float_references": sorted(float_like_references - labels),
            "missing_label_count": sum(1 for item in definitions if not item["label"]),
            "missing_caption_count": sum(1 for item in definitions if not item["caption"]),
        }

    images = [
        {"kind": "figure", "label": target.strip(), "caption": alt.strip()}
        for alt, target in re.findall(r"!\[([^]]*)\]\(([^)]+)\)", raw)
    ]
    return {
        "definitions": images,
        "defined_labels": [item["label"] for item in images],
        "referenced_labels": [],
        "unreferenced_labels": [],
        "undefined_float_references": [],
        "missing_label_count": 0,
        "missing_caption_count": sum(1 for item in images if not item["caption"]),
    }


def split_sentences(text: str) -> list[str]:
    candidates = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9\[])|\n+", text)
    return [re.sub(r"\s+", " ", item).strip() for item in candidates if item.strip()]


def excerpts(sentences: list[str], pattern: re.Pattern[str], limit: int) -> list[str]:
    found: list[str] = []
    for sentence in sentences:
        if pattern.search(sentence):
            clipped = sentence if len(sentence) <= 240 else sentence[:237].rstrip() + "..."
            found.append(clipped)
            if len(found) >= limit:
                break
    return found


def analyze(raw: str, suffix: str, max_excerpts: int = 2) -> dict[str, Any]:
    text = visible_text(raw, suffix)
    sentences = split_sentences(text)
    sections = extract_sections(raw)
    reverse_outline = extract_section_blocks(raw, suffix)
    float_integrity = extract_float_integrity(raw, suffix)

    strong_claims: dict[str, dict[str, Any]] = {}
    for label, regex in STRONG_CLAIMS.items():
        pattern = re.compile(regex, re.IGNORECASE)
        matches = pattern.findall(text)
        if matches:
            strong_claims[label] = {
                "count": len(matches),
                "excerpts": excerpts(sentences, pattern, max_excerpts),
            }

    contribution_excerpts = excerpts(sentences, CONTRIBUTION_PATTERN, max(3, max_excerpts))
    rq_matches = sorted({re.sub(r"\s+", "", match) for match in RQ_PATTERN.findall(text)})
    evidence_counts = {
        label: sum(text.lower().count(marker) for marker in markers)
        for label, markers in EVIDENCE_MARKERS.items()
    }
    evidence_counts = {label: count for label, count in evidence_counts.items() if count}

    section_tokens = Counter(
        token
        for section in sections
        for token in re.findall(r"[A-Za-z]+", section.lower())
    )
    warnings: list[str] = []
    lowered_sections = " ".join(sections).lower()
    if sections and "abstract" not in lowered_sections:
        warnings.append("No Abstract heading was detected.")
    if sections and "introduction" not in lowered_sections:
        warnings.append("No Introduction heading was detected.")
    if not contribution_excerpts:
        warnings.append("No explicit contribution sentence was detected; check framing manually.")
    if not rq_matches:
        warnings.append("No explicit RQ marker was detected; this may be intentional.")
    if strong_claims and not evidence_counts:
        warnings.append("Strong-claim terms were detected but no common evidence markers were found.")
    todo_count = len(TODO_PATTERN.findall(raw))
    if todo_count:
        warnings.append(f"Detected {todo_count} unfinished-text marker(s).")
    if float_integrity["missing_label_count"]:
        warnings.append(
            f"Detected {float_integrity['missing_label_count']} figure/table environment(s) without a label."
        )
    if float_integrity["missing_caption_count"]:
        warnings.append(
            f"Detected {float_integrity['missing_caption_count']} figure/table item(s) without a caption or alt text."
        )
    if float_integrity["unreferenced_labels"]:
        warnings.append(
            "Defined figure/table labels not referenced in text: "
            + ", ".join(float_integrity["unreferenced_labels"])
        )
    if float_integrity["undefined_float_references"]:
        warnings.append(
            "Figure/table references without a detected definition: "
            + ", ".join(float_integrity["undefined_float_references"])
        )
    empty_openings = [item["section"] for item in reverse_outline if not item["opening_move"]]
    if empty_openings:
        warnings.append("Sections with no detectable prose opening: " + ", ".join(empty_openings))

    return {
        "schema_version": "0.2.0",
        "summary": {
            "characters": len(raw),
            "approx_words": len(re.findall(r"\b\w+\b", text)),
            "sections_detected": len(sections),
            "unfinished_markers": todo_count,
        },
        "sections": sections,
        "reverse_outline": reverse_outline,
        "research_question_markers": rq_matches,
        "contribution_candidates": contribution_excerpts,
        "strong_claim_terms": strong_claims,
        "evidence_marker_counts": evidence_counts,
        "section_vocabulary": dict(section_tokens.most_common(12)),
        "figure_table_integrity": float_integrity,
        "warnings": warnings,
        "interpretation_note": (
            "These are deterministic review leads. Absence or presence of a marker does not establish quality."
        ),
    }


def markdown_report(path: Path, result: dict[str, Any]) -> str:
    summary = result["summary"]
    lines = [
        "# Local Manuscript Preflight",
        "",
        f"- File: `{path.name}`",
        f"- Approximate words: {summary['approx_words']}",
        f"- Sections detected: {summary['sections_detected']}",
        f"- Unfinished markers: {summary['unfinished_markers']}",
        "- Privacy: local read-only scan; no network requests",
        "",
        "## Sections",
        "",
    ]
    lines.extend(f"- {section}" for section in result["sections"] or ["None detected"])
    lines.extend(["", "## Reverse Outline", "", "| Section | Opening move |", "|---|---|"])
    if result["reverse_outline"]:
        for item in result["reverse_outline"]:
            opening = item["opening_move"].replace("|", "\\|") or "No prose detected"
            lines.append(f"| {item['section']} | {opening} |")
    else:
        lines.append("| None detected | |")
    lines.extend(["", "## Contribution Candidates", ""])
    lines.extend(f"- {item}" for item in result["contribution_candidates"] or ["None detected"])
    lines.extend(["", "## Strong-Claim Terms", "", "| Construct | Count | Example |", "|---|---:|---|"])
    if result["strong_claim_terms"]:
        for label, data in result["strong_claim_terms"].items():
            example = (data["excerpts"] or [""])[0].replace("|", "\\|")
            lines.append(f"| {label} | {data['count']} | {example} |")
    else:
        lines.append("| None detected | 0 | |")
    lines.extend(["", "## Evidence Markers", ""])
    lines.extend(
        f"- {label}: {count}" for label, count in result["evidence_marker_counts"].items()
    )
    if not result["evidence_marker_counts"]:
        lines.append("- None detected")
    integrity = result["figure_table_integrity"]
    lines.extend(
        [
            "",
            "## Figure and Table Integrity",
            "",
            f"- Items detected: {len(integrity['definitions'])}",
            f"- Missing labels: {integrity['missing_label_count']}",
            f"- Missing captions or alt text: {integrity['missing_caption_count']}",
            "- Unreferenced labels: " + (", ".join(integrity["unreferenced_labels"]) or "None"),
            "- Undefined figure/table references: "
            + (", ".join(integrity["undefined_float_references"]) or "None"),
        ]
    )
    lines.extend(["", "## Review Leads", ""])
    lines.extend(f"- {item}" for item in result["warnings"] or ["No structural warnings detected."])
    lines.extend(["", f"> {result['interpretation_note']}", ""])
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manuscript", type=Path, help="Path to a .md, .tex, or .txt manuscript")
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    parser.add_argument("--max-excerpts", type=int, default=2)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.max_excerpts < 1:
        raise SystemExit("--max-excerpts must be at least 1")
    raw = read_manuscript(args.manuscript)
    result = analyze(raw, args.manuscript.suffix, args.max_excerpts)
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(markdown_report(args.manuscript, result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
