"""Check current project documents, resolving compatibility links to their authoring location."""
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

root = Path(sys.argv[1]).resolve()
errors = []
count = 0

def prose(path):
    return re.sub(r"^(`{3,}|~{3,}).*?^\1[^\n]*$", "", path.read_text(encoding="utf-8"), flags=re.M | re.S)

def anchors(path):
    text = prose(path)
    found = set(re.findall(r'<a\s+(?:id|name)=[\"\']([^\"\']+)', text))
    seen = {}
    for heading in re.findall(r"^#{1,6}\s+(.+?)\s*#*\s*$", text, re.M):
        slug = re.sub(r"[^\w\- ]", "", heading.lower()).replace(" ", "-")
        n = seen.get(slug, 0)
        seen[slug] = n + 1
        found.add(slug + ("-" + str(n) if n else ""))
    return found

seen = set()
for entry in sorted(root.rglob("*.md")):
    if ".git" in entry.relative_to(root).parts:
        continue
    path = entry.resolve()
    if path in seen:
        continue
    seen.add(path)
    count += 1
    text = prose(path)
    for n, line in enumerate(text.splitlines(), 1):
        if re.match(r"^#{1,6}\s", line) and re.search(r"[\u3400-\u9fff]", line):
            errors.append(f"{entry.relative_to(root)}: Chinese heading: {line}")
    for link in re.findall(r"\[[^\]\n]*\]\(([^)]+)\)", text):
        url = urlsplit(link.strip("<>"))
        if url.scheme or url.netloc:
            continue
        target = (path.parent / unquote(url.path)).resolve() if url.path else path
        if not target.exists():
            errors.append(f"{entry.relative_to(root)}: missing target: {link}")
        elif url.fragment and target.is_file() and target.suffix.lower() == ".md" and unquote(url.fragment) not in anchors(target):
            errors.append(f"{entry.relative_to(root)}: missing anchor: {link}")
print(f"Checked {count} Markdown documents: local links, anchors, English headings (outside fenced examples).")
for error in errors:
    print(error)
print(f"Findings: {len(errors)}")
sys.exit(bool(errors))
