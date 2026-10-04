from pathlib import Path
import json,hashlib,urllib.request,re,sys
from concurrent.futures import ThreadPoolExecutor
R=Path('/Users/ahimanikya/Projects/Kabita Live');K=R/'kb/research/poem-ending-release-2026-10-04';C=Path(sys.argv[1]);S=C/'projects/site';v=json.loads((K/'verification.json').read_text());base='https://ahimanikya.github.io/kabita-live/'
files=list(v['assets'])+['assets/reading-all.json','assets/reading-editions/issue-7.json','assets/reading-editions/issue-47.json','runtime-config.json']
poems=json.loads((S/'assets/reading-all.json').read_text())['poems'];ids={201,818,809,385,640,641};pages=[p['route'] for p in poems if p['id'] in ids]
def fetch(name):
 req=urllib.request.Request(base+name+'?ending=48934b0e',headers={'User-Agent':'Kabita-Live-publication-verification'})
 with urllib.request.urlopen(req,timeout=30) as resp:raw=resp.read();assert resp.status==200
 return name,raw
responses=dict(ThreadPoolExecutor(max_workers=4).map(fetch,files+pages))
checks={}
for name in files:
 raw=responses[name];expected=(S/'dist'/name).read_bytes()
 if name=='runtime-config.json':assert json.loads(raw)==json.loads(expected),name
 else:assert raw==expected,name
 checks[name]=hashlib.sha256(raw).hexdigest()
for route in pages:
 html=responses[route].decode();local=(S/'dist'/route).read_text();assert 'noindex,nofollow' in html
 rd=lambda h:json.loads(re.search(r'id="reading-data">(.*?)</script>',h,re.S)[1])
 assert rd(html)==rd(local),route
 for cls in ['poem-closing-mark','poem-step-title']:assert html.count('class="'+cls+'"')==local.count('class="'+cls+'"'),(route,cls)
 assert re.findall(r'<img\b[^>]+src="([^"]+)"',html)==re.findall(r'<img\b[^>]+src="([^"]+)"',local),route
result={'result':'PASS','url':base,'sample_poem_pages':pages,'all_reader_poems':len(poems),'assets_and_payload_hashes':checks,'noindex':True,'runtime_exact_match':True,'sample_published_art_and_portraits_preserved':True}
(K/'live-verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
