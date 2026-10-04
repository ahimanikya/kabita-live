from pathlib import Path
import json,shutil,hashlib,subprocess,re
R=Path('/Users/ahimanikya/Projects/Kabita Live');C=Path('/private/tmp/kbl-final-portraits-20261004');B=Path(__file__).resolve().parent;S=C/'projects/site'
def cp(rel):
 p=C/rel;p.parent.mkdir(parents=True,exist_ok=True)
 if (R/rel).is_dir():shutil.copytree(R/rel,p,dirs_exist_ok=True,ignore=shutil.ignore_patterns('__pycache__'))
 else:shutil.copy2(R/rel,p)
base={'commit':subprocess.check_output(['git','-C',str(C),'rev-parse','HEAD']).decode().strip(),'protected':{},'variants':{}}
for folder in ['content','assets','data']:
 for p in (S/folder).rglob('*'):
  if p.is_file() and p.name!='writer-portraits.json':base['protected'][str(p.relative_to(C))]=hashlib.sha256(p.read_bytes()).hexdigest()
for n in ['runtime-config.json','styles.css','site.js','robots.txt','build-public.py']:
 p=S/n
 if p.exists():base['protected'][str(p.relative_to(C))]=hashlib.sha256(p.read_bytes()).hexdigest()
for p in S.glob('*.html'):
 m=re.search(r'<script type="application/json" id="reading-data">(.*?)</script>',p.read_text(),re.S)
 if m:base['variants'][p.name]=json.loads(m[1])['variants']
(B/'release-baseline.json').write_text(json.dumps(base,indent=2)+'\n')
d=json.loads((R/'kb/records/accepted-candidate-two-2026-10-04.json').read_text());local=json.loads((R/'projects/site/data/writer-portraits.json').read_text());mapping=json.loads((S/'data/writer-portraits.json').read_text())
for x in d['decisions']:
 mapping[str(x['writer_id'])]=local[str(x['writer_id'])]
 for n in ['', '-64','-128']:cp('projects/site/'+x['web_asset'].replace('.webp',n+'.webp'))
(S/'data/writer-portraits.json').write_text(json.dumps(mapping,ensure_ascii=False,indent=2)+'\n')
for rel in ['kb/records/accepted-candidate-two-2026-10-04.json','kb/research/writers/accepted-candidate-two-2026-10-04','kb/research/writers/portrait-edits.json','kb/research/writers/portrait-batches.json','kb/records/poet-watercolor-loop.json','kb/records/poet-watercolor-rollout.json','kb/records/likeness-decisions-2026-10-04.json','kb/research/writers/likeness-decisions-2026-10-04/build_results.py','kb/artifacts/review/likeness-decisions-2026-10-04']:cp(rel)
p=C/'kb/registers/activity.jsonl';rows=[json.loads(x) for x in p.read_text().splitlines()];event=json.loads((R/'kb/registers/activity.jsonl').read_text().splitlines()[-1]);event['id']=f'KBL-EVT-{max(int(x["id"].split("-")[-1]) for x in rows)+1:03}'
with p.open('a') as f:f.write(json.dumps(event,ensure_ascii=False)+'\n')
print('Prepared eight-portrait follow-up on',base['commit'])
