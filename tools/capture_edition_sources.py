#!/usr/bin/env python3
"""Archive public edition/poem HTML from observed links, with resumable receipts."""
import concurrent.futures
import hashlib
import json
import re
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'kb/artifacts/content-import/editions'
RESEARCH = ROOT / 'kb/research/editions'


def ident(url):
    return int(parse_qs(urlsplit(url).query)['id'][0])


def fetch(item):
    path = SOURCE / item['path']
    path.parent.mkdir(parents=True, exist_ok=True)
    receipt_path = path.with_suffix('.receipt.json')
    if path.exists() and receipt_path.exists():
        old = json.loads(receipt_path.read_text())
        if old.get('sha256') == hashlib.sha256(path.read_bytes()).hexdigest():
            return old
    error = None
    for attempt in range(3):
        try:
            request = urllib.request.Request(item['url'], headers={
                'Referer': item['referer'], 'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(request, timeout=25) as response:
                raw = response.read()
                if response.url != item['url']:
                    raise ValueError('Unexpected redirect: ' + response.url)
            # Directory truncation can cut a multibyte name mid-character. Preserve raw bytes;
            # reader titles/bylines come from each untruncated full poem page.
            html = raw.decode('utf-8', errors='replace')
            if item['kind'] == 'poem' and ('display-6' not in html or 'Leave Your Comment' not in html):
                raise ValueError('Poem template missing')
            if item['kind'] == 'edition' and 'poemview.php' not in html:
                raise ValueError('Edition contents missing')
            path.write_bytes(raw)
            result = dict(item, captured_at=datetime.now(timezone.utc).isoformat(),
                          sha256=hashlib.sha256(raw).hexdigest(), bytes=len(raw),
                          decoding_replacements=html.count('\ufffd'), status='captured')
            receipt_path.write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
            return result
        except Exception as exc:
            error = str(exc)
    return dict(item, status='failed', error=error)


def main():
    editions = json.loads((RESEARCH / 'captured-editions.json').read_text())
    writers = json.loads((ROOT / 'kb/research/writers/captured-profiles.json').read_text())
    items, seen = [], set()
    for edition in editions:
        folder = f'issue-{edition["number"]:02d}'
        items.append(dict(kind='edition', edition=edition['number'], url=edition['url'],
                          referer='https://kabitalive.com/archive.php', path=f'{folder}/edition.html'))
        for poem in edition['poems']:
            pid = ident(poem['url'])
            if pid in seen:
                continue
            seen.add(pid)
            items.append(dict(kind='poem', edition=edition['number'], id=pid, url=poem['url'],
                              referer=edition['url'], path=f'{folder}/poem-{pid}.html'))
    for writer in writers:
        for poem in writer['works']:
            pid = ident(poem['url'])
            if pid in seen:
                continue
            seen.add(pid)
            items.append(dict(kind='poem', edition=None, id=pid, url=poem['url'],
                              referer=writer['url'], path=f'unassigned/poem-{pid}.html'))
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        for result in pool.map(fetch, items):
            results.append(result)
            if len(results) % 25 == 0:
                print(f'{len(results)}/{len(items)} source pages preserved', flush=True)
                (RESEARCH / 'source-receipts.json').write_text(json.dumps(results, ensure_ascii=False, indent=2)+'\n')
    (RESEARCH / 'source-receipts.json').write_text(json.dumps(results, ensure_ascii=False, indent=2)+'\n')
    failed = [x for x in results if x['status'] != 'captured']
    print(json.dumps({'pages': len(results), 'poems': len(seen), 'failures': failed}, ensure_ascii=False), flush=True)
    if failed:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
