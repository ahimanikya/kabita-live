"""Prepare the authorized three-edition release on a clean latest-main checkout."""
import json,shutil,hashlib,re,subprocess
from pathlib import Path
from datetime import datetime,timezone
R=Path(__file__).resolve().parents[3];C=Path('/private/tmp/kbl-selective-portraits-20261003');K=Path(__file__).resolve().parent;S=R/'projects/site';T=C/'projects/site';now=datetime.now(timezone.utc).isoformat()
def git(*args):return subprocess.check_output(['git','-C',str(C),*args]).decode().strip()
def save(p,d):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
assert not git('status','--porcelain'),'Checkout is owned or dirty; stop'
assert git('rev-parse','HEAD')==git('rev-parse','origin/main'),'Refresh clean base first'
batches=[json.loads((K/f'batches/edition-{n}/batch.json').read_text()) for n in [41,40,39]]
assert all(b['status']=='verified_local_pending_publication' for b in batches)
routes=json.loads((T/'data/local-routes.json').read_text());selected={routes[str(i['poem_id'])] for b in batches for i in b['items']+b['text_led']}
baseline=dict(base_commit=git('rev-parse','HEAD'),protected_files={},reader_variants={},other_site_files={},selected_pages=sorted(selected))
for folder in ['content/editions','assets/covers','assets/writers']:
 for p in (T/folder).rglob('*'):
  if p.is_file():baseline['protected_files'][str(p.relative_to(C))]=hashlib.sha256(p.read_bytes()).hexdigest()
for name in ['runtime-config.json','data/writer-portraits.json','data/poem-art-assignments.json','data/poem-art-library.json','styles.css','site.js','robots.txt']:
 p=T/name
 if p.exists():baseline['protected_files'][str(p.relative_to(C))]=hashlib.sha256(p.read_bytes()).hexdigest()
for route in routes.values():
 text=(T/route).read_text();baseline['reader_variants'][route]=json.loads(re.search(r'<script type="application/json" id="reading-data">(.*?)</script>',text,re.S)[1])['variants']
 if route not in selected:baseline['other_site_files'][route]=hashlib.sha256((T/route).read_bytes()).hexdigest()
save(K/'checkpoint-41-39-baseline.json',baseline)
manifest=json.loads((T/'data/edition-art-direction.json').read_text());local=json.loads((S/'data/edition-art-direction.json').read_text())
for b in batches:
 for i in b['items']+b['text_led']:
  pid=str(i['poem_id']);assert pid not in manifest['poems'],'Do not overwrite a concurrent explicit assignment';manifest['poems'][pid]=local['poems'][pid]
 for i in b['items']:
  source=S/i['public_asset'];target=T/i['public_asset'];target.parent.mkdir(parents=True,exist_ok=True);assert not target.exists();shutil.copy2(source,target)
save(T/'data/edition-art-direction.json',manifest)
record_path=R/'kb/records/edition-art-rollout-2026-10-04.json';record=json.loads(record_path.read_text());record['current_publication']=dict(id='checkpoint-41-39',status='prepared',editions=[41,40,39],artworks=9,text_led=9,base_commit=baseline['base_commit'],release_checkout=str(C),prepared_at=now);save(record_path,record)
for rel in ['kb/research/edition-art-rollout-2026-10-04','kb/artifacts/artwork/edition-art-rollout-2026-10-04']:
 shutil.copytree(R/rel,C/rel,dirs_exist_ok=True,ignore=shutil.ignore_patterns('__pycache__'))
shutil.copy2(record_path,C/record_path.relative_to(R))
p=C/'kb/registers/activity.jsonl';events=[json.loads(s) for s in p.read_text().splitlines() if s.strip()];eid=max(int(x['id'].split('-')[-1]) for x in events)+1
with p.open('a') as f:f.write(json.dumps(dict(id=f'KBL-EVT-{eid:03}',recorded_at=now,actor=dict(kind='ai_assistant',name='Current assistant; same-assistant art review'),summary='Prepared authorized editions41/40/39 checkpoint:9 Human Natural / Poetic Natural interior artworks and9 text-led poem openings. All41 listed poems and one unlisted source read before planning; full snapshots, exact prompts, masters/hashes and desktop/mobile self-review retained. Latest remote portraits, active Firebase engagement, analytics consent, historical covers and poetry preserved.',refs=['KBL-WORK-022','KBL-DEC-046'],evidence=['records/edition-art-rollout-2026-10-04.json'],next_action='Build, validate, push and publish through the manual preview workflow; verify live hashes.'))+'\n')
print('Prepared scoped18-page checkpoint on',baseline['base_commit'])
