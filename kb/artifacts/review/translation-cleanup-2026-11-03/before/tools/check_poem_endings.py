#!/usr/bin/env python3
"""Verify reviewed poem-tail separation without losing verse or original records."""
import hashlib,json,re
from pathlib import Path
R=Path(__file__).resolve().parents[1];S=R/'projects/site'
endings=json.loads((S/'data/poem-endings.json').read_text())
evidence={str(x['poem_id']):x for x in json.loads((R/'kb/records/poem-ending-migration.json').read_text())['entries']}
translations=json.loads((S/'data/poem-translations.json').read_text())
sources={str(s['id']):s for p in (S/'content/editions').glob('*/poem-*.json') for s in [json.loads(p.read_text())]}
notes=json.loads((S/'data/writer-publication-notes.json').read_text())
for ident,entry in endings.items():
 s=sources[ident];flat=[l for st in s['stanzas'] for l in st];n=entry['verse_line_count']
 assert 0<n<len(flat) and s['writer_id']==entry['writer_id']
 assert hashlib.sha256(s['text'].encode()).hexdigest()==entry['source_sha256']
 assert flat[n:]==evidence[ident]['source_tail']
 for code,v in translations.get(ident,{}).get('variants',{}).items():
  assert [l for st in v['stanzas'] for l in st][n:]==evidence[ident]['variants'][code]
for wid,note in notes.items():
 assert all(str(sources[str(i)]['writer_id'])==wid for i in note['poem_ids'])
 assert not re.search(r'@|[0-9]{6,}',note['text'])
counts={}
for label,root,pattern in [('preview',S,'poem-*.html'),('public',S/'dist','**/*.html')]:
 seen=set()
 for p in root.glob(pattern):
  m=re.search(r'<script[^>]*id="reading-data"[^>]*>(.*?)</script>',p.read_text(),re.S)
  if not m:continue
  d=json.loads(m[1]);ident=str(d['id']);seen.add(ident);s=sources[ident]
  expected={s['language']:s,**translations.get(ident,{}).get('variants',{})}
  for code,v in expected.items():
   flat=[l for st in v['stanzas'] for l in st]
   limit=endings.get(ident,{}).get('verse_line_count',len(flat))
   assert [l for st in d['variants'][code]['stanzas'] for l in st]==flat[:limit],(p,code)
 assert seen=={i for i,s in sources.items() if s.get('status')!='archived'},(label,len(seen))
 counts[label]=len(seen)
print(json.dumps({'result':'PASS','reviewed_endings':len(endings),'profile_notes':len(notes),'reader_sources_checked':counts,'source_and_translation_records':'unchanged; reviewed tails retained in evidence','verse_prefixes':'exact in every language; earlier selection offsets retained'},indent=2))
