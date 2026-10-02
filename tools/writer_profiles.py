#!/usr/bin/env python3
"""Normalize browser-captured writer records; keep provenance and gaps in the KB."""
import collections
import json
import re
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'projects/site'
if not SITE.exists():
    SITE = ROOT / 'site'
RESEARCH = ROOT / 'kb/research/writers'


def ident(url):
    return int(parse_qs(urlsplit(url).query)['id'][0])


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def main():
    directory = json.loads((RESEARCH / 'live-directory.json').read_text())
    captures = json.loads((RESEARCH / 'captured-profiles.json').read_text())
    expected = {ident(x['url']) for x in directory}
    assert len(expected) == len(directory), 'Duplicate writer IDs in directory'
    by_id = {ident(x['url']): x for x in captures}
    assert len(by_id) == len(captures), 'Duplicate captures'
    assert set(by_id) <= expected, 'Unexpected writer IDs'
    repeat = collections.Counter(x.get('biography', '').strip() for x in captures)
    portrait_path = RESEARCH / 'portrait-sources.json'
    portraits = json.loads(portrait_path.read_text()) if portrait_path.exists() else []
    saved_portraits = {p['writer_id'] for p in portraits}
    profiles, queue, claims, problems = [], [], collections.defaultdict(list), []
    pattern = re.compile(r'^\d+\s+(.+?)\s*\(ISSUE#(\d+)\s*-\s*(\w+)\s+(\d{4})\)\s*$', re.I)
    for entry in directory:
        wid = ident(entry['url'])
        raw = by_id.get(wid)
        if raw is None:
            queue.append({'id': wid, 'name': entry['name'], 'capture': 'pending'})
            continue
        bio = raw.get('biography', '').strip()
        flags = []
        if bio and repeat[bio] > 1:
            flags.append('Repeated biography needs identity review')
            bio = ''
        # Personal contact details are unnecessary on public literary profiles.
        bio = re.sub(r'\b[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}\b', '', bio)
        bio = re.sub(r'(?i)(?:mobile|phone|contact|whatsapp)\s*[:：-]?\s*\+?[\d ()-]{8,}', '', bio)
        works = []
        for work in raw['works']:
            match = pattern.fullmatch(' '.join(work['label'].split()))
            if not match:
                problems.append({'writer_id': wid, 'work': work, 'problem': 'Unparsed contribution label'})
                title = re.sub(r'^\d+\s+', '', work['label']).removesuffix(' ( - )').strip()
                item = {'id': ident(work['url']), 'title': title, 'issue': None, 'month': None, 'year': None}
            else:
                title, issue, month, year = match.groups()
                item = {'id': ident(work['url']), 'title': title, 'issue': int(issue), 'month': month, 'year': int(year)}
            works.append(item)
            claims[item['id']].append(wid)
        works.sort(key=lambda x: (x['issue'] or 0, x['id']), reverse=True)
        profiles.append({'id': wid, 'name': ' '.join(raw['name'].split()), 'biography': bio,
                         'biography_kind': 'journal_supplied', 'works': works})
        queue.append({'id': wid, 'name': entry['name'], 'capture': 'complete',
                      'biography': 'captured' if bio else 'missing_or_held',
                      'independent_research': 'pending',
                      'portrait': 'original_saved' if wid in saved_portraits else 'source_url_captured' if raw.get('portrait') and not raw['portrait'].endswith('/') else 'missing',
                      'portrait_generation': 'pending', 'contributions': len(works), 'flags': flags})
    conflicts = [{'poem_id': pid, 'writer_ids': sorted(set(ids))} for pid, ids in claims.items() if len(set(ids)) > 1]
    summary = {'captured_on': '2026-09-29', 'directory_writers': len(directory), 'captured_profiles': len(captures),
               'biographies': sum(bool(p['biography']) for p in profiles),
               'missing_biographies': sum(not p['biography'] for p in profiles),
               'contribution_links': sum(len(p['works']) for p in profiles), 'distinct_poems': len(claims),
               'contribution_conflicts': conflicts, 'unparsed': problems,
               'independently_researched_profiles': 0, 'new_artistic_portraits': 0,
               'source_portraits_saved': len(saved_portraits),
               'scope': 'Browser-visible profiles and contribution metadata; full poem text is not captured.'}
    save(SITE / 'data/writer-profiles.json', profiles)
    save(RESEARCH / 'research-queue.json', queue)
    save(RESEARCH / 'capture-summary.json', summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
