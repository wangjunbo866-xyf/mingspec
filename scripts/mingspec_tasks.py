"""Read-only checks of explicitly declared task documents (standard library only)."""
import json
import re
from pathlib import Path

PATCH_STATES = {'draft', 'ready', 'implemented', 'accepted', 'absorbed', 'retired'}
TASK_STATES = {'pending', 'in_progress', 'completed', 'needs_recheck', 'retired'}
FIELDS = {'state', 'blocked_by', 'rules', 'acs', 'questions'}
ID = r'[A-Za-z][A-Za-z0-9_-]*'
TASK_ID = r'(?:' + ID + r'|[0-9]+(?:\.[0-9]+)*)'


class Checker:
    def __init__(self, root):
        self.root = root
        self.findings = []
        self.documents = {}
        self.tasks = {}
        self.indices = {}
        self.notes = []

    def report(self, code, path, message, tid=None):
        subject = str(path)
        try:
            subject = path.relative_to(self.root).as_posix()
        except ValueError:
            pass
        if tid:
            subject += '#' + tid
        self.findings.append((code, subject, message))

    def resolve(self, base, value):
        try:
            path = (base / value).resolve()
            path.relative_to(self.root)
            return path
        except (OSError, RuntimeError, ValueError):
            self.report(4, base, 'source outside root or unresolvable: ' + value)
            return None

    def read(self, path):
        if path in self.documents:
            return self.documents[path]
        self.documents[path] = None
        try:
            if not path.is_file():
                raise OSError('not a readable regular file')
            text = path.read_text(encoding='utf-8')
        except (OSError, UnicodeError) as exc:
            self.report(4, path, 'unreadable source: ' + str(exc))
            return None
        # Remove fenced/indented examples and comments before looking for facts.
        visible, fence, comment = [], None, False
        for line in text.splitlines():
            if fence:
                if re.fullmatch(r' {0,3}' + re.escape(fence[0]) + '{' + str(fence[1]) + r',}\s*', line):
                    fence = None
                visible.append('')
                continue
            if comment:
                end = line.find('-->')
                if end < 0:
                    visible.append('')
                    continue
                line, comment = line[end + 3:], False
            while '<!--' in line:
                start = line.index('<!--')
                end = line.find('-->', start + 4)
                if end < 0:
                    line, comment = line[:start], True
                    break
                line = line[:start] + line[end + 3:]
            mark = re.match(r'^ {0,3}(`{3,}|~{3,})(.*)$', line)
            if mark:
                fence = (mark[1][0], len(mark[1]))
                visible.append('')
            elif line.startswith(('    ', '\t')):
                visible.append('')
            else:
                visible.append(line)
        if fence or comment:
            self.report(4, path, 'unclosed code fence or comment')
        self.documents[path] = visible
        return visible

    def frontmatter(self, path, lines):
        if not lines or lines[0] != '---':
            return {}
        try:
            end = lines.index('---', 1)
        except ValueError:
            self.report(4, path, 'unclosed frontmatter')
            return {}
        fields = {}
        for line in lines[1:end]:
            if not line.strip():
                continue
            match = re.fullmatch(r'([A-Za-z][A-Za-z0-9_-]*):\s*([^\[\]{}\'"|>]+)', line)
            if not match:
                self.report(4, path, 'unsupported frontmatter: ' + line)
                continue
            key, value = match[1], match[2].strip()
            if key in fields:
                self.report(3, path, 'Patch state duplicate' if key == 'status' else 'duplicate field ' + key)
            fields[key] = value
        return fields

    def check_patch_source(self, path, header):
        spec = path.with_name('spec.md')
        legacy = header.get('legacy_spec')
        if legacy is not None:
            if spec.is_symlink() or spec.exists():
                self.report(3, path, 'legacy_spec conflicts with existing spec.md')
                legacy = None
            elif (Path(legacy).is_absolute() or '://' in legacy or '#' in legacy or
                  Path(legacy).suffix != '.md' or Path(legacy).name == 'tasks.md'):
                self.report(3, path, 'invalid legacy_spec: ' + legacy)
                return
            else:
                spec = path.parent / legacy
        spec = self.resolve(spec.parent, spec.name)
        if spec is not None:
            lines = self.read(spec)
            if lines is not None:
                if legacy is not None:
                    try:
                        same_source = spec.samefile(path)
                    except OSError as exc:
                        self.report(4, spec, 'unreadable source identity: ' + str(exc))
                        return
                    if same_source:
                        self.report(3, path, 'invalid legacy_spec: source is the task document')
                        return
                header = self.frontmatter(spec, lines)
                if legacy is not None and not any(line.strip() for line in lines):
                    self.report(4, spec, 'empty historical source')
                elif legacy is not None and 'status' not in header:
                    self.notes.append(str(spec.relative_to(self.root)) +
                                      ': 历史来源未声明 Patch 状态；仅检查任务状态、依赖及引用，不推断历史交付状态。')
                elif header.get('status') not in PATCH_STATES:
                    self.report(3, spec, 'Patch state missing or invalid')

    def load_tasks(self, path):
        if path in self.tasks:
            return self.tasks[path]
        tasks = self.tasks[path] = {}
        lines = self.read(path)
        header = self.frontmatter(path, lines) if lines is not None else {}
        self.check_patch_source(path, header)
        if lines is None:
            return tasks
        if header.get('format') != 'mingspec-tasks-v1':
            self.report(4, path, 'unsupported tasks format; expected mingspec-tasks-v1')
            return tasks
        current = None
        for line in lines:
            if line.startswith('## '):
                match = re.fullmatch(r'## (' + TASK_ID + r') .+', line)
                current = None
                if not match:
                    self.report(3, path, 'invalid task heading: ' + line)
                    continue
                current = match[1]
                if current in tasks:
                    self.report(3, path, 'duplicate task', current)
                else:
                    tasks[current] = {}
            if current is None:
                continue
            if re.match(r'^- \[[ xX]\]|^- (状态(?:/结果)?|规格|阻塞)[：:]', line):
                self.report(3, path, 'conflicting legacy task declaration', current)
            field = re.fullmatch(r'- (state|blocked_by|rules|acs|questions):\s*(.*)', line)
            if not field:
                continue
            key, value = field[1], field[2]
            if key in tasks[current]:
                self.report(3, path, 'duplicate field ' + key, current)
            if key != 'state':
                try:
                    value = json.loads(value)
                    valid = isinstance(value, list)
                    if key == 'questions':
                        valid = valid and all(isinstance(v, list) and len(v) == 2 and
                                              all(isinstance(s, str) for s in v) for v in value)
                    else:
                        valid = valid and all(isinstance(v, str) for v in value)
                    if not valid:
                        raise ValueError('expected reference array')
                except (ValueError, TypeError):
                    self.report(3, path, 'invalid field ' + key, current)
                    value = []
            tasks[current][key] = value
        for tid, fields in tasks.items():
            for missing in sorted(FIELDS - fields.keys()):
                self.report(3, path, 'missing field ' + missing, tid)
            if fields.get('state') not in TASK_STATES:
                self.report(3, path, 'invalid task state', tid)
            if not any(fields.get(k) for k in ('rules', 'acs', 'questions')):
                self.report(3, path, 'task requires rule, AC or question reference', tid)
        if not tasks:
            self.report(4, path, 'empty task scope')
        return tasks

    def index_spec(self, path):
        if path in self.indices:
            return self.indices[path]
        lines = self.read(path)
        if lines is None:
            return None
        anchors, slugs, acs = {}, {}, {}
        acceptance = False
        legacy_acceptance = False
        table = 0
        columns = 0
        for line in lines:
            prose = re.sub(r'(?<!`)(`+)(?!`)(.*?)(?<!`)\1(?!`)', '', line)
            for anchor in re.findall(r'<a\s+(?:id|name)=["\']([^"\']+)["\'][^>]*>', prose):
                anchors[anchor] = anchors.get(anchor, 0) + 1
            heading = re.fullmatch(r'(#{1,6})\s+(.+?)\s*#*\s*', line)
            if heading:
                title = heading[2]
                slug = re.sub(r'[^\w\- ]', '', title.lower()).replace(' ', '-')
                count = slugs.get(slug, 0)
                slugs[slug] = count + 1
                actual = slug + ('-' + str(count) if count else '')
                anchors[actual] = anchors.get(actual, 0) + 1
                level = len(heading[1])
                if level <= 2:
                    legacy_acceptance = level == 2 and title == '3. Behavior and Acceptance'
                if level <= 3:
                    acceptance = legacy_acceptance or (level == 3 and title == 'Acceptance')
                    table = False
            if not acceptance:
                continue
            if line.startswith('|'):
                cells = [c.strip() for c in line.strip().strip('|').split('|')]
                if cells[0] == 'ID':
                    table, columns = 1, len(cells)
                    continue
                if table == 1:
                    if len(cells) == columns and all(re.fullmatch(r':?-{3,}:?', c) for c in cells):
                        table = 2
                        continue
                    self.report(4, path, 'unsupported Acceptance table delimiter')
                    table = 0
                if table == 2:
                    cells[0] = re.sub(r'^<a\s+(?:id|name)=["\'][^"\']+["\']\s*></a>\s*',
                                      '', cells[0])
                    if not re.fullmatch(ID, cells[0]) or len(cells) != columns or columns < 2:
                        self.report(4, path, 'unsupported Acceptance table row')
                        continue
                    acs[cells[0]] = acs.get(cells[0], 0) + 1
            else:
                table = False
        self.indices[path] = (anchors, acs)
        return anchors, acs

    def check_reference(self, path, tid, ref, kind):
        if ref.count('#') != 1:
            self.report(3, path, 'invalid ' + kind + ' reference: ' + ref, tid)
            return
        filename, target = ref.split('#')
        if not filename or not target or Path(filename).is_absolute() or '://' in filename:
            self.report(3, path, 'invalid ' + kind + ' reference: ' + ref, tid)
            return
        source = self.resolve(path.parent, filename)
        if source is None:
            return
        index = self.index_spec(source)
        if index is not None:
            definitions = index[1] if kind == 'AC' else index[0]
            if definitions.get(target) != 1:
                self.report(3, path, 'missing or ambiguous ' + kind + ': ' + ref, tid)

    def check_references(self):
        for path, tasks in self.tasks.items():
            for tid, fields in tasks.items():
                for key, kind in [('rules', 'rule'), ('acs', 'AC')]:
                    for ref in fields.get(key, []):
                        self.check_reference(path, tid, ref, kind)
                for pair in fields.get('questions', []):
                    for ref in pair:
                        self.check_reference(path, tid, ref, 'question/criterion')

    def check_graph(self, start):
        queue, queued, edges = [start], {start}, {}
        for path in queue:
            for tid, task in self.load_tasks(path).items():
                node = (path, tid)
                edges[node] = []
                for ref in task.get('blocked_by', []):
                    if '#' in ref:
                        filename, target = ref.rsplit('#', 1)
                        if not filename or Path(filename).is_absolute() or Path(filename).name != 'tasks.md':
                            self.report(3, path, 'invalid blocker reference: ' + ref, tid)
                            continue
                        source = self.resolve(path.parent, filename)
                    else:
                        source, target = path, ref
                    if not re.fullmatch(TASK_ID, target):
                        self.report(3, path, 'invalid blocker ID: ' + ref, tid)
                        continue
                    if source is None:
                        continue
                    if source not in queued:
                        queued.add(source)
                        queue.append(source)
                    edges[node].append((source, target))
        for (path, tid), blockers in edges.items():
            for source, target in blockers:
                other = self.tasks.get(source, {}).get(target)
                if other is None:
                    # A missing/unreadable source has its own UNAVAILABLE result.
                    if self.documents.get(source) is not None and self.tasks.get(source):
                        self.report(3, path, 'unknown blocker: ' + str(source) + '#' + target, tid)
                    continue
                if other.get('state') == 'retired':
                    self.report(3, path, 'retired blocker: ' + target, tid)
                if self.tasks[path][tid].get('state') == 'completed' and other.get('state') != 'completed':
                    self.report(3, path, 'blocker not completed: ' + target, tid)
        # Iterative DFS keeps large but valid task chains off Python's call stack.
        color = {}
        for start in edges:
            if color.get(start):
                continue
            color[start] = 1
            stack = [(start, iter(edges[start]))]
            while stack:
                node, children = stack[-1]
                child = next(children, None)
                if child is None:
                    color[node] = 2
                    stack.pop()
                elif color.get(child) == 1:
                    self.report(3, node[0], 'dependency cycle -> ' + str(child[0]) + '#' + child[1], node[1])
                elif child in edges and not color.get(child):
                    color[child] = 1
                    stack.append((child, iter(edges[child])))

    def finish(self):
        for note in self.notes:
            print('NOTE ' + note)
        for path, tasks in self.tasks.items():
            for tid in tasks:
                print('CHECKED ' + path.relative_to(self.root).as_posix() + '#' + tid)
        for code, subject, message in self.findings:
            print(('UNAVAILABLE' if code == 4 else 'FAIL') + ' ' + subject + ': ' + message)
        if self.findings:
            return 4 if any(code == 4 for code, _, _ in self.findings) else 3
        print('当前声明检查通过；不证明任务真实完成、状态历史或业务验收。')
        return 0


def check_tasks(root, patch):
    try:
        root = Path(root).resolve()
        checker = Checker(root)
        path = checker.resolve(root, patch)
        if path is not None:
            path = checker.resolve(path, 'tasks.md')
        if path is not None:
            checker.check_graph(path)
            checker.check_references()
        return checker.finish()
    except (OSError, RuntimeError) as exc:
        print('运行失败：' + str(exc))
        return 1
