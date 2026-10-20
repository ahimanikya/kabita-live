"""Acquire official Google Fonts originals and verify lossless WOFF2 delivery."""
import hashlib
import json
from pathlib import Path
import urllib.request
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parents[4]
FONT_ROOT = ROOT / 'projects/site/assets/fonts'
records = []
for folder, family in [('newsreader', 'Newsreader'), ('literata', 'Literata')]:
    entries = json.load(urllib.request.urlopen('https://api.github.com/repos/google/fonts/contents/ofl/' + folder, timeout=30))
    for entry in entries:
        name = entry['name']
        if not (name.endswith('.ttf') or name == 'OFL.txt'):
            continue
        payload = urllib.request.urlopen(entry['download_url'], timeout=30).read()
        assert hashlib.sha1(b'blob ' + str(len(payload)).encode() + b'\0' + payload).hexdigest() == entry['sha']
        local = family + '-OFL.txt' if name == 'OFL.txt' else family + ('-Italic' if 'Italic' in name else '') + '-Variable.ttf'
        target = FONT_ROOT / local
        if target.exists():
            assert target.read_bytes() == payload, 'Existing font differs: ' + local
        else:
            target.write_bytes(payload)
        record = {'family': family, 'source_url': entry['download_url'], 'git_blob_sha': entry['sha'], 'local': str(target.relative_to(ROOT)), 'sha256': hashlib.sha256(payload).hexdigest(), 'bytes': len(payload)}
        if name.endswith('.ttf'):
            font = TTFont(target)
            font.flavor = 'woff2'
            output = target.with_suffix('.woff2')
            font.save(output)
            original, converted = TTFont(target), TTFont(output)
            assert original.getBestCmap() == converted.getBestCmap()
            assert original.getGlyphOrder() == converted.getGlyphOrder()
            for tag in ('GSUB', 'GPOS', 'GDEF', 'fvar'):
                if tag in original:
                    assert original[tag].compile(original) == converted[tag].compile(converted)
            record.update(woff2=str(output.relative_to(ROOT)), woff2_sha256=hashlib.sha256(output.read_bytes()).hexdigest(), woff2_bytes=output.stat().st_size, glyphs=len(original.getGlyphOrder()), axes=[a.axisTag for a in original['fvar'].axes], shaping_preserved=True)
        records.append(record)
Path(__file__).with_name('font-provenance.json').write_text(json.dumps(records, indent=2) + '\n')
print('Saved official font sources/licences and verified four full-glyph WOFF2 conversions.')
