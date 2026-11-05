#!/usr/bin/env python3
"""Check/refresh the counter's fixed public-route catalogue; never deploy it.

Run after the public build, before publication:
  python3 tools/check_audience_pages.py
For the already-published website:
  python3 tools/check_audience_pages.py --live [--update]
Refresh retains previously approved routes so old aggregate reports remain readable.
"""
import argparse
import json
from pathlib import Path
import re
import sys
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
LIVE_URL = 'https://kabitalive.com/runtime-config.json'
MANIFEST = ROOT / 'kb/production/editorial-service/backend/audience-pages.json'
RUNTIME = ROOT / 'projects/site/.public/runtime-config.json'
PUBLIC_PATH = re.compile(r'/(?:index|about|archive|poems|poets|poem-[A-Za-z0-9-]+|issue-\d+|poet-\d+|thirty-languages-and-the-journey-of-a-poem)\.html')


def validate_pages(pages):
    if not isinstance(pages, dict) or not pages or len(pages) > 10000:
        raise ValueError('Expected a bounded, nonempty public route/title map')
    for path, title in pages.items():
        if path != '/' and not PUBLIC_PATH.fullmatch(path):
            raise ValueError(f'Unapproved public route: {path!r}')
        if not isinstance(title, str) or not title.strip() or len(title) > 1000 or any(ord(c) < 32 for c in title):
            raise ValueError(f'Invalid page title for {path!r}')
    return pages


def reconcile(existing, public):
    validate_pages(existing)
    validate_pages(public)
    missing = sorted(set(public) - set(existing))
    # Keep historical approved paths: combineDays uses this map to read old counts.
    merged = dict(sorted({**existing, **public}.items()))
    return missing, merged


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--runtime-config', '--runtime', dest='runtime', type=Path, default=RUNTIME)
    parser.add_argument('--manifest', type=Path, default=MANIFEST)
    parser.add_argument('--live', action='store_true', help='Read only the fixed Kabita Live runtime URL')
    parser.add_argument('--update', action='store_true', help='Write the local manifest; deployment remains separate')
    args = parser.parse_args()
    if args.live:
        with urllib.request.urlopen(LIVE_URL, timeout=30) as response:
            if response.geturl() != LIVE_URL:
                raise ValueError('Unexpected runtime redirect')
            data = response.read(2_000_001)
            if len(data) > 2_000_000:
                raise ValueError('Runtime configuration exceeds size bound')
            runtime = json.loads(data)
    else:
        runtime = json.loads(args.runtime.read_text())
    existing = json.loads(args.manifest.read_text())
    missing, merged = reconcile(existing, runtime['audience']['publicPages'])
    if args.update:
        args.manifest.write_text(json.dumps(merged, ensure_ascii=False, indent=2) + '\n')
    result = {'result': 'UPDATED' if args.update else ('FAIL' if missing else 'PASS'),
              'source': LIVE_URL if args.live else str(args.runtime),
              'backend_pages_before': len(existing), 'public_pages': len(runtime['audience']['publicPages']),
              'missing_routes': missing, 'backend_pages_after': len(merged) if args.update else len(existing),
              'deployed': False}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if args.update or not missing else 1


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (ValueError, KeyError, OSError) as exc:
        print(f'Audience catalogue check failed: {exc}', file=sys.stderr)
        sys.exit(1)
