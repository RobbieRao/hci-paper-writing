from pathlib import Path
import sys
import tempfile
import unittest
import zipfile


SCRIPT_DIR = Path(__file__).resolve().parents[1] / "skills" / "hci-paper-writing" / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

from manuscript_audit import (  # noqa: E402
    analyze,
    extract_anonymity_risks,
    expand_latex_inputs,
    extract_float_integrity,
    extract_latex_project_integrity,
    extract_section_blocks,
    extract_sections,
    markdown_report,
    read_manuscript,
    strict_issue_count,
)


SAMPLE = """# Abstract
We present a collaborative interface for community archivists.

# Introduction
RQ1: How do archivists understand provenance warnings?
We introduce a workflow that may improve understanding and trust.

# Method
We recruited 12 participants for interviews and obtained informed consent.

# Findings
Participants reported that warnings were useful, but not always transparent.

# Limitations
Our prototype and sample bound transferability.
"""


class ManuscriptAuditTests(unittest.TestCase):
    def test_extracts_markdown_sections(self) -> None:
        self.assertEqual(
            extract_sections(SAMPLE),
            ["Abstract", "Introduction", "Method", "Findings", "Limitations"],
        )

    def test_finds_claims_and_evidence(self) -> None:
        result = analyze(SAMPLE, ".md")
        self.assertIn("trust", result["strong_claim_terms"])
        self.assertIn("participants", result["evidence_marker_counts"])
        self.assertTrue(result["contribution_candidates"])
        self.assertIn(
            "We present a collaborative interface for community archivists.",
            result["contribution_candidates"],
        )
        self.assertIn("RQ1", result["research_question_markers"])

    def test_markdown_report_is_renderable(self) -> None:
        report = markdown_report(Path("sample.md"), analyze(SAMPLE, ".md"))
        self.assertIn("# Local Manuscript Preflight", report)
        self.assertIn("local read-only scan", report)
        self.assertIn("## Reverse Outline", report)

    def test_reverse_outline_captures_opening_move(self) -> None:
        outline = extract_section_blocks(SAMPLE, ".md")
        self.assertEqual(outline[1]["section"], "Introduction")
        self.assertTrue(outline[1]["opening_move"].startswith("RQ1"))

    def test_latex_float_integrity(self) -> None:
        latex = r"""
\section{Results}
See \autoref{fig:system} and \ref{tab:missing}.
\begin{figure}
\caption{System overview}
\label{fig:system}
\end{figure}
\begin{table}
\caption{Conditions}
\label{tab:unused}
\end{table}
"""
        integrity = extract_float_integrity(latex, ".tex")
        self.assertEqual(integrity["referenced_labels"], ["fig:system"])
        self.assertEqual(integrity["unreferenced_labels"], ["tab:unused"])
        self.assertEqual(integrity["undefined_float_references"], ["tab:missing"])

    def test_latex_dependencies_and_citations(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "section.tex").write_text("Results", encoding="utf-8")
            (root / "refs.bib").write_text("@article{known, title={Known}}", encoding="utf-8")
            raw = r"""
\input{section}
\input{missing-section}
\includegraphics{missing-figure}
\bibliography{refs}
\cite{known,unknown}
"""
            integrity = extract_latex_project_integrity(raw, root)
            self.assertEqual(integrity["missing_inputs"], ["missing-section"])
            self.assertEqual(integrity["missing_graphics"], ["missing-figure"])
            self.assertEqual(integrity["undefined_citation_keys"], ["unknown"])

    def test_expands_multifile_latex_for_semantic_audit(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "intro.tex").write_text(
                r"\section{Introduction} We contribute an HCI method.", encoding="utf-8"
            )
            main = root / "main.tex"
            main.write_text(r"\input{intro}", encoding="utf-8")
            expanded = expand_latex_inputs(main)
            result = analyze(main.read_text(), ".tex", semantic_raw=expanded)
            self.assertEqual(result["sections"], ["Introduction"])
            self.assertTrue(result["contribution_candidates"])

    def test_anonymity_risks_have_locations(self) -> None:
        risks = extract_anonymity_risks("Contact author@example.edu\n\\section{Method}")
        self.assertEqual(risks[0]["type"], "email address")
        self.assertEqual(risks[0]["line"], 1)

    def test_reads_minimal_docx_locally(self) -> None:
        xml = """<?xml version="1.0" encoding="UTF-8"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
<w:body><w:p><w:r><w:t>HCI manuscript text</w:t></w:r></w:p></w:body></w:document>"""
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "paper.docx"
            with zipfile.ZipFile(path, "w") as archive:
                archive.writestr("word/document.xml", xml)
            self.assertEqual(read_manuscript(path), "HCI manuscript text")

    def test_strict_count_ignores_semantic_only_warnings(self) -> None:
        result = analyze(SAMPLE, ".md")
        self.assertEqual(strict_issue_count(result), 0)
        risky = analyze("# Draft\nTODO", ".md")
        self.assertGreater(strict_issue_count(risky), 0)


if __name__ == "__main__":
    unittest.main()
