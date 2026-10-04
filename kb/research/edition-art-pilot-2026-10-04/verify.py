"""Verify the pilot without treating generation counts as completion."""
import json,hashlib,re,sys
from pathlib import Path
from datetime import datetime,timezone
R=Path(__file__).resolve().parents[3];K=Path(__file__).resolve().parent;S=R/'projects/site'
q=json.loads((K/'queue.json').read_text());b=json.loads((K/'baseline.json').read_text());routes=json.loads((S/'data/local-routes.json').read_text());direction=json.loads((S/'data/edition-art-direction.json').read_text())['poems']
for kind in ['poem_files','cover_files']:
 for p,digest in b[kind].items():assert hashlib.sha256((R/p).read_bytes()).hexdigest()==digest,p
assert json.loads((S/'data/poem-art-assignments.json').read_text())['assignments']==b['assignments']
reader_base=json.loads((K/'reader-baseline.json').read_text())
for route in routes.values():
 text=(S/route).read_text()
 for ident in ['page-bookmarks','page-bookmarks-button','open-focus','focus-reader','reading-panel','poem-secondary-links']:
  assert text.count(f'id="{ident}"')==1,(route,ident)
for name,variants in reader_base.items():
 text=(S/name).read_text();m=re.search(r'<script type="application/json" id="reading-data">(.*?)</script>',text,re.S)
 assert json.loads(m[1])['variants']==variants,name
for pid,d in direction.items():
 text=(S/routes[pid]).read_text()
 for ident in ['page-bookmarks','page-bookmarks-button','open-focus','focus-reader','reading-panel','poem-secondary-links']:
  assert text.count(f'id="{ident}"')==1,(pid,ident)
 assert f'contact.html?poem={pid}' in text
 assert 'data-engagement' in text or 'id="poem-engagement"' in text or 'class="poem-engagement"' in text
 if d['mode']=='text':
  assert '<aside class="poem-art poem-text-context"' in text
  assert '<figure class="poem-art' not in text
 else:
  assert d['src'] in text
  assert d['src'] in (S/'dist'/routes[pid]).read_text()
  assert (S/'dist'/d['src']).is_file()
  i=next(x for x in q['items'] if x['poem_id']==int(pid))
  assert hashlib.sha256((S/d['src']).read_bytes()).hexdigest()==i['public_sha256']
  assert hashlib.sha256((R/i['output']).read_bytes()).hexdigest()==i['output_sha256']
result={'result':'PASS','recorded_at':datetime.now(timezone.utc).isoformat(),'independent':False,'unchanged_poem_source_files':len(b['poem_files']),'unchanged_cover_assets':len(b['cover_files']),'unchanged_reader_variants':len(reader_base),'generic_assignments_unchanged':len(b['assignments']),'directed_pages':len(direction),'integrated_artworks':sum(i['status']=='integrated_local' for i in q['items']),'text_led_pages':sum(i['status']=='integrated_local' for i in q['text_led']),'checks':['Source and cover SHA256 integrity','All reader variants unchanged','New art outside the generic assignment pool','Exactly one set of reader controls','Editor link and engagement markup preserved','Text-led pages have no empty artwork figures','Master and delivery hashes match']}
(K/f'verification-{sys.argv[1]}.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
