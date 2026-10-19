"""Validate relative Markdown links in the repository."""
from pathlib import Path
from urllib.parse import unquote, urlsplit
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
LINK = re.compile(r'\[[^\]]+\]\(([^\s)]+)\)')

def validate(root: Path) -> list[str]:
    errors = []
    for document in sorted(root.rglob('*.md')):
        if '.git' in document.parts:
            continue
        content = re.sub(r'```.*?```', '', document.read_text(encoding='utf-8'), flags=re.S)
        for match in LINK.finditer(content):
            target = match.group(1).strip('<>')
            parsed = urlsplit(target)
            if parsed.scheme or target.startswith(('#', '//', 'mailto:')):
                continue
            candidate = (document.parent / unquote(parsed.path)).resolve()
            if not candidate.is_relative_to(root.resolve()) or not candidate.exists():
                errors.append(f'{document.relative_to(root)}: broken link {target}')
    return errors

if __name__ == '__main__':
    failures = validate(ROOT)
    print('\n'.join(failures) if failures else 'Relative Markdown links: OK')
    sys.exit(bool(failures))
