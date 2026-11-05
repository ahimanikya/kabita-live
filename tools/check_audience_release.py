#!/usr/bin/env python3
"""Block publication when source or deployed aggregate counters omit public routes."""
import argparse
import json
import re
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import URLError

ROOT = Path(__file__).resolve().parents[1]
COUNTER = 'https://asia-south1-kabita-live.cloudfunctions.net/audienceCount'
ROUTE = re.compile(r'^/(?:$|(?:index|about|archive|poems|poets|poem-[A-Za-z0-9-]+|issue-[0-9]+|poet-[0-9]+|thirty-languages-and-the-journey-of-a-poem)\.html$)')


def public_pages(value):
    if not isinstance(value, dict) or not value or len(value) > 10000:
        raise ValueError('Missing or oversized public route catalogue')
    if any(not isinstance(p, str) or not ROUTE.fullmatch(p) or not isinstance(t, str) or not t.strip() for p, t in value.items()):
        raise ValueError('Invalid or private path in audience catalogue')
    return value


def verify(expected, source, deployed=None):
    expected = public_pages(expected)
    source = public_pages(source)
    missing = sorted(set(expected) - set(source))
    if missing:
        raise ValueError('Counter source omits public routes: ' + ', '.join(missing[:25]) + '. Run kb/production/audience-statistics/prepare.py after the public build.')
    if deployed is not None:
        if not isinstance(deployed, dict) or deployed.get('version') != 1 or not isinstance(deployed.get('paths'), list):
            raise ValueError('Counter coverage endpoint unavailable or unsupported; deploy the reviewed counter update before publishing.')
        paths = deployed['paths']
        if len(paths) > 10000 or any(not isinstance(p, str) or not ROUTE.fullmatch(p) for p in paths):
            raise ValueError('Invalid deployed counter coverage')
        missing = sorted(set(expected) - set(paths))
        if missing:
            raise ValueError('Deployed counter omits public routes: ' + ', '.join(missing[:25]) + '. Deploy the reviewed counter catalogue before publishing. No synthetic views were sent.')
    return len(expected)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('runtime', type=Path)
    parser.add_argument('--offline', action='store_true', help='Check source only; never sufficient for publication')
    args = parser.parse_args()
    runtime = json.loads(args.runtime.read_text())
    expected = runtime['audience']['publicPages']
    source = json.loads((ROOT/'kb/production/editorial-service/backend/audience-pages.json').read_text())
    verify(expected, source)
    deployed = None
    if not args.offline:
        request = Request(COUNTER+'?check=coverage', headers={'Cache-Control': 'no-cache'})
        with urlopen(request, timeout=30) as response:
            raw = response.read(1_000_001)
        if len(raw) > 1_000_000:
            raise ValueError('Oversized counter coverage response')
        deployed = json.loads(raw)
    count = verify(expected, source, deployed)
    print(f'Audience coverage PASS: {count} public routes; '+('source only (offline)' if args.offline else 'source and deployed counter; no view events sent'))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, KeyError, OSError, URLError) as error:
        raise SystemExit(f'Audience release gate FAILED: {error}. Do not publish until the source and deployed counter coverage checks pass.')
