from apply_decisions import *
P=ROOT/'output/kabita-live-project';hist=B/'handoff-interrupted-snapshots';hist.mkdir(exist_ok=True)
paths=['kb/research/writers/portrait-edits.json','kb/research/edition-art-rollout-2026-10-04/queue.json','kb/artifacts/artwork/edition-art-rollout-2026-10-04/index.html','kb/records/likeness-decisions-2026-10-04.json','kb/records/edition-art-rollout-2026-10-04.json','kb/registers/DASHBOARD.md','kb/registers/activity.jsonl','site/about.html','site/poems.html','site/poets.html','site/data/edition-art-direction.json','site/data/writer-portraits.json','site/assets/reading-all.json']
notes=[]
for rel in paths:
 source=ROOT/(rel if rel.startswith('kb/') else 'projects/'+rel);dest=P/rel
 a=source.read_bytes();b=dest.read_bytes()
 if a==b:continue
 saved=hist/(rel.replace('/','__')+'.saved');saved.write_bytes(b)
 notes.append({'path':rel,'primary_sha256':hashlib.sha256(a).hexdigest(),'portable_previous_sha256':hashlib.sha256(b).hexdigest(),'preserved_snapshot':str(saved.relative_to(ROOT/'kb'))})
 assert dest.read_bytes()==b and source.read_bytes()==a,'Concurrent change; inspect before retry'
 dest.write_bytes(a)
write(str(B.relative_to(ROOT)/'handoff-reconciliation.json'),{'reason':'Interrupted concurrent sync copied earlier checkpoints without completing baseline. Inspected: portrait edits were prior prefix; user decision differences were pending versus completed retries; portrait map changed only authorized retry IDs; activity was prior prefix; reader payload changes only portrait fields; edition queue progressed43 to42 and art mapping additions preserved existing entries. Generated pages and dashboards rebuilt from canonical current data. Earlier portable bytes retained for audit. No canonical concurrent work overwritten.','files':notes})
print('Reconciled',len(notes),'earlier portable snapshots')
