from pathlib import Path
import json,datetime
R=Path('/Users/ahimanikya/Projects/Kabita Live');B=Path(__file__).resolve().parent;now=datetime.datetime.now(datetime.timezone.utc).isoformat()
def read(p):return json.loads((R/p).read_text())
def write(p,d):(R/p).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
rec='kb/records/accepted-candidate-two-2026-10-04.json';d=read(rec);ids=[x['writer_id'] for x in d['decisions']]
for f in ['author-check.json','edition-check.json','hash-check.json']:assert json.loads((B/f).read_text())['result']=='PASS'
assert json.loads((B/'author-check.json').read_text())['new_artistic_portraits']==424
d.update(status='verified_locally_pending_deployment',verification={'build':'PASS','author_pages':'424 artistic,0 source photos,3 generic','editions':'PASS','hashes':'3511 protected paths; only portrait map changed','visual':'Eight64/128 circular crops; Sutanuka desktop1280 and mobile360, no horizontal overflow','independent':False});
for x in d['decisions']:x['status']='user_accepted_verified_locally'
write(rec,d)
for rel in ['kb/research/writers/portrait-batches.json','kb/records/poet-watercolor-loop.json','kb/records/poet-watercolor-rollout.json']:
 q=read(rel);remaining=[]
 for h in q['likeness_holds']:
  if h['writer_id'] in ids:q.setdefault('resolved_likeness_holds',[]).append(dict(h,resolved_at=now,resolution='User accepted saved candidate',resolution_record=rec.removeprefix('kb/')))
  else:remaining.append(h)
 q['likeness_holds']=remaining;q['counts'].update(newly_verified=420,likeness_holds=0,pending_photographs=0,newly_integrated_pending_verification=0);q['updated_at']=now;q['deployment_resume']='Eight remaining candidates accepted by user; verified locally, follow-up publication pending. Portrait automation remains paused.'
 if 'batches'in q:
  for b in q['batches']:
   accepted=[i for i in b.get('held_writer_ids',[]) if i in ids]
   if accepted:b['held_writer_ids']=[i for i in b['held_writer_ids'] if i not in ids];b['integrated_writer_ids']=list(dict.fromkeys(b.get('integrated_writer_ids',[])+accepted));b['later_user_acceptance']=rec.removeprefix('kb/')
 write(rel,q)
edits=read('kb/research/writers/portrait-edits.json')
for e in edits:
 if e.get('verification_batch')=='accepted-candidate-two-2026-10-04':e.update(status='user_approved_integrated_verified_locally',verification='passed')
write('kb/research/writers/portrait-edits.json',edits)
p='kb/records/likeness-decisions-2026-10-04.json';q=read(p);q['subsequent_acceptance_record']=rec.removeprefix('kb/');q['status']='all_decisions_applied_after_later_retry_acceptance'
for x in q['decisions']:
 if x['writer_id'] in [150,227]:
  new=next(z for z in d['decisions'] if z['writer_id']==x['writer_id']);x.update(status='user_accepted_retry_verified_locally',web_asset=new['web_asset'],review='Later user instruction accepted this existing retry. Earlier concern preserved: '+x.get('review',''),later_user_decision='Accept their existing retries too')
write(p,q)
f=R/'kb/registers/activity.jsonl';rows=[json.loads(x) for x in f.read_text().splitlines()];n=max(int(x['id'].split('-')[-1]) for x in rows)+1
with f.open('a') as out:out.write(json.dumps(dict(id=f'KBL-EVT-{n:03}',recorded_at=now,actor={'kind':'ai_assistant','name':'Current assistant; implementation and self-review'},summary='Applied user acceptance of six saved Candidate2 portraits plus existing retries for Sutanuka Ghosh Roy and Sweety Sony Lall.424 artistic portraits,0 active likeness holds,3 generic artworks with source-photo holds open. Prior concerns and all originals retained; independent author/editor confirmation not claimed. Build, author/edition checks, hashes and desktop/mobile thumbnails passed.',refs=['KBL-WORK-004'],evidence=[rec.removeprefix('kb/')],next_action='Publish verified follow-up portrait update using manual Pages preview workflow.'),ensure_ascii=False)+'\n')
print('Verified eight user-accepted portraits')
