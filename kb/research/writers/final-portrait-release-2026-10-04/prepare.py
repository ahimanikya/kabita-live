from pathlib import Path
import json,shutil,hashlib,subprocess,re,datetime
R=Path('/Users/ahimanikya/Projects/Kabita Live');C=Path('/private/tmp/kbl-final-portraits-20261004');K=R/'kb/research/writers/final-portrait-release-2026-10-04';S=C/'projects/site'
def save(p,d):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def cp(rel):
 a=R/rel;b=C/rel;b.parent.mkdir(parents=True,exist_ok=True)
 if a.is_dir():shutil.copytree(a,b,dirs_exist_ok=True,ignore=shutil.ignore_patterns('__pycache__'))
 else:shutil.copy2(a,b)
assert not subprocess.check_output(['git','-C',str(C),'status','--porcelain']).strip()
base={'commit':subprocess.check_output(['git','-C',str(C),'rev-parse','HEAD']).decode().strip(),'protected':{},'variants':{}}
for folder in ['content','assets']:
 for p in (S/folder).rglob('*'):
  if p.is_file():base['protected'][str(p.relative_to(C))]=hashlib.sha256(p.read_bytes()).hexdigest()
for p in (S/'data').glob('*.json'):
 if p.name!='writer-portraits.json':base['protected'][str(p.relative_to(C))]=hashlib.sha256(p.read_bytes()).hexdigest()
for n in ['runtime-config.json','styles.css','site.js','robots.txt','build-public.py','astro.config.mjs']:
 p=S/n
 if p.exists():base['protected'][str(p.relative_to(C))]=hashlib.sha256(p.read_bytes()).hexdigest()
for p in S.glob('*.html'):
 m=re.search(r'<script type="application/json" id="reading-data">(.*?)</script>',p.read_text(),re.S)
 if m:base['variants'][p.name]=json.loads(m[1])['variants']
save(K/'baseline.json',base)
q=json.loads((R/'kb/research/writers/portrait-batches.json').read_text());assert q['counts']['pending_photographs']==0 and all(b['verification']=='passed' for b in q['batches'])
for rel in ['projects/site/data/writer-portraits.json','projects/site/assets/writers','kb/artifacts/artwork/writer-portraits','kb/research/writers/portrait-batches','kb/research/writers/portrait-batches.json','kb/research/writers/portrait-edits.json','kb/records/poet-watercolor-loop.json','kb/records/poet-watercolor-rollout.json','kb/records/portrait-human-natural-2026-10-03.json','kb/records/generic-portrait-placeholders-2026-10-04.json','kb/research/writers/generic-placeholders-2026-10-04','kb/records/likeness-decisions-2026-10-04.json','kb/research/writers/likeness-decisions-2026-10-04','kb/artifacts/review/likeness-decisions-2026-10-04','kb/artifacts/review/likeness-holds-2026-10-04','kb/research/writers/likeness-holds-review-2026-10-04','projects/site/author-pages.py','tools/check_author_pages.py']:
 cp(rel)
# Only generic-avatar rendering is transferred; retain published directory wording.
p=S/'poet_directory.py';s=p.read_text();local=(R/'projects/site/poet_directory.py').read_text();start='     generic=portraits.get(wid,{}).get';chunk=local[local.index(start):local.index('     body=',local.index(start))];a=s.index('     pic=');z=s.index('     body=',a);p.write_text(s[:a]+chunk+s[z:])
record=dict(recorded_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),status='prepared',base_commit=base['commit'],release_checkout=str(C),artistic_portraits=416,generic_artwork_profiles=3,likeness_holds=q['likeness_holds'],missing_source_writer_ids=[233,258,416],independent_likeness_review='pending',authorization='Final portrait rollout deployment and user-imported likeness decisions; preserve unrelated published changes',resume='Build isolated release; verify scope; commit/push without force; manual preview Pages workflow; live checks; pause heartbeat only after success')
save(R/'kb/records/final-portrait-deployment-2026-10-04.json',record);cp('kb/records/final-portrait-deployment-2026-10-04.json');cp('kb/research/writers/final-portrait-release-2026-10-04')
p=C/'kb/registers/activity.jsonl';rows=[json.loads(x) for x in p.read_text().splitlines()];n=max(int(x['id'].split('-')[-1]) for x in rows)+1
with p.open('a') as f:f.write(json.dumps(dict(id=f'KBL-EVT-{n:03}',recorded_at=record['recorded_at'],actor={'kind':'ai_assistant','name':'Current assistant; self-review'},summary='Final portrait queue processed and verified:416 artistic portraits,8 likeness holds retaining photos,3 labelled generic placeholders with missing-source records open. Imported35 review decisions applied:23 selected candidates and10 successful retries;2 retry holds retained. No independent author confirmation claimed.',refs=['KBL-WORK-004'],evidence=['records/final-portrait-deployment-2026-10-04.json','records/likeness-decisions-2026-10-04.json'],next_action='Verify scoped release, deploy manual public preview and check live assets.') )+'\n')
print('Prepared final release on',base['commit'])
