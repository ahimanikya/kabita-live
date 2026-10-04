"""Check every reader plus protected content and both pilot/rollout artwork."""
import json,re,hashlib,sys
from pathlib import Path
from datetime import datetime,timezone
R=Path(__file__).resolve().parents[3];K=Path(__file__).resolve().parent;S=R/'projects/site';ed=int(sys.argv[1]);baseline=json.loads((K/'baseline.json').read_text())
for p,h in baseline['files'].items():assert hashlib.sha256((R/p).read_bytes()).hexdigest()==h,p
assert json.loads((S/'data/poem-art-assignments.json').read_text())==baseline['generic_assignments']
direction=json.loads((S/'data/edition-art-direction.json').read_text())['poems']
for pid,d in baseline['art_direction']['poems'].items():assert direction[pid]==d,('Pilot entry changed',pid)
variants=json.loads((R/'kb/research/edition-art-pilot-2026-10-04/reader-baseline.json').read_text());routes=json.loads((S/'data/local-routes.json').read_text())
for route,v in variants.items():
 text=(S/route).read_text();assert json.loads(re.search(r'<script type="application/json" id="reading-data">(.*?)</script>',text,re.S)[1])['variants']==v,route
for pid,route in routes.items():
 text=(S/route).read_text()
 for key in ['page-bookmarks','page-bookmarks-button','reading-panel','open-focus','focus-reader','poem-secondary-links']:assert text.count(f'id="{key}"')==1,(pid,key)
 assert f'contact.html?poem={pid}' in text
for path in (K/'batches').glob('edition-*/batch.json'):
 b=json.loads(path.read_text())
 for i in b['items']:
  if i['status']!='integrated_local':continue
  assert hashlib.sha256((R/i['output']).read_bytes()).hexdigest()==i['output_sha256']
  assert hashlib.sha256((S/i['public_asset']).read_bytes()).hexdigest()==i['public_sha256']
  assert (S/'dist'/i['public_asset']).exists()
  assert i['public_asset'] in (S/'dist'/routes[str(i['poem_id'])]).read_text()
 for i in b['text_led']:
  if i['status']!='integrated_local':continue
  text=(S/routes[str(i['poem_id'])]).read_text();assert '<aside class="poem-art poem-text-context"' in text and '<figure class="poem-art' not in text
r={'result':'PASS','at':datetime.now(timezone.utc).isoformat(),'independent':False,'protected_content_cover_files':len(baseline['files']),'unchanged_stored_reader_variants':len(variants),'active_reader_controls':len(routes),'pilot_entries_unchanged':len(baseline['art_direction']['poems']),'generic_pool_unchanged':True,'master_delivery_build_assets':'PASS'}
(K/f'batches/edition-{ed}/verification.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
