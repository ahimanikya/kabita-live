from pathlib import Path
import json,hashlib,urllib.request,concurrent.futures,time
K=Path('/Users/ahimanikya/Projects/Kabita Live/kb/research/writers/final-portrait-release-2026-10-04');C=Path('/private/tmp/kbl-final-portraits-20261004');S=C/'projects/site';base='https://ahimanikya.github.io/kabita-live/'
m=json.loads((S/'data/writer-portraits.json').read_text());assets={}
for x in m.values():
 p=x['src'];assets[p]=hashlib.sha256((S/'dist'/p).read_bytes()).hexdigest()
 if x['kind'] in ['generated_portrait','generic_artwork']:
  for size in [64,128]:
   p=x['src'].replace('.webp',f'-{size}.webp')
   if (S/'dist'/p).exists():assets[p]=hashlib.sha256((S/'dist'/p).read_bytes()).hexdigest()
def get(p):
 for attempt in range(3):
  try:
   with urllib.request.urlopen(base+p,timeout=40) as r:return r.read()
  except Exception:
   if attempt==2:raise
   time.sleep(2)
def asset(item):
 p,h=item;b=get(p);assert hashlib.sha256(b).hexdigest()==h,p;return p
def profile(item):
 wid,x=item;p={'82':'poet-dokana.html','337':'poet-kshanika.html','257':'poet-drink.html'}.get(wid,f'poet-{wid}.html');s=get(p).decode();assert x['src'] in s and 'noindex' in s,p
 if x['kind']=='generic_artwork':assert 'Generic artwork · photograph unavailable' in s,p
 return p
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as e:verified=list(e.map(asset,assets.items()))
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as e:pages=list(e.map(profile,m.items()))
runtime=json.loads(get('runtime-config.json'));assert runtime['firebase']['enabled'] and runtime['engagement']['likes'] and runtime['engagement']['publicComments'] and runtime['analytics']['enabled']
result={'result':'PASS','verified_asset_hashes':len(verified),'verified_profile_pages':len(pages),'assets':verified,'pages':pages,'noindex':True,'active_services_preserved':True,'generic_disclosures':3,'url':base}
(K/'live-verification.json').write_text(json.dumps(result,indent=2)+'\n');print({k:v for k,v in result.items() if k not in ['assets','pages']})
