from pathlib import Path
import sys
import unittest


SCRIPT_DIR = Path(__file__).resolve().parents[1] / "skills" / "hci-paper-writing" / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

from manuscript_audit import (  # noqa: E402
    analyze,
    extract_float_integrity,
    extract_section_blocks,
    extract_sections,
    markdown_report,
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


if __name__ == "__main__":
    unittest.main()
