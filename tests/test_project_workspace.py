import json
from pathlib import Path
import sys
import tempfile
import unittest


SCRIPT_DIR = Path(__file__).resolve().parents[1] / "skills" / "hci-paper-writing" / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

from project_workspace import create_workspace, plan_workspace  # noqa: E402


class ProjectWorkspaceTests(unittest.TestCase):
    def test_plan_does_not_write(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            result = plan_workspace(root)
            self.assertFalse((root / ".hci-paper").exists())
            self.assertEqual(result["schema_version"], "0.2.0")

    def test_creates_expected_workspace(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            result = create_workspace(root, "paper.tex")
            workspace = root / ".hci-paper"
            self.assertEqual(result["workspace"], str(workspace))
            self.assertTrue((workspace / "runs").is_dir())
            self.assertIn("paper.tex", (workspace / "context.md").read_text())
            manifest = json.loads((workspace / "manifest.json").read_text())
            self.assertEqual(manifest["schema_version"], "0.2.0")

    def test_refuses_to_overwrite(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            create_workspace(root)
            with self.assertRaises(FileExistsError):
                create_workspace(root)


if __name__ == "__main__":
    unittest.main()
