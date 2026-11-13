"""Real file checks for canonical documents and linked document resources."""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

CHECKER = Path(__file__).resolve().parents[1] / "scripts/check_documents.py"


class DocumentChecks(unittest.TestCase):
    def run_check(self, root, cwd=None):
        return subprocess.run([sys.executable, "-B", str(CHECKER), str(root)],
                              cwd=cwd, capture_output=True, text=True)

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

    def test_relative_links_and_relative_or_absolute_root_are_read_only(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "project"
            (root / "docs").mkdir(parents=True)
            (root / "docs/source name.md").write_text('# Source\n\n<a id="stable"></a>\n')
            (root / "asset.txt").write_text("asset\n")
            (root / "docs/entry.md").write_text(
                "# Entry\n\n[Self](#entry) [Source](../docs/source%20name.md#stable)\n"
                "[Asset](../asset.txt) [Directory](../docs/)\n")
            before = {p.relative_to(root): p.read_bytes() for p in root.rglob('*') if p.is_file()}
            for argument in (root, Path("project")):
                with self.subTest(argument=argument):
                    result = self.run_check(argument, cwd=directory)
                    self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(before, {p.relative_to(root): p.read_bytes()
                                      for p in root.rglob('*') if p.is_file()})

    def test_machine_specific_links_are_rejected_even_when_targets_exist(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "source.txt"
            target.write_text("exists\n")
            for link in (str(target), str(target).replace('/', '%2F'), target.as_uri(),
                         'FILE:///tmp/source.txt', 'file%3A///tmp/source.txt',
                         'C:/source.md', r'C:\source.md', 'C:source.md',
                         'C%3A%5Csource.md', r'\\server\share\source.md',
                         '//server/share/source.md', '%5C%5Cserver%5Cshare%5Csource.md'):
                with self.subTest(link=link):
                    (root / "entry.md").write_text(f"# Entry\n\n[Source]({link})\n")
                    result = self.run_check(root)
                    self.assertNotEqual(result.returncode, 0, result.stdout)
                    self.assertIn("local link must be relative", result.stdout)
                    self.assertNotIn("Traceback", result.stderr)

    def test_relative_escape_is_rejected_before_reading_external_anchors(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "project"
            root.mkdir()
            # A sibling whose name starts with the root name is still outside.
            sibling = root.parent / "project-other"
            sibling.mkdir()
            (sibling / "outside.md").write_bytes(b'\xff')
            for link in ('../project-other/outside.md#secret',
                         '%2E%2E/project-other/outside.md#secret'):
                with self.subTest(link=link):
                    (root / "entry.md").write_text(f"# Entry\n\n[Outside]({link})\n")
                    result = self.run_check(root)
                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn("target outside root", result.stdout)
                    self.assertNotIn("Traceback", result.stderr)

    def test_scanned_markdown_symlink_cannot_read_external_document(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "project"
            root.mkdir()
            outside = root.parent / "outside.md"
            outside.write_bytes(b'\xff')
            (root / "entry.md").symlink_to(outside)
            result = self.run_check(root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("document outside root", result.stdout)
            self.assertNotIn("Traceback", result.stderr)

    def test_linked_file_or_directory_symlink_cannot_escape(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "project"
            root.mkdir()
            outside = root.parent / "outside"
            outside.mkdir()
            (outside / "source.md").write_bytes(b'\xff')
            (root / "file-link").symlink_to(outside / "source.md")
            (root / "directory-link").symlink_to(outside, target_is_directory=True)
            for link in ('file-link#secret', 'directory-link/source.md#secret', 'directory-link/'):
                with self.subTest(link=link):
                    (root / "entry.md").write_text(f"# Entry\n\n[Outside]({link})\n")
                    result = self.run_check(root)
                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn("target outside root", result.stdout)
                    self.assertNotIn("Traceback", result.stderr)

    def test_external_urls_are_reported_as_unchecked(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "entry.md").write_text(
                "# Entry\n\n[Web](https://example.invalid/missing#anchor)\n"
                "[Mail](mailto:owner@example.invalid)\n")
            result = self.run_check(root)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("Skipped external links: 2 (not checked)", result.stdout)

    def test_control_characters_cannot_hide_local_addresses(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for link in ('fi\tle:///tmp/outside.md', '\x01file:///tmp/outside.md',
                         'C\t:/outside.md', 'fi%09le:///tmp/outside.md',
                         '%01file:///tmp/outside.md', 'C%0A:/outside.md'):
                with self.subTest(link=link):
                    (root / "entry.md").write_text(f"# Entry\n\n[Source]({link})\n")
                    result = self.run_check(root)
                    self.assertNotEqual(result.returncode, 0, result.stdout)
                    self.assertIn("invalid link: control character", result.stdout)
                    self.assertNotIn("Traceback", result.stderr)

    def test_unresolvable_paths_report_findings_without_tracebacks(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "loop.md").symlink_to("loop.md")
            (root / "entry.md").write_text("# Entry\n\n[Loop](loop.md#anchor)\n")
            result = self.run_check(root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("cannot resolve", result.stdout)
            self.assertNotIn("Traceback", result.stderr)
