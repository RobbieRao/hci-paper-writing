from pathlib import Path
import subprocess
import tempfile
import unittest


import sys

SCRIPT_DIR = Path(__file__).resolve().parents[1] / "skills" / "hci-paper-writing" / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

from release_guard import require_index_matches_worktree, scan_paths  # noqa: E402


class ReleaseGuardTests(unittest.TestCase):
    def test_allows_normal_public_files(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            safe = root / "README.md"
            safe.write_text("Public documentation with no private artifacts.\n", encoding="utf-8")
            self.assertEqual(scan_paths(root, [safe]), [])

    def test_allows_rights_cleared_public_benchmark_fixture(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            safe = root / "benchmark" / "public-fixture.json"
            safe.parent.mkdir()
            safe.write_text('{"kind": "synthetic"}\n', encoding="utf-8")
            self.assertEqual(scan_paths(root, [safe]), [])

    def test_blocks_weights_indexes_and_private_directories(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            weight = root / "weights" / "adapter.safetensors"
            weight.parent.mkdir()
            weight.write_bytes(b"not-a-real-weight")
            findings = scan_paths(root, [weight])
            reasons = " ".join(item.reason for item in findings)
            self.assertIn("private artifact directory", reasons)
            self.assertIn("private artifact suffix", reasons)

    def test_blocks_absolute_user_paths_and_secret_shapes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            unsafe = root / "notes.md"
            user_path = "/" + "Users" + "/someone/private-file"
            secret = "sk-" + "a" * 30
            unsafe.write_text(f"{user_path}\n{secret}\n", encoding="utf-8")
            reasons = {item.reason for item in scan_paths(root, [unsafe])}
            self.assertIn("macOS/Linux user path", reasons)
            self.assertIn("OpenAI-style secret", reasons)

    def test_blocks_external_symlink(self) -> None:
        with tempfile.TemporaryDirectory() as directory, tempfile.TemporaryDirectory() as outside:
            root = Path(directory)
            target = Path(outside) / "private.txt"
            target.write_text("secret", encoding="utf-8")
            link = root / "linked.txt"
            link.symlink_to(target)
            findings = scan_paths(root, [link])
            self.assertIn("symlink target is outside repository", {item.reason for item in findings})

    def test_blocks_oversize_file(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            large = root / "large.txt"
            large.write_bytes(b"x" * 65)
            findings = scan_paths(root, [large], max_file_bytes=64)
            self.assertIn("file exceeds release size limit", findings[0].reason)

    def test_refuses_staged_content_hidden_by_unstaged_edit(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            staged = root / "notes.md"
            staged.write_text("sensitive staged content\n", encoding="utf-8")
            subprocess.run(["git", "add", "notes.md"], cwd=root, check=True)
            staged.write_text("sanitized working content\n", encoding="utf-8")
            with self.assertRaisesRegex(RuntimeError, "unstaged changes"):
                require_index_matches_worktree(root)


if __name__ == "__main__":
    unittest.main()
