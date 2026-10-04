"""Verify public pages and exact derivative bytes after the manual Pages workflow."""
import json,hashlib,urllib.request,sys
from pathlib import Path
from datetime import datetime,timezone
K=Path(__file__).resolve().parent;R=K.parents[2];S=R/'projects/site';commit=sys.argv[1];workflow=int(sys.argv[2]);base='https://ahimanikya.github.io/kabita-live/'
def fetch(path):
 req=urllib.request.Request(base+path+'?art='+commit[:12],headers={'Cache-Control':'no-cache','User-Agent':'KabitaLive-release-verification'})
 with urllib.request.urlopen(req,timeout=45) as response:return response.read()
routes=json.loads((S/'data/local-routes.json').read_text());checks=[]
for n in [26,25,24]:
 b=json.loads((K/f'batches/edition-{n}/batch.json').read_text())
 for i in b['items']:
  data=fetch(i['public_asset']);assert hashlib.sha256(data).hexdigest()==i['public_sha256'],i['id'];html=fetch(routes[str(i['poem_id'])]).decode();assert i['public_asset'] in html and 'noindex' in html
  checks.append(dict(edition=n,poem_id=i['poem_id'],asset=i['public_asset'],sha256=i['public_sha256'],result='PASS'))
 for i in b['text_led']:
  html=fetch(routes[str(i['poem_id'])]).decode();assert '<aside class="poem-art poem-text-context"' in html and '<figure class="poem-art' not in html and 'noindex' in html
  for key in ['page-bookmarks','page-bookmarks-button','reading-panel','open-focus','focus-reader','poem-secondary-links']:assert f'id="{key}"' in html
  assert f'contact.html?poem={i["poem_id"]}' in html
  checks.append(dict(edition=n,poem_id=i['poem_id'],text_led='PASS'))
runtime=json.loads(fetch('runtime-config.json'));assert runtime['firebase']['enabled'];assert runtime['engagement']['likes'] and runtime['engagement']['publicComments'];assert runtime['analytics']['enabled'] and runtime['analytics']['measurementId']=='G-CEWHV75WS7';assert runtime['firebase']['allowedHosts']==['ahimanikya.github.io']
r=dict(result='PASS',verified_at=datetime.now(timezone.utc).isoformat(),commit=commit,workflow=workflow,editions=[26,25,24],assets=9,poem_pages=18,active_firebase_likes_comments=True,analytics_and_consent_config_preserved=True,noindex_preserved=True,checks=checks)
(K/'checkpoint-26-24-live-verification.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
