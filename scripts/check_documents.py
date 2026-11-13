"""Check relative document links inside a resolved project root."""
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

root = Path(sys.argv[1]).resolve()
errors = []
count = 0
skipped_external = 0

def confined_path(candidate, entry, kind):
    try:
        resolved = candidate.resolve()
    except (OSError, RuntimeError, ValueError) as error:
        errors.append(f"{entry.relative_to(root)}: cannot resolve {kind}: {error}")
        return None
    try:
        resolved.relative_to(root)
    except ValueError:
        errors.append(f"{entry.relative_to(root)}: {kind} outside root: {candidate}")
        return None
    return resolved

def machine_path(value):
    # Check both native and Windows forms on every host, after URL decoding.
    return (value.startswith(("/", "\\"))
            or re.match(r"^[A-Za-z]:", value) is not None
            or value.lower().startswith("file:"))

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
    path = confined_path(entry, entry, "document")
    if path is None or path in seen:
        continue
    seen.add(path)
    count += 1
    try:
        text = prose(path)
    except (OSError, UnicodeError, ValueError) as error:
        errors.append(f"{entry.relative_to(root)}: cannot read document: {error}")
        continue
    for n, line in enumerate(text.splitlines(), 1):
        if re.match(r"^#{1,6}\s", line) and re.search(r"[\u3400-\u9fff]", line):
            errors.append(f"{entry.relative_to(root)}: Chinese heading: {line}")
    for link in re.findall(r"\[[^\]\n]*\]\(([^)]+)\)", text):
        value = link.strip().strip("<>")
        decoded = unquote(value)
        # urlsplit removes some control characters; reject them before classification.
        if any(ord(char) < 32 or ord(char) == 127 for char in decoded):
            errors.append(f"{entry.relative_to(root)}: invalid link: control character: {link!r}")
            continue
        try:
            url = urlsplit(value)
        except ValueError as error:
            errors.append(f"{entry.relative_to(root)}: invalid link: {link}: {error}")
            continue
        local_path = unquote(url.path)
        if machine_path(decoded) or (not url.scheme and machine_path(local_path)):
            errors.append(f"{entry.relative_to(root)}: local link must be relative: {link}")
            continue
        if url.scheme or url.netloc:
            skipped_external += 1
            continue
        target = confined_path(path.parent / local_path if local_path else path, entry, "target")
        if target is None:
            continue
        try:
            if not target.exists():
                errors.append(f"{entry.relative_to(root)}: missing target: {link}")
            elif url.fragment and target.is_file() and target.suffix.lower() == ".md" and unquote(url.fragment) not in anchors(target):
                errors.append(f"{entry.relative_to(root)}: missing anchor: {link}")
        except (OSError, UnicodeError, ValueError) as error:
            errors.append(f"{entry.relative_to(root)}: cannot read target: {link}: {error}")
print(f"Checked {count} Markdown documents: local links, anchors, English headings (outside fenced examples).")
print(f"Skipped external links: {skipped_external} (not checked)")
for error in errors:
    print(error)
print(f"Findings: {len(errors)}")
sys.exit(bool(errors))
