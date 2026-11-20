"""Offline Markdown reference checker. Python 3.9+, no dependencies."""
import argparse
import difflib
import html
import json
import os
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit

SKIP = {'.git', '.venv', 'node_modules', 'build', 'dist', '__pycache__'}
LINK = re.compile(r'!?\[[^\]\n]*\]\(\s*(?:<([^>]+)>|((?:[^()\s]|\([^()\s]*\))+))(?:\s+"[^"]*")?\s*\)')


def content(path):
    fence = ''
    for number, line in enumerate(path.read_text(encoding='utf-8-sig').splitlines(), 1):
        marker = re.match(r'^ {0,3}(`{3,}|~{3,})(.*)$', line)
        if fence:
            if marker and marker[1].startswith(fence) and not marker[2].strip():
                fence = ''
            continue
        if marker:
            fence = marker[1]
        else:
            yield number, line


def scan(root):
    root = root.resolve()
    docs = {}
    for folder, dirs, files in os.walk(root):
        dirs[:] = sorted(d for d in dirs if d not in SKIP and not d.startswith('.'))
        for name in sorted(files):
            p = Path(folder, name)
            if p.suffix.lower() == '.md' and not p.is_symlink():
                docs[p] = list(content(p))
    anchors = {}
    for p, lines in docs.items():
        ids = set()
        for _, line in lines:
            heading = re.match(r'^ {0,3}#{1,6}\s+(.+)', line)
            if heading:
                base = re.sub(r'[^\w -]', '', re.sub(r'\s+#+\s*$', '', heading[1]).strip().lower()).replace(' ', '-')
                slug, n = base, 0
                while slug in ids:
                    n += 1
                    slug = f'{base}-{n}'
                ids.add(slug)
        anchors[p] = ids
    issues, checked = [], 0
    for p, lines in docs.items():
        for number, line in lines:
            for match in LINK.finditer(re.sub(r'(`+)(.+?)\1', '', line)):
                ref = match[1] or match[2]
                if ref.startswith('//') or re.match(r'^[A-Za-z][\w+.-]*:', ref):
                    continue
                checked += 1
                url = urlsplit(ref)
                path, fragment = unquote(url.path), unquote(url.fragment)
                dest = ((root if path.startswith('/') else p.parent) / path.lstrip('/')).resolve() if path else p
                hint = ''
                if not dest.is_relative_to(root):
                    kind = 'outside-root'
                elif not dest.exists():
                    kind = 'missing-file'
                    if dest.parent.is_dir():
                        hint = next(iter(difflib.get_close_matches(dest.name, sorted(x.name for x in dest.parent.iterdir()), n=1)), '')
                elif fragment and dest in anchors and fragment not in anchors[dest]:
                    kind = 'missing-heading'
                    hint = next(iter(difflib.get_close_matches(fragment, sorted(anchors[dest]), n=1)), '')
                else:
                    continue
                issues.append(dict(file=p.relative_to(root).as_posix(), line=number, target=ref, kind=kind, suggestion=hint))
    return dict(documents=len(docs), references=checked, issues=issues)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('root', type=Path, nargs='?', default=Path('.'))
    ap.add_argument('--format', choices=['text', 'json', 'html'], default='text')
    args = ap.parse_args()
    if not args.root.is_dir():
        ap.error('root must be an existing directory')
    report = scan(args.root)
    rows = report['issues']
    summary = f"{report['documents']} documents | {report['references']} local references | {len(rows)} issues"
    if args.format == 'json':
        print(json.dumps(report, ensure_ascii=False, indent=2))
    elif args.format == 'html':
        print('<!doctype html><meta charset=utf-8><title>DocSignal report</title><style>body{font:18px system-ui;max-width:65em;margin:4em auto;padding:1em;color:#153537}li{padding:1em;background:#eff6f4;margin:.6em 0}small{color:#34655c}</style><small>PROJECT-A / DOCUMENTATION HEALTH</small><h1>DocSignal</h1><p>'+summary+'</p><ol>')
        for row in rows:
            print('<li>'+html.escape('{file}:{line} — {kind}: {target}'.format(**row)) + (' → '+html.escape(row['suggestion']) if row['suggestion'] else '')+'</li>')
        print('</ol>')
    else:
        print(summary)
        for row in rows:
            print('{file}:{line}: {kind}: {target}'.format(**row), ('→ '+row['suggestion']) if row['suggestion'] else '')
    return int(bool(rows))


if __name__ == '__main__':
    raise SystemExit(main())
