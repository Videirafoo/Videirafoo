"""Check local Markdown links and optionally probe external HTTPS URLs."""
import argparse
from pathlib import Path
import re
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import unquote, urlsplit
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
INLINE = re.compile(r'(?<!!)\[[^\]]+\]\(<?([^\s)>]+)>?(?:\s+"[^"]+")?\)')
REFERENCE = re.compile(r'^\s*\[[^\]]+\]:\s*<?([^\s>]+)>?', re.M)
FENCE = re.compile(r'^\s*(```|~~~).*?^\s*\1\s*$', re.M | re.S)


def targets(text):
    text = FENCE.sub('', text)
    return [m.group(1) for pattern in (INLINE, REFERENCE) for m in pattern.finditer(text)]


def check_external(url, timeout=6):
    if urlsplit(url).scheme != 'https':
        return None  # HTTP links are documented but not contacted automatically.
    try:
        request = Request(url, headers={'User-Agent': 'Videirafoo-Docs-LinkCheck/1.0'}, method='HEAD')
        with urlopen(request, timeout=timeout) as response:
            return None if response.status < 400 else str(response.status)
    except HTTPError as error:
        if error.code in (403, 405, 429):
            return None  # Access controls and rate limiting are inconclusive.
        return str(error.code)
    except (URLError, TimeoutError):
        return None  # Network outages must not break documentation CI.


def validate(root, external=False):
    errors = []
    checked = {}
    for document in sorted(root.rglob('*.md')):
        if '.git' in document.parts:
            continue
        for target in targets(document.read_text(encoding='utf-8')):
            parsed = urlsplit(target)
            if parsed.scheme in ('https', 'http'):
                if external and target not in checked:
                    checked[target] = check_external(target)
                if external and checked.get(target):
                    errors.append(f'{document.relative_to(root)}: external {target}: {checked[target]}')
                continue
            if parsed.scheme or target.startswith(('#', '//')):
                continue
            if not parsed.path:
                continue
            candidate = (document.parent / unquote(parsed.path)).resolve()
            if not candidate.is_relative_to(root.resolve()) or not candidate.exists():
                errors.append(f'{document.relative_to(root)}: broken link {target}')
    return errors


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--external', action='store_true', help='Probe external HTTPS links (best effort)')
    args = parser.parse_args()
    failures = validate(ROOT, external=args.external)
    print('\n'.join(failures) if failures else 'Markdown links: OK')
    sys.exit(bool(failures))
