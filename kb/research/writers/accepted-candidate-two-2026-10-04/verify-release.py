from pathlib import Path
import json,hashlib,re,subprocess
R=Path('/Users/ahimanikya/Projects/Kabita Live');K=R/'kb/research/writers/accepted-candidate-two-2026-10-04';C=Path('/private/tmp/kbl-final-portraits-20261004');S=C/'projects/site';B=json.loads((K/'release-baseline.json').read_text())
def strip_portraits(x):
 if isinstance(x,dict):return {k:strip_portraits(v) for k,v in x.items() if k!='portrait'}
 if isinstance(x,list):return [strip_portraits(v) for v in x]
 return x
for p,h in B['protected'].items():
 if hashlib.sha256((C/p).read_bytes()).hexdigest()==h:continue
 assert '/assets/reading-' in p and p.endswith('.json'),p
 rel=str((C/p).resolve().relative_to(C))
 old=json.loads(subprocess.check_output(['git','-C',str(C),'show',B['commit']+':'+rel]))
 assert strip_portraits(old)==strip_portraits(json.loads((C/p).read_text())),p
for route,v in B['variants'].items():
 s=(S/route).read_text();assert json.loads(re.search(r'<script type="application/json" id="reading-data">(.*?)</script>',s,re.S)[1])['variants']==v,route
 if (S/'dist'/route).exists():assert 'noindex' in (S/'dist'/route).read_text()
q=json.loads((C/'kb/research/writers/portrait-batches.json').read_text());m=json.loads((S/'data/writer-portraits.json').read_text());assert sum(x['kind']=='generated_portrait' for x in m.values())==424
assert len(q['likeness_holds'])==0
for h in q['likeness_holds']:assert m[str(h['writer_id'])]['kind']=='journal_photo'
for i in [233,258,416]:assert m[str(i)]['kind']=='generic_artwork' and 'Generic artwork · photograph unavailable' in (S/'dist'/f'poet-{i}.html').read_text()
assets={}
for wid,x in m.items():
 p=x['src'];assert (S/'dist'/p).is_file(),p;assets[p]=hashlib.sha256((S/'dist'/p).read_bytes()).hexdigest()
 for name in ['thumbnail','thumbnail_128']:
  if x.get(name):p=x[name];assert (S/'dist'/p).is_file();assets[p]=hashlib.sha256((S/'dist'/p).read_bytes()).hexdigest()
assert not (S/'dist/kb').exists()
runtime=json.loads((S/'dist/runtime-config.json').read_text());runtime['analytics'].pop('basePath',None);runtime['analytics'].pop('publicPages',None);assert runtime==json.loads((S/'runtime-config.json').read_text())
for fname in ['/tmp/kbl-accepted-release-authors.json','/tmp/kbl-accepted-release-editions.json']:assert json.loads(Path(fname).read_text())['result']=='PASS'
record={'result':'PASS','protected_file_hashes':len(B['protected']),'unchanged_poetry_payloads':len(B['variants']),'artistic_portraits':424,'likeness_holds':0,'generic_artwork':3,'public_assets':assets,'noindex':True,'runtime_and_published_art_preserved':True,'kb_excluded':True}
(K/'verification.json').write_text(json.dumps(record,indent=2)+'\n');print({k:v for k,v in record.items() if k!='public_assets'})
