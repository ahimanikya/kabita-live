"""Verify deployed portrait references and bytes; do not download media to disk."""
from pathlib import Path
import json,hashlib,re,urllib.request,concurrent.futures,datetime
ROOT=Path(__file__).resolve().parents[4]
HERE=Path(__file__).resolve().parent
DIST=Path('/private/tmp/kbl-selective-portraits-20261003/projects/site/dist')
q=json.loads((ROOT/'kb/records/selective-portrait-fixes-2026-10-03.json').read_text())
BASE='https://ahimanikya.github.io/kabita-live/'
def fetch(path):
 req=urllib.request.Request(BASE+path+'?portrait-check='+q['release_commit'][:12],headers={'Cache-Control':'no-cache','User-Agent':'KabitaLive-publication-verification'})
 with urllib.request.urlopen(req,timeout=45) as response:return response.read(),response.status
def hashcheck(path):
 raw,status=fetch(path);expected=hashlib.sha256((DIST/path).read_bytes()).hexdigest();actual=hashlib.sha256(raw).hexdigest()
 return {'path':path,'status':status,'sha256':actual,'expected_sha256':expected,'pass':actual==expected}
paths=[]
for r in q['items']:
 if r.get('selected_asset'):
  paths.extend(r['selected_asset'].replace('.webp',suffix) for suffix in ['.webp','-128.webp','-64.webp'])
paths+=['runtime-config.json','assets/analytics.js','assets/engagement.js']
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:assets=list(pool.map(hashcheck,paths))
profiles=[]
for r in q['items']:
 if not r.get('selected_asset'):continue
 route='poet-kshanika.html' if r['writer_id']==337 else f'poet-{r["writer_id"]}.html'
 raw,status=fetch(route);text=raw.decode();robots=re.search(r'<meta name="robots" content="([^"]+)"',text)
 profiles.append({'writer_id':r['writer_id'],'route':route,'status':status,'selected_portrait_present':r['selected_asset'] in text,'noindex_preserved':bool(robots and 'noindex' in robots[1]),'pass':r['selected_asset'] in text and bool(robots and 'noindex' in robots[1])})
directory=fetch('poets.html')[0].decode();reader=fetch('assets/reading-all.json')[0].decode()
directory_ok=all(r['selected_asset'] in directory for r in q['items'] if r.get('selected_asset'))
reader_ok=all(r['selected_asset'].replace('.webp','-64.webp') in reader for r in q['items'] if r.get('selected_asset'))
result={'result':'PASS' if all(x['pass'] for x in assets+profiles) and directory_ok and reader_ok else 'FAIL','verified_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'release_commit':q['release_commit'],'workflow_url':q['workflow_url'],'assets':assets,'profiles':profiles,'directory_thumbnails':directory_ok,'collection_reader_portraits':reader_ok,'independent':False}
(HERE/'live-verification.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ('assets','profiles')})+'\n'+str(len(assets))+' asset/config hashes; '+str(len(profiles))+' live profiles')
raise SystemExit(result['result']!='PASS')
