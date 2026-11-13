"""Task declarations checked through the public CLI in real projects."""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

CLI = Path(__file__).resolve().parents[1] / 'scripts/mingspec'
SPEC = '''---
status: draft
revision: R1
---
# Example
<a id="rule-one"></a>
## Rule
A rule.
### Acceptance
| ID | Expectation |
| --- | --- |
| AC-1 | Observable result. |
<a id="question-one"></a>
## Question
Question and criterion.
'''


def task(tid='T1', state='pending', blockers=None, rules=None, acs=None, questions=None):
    fields = {'state': state, 'blocked_by': blockers or [],
              'rules': ['spec.md#rule-one'] if rules is None else rules,
              'acs': ['spec.md#AC-1'] if acs is None else acs,
              'questions': questions or []}
    return '\n## ' + tid + ' Deliver Result\n' + '\n'.join(
        '- ' + k + ': ' + (v if k == 'state' else json.dumps(v))
        for k, v in fields.items()) + '\n'


def snapshot(root):
    return {str(p.relative_to(root)): ('link', os.readlink(p)) if p.is_symlink()
            else ('dir',) if p.is_dir() else ('file', p.read_bytes())
            for p in root.rglob('*')}


class TaskChecks(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / '中文 project'
        self.root.mkdir()
        self.patch = self.root / 'patch'
        self.patch.mkdir()
        self.write_patch(self.patch, task())

    def write_patch(self, path, tasks, spec=SPEC):
        path.mkdir(exist_ok=True)
        (path / 'spec.md').write_text(spec, encoding='utf-8')
        (path / 'tasks.md').write_text('---\nformat: mingspec-tasks-v1\n---\n# Tasks\n' + tasks,
                                      encoding='utf-8')

    def run_cli(self, *args, env=None):
        return subprocess.run([sys.executable, '-B', str(CLI), *(args or (
            'tasks', '--root', str(self.root), '--patch', 'patch'))],
            cwd=self.root, capture_output=True, text=True, timeout=10, env=env)

    def test_valid_current_declarations_are_read_only_without_git(self):
        self.write_patch(self.patch, task('T1', 'completed') + task('T2', 'completed', ['T1']))
        (self.root / 'untracked.bin').write_bytes(b'\xff\x00')
        for p in self.patch.iterdir():
            p.write_bytes(p.read_bytes().replace(b'\n', b'\r\n'))
        before = snapshot(self.root)
        for _ in range(2):
            result = self.run_cli(env={**os.environ, 'PATH': ''})
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn('当前声明检查通过', result.stdout)
            self.assertIn('patch/tasks.md#T2', result.stdout)
            self.assertEqual(snapshot(self.root), before)

    def test_numeric_task_ids_keep_local_and_cross_patch_dependencies(self):
        other = self.root / 'other'
        self.write_patch(other, task('1.1', 'completed'))
        self.write_patch(self.patch, task('1', 'completed', ['../other/tasks.md#1.1']) +
                         task('2.1', 'completed', ['1']))
        before = snapshot(self.root)
        result = self.run_cli()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('tasks.md#2.1', result.stdout)
        self.assertEqual(snapshot(self.root), before)
        for body, expected in [
            (task('1', blockers=['1.1']) + task('1.1', blockers=['1']), 'cycle'),
            (task('1', blockers=['2.3']), 'unknown blocker'),
            (task('1', 'completed', ['1.1']) + task('1.1'), 'blocker not completed'),
            (task('1..2'), 'invalid task heading'),
            (task('1.'), 'invalid task heading'),
        ]:
            with self.subTest(body=body):
                self.write_patch(self.patch, body + task('Independent'))
                result = self.run_cli()
                self.assertEqual(result.returncode, 3, result.stdout + result.stderr)
                self.assertIn(expected, result.stdout)

    def test_explicit_legacy_source_preserves_unrecorded_patch_state(self):
        (self.patch / 'spec.md').unlink()
        source = self.patch / 'proposal.md'
        source.write_text('# Historic Proposal\n## Rule\nOriginal requirement.\n')
        body = task('1', 'completed', rules=['proposal.md#rule'], acs=[])
        header = '---\nformat: mingspec-tasks-v1\nlegacy_spec: proposal.md\n---\n# Tasks\n'
        (self.patch / 'tasks.md').write_text(header + body)
        before = snapshot(self.root)
        result = self.run_cli()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('历史来源未声明 Patch 状态', result.stdout)
        self.assertEqual(snapshot(self.root), before)
        for status, code in [('status: accepted', 0), ('status: unknown', 3),
                             ('status: accepted\nstatus: absorbed', 3)]:
            with self.subTest(status=status):
                source.write_text('---\n' + status + '\n---\n## Rule\nOriginal requirement.\n')
                self.assertEqual(self.run_cli().returncode, code)
        (self.patch / 'tasks.md').write_text(header.replace('legacy_spec: proposal.md\n', '') + body)
        self.assertEqual(self.run_cli().returncode, 4)
        (self.patch / 'tasks.md').write_text(header + body)
        (self.patch / 'spec.md').write_text(SPEC)
        result = self.run_cli()
        self.assertEqual(result.returncode, 3, result.stdout + result.stderr)
        self.assertIn('legacy_spec conflicts', result.stdout)

    def test_legacy_source_cannot_hide_invalid_or_escaped_inputs(self):
        (self.patch / 'spec.md').unlink()
        outside = self.root.parent / 'outside.md'
        outside.write_text('secret input')
        (self.patch / 'escaped.md').symlink_to(outside)
        (self.patch / 'alias.md').symlink_to(self.patch / 'tasks.md')
        os.link(self.patch / 'tasks.md', self.patch / 'hardlink.md')
        (self.patch / 'invalid.md').write_bytes(b'\xff')
        (self.patch / 'empty.md').write_text('')
        (self.patch / 'rules.md').write_text('## Rule\nUnchanged requirement.\n')
        for source, code in [('missing.md', 4), ('../../outside.md', 4),
                             ('escaped.md', 4), ('invalid.md', 4),
                             ('empty.md', 4), ('tasks.md', 3), ('alias.md', 3), ('hardlink.md', 3), ('notes.txt', 3),
                             (str(outside), 3), ('https://example.com/spec.md', 3)]:
            with self.subTest(source=source):
                (self.patch / 'tasks.md').write_text(
                    '---\nformat: mingspec-tasks-v1\nlegacy_spec: ' + source + '\n---\n# Tasks\n' +
                    task(rules=['rules.md#rule'], acs=[]))
                result = self.run_cli()
                self.assertEqual(result.returncode, code, result.stdout + result.stderr)
                self.assertIn('UNAVAILABLE' if code == 4 else 'invalid legacy_spec', result.stdout)
                self.assertNotIn('secret input', result.stdout)
                self.assertNotIn('当前声明检查通过', result.stdout)

    def test_legacy_acceptance_tables_keep_scope_and_reject_ambiguity(self):
        legacy = SPEC.replace('### Acceptance', '## 3. Behavior and Acceptance\n### Requirement: Original')
        legacy = legacy.replace('| AC-1 |', '| <a id="ac-1"></a>AC-1 |')
        self.write_patch(self.patch, task(), legacy)
        result = self.run_cli()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        for spec, body, code in [
            (legacy.replace('## 3. Behavior and Acceptance', '## Other Material'), task(), 3),
            (legacy + '\n## Other\n| ID | Result |\n| --- | --- |\n| AC-2 | Extra |\n',
             task(acs=['spec.md#AC-2']), 3),
            (legacy.replace('| --- | --- |', '| broken | --- |'), task(), 4),
            (legacy + '\n### Acceptance\n| ID | Result |\n| --- | --- |\n| AC-1 | Duplicate |\n',
             task(), 3),
            (legacy.replace('| <a id="ac-1"></a>AC-1 |', '| 1.1 |'), task(), 4),
        ]:
            with self.subTest(spec=spec):
                self.write_patch(self.patch, body, spec)
                self.assertEqual(self.run_cli().returncode, code)

    def test_legacy_conflict_keeps_unreadable_symlink_diagnostics(self):
        product = self.root / 'readable product'
        shutil.copytree(CLI.parent, product)
        Path(self.tmp.name).chmod(0o755)
        self.root.chmod(0o755)
        self.patch.chmod(0o755)
        private = self.root / 'private'
        private.mkdir()
        (private / 'source.md').write_text(SPEC)
        (self.patch / 'spec.md').unlink()
        (self.patch / 'spec.md').symlink_to(private / 'source.md')
        (self.patch / 'proposal.md').write_text(SPEC)
        (self.patch / 'tasks.md').write_text(
            '---\nformat: mingspec-tasks-v1\nlegacy_spec: proposal.md\n---\n# Tasks\n' +
            task() + task('Independent', state='unknown'))
        private.chmod(0)
        try:
            identity = {'user': 65534, 'group': 65534, 'extra_groups': ()} if os.geteuid() == 0 else {}
            result = subprocess.run([sys.executable, '-B', str(product / 'mingspec'),
                                     'tasks', '--root', str(self.root), '--patch', 'patch'],
                                    cwd=self.root, capture_output=True, text=True, timeout=10, **identity)
        finally:
            private.chmod(0o755)
        self.assertEqual(result.returncode, 4, result.stdout + result.stderr)
        for diagnostic in ['legacy_spec conflicts', 'UNAVAILABLE', '#Independent', 'invalid task state']:
            self.assertIn(diagnostic, result.stdout)

    def test_invalid_or_conflicting_states_and_duplicate_ids_are_reported(self):
        for spec, body, expected in [
            (SPEC.replace('draft', 'unknown'), task(), 'Patch state'),
            (SPEC.replace('status: draft\n', ''), task(), 'Patch state'),
            (SPEC.replace('status: draft', 'status: draft\nstatus: accepted'), task(), 'Patch state'),
            (SPEC, task(state='unknown'), 'task state'),
            (SPEC, task().replace('- state: pending', '- state: pending\n- state: completed'), 'duplicate field'),
            (SPEC, task() + task(), 'duplicate task'),
        ]:
            with self.subTest(expected=expected, spec=spec, body=body):
                self.write_patch(self.patch, body, spec)
                result = self.run_cli()
                self.assertEqual(result.returncode, 3, result.stdout + result.stderr)
                self.assertIn(expected, result.stdout)
                self.assertNotIn('当前声明检查通过', result.stdout)

    def test_explicit_profile_rejects_bad_fields_and_ignores_examples(self):
        cases = [
            ('format: future-v2', task(), 4),
            ('format: mingspec-tasks-v1', task().replace('- blocked_by: []\n', ''), 3),
            ('format: mingspec-tasks-v1', task().replace('blocked_by: []', 'blocked_by: {}'), 3),
            ('format: mingspec-tasks-v1', task().replace('blocked_by: []', 'blocked_by: [NaN]'), 3),
            ('format: mingspec-tasks-v1', task() + '- [x] Done\n', 3),
            ('format: mingspec-tasks-v1', '', 4),
            ('format: mingspec-tasks-v1', task() + '\n```text\nunclosed', 4),
        ]
        for header, body, expected in cases:
            with self.subTest(body=body, header=header):
                (self.patch / 'tasks.md').write_text('---\n' + header + '\n---\n# Tasks\n' + body)
                result = self.run_cli()
                self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        examples = '\n````text\n```\n' + task(state='bad') + '\n```\n````\n'
        examples += '\n<!--\n' + task(state='bad') + '\n-->\n'
        examples += '\n' + '\n'.join('    ' + line for line in task(state='bad').splitlines())
        self.write_patch(self.patch, task() + examples)
        result = self.run_cli()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_unavailable_files_and_root_escape_never_pass_or_block(self):
        for filename, data in [('tasks.md', b'\xff'), ('spec.md', b'\xff')]:
            self.write_patch(self.patch, task())
            (self.patch / filename).write_bytes(data)
            result = self.run_cli()
            self.assertEqual(result.returncode, 4, result.stdout + result.stderr)
        self.write_patch(self.patch, task())
        (self.patch / 'tasks.md').unlink()
        result = self.run_cli()
        self.assertEqual(result.returncode, 4, result.stdout + result.stderr)
        (self.patch / 'tasks.md').mkdir()
        self.assertEqual(self.run_cli().returncode, 4)
        (self.patch / 'tasks.md').rmdir()
        os.mkfifo(self.patch / 'tasks.md')
        self.assertEqual(self.run_cli().returncode, 4)
        (self.patch / 'tasks.md').unlink()
        outside = self.root.parent / 'outside.md'
        outside.write_text('secret input')
        (self.patch / 'tasks.md').symlink_to(outside)
        before = snapshot(self.root)
        result = self.run_cli()
        self.assertEqual(result.returncode, 4, result.stdout + result.stderr)
        self.assertNotIn('secret input', result.stdout)
        self.assertEqual(snapshot(self.root), before)

    def test_dependency_errors_do_not_hide_an_independent_component(self):
        cases = [(task('T1', blockers=['T1']), 'cycle'),
                 (task('T1', blockers=['missing']), 'unknown blocker'),
                 (task('T1', blockers=['T2']) + task('T2', 'retired'), 'retired blocker'),
                 (task('T1', 'completed', ['T2']) + task('T2', 'needs_recheck'), 'blocker not completed'),
                 (task('T1', 'completed', ['T2']) + task('T2', 'pending'), 'blocker not completed')]
        for body, expected in cases:
            with self.subTest(expected=expected):
                self.write_patch(self.patch, body + task('Independent'))
                result = self.run_cli()
                self.assertEqual(result.returncode, 3, result.stdout + result.stderr)
                self.assertIn(expected, result.stdout)
                self.assertIn('#Independent', result.stdout)

    def test_cross_patch_cycle_and_missing_file_are_reported_together(self):
        other = self.root / 'other'
        self.write_patch(other, task('T1', blockers=['../patch/tasks.md#T1']))
        self.write_patch(self.patch, task('T1', blockers=['../other/tasks.md#T1']) +
                         task('T2', blockers=['../missing/tasks.md#T1']) + task('Independent'))
        result = self.run_cli()
        self.assertEqual(result.returncode, 4, result.stdout + result.stderr)
        for message in ['cycle', 'UNAVAILABLE', 'other/tasks.md#T1', '#Independent']:
            self.assertIn(message, result.stdout)
        self.write_patch(other, task('T1', 'completed'))
        self.write_patch(self.patch, task('T1', 'completed', ['../other/tasks.md#T1']))
        self.assertEqual(self.run_cli().returncode, 0)

    def test_references_are_scoped_by_spec_and_questions_need_no_fake_ac(self):
        (self.patch / 'second.md').write_text(SPEC)
        self.write_patch(self.patch, task(rules=['spec.md#rule-one', 'second.md#rule-one'],
                                         acs=['spec.md#AC-1', 'second.md#AC-1']) +
                         task('Q', rules=[], acs=[], questions=[['spec.md#question-one', 'spec.md#question-one']]))
        self.assertEqual(self.run_cli().returncode, 0)
        for body, spec, expected in [
            (task(rules=['spec.md#missing']), SPEC, 'missing or ambiguous rule'),
            (task(acs=['spec.md#AC-9']), SPEC, 'missing or ambiguous AC'),
            (task(rules=[], acs=[], questions=[['spec.md#question-one', 'spec.md#missing']]), SPEC, 'missing or ambiguous question'),
            (task(), SPEC + '\n<a id="rule-one"></a>\n', 'missing or ambiguous rule'),
            (task(), SPEC.replace('| AC-1 | Observable result. |', '| AC-1 | Result. |\n| AC-1 | Duplicate. |'), 'missing or ambiguous AC'),
            (task(), SPEC.replace('<a id="rule-one"></a>', '```text\n<a id="rule-one"></a>\n```'), 'missing or ambiguous rule'),
        ]:
            with self.subTest(expected=expected, body=body):
                self.write_patch(self.patch, body, spec)
                result = self.run_cli()
                self.assertEqual(result.returncode, 3, result.stdout + result.stderr)
                self.assertIn(expected, result.stdout)
        self.write_patch(self.patch, task(rules=['missing.md#rule-one']))
        self.assertEqual(self.run_cli().returncode, 4)

    def test_invalid_arguments_and_absolute_patch_do_not_run_checks(self):
        before = snapshot(self.root)
        for args in [('tasks',), ('tasks', '--root', str(self.root)),
                     ('tasks', '--root', str(self.root), '--patch', str(self.patch)),
                     ('tasks', '--root', str(self.root), '--patch', '')]:
            result = self.run_cli(*args)
            self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
            self.assertNotIn('CHECKED', result.stdout)
            self.assertEqual(snapshot(self.root), before)

    def test_malformed_acceptance_table_is_not_a_definition(self):
        self.write_patch(self.patch, task(), SPEC.replace('| --- | --- |\n', ''))
        result = self.run_cli()
        self.assertEqual(result.returncode, 4, result.stdout + result.stderr)

    def test_relocated_command_and_unreadable_input(self):
        product = self.root / 'moved tool'
        shutil.copytree(CLI.parent, product)
        before = snapshot(self.root)
        result = subprocess.run([sys.executable, '-B', str(product / 'mingspec'), 'tasks',
                                 '--root', str(self.root), '--patch', 'patch'],
                                cwd=self.root.parent, capture_output=True, text=True, timeout=10)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(snapshot(self.root), before)
        if os.geteuid() == 0:
            Path(self.tmp.name).chmod(0o755)
            self.root.chmod(0o755)
            self.patch.chmod(0o755)
            (self.patch / 'tasks.md').chmod(0)
            result = subprocess.run([sys.executable, '-B', str(product / 'mingspec'), 'tasks',
                                     '--root', str(self.root), '--patch', 'patch'],
                                    cwd=self.root, capture_output=True, text=True, timeout=10,
                                    user=65534, group=65534, extra_groups=())
            self.assertEqual(result.returncode, 4, result.stdout + result.stderr)

    def test_inline_code_cannot_define_a_rule_anchor(self):
        spec = SPEC.replace('<a id="rule-one"></a>', '`<a id="rule-one"></a>`')
        self.write_patch(self.patch, task(), spec)
        result = self.run_cli()
        self.assertEqual(result.returncode, 3, result.stdout + result.stderr)
        self.assertIn('missing or ambiguous rule', result.stdout)

    def test_root_resolution_runtime_failure_reports_exit_one(self):
        loop = self.root / 'loop'
        loop.symlink_to('loop')
        result = self.run_cli('tasks', '--root', str(loop), '--patch', 'patch')
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn('运行失败', result.stdout)
        self.assertNotIn('当前声明检查通过', result.stdout)
