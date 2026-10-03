"""Overlay only the authorized portrait revisions on the published baseline."""
from pathlib import Path
import json, shutil
ROOT=Path(__file__).resolve().parents[4]
DEST=Path('/private/tmp/kbl-selective-portraits-20261003')
def read(root,path): return json.loads((root/path).read_text())
def write(root,path,data):
 p=root/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
q=read(ROOT,'kb/records/selective-portrait-fixes-2026-10-03.json')
mapping=read(DEST,'projects/site/data/writer-portraits.json')
current=read(ROOT,'projects/site/data/writer-portraits.json')
edits=read(DEST,'kb/research/writers/portrait-edits.json')
new=[r for r in read(ROOT,'kb/research/writers/portrait-edits.json') if r.get('verification_batch')=='selective-portrait-fixes-2026-10-03']
assert len(new)==sum(r.get('selected_asset') is not None for r in q['items'])
for r in q['items']:
 for h in r.get('candidate_history',[]):
  target=DEST/h['candidate'];target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/h['candidate'],target)
 if r.get('pair'):
  target=DEST/r['pair'];target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/r['pair'],target)
 if not r.get('selected_asset'): continue
 wid=str(r['writer_id']);mapping[wid]=current[wid]
 for path in [r['candidate']]+[r['selected_asset'].replace('.webp',suffix) for suffix in ['.webp','-128.webp','-64.webp']]:
  if path.startswith('assets/'): path='projects/site/'+path
  target=DEST/path;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/path,target)
edits=[r for r in edits if r.get('verification_batch')!='selective-portrait-fixes-2026-10-03']+new
write(DEST,'projects/site/data/writer-portraits.json',mapping)
write(DEST,'kb/research/writers/portrait-edits.json',edits)
for directory in ['kb/research/writers/selective-portrait-fixes-2026-10-03','kb/artifacts/review/selective-portrait-fixes-2026-10-03']:
 shutil.copytree(ROOT/directory,DEST/directory,dirs_exist_ok=True)
shutil.copy2(ROOT/'kb/records/selective-portrait-fixes-2026-10-03.json',DEST/'kb/records/selective-portrait-fixes-2026-10-03.json')
records=read(DEST,'kb/registers/records.json')
decision=next(r for r in read(ROOT,'kb/registers/records.json')['decisions'] if r['id']=='KBL-DEC-044')
records['decisions']=[r for r in records['decisions'] if r['id']!='KBL-DEC-044']+[decision]
write(DEST,'kb/registers/records.json',records)
ledger=DEST/'kb/registers/activity.jsonl'
existing={json.loads(line)['id'] for line in ledger.read_text().splitlines() if line}
for line in (ROOT/'kb/registers/activity.jsonl').read_text().splitlines():
 if line and json.loads(line)['id'] in q.get('activity_ids',[]) and json.loads(line)['id'] not in existing:
  with ledger.open('a') as f:f.write(line+'\n')
print('Scoped release overlay complete:',len(new),'revisions')
