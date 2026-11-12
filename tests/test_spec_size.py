"""Exercise size reminders through the distributed CLI and real projects."""

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / 'scripts/mingspec'
SPEC = 'mingspec/specs/orders/checkout/spec.md'


class SpecSizeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='mingspec size ')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.spec = self.root / SPEC
        self.spec.parent.mkdir(parents=True)

    def run_cli(self, spec=SPEC, root=None, cli=CLI):
        return subprocess.run(
            [sys.executable, '-B', str(cli), 'spec-size',
             '--root', str(root or self.root), '--spec', spec],
            cwd=self.root, text=True, capture_output=True, timeout=10)

    def test_size_boundary_is_advisory_and_read_only(self):
        # Each block has five physical lines including a blank and a table row.
        block = b'# Rule\n\n| a | b |\n```text\n```\n'
        cases = [(b'', 0), (block * 60, 300),
                 (block * 60 + b'final', 301),
                 ((block * 60).replace(b'\n', b'\r\n'), 300),
                 ((block * 60 + b'final\n').replace(b'\n', b'\r\n'), 301)]
        for content, expected in cases:
            with self.subTest(lines=expected, ending=content[-8:]):
                self.spec.write_bytes(content)
                before = {str(p.relative_to(self.root)): p.read_bytes()
                          for p in self.root.rglob('*') if p.is_file()}
                result = self.run_cli()
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertIn(f'{SPEC}: {expected} 行', result.stdout)
                self.assertEqual('提醒' in result.stdout, expected > 300)
                if expected > 300:
                    self.assertIn('拆分', result.stdout)
                self.assertEqual(before, {str(p.relative_to(self.root)): p.read_bytes()
                                         for p in self.root.rglob('*') if p.is_file()})

    def test_invalid_sources_are_not_reported_as_checked(self):
        self.spec.write_text('# Main\n', encoding='utf-8')
        for wrong in ('', str(self.spec), '../spec.md',
                      'mingspec/specs/orders/checkout/patches/P/spec.md',
                      'mingspec/specs/orders/checkout/../checkout/spec.md'):
            with self.subTest(path=wrong):
                result = self.run_cli(spec=wrong)
                self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        result = self.run_cli(root=self.root / 'missing')
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.spec.unlink()
        for kind in ('missing', 'directory', 'invalid-utf8', 'fifo'):
            with self.subTest(kind=kind):
                if self.spec.is_dir():
                    self.spec.rmdir()
                elif self.spec.exists():
                    self.spec.unlink()
                if kind == 'directory':
                    self.spec.mkdir()
                elif kind == 'invalid-utf8':
                    self.spec.write_bytes(b'\xff\n')
                elif kind == 'fifo':
                    import os
                    os.mkfifo(self.spec)
                result = self.run_cli()
                self.assertEqual(result.returncode, 4, result.stdout + result.stderr)
                self.assertIn('未检查', result.stdout + result.stderr)
                if self.spec.is_dir():
                    self.spec.rmdir()
                elif self.spec.exists():
                    self.spec.unlink()

    def test_links_cannot_escape_project_or_select_candidate(self):
        with tempfile.TemporaryDirectory() as outside:
            external = Path(outside) / 'spec.md'
            external.write_bytes(b'outside\n')
            candidate = self.spec.parent / 'patches/P/spec.md'
            candidate.parent.mkdir(parents=True)
            candidate.write_bytes(b'candidate\n' * 301)
            for target in (external, candidate, self.spec):
                with self.subTest(target=str(target)):
                    self.spec.symlink_to(target)
                    try:
                        result = self.run_cli()
                        self.assertEqual(result.returncode, 4, result.stdout + result.stderr)
                        self.assertIn('未检查', result.stdout)
                    finally:
                        self.spec.unlink()
            self.assertEqual(external.read_bytes(), b'outside\n')
            self.assertEqual(candidate.read_bytes(), b'candidate\n' * 301)

    def test_relocated_product_checks_only_explicit_target(self):
        with tempfile.TemporaryDirectory(prefix='moved mingspec ') as directory:
            product = Path(directory)
            for name in ('scripts', 'skills', 'templates'):
                shutil.copytree(ROOT / name, product / name)
            self.spec.write_bytes(b'current\n' * 301)
            unrelated = self.root / 'mingspec/specs/other/module/spec.md'
            unrelated.parent.mkdir(parents=True)
            unrelated.write_bytes(b'\xff')
            candidate = self.spec.parent / 'patches/P/spec.md'
            candidate.parent.mkdir(parents=True)
            candidate.write_bytes(b'\xff')
            result = self.run_cli(cli=product / 'scripts/mingspec')
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn(f'{SPEC}: 301 行', result.stdout)
            self.assertNotIn('未检查', result.stdout)


if __name__ == '__main__':
    unittest.main()
