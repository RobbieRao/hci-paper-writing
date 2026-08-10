from pathlib import Path
import sys
import unittest


SCRIPT_DIR = Path(__file__).resolve().parents[1] / "skills" / "hci-paper-writing" / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

from manuscript_audit import analyze, extract_sections, markdown_report  # noqa: E402


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


if __name__ == "__main__":
    unittest.main()
