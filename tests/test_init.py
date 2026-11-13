"""Exercise the public CLI against real project directories."""

import os
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


CLI = Path(__file__).resolve().parents[1] / 'scripts' / 'mingspec'


def snapshot(root):
    result = {}
    for path in root.rglob('*'):
        name = path.relative_to(root).as_posix()
        if path.is_symlink():
            result[name] = ('link', str(path.readlink()))
        elif path.is_dir():
            result[name] = ('directory', None)
        else:
            result[name] = ('file', path.read_bytes())
    return result


class InitTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def run_cli(self, *args, cwd=None):
        return subprocess.run([str(CLI), *map(str, args)], cwd=cwd or self.root,
                              capture_output=True, text=True, timeout=10)

    def test_creates_new_project_skeleton(self):
        target = self.root / '新项目 with spaces'
        result = self.run_cli('init', target)
        self.assertEqual(result.returncode, 0, result.stderr)
        files = {p.relative_to(target).as_posix() for p in target.rglob('*') if p.is_file()}
        self.assertEqual(files, {'AGENTS.md', 'mingspec/readme.md',
                                 'mingspec/runbook/readme.md', 'mingspec/specs/readme.md',
                                 'mingspec/vendor/readme.md'})
        self.assertIn('specs/readme.md', (target / 'mingspec/readme.md').read_text())
        self.assertIn('runbook/readme.md', (target / 'mingspec/readme.md').read_text())
        self.assertIn(str(target), result.stdout)
        self.assertFalse((target / '.git').exists())
        for name in files:
            document = target / name
            for link in re.findall(r'\[[^\]]+\]\(([^)]+)\)', document.read_text()):
                self.assertTrue((document.parent / link).is_file(), f'{name}: {link}')

    def test_existing_code_without_agents_gets_skeleton(self):
        source = self.root / 'app.py'
        original = b'raise RuntimeError("init must never execute project code")\n'
        source.write_bytes(original)
        result = self.run_cli('init')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((self.root / 'AGENTS.md').is_file(), result.stdout)
        self.assertTrue((self.root / 'mingspec/specs/readme.md').is_file())
        self.assertEqual(source.read_bytes(), original)
        self.assertIn('初始化完成', result.stdout)

    def test_existing_agents_is_never_parsed_or_changed_by_init(self):
        for index, original in enumerate([b'# Existing rules\nkeep this rule\n',
                                           b'\xff\x00legacy bytes',
                                           b'# Notes\n```text\nunfinished example\n']):
            with self.subTest(index=index):
                target = self.root / str(index)
                target.mkdir()
                (target / 'AGENTS.md').write_bytes(original)
                result = self.run_cli('init', target)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual((target / 'AGENTS.md').read_bytes(), original)
                self.assertTrue((target / 'mingspec/runbook/readme.md').is_file())
                before = snapshot(target)
                repeated = self.run_cli('init', target)
                self.assertEqual(repeated.returncode, 0, repeated.stderr)
                self.assertEqual(snapshot(target), before)

    def test_existing_navigation_is_kept_without_duplicate_blocks(self):
        original = '# Existing Rules\n\n开发入口仅 api/；legacy/ 禁止改动。\n\n[知识](./mingspec/readme.md)\n'.encode()
        (self.root / 'AGENTS.md').write_bytes(original)
        result = self.run_cli('init')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((self.root / 'AGENTS.md').read_bytes(), original)
        self.assertTrue((self.root / 'mingspec/readme.md').is_file())
        before = snapshot(self.root)
        again = self.run_cli('init')
        self.assertEqual(again.returncode, 0, again.stderr)
        self.assertEqual(snapshot(self.root), before)

    def test_relocated_package_runs_without_the_business_repository(self):
        package = self.root / '独立 skill'
        shutil.copytree(CLI.parents[1], package, ignore=shutil.ignore_patterns('__pycache__'))
        before = snapshot(package)
        target = self.root / 'another project'
        command = [str(package / 'scripts/mingspec'), 'init', str(target)]
        created = subprocess.run(command, cwd=self.root, capture_output=True, text=True, timeout=10)
        self.assertEqual(created.returncode, 0, created.stderr)
        self.assertTrue((target / 'AGENTS.md').is_file())
        target_before = snapshot(target)
        repeated = subprocess.run(command, cwd=self.root, capture_output=True, text=True, timeout=10)
        self.assertEqual(repeated.returncode, 0, repeated.stderr)
        self.assertIn('初始化完成', repeated.stdout)
        self.assertEqual(snapshot(target), target_before)
        self.assertEqual(snapshot(package), before)

    def test_preserves_existing_content_and_repeated_user_edits(self):
        agents = self.root / 'AGENTS.md'
        original = '# Existing Rules\r\n已有约定必须保留。'.encode()
        agents.write_bytes(original)
        (self.root / 'mingspec/specs').mkdir(parents=True)
        (self.root / 'mingspec/readme.md').write_bytes(b'existing bytes: \xff')
        (self.root / 'business.txt').write_bytes(b'keep business data')
        result = self.run_cli('init')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(agents.read_bytes(), original)
        self.assertNotIn(b'## Repository Map', agents.read_bytes())
        self.assertEqual((self.root / 'mingspec/readme.md').read_bytes(), b'existing bytes: \xff')
        self.assertEqual((self.root / 'business.txt').read_bytes(), b'keep business data')
        self.assertTrue((self.root / 'mingspec/runbook/readme.md').is_file())
        self.assertTrue((self.root / 'mingspec/vendor/readme.md').is_file())
        agents.write_bytes(agents.read_bytes() + b'\nUser edit\n')
        (self.root / 'mingspec/specs/readme.md').write_text('# My Specifications\n用户编辑\n')
        before = snapshot(self.root)
        again = self.run_cli('init')
        self.assertEqual(again.returncode, 0, again.stderr)
        self.assertEqual(snapshot(self.root), before)

    def test_type_conflicts_never_change_existing_paths(self):
        for index, (name, kind) in enumerate([
            ('', 'file'), ('mingspec', 'file'), ('mingspec/runbook', 'file'),
            ('mingspec/specs', 'file'), ('AGENTS.md', 'directory'),
            ('mingspec/readme.md', 'directory'),
            ('mingspec/runbook/readme.md', 'directory'),
            ('mingspec/specs/readme.md', 'directory'),
            ('mingspec/vendor', 'file'), ('mingspec/vendor/readme.md', 'directory'),
        ]):
            with self.subTest(path=name):
                target = self.root / str(index)
                conflict = target / name
                conflict.parent.mkdir(parents=True, exist_ok=True)
                if kind == 'file':
                    conflict.write_bytes(b'keep existing content')
                else:
                    conflict.mkdir()
                before = snapshot(self.root)
                result = self.run_cli('init', target)
                self.assertEqual(result.returncode, 2, result.stderr)
                self.assertIn(str(conflict), result.stderr)
                self.assertEqual(snapshot(self.root), before)
                self.assertNotIn('初始化完成', result.stdout)

    def test_symbolic_links_are_rejected_without_writes(self):
        for index, name in enumerate(['', 'mingspec', 'mingspec/specs', 'AGENTS.md',
                                      'mingspec/readme.md', 'mingspec/vendor',
                                      'mingspec/vendor/readme.md', 'ancestor', 'dangling']):
            with self.subTest(path=name):
                case = self.root / str(index)
                case.mkdir()
                outside = case / 'outside'
                outside.mkdir()
                (outside / 'original.txt').write_bytes(b'outside data')
                target = case / 'project'
                if name == 'ancestor':
                    target.symlink_to(outside, target_is_directory=True)
                    target = target / 'nested'
                else:
                    link = target / ('mingspec/runbook' if name == 'dangling' else name)
                    link.parent.mkdir(parents=True, exist_ok=True)
                    link.symlink_to(outside / 'missing' if name == 'dangling' else outside)
                before = snapshot(case)
                result = self.run_cli('init', target)
                self.assertEqual(result.returncode, 2, result.stderr)
                self.assertIn('符号链接', result.stderr)
                self.assertEqual(snapshot(case), before)

    def test_legacy_markers_are_preserved_without_semantic_processing(self):
        start = b'<!-- mingspec:init:start -->'
        end = b'<!-- mingspec:init:end -->'
        for index, content in enumerate([start, end, end + start,
                                         start + start + end, start + end + end]):
            with self.subTest(content=content):
                target = self.root / str(index)
                target.mkdir()
                (target / 'AGENTS.md').write_bytes(content)
                result = self.run_cli('init', target)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual((target / 'AGENTS.md').read_bytes(), content)
                before = snapshot(target)
                again = self.run_cli('init', target)
                self.assertEqual(again.returncode, 0, again.stderr)
                self.assertEqual(snapshot(target), before)

    def test_agents_template_and_long_existing_entry(self):
        target = self.root / 'fresh'
        result = self.run_cli('init', target)
        self.assertEqual(result.returncode, 0, result.stderr)
        agents = (target / 'AGENTS.md').read_text()
        for heading in ['Repository Map', 'Quick Commands', 'Key Conventions', 'Current Status']:
            self.assertIn('## ' + heading, agents)
        conventions = agents.split('## Key Conventions', 1)[1].split('## Current Status', 1)[0]
        self.assertIn('| 动作 | 规则入口 |', conventions)
        self.assertNotIn('一句话', conventions)
        self.assertLess(len(agents.splitlines()), 115)
        self.assertNotIn('待确认', agents)
        self.assertIn('vendor/readme.md', (target / 'mingspec/readme.md').read_text())
        existing = self.root / 'existing'
        existing.mkdir()
        original = '# My Rules\n' + '已有规则\n' * 114
        (existing / 'AGENTS.md').write_text(original)
        report = self.run_cli('init', existing)
        self.assertEqual(report.returncode, 0, report.stderr)
        self.assertTrue((existing / 'AGENTS.md').read_text().startswith(original))
        self.assertNotIn('115', report.stderr)
        self.assertNotIn('缺少', report.stderr)

    def test_default_and_relative_target_paths(self):
        result = self.run_cli('init')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((self.root / 'AGENTS.md').is_file())
        nested = self.run_cli('init', 'nested/project')
        self.assertEqual(nested.returncode, 0, nested.stderr)
        self.assertTrue((self.root / 'nested/project/AGENTS.md').is_file())

    def test_help_and_invalid_arguments_do_not_write(self):
        for args, code in [([], 2), (['--help'], 0), (['init', '--help'], 0),
                           (['unknown'], 2), (['init', 'a', 'b'], 2),
                           (['init', '--force'], 2)]:
            with self.subTest(args=args):
                before = snapshot(self.root)
                result = self.run_cli(*args)
                self.assertEqual(result.returncode, code, result.stderr)
                self.assertEqual(snapshot(self.root), before)

    def test_removed_review_options_do_not_write(self):
        for options in [('--review', 'review.json'),
                        ('--apply', 'review.json', '--expected-review', 'a' * 64),
                        ('--expected-review', 'a' * 64)]:
            with self.subTest(options=options):
                before = snapshot(self.root)
                result = self.run_cli('init', *options)
                self.assertEqual(result.returncode, 2, result.stderr)
                self.assertIn('unrecognized arguments', result.stderr)
                self.assertEqual(snapshot(self.root), before)
        help_result = self.run_cli('init', '--help')
        self.assertNotIn('--review', help_result.stdout)
        self.assertNotIn('--apply', help_result.stdout)

    def test_unwritable_target_reports_failure(self):
        self.root.chmod(0o755)
        distribution = self.root / 'tool'
        shutil.copytree(CLI.parents[1], distribution)
        target = self.root / 'locked'
        target.mkdir(mode=0o555)
        before = snapshot(target)
        credentials = dict(user=65534, group=65534, extra_groups=()) if os.geteuid() == 0 else {}
        try:
            result = subprocess.run([str(distribution / 'scripts/mingspec'), 'init', str(target)],
                                    cwd=self.root, capture_output=True, text=True,
                                    timeout=10, **credentials)
            self.assertEqual(result.returncode, 1, result.stderr)
            self.assertIn('mingspec init:', result.stderr)
            self.assertIn('重跑', result.stderr)
            self.assertNotIn('初始化完成', result.stdout)
            self.assertEqual(snapshot(target), before)
        finally:
            target.chmod(0o755)

    def test_hardlinked_agents_is_preserved_without_modifying_external_content(self):
        outside = self.root / 'outside.md'
        original = b'# Existing shared rules\n'
        outside.write_bytes(original)
        target = self.root / 'project'
        target.mkdir()
        os.link(outside, target / 'AGENTS.md')
        result = self.run_cli('init', target)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(outside.read_bytes(), original)
        self.assertEqual((target / 'AGENTS.md').read_bytes(), original)
        self.assertTrue((target / 'mingspec/runbook/readme.md').is_file())
        before = snapshot(self.root)
        repeat = self.run_cli('init', target)
        self.assertEqual(repeat.returncode, 0, repeat.stderr)
        self.assertEqual(snapshot(self.root), before)


if __name__ == '__main__':
    unittest.main()
