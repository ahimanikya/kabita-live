"""Prepare only the approved pilot on the clean, current remote release checkout."""
import json,shutil,hashlib,re,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[3];C=Path('/private/tmp/kbl-selective-portraits-20261003');S=R/'projects/site';T=C/'projects/site';K=Path(__file__).resolve().parent
assert not subprocess.check_output(['git','-C',str(C),'status','--porcelain']).strip(),'Release checkout not clean'
assert subprocess.check_output(['git','-C',str(C),'rev-parse','HEAD']).strip()==subprocess.check_output(['git','-C',str(C),'rev-parse','origin/main']).strip(),'Refresh base first'
def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
baseline={'base_commit':subprocess.check_output(['git','-C',str(C),'rev-parse','HEAD']).decode().strip(),'protected_files':{},'reader_variants':{}}
for folder in ['content/editions','assets/covers','assets/writer-portraits']:
 for p in (T/folder).rglob('*'):
  if p.is_file():baseline['protected_files'][str(p.relative_to(C))]=hashlib.sha256(p.read_bytes()).hexdigest()
for p in [T/'runtime-config.json',T/'data/writer-portraits.json']:
 if p.exists():baseline['protected_files'][str(p.relative_to(C))]=hashlib.sha256(p.read_bytes()).hexdigest()
for route in json.loads((T/'data/local-routes.json').read_text()).values():
 m=re.search(r'<script type="application/json" id="reading-data">(.*?)</script>',(T/route).read_text(),re.S)
 baseline['reader_variants'][route]=json.loads(m[1])['variants']
save(K/'pilot-release-baseline.json',baseline)
old=(T/'edition-pages.py').read_text();new=(S/'edition-pages.py').read_text()
start="poem_art_captions=json.loads((R/'data/poem-art-captions.json').read_text())"
end="    elif ident in sample_routes:"
replacement=new[new.index(start):new.index(end)+len(end)]
old_start=old.index(start);old_end=old.index('    if ident in sample_routes:',old_start)+len('    if ident in sample_routes:')
(T/'edition-pages.py').write_text(old[:old_start]+replacement+old[old_end:])
shutil.copy2(S/'poem_experience.py',T/'poem_experience.py')
shutil.copy2(S/'data/edition-art-direction.json',T/'data/edition-art-direction.json')
shutil.copytree(S/'assets/poem-art/editions',T/'assets/poem-art/editions',dirs_exist_ok=True)
for path in ['kb/research/edition-art-pilot-2026-10-04','kb/artifacts/artwork/edition-art-pilot-2026-10-04','kb/research/edition-art-rollout-2026-10-04','kb/artifacts/artwork/edition-art-rollout-2026-10-04']:
 shutil.copytree(R/path,C/path,dirs_exist_ok=True,ignore=shutil.ignore_patterns('__pycache__'))
for name in ['edition-art-pilot-2026-10-04.json','edition-art-rollout-2026-10-04.json']:
 shutil.copy2(R/'kb/records'/name,C/'kb/records'/name)
p=C/'kb/registers/records.json';reg=json.loads(p.read_text());local=json.loads((R/'kb/registers/records.json').read_text())
for key,ids in [('decisions',['KBL-DEC-045','KBL-DEC-046']),('work',['KBL-WORK-021','KBL-WORK-022'])]:
 assert not any(x['id'] in ids for x in reg[key])
 reg[key].extend(x for x in local[key] if x['id'] in ids)
save(p,reg)
agents=(R/'AGENTS.md').read_text();section=agents[agents.index('## Edition-specific artwork pilot loop'):agents.index('On 2026-10-01, Ahimanikya explicitly approved')]
with (C/'AGENTS.md').open('a') as f:f.write('\n'+section)
with (C/'kb/index.md').open('a') as f:f.write('\n- [Approved edition artwork pilot](artifacts/artwork/edition-art-pilot-2026-10-04/index.html) · [All-edition rollout](records/edition-art-rollout-2026-10-04.json)\n')
print('Scoped source/assets/provenance copied; latest published portraits and service settings preserved.')
