"""Real file checks for canonical documents and linked document resources."""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

CHECKER = Path(__file__).resolve().parents[1] / "scripts/check_documents.py"


class DocumentChecks(unittest.TestCase):
    def run_check(self, root):
        return subprocess.run([sys.executable, "-B", str(CHECKER), str(root)], capture_output=True, text=True)

    def test_compatibility_link_uses_canonical_relative_resources(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "canonical").mkdir()
            (root / "compatibility").mkdir()
            (root / "canonical/entry.md").write_text("# Entry\n\n[Source](source.md#stable)\n")
            (root / "canonical/source.md").write_text('# Source\n\n<a id="stable"></a>\n')
            (root / "compatibility/spec.md").symlink_to("../canonical/entry.md")
            result = self.run_check(root)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            (root / "canonical/source.md").write_text("# Source\n")
            result = self.run_check(root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("missing anchor", result.stdout)

    def test_broken_canonical_link_is_not_hidden_by_compatibility(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "canonical").mkdir()
            (root / "compatibility").mkdir()
            (root / "canonical/entry.md").write_text("# Entry\n\n[Missing](missing.md)\n")
            (root / "compatibility/spec.md").symlink_to("../canonical/entry.md")
            result = self.run_check(root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("missing target", result.stdout)
