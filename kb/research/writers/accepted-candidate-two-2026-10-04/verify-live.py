from pathlib import Path
import json,urllib.request,hashlib,concurrent.futures
R=Path('/Users/ahimanikya/Projects/Kabita Live');B=Path(__file__).resolve().parent;S=Path('/private/tmp/kbl-final-portraits-20261004/projects/site/dist');base='https://ahimanikya.github.io/kabita-live/'
d=json.loads((R/'kb/records/accepted-candidate-two-2026-10-04.json').read_text())
def get(p):
 with urllib.request.urlopen(base+p,timeout=40) as r:return r.read()
def check(x):
 i=x['writer_id'];route=f'poet-{i}.html';s=get(route).decode();assert x['web_asset'] in s and 'noindex' in s,route
 assets=[]
 for suffix in ['', '-64','-128']:
  p=x['web_asset'].replace('.webp',suffix+'.webp');h=hashlib.sha256(get(p)).hexdigest();assert h==hashlib.sha256((S/p).read_bytes()).hexdigest(),p;assets.append({'asset':p,'sha256':h})
 return {'writer_id':i,'profile':route,'assets':assets}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:rows=list(ex.map(check,d['decisions']))
runtime=json.loads(get('runtime-config.json'));assert runtime['firebase']['enabled'] and runtime['engagement']['likes'] and runtime['engagement']['publicComments'] and runtime['analytics']['enabled']
(B/'live-verification.json').write_text(json.dumps({'result':'PASS','profiles':8,'asset_hashes':24,'noindex':True,'active_services_preserved':True,'rows':rows,'url':base},indent=2)+'\n');print('PASS8 live profiles,24 asset hashes,noindex and active services')
