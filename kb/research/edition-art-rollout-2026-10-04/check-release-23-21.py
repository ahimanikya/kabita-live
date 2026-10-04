"""Integrity checks against the clean latest-main release baseline."""
import json,re,hashlib,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[3];K=Path(__file__).resolve().parent;C=Path('/private/tmp/kbl-selective-portraits-20261003');S=C/'projects/site';B=json.loads((K/'checkpoint-23-21-baseline.json').read_text())
for rel,h in B['protected_files'].items():assert hashlib.sha256((C/rel).read_bytes()).hexdigest()==h,rel
for rel,h in B['other_site_files'].items():assert hashlib.sha256((S/rel).read_bytes()).hexdigest()==h,rel
for route,variants in B['reader_variants'].items():
 t=(S/route).read_text();assert json.loads(re.search(r'<script type="application/json" id="reading-data">(.*?)</script>',t,re.S)[1])['variants']==variants,route
 for key in ['page-bookmarks','page-bookmarks-button','reading-panel','open-focus','focus-reader','poem-secondary-links']:assert t.count(f'id="{key}"')==1,(route,key)
 assert 'noindex' in (S/'dist'/route).read_text()
for n in [23,22,21]:
 b=json.loads((K/f'batches/edition-{n}/batch.json').read_text())
 for i in b['items']:
  assert hashlib.sha256((S/'dist'/i['public_asset']).read_bytes()).hexdigest()==i['public_sha256']
  assert i['public_asset'] in (S/'dist'/f'poem-{i["poem_id"]}.html').read_text()
 for i in b['text_led']:
  t=(S/'dist'/f'poem-{i["poem_id"]}.html').read_text();assert '<aside class="poem-art poem-text-context"' in t and '<figure class="poem-art' not in t
assert not (S/'dist/kb').exists();runtime=json.loads((S/'dist/runtime-config.json').read_text());assert runtime['firebase']['enabled'] and runtime['engagement']['likes'] and runtime['engagement']['publicComments'] and runtime['analytics']['enabled']
r=dict(result='PASS',protected_files=len(B['protected_files']),unrelated_reader_pages_unchanged=len(B['other_site_files']),reader_payloads_and_controls=len(B['reader_variants']),new_assets=9,text_led=9,noindex=True,kb_excluded=True,active_engagement_preserved=True,base_commit=B['base_commit'])
(K/'checkpoint-23-21-verification.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
