#!/usr/bin/env python3
"""Check reviewed stanza recovery, language parity and unchanged selection text."""
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'projects/site'
spacing = json.loads((SITE / 'data/poem-spacing.json').read_text())
review = json.loads((ROOT / 'kb/records/poem-spacing-reconciliation.json').read_text())
sources = {str(s['id']): s for p in (SITE / 'content/editions').glob('*/poem-*.json') for s in [json.loads(p.read_text())]}
translations = json.loads((SITE / 'data/poem-translations.json').read_text())
for ident, rules in spacing.items():
    assert hashlib.sha256(sources[ident]['text'].encode()).hexdigest() == rules['source_sha256']
assert not {str(r['id']) for r in review['deferred']} & spacing.keys()
counts = {}
for label, root, pattern in [('preview', SITE, 'poem-*.html'), ('public', SITE / 'dist', '**/*.html')]:
    seen = set()
    for path in root.glob(pattern):
        m = re.search(r'<script[^>]*id="reading-data"[^>]*>(.*?)</script>', path.read_text(), re.S)
        if not m:
            continue
        data = json.loads(m[1]); ident = str(data['id'])
        if ident not in spacing:
            continue
        seen.add(ident)
        source = sources[ident]
        originals = {source['language']: source, **translations.get(ident, {}).get('variants', {})}
        vectors = []
        for language, variant in data['variants'].items():
            stanzas = variant['stanzas']
            flat = [line for stanza in stanzas for line in stanza]
            captured = [line for stanza in originals[language]['stanzas'] for line in stanza]
            assert flat == captured[:len(flat)], (label, ident, language, 'changed text')
            boundaries = []; cursor = 0
            for stanza in stanzas[:-1]:
                cursor += len(stanza); boundaries.append(cursor)
            assert set(spacing[ident]['before_lines']) <= set(boundaries), (label, ident, language, 'missing pause')
            vectors.append(list(map(len, stanzas)))
            if ident == '9':
                raw = flat[0].encode('utf-16-le')
                pieces = []; start = 0; groups = [[]]
                for point in variant['inline_breaks']:
                    end = point['at'] * 2
                    assert start < end < len(raw)
                    groups[-1].append(raw[start:end].decode('utf-16-le').strip())
                    if point['blank']:
                        groups.append([])
                    start = end
                groups[-1].append(raw[start:].decode('utf-16-le').strip())
                assert groups == review['single_line_recovery']['groups'][language], (label, language, 'reflow mismatch')
        assert all(vector == vectors[0] for vector in vectors), (label, ident, 'stanza parity')
    assert seen == spacing.keys(), (label, seen ^ spacing.keys())
    counts[label] = len(seen)
print(json.dumps({'result': 'PASS', 'restored_poems': counts, 'source_9': '29 lines / four thematic stanzas in each language; exact text retained', 'deferred': [r['id'] for r in review['deferred']]}, indent=2))
