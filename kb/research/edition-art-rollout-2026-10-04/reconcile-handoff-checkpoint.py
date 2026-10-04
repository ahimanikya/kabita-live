"""Preserve and reconcile the inspected partial-sync copies; never changes canonical portraits."""
import json,hashlib,subprocess,shutil
from pathlib import Path
from datetime import datetime,timezone
R=Path(__file__).resolve().parents[3];H=R/'output/kabita-live-project';A=R/'kb/history/handoff-reconciliation-2026-10-04-art-checkpoint';A.mkdir(parents=True,exist_ok=True)
r=subprocess.run(['python3',str(R/'tools/sync_handoff.py')],capture_output=True,text=True)
if r.returncode==0:print(r.stdout);raise SystemExit()
out=r.stdout+r.stderr
assert out.startswith('Handoff has divergent edits; preserve/reconcile before sync:'),out
paths=out.strip().splitlines()[1:]
allowed={'kb/research/writers/portrait-edits.json','kb/research/edition-art-rollout-2026-10-04/queue.json','kb/artifacts/artwork/edition-art-rollout-2026-10-04/index.html','kb/records/likeness-decisions-2026-10-04.json','kb/records/edition-art-rollout-2026-10-04.json','kb/registers/DASHBOARD.md','kb/registers/activity.jsonl','site/about.html','site/poems.html','site/poets.html','site/data/edition-art-direction.json','site/data/writer-portraits.json','site/assets/reading-all.json'}
assert set(paths)<=allowed,paths
# Verify independent handoff content has not appeared in the canonical append-only records.
a=json.loads((H/'kb/research/writers/portrait-edits.json').read_text());b=json.loads((R/'kb/research/writers/portrait-edits.json').read_text());assert len(b)>=len(a)
for old,new in zip(a,b):
 assert {k:v for k,v in old.items() if k not in ['status','verification','verified_at']}=={k:v for k,v in new.items() if k not in ['status','verification','verified_at']},'Unexpected portrait provenance drift'
 if old!=new:assert new.get('status')=='integrated_verified_locally' and new.get('verification')=='passed'
assert (R/'kb/registers/activity.jsonl').read_text().startswith((H/'kb/registers/activity.jsonl').read_text())
a=json.loads((H/'site/assets/reading-all.json').read_text());b=json.loads((R/'projects/site/assets/reading-all.json').read_text())
for doc in [a,b]:
 for poem in doc['poems']:poem.pop('portrait',None)
assert a==b,'Nonportrait reader data drift; stop'
record=dict(at=datetime.now(timezone.utc).isoformat(),cause='Failed edition43 sync copied files but did not commit its hash baseline because canonical likeness records changed during verification. Inspection confirms newer source portrait retries299/327, append-only289 retry provenance, edition42 additions and derived pages; no independent handoff edits found.',policy='Preserve every inspected prior portable byte and hash before reconciling to canonical source; canonical portrait files never modified.',files=[])
staged=[]
for rel in paths:
 source=R/rel if rel.startswith('kb/') else R/'projects'/rel;target=H/rel;old=target.read_bytes();new=source.read_bytes();backup=A/'portable-before'/rel;assert not backup.exists(),backup;backup.parent.mkdir(parents=True,exist_ok=True);backup.write_bytes(old)
 record['files'].append(dict(path=rel,portable_sha256=hashlib.sha256(old).hexdigest(),source_sha256=hashlib.sha256(new).hexdigest(),preserved=str(backup.relative_to(R))))
 staged.append((source,target,old,new))
(A/'receipt.json').write_text(json.dumps(record,indent=2)+'\n')
for source,target,old,new in staged:
 assert target.read_bytes()==old and source.read_bytes()==new,'Concurrent change; stop without overwriting it'
 target.write_bytes(new)
print('Preserved and reconciled',len(staged),'inspected partial-sync files.')
