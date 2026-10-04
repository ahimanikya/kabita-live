from pathlib import Path
import json,datetime,sys
num=sys.argv[1];rep=sys.argv[2];b=Path('kb/research/writers/portrait-batches')/('portrait-'+num);now=datetime.datetime.now(datetime.timezone.utc).isoformat()
def read(p):return json.loads(Path(p).read_text())
def write(p,d):Path(p).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
queue=read('kb/research/writers/portrait-batches.json');batch=next(x for x in queue['batches'] if x['id']=='portrait-'+num);assert batch['verification']!='passed';ids=batch['writer_ids'];a=read(b/'author-check.json');e=read(b/'edition-check.json');h=read(b/'hash-check.json');assert a['result']==e['result']==h['result']=='PASS'
art=a['new_artistic_portraits'];holds=len(queue['likeness_holds']);pending=a['source_photo_profiles']-holds
nextbatch=next((x for x in queue['batches'] if x['id']>batch['id'] and x['verification']!='passed'),None);nextid=nextbatch['writer_ids'][0] if nextbatch else None;nextname=nextbatch['id'] if nextbatch else None
checks=['Node24 public Astro build passed',f'Author check passed:{art} artistic portraits,{a["source_photo_profiles"]} photographs including{holds} holds,3 generic placeholders','Edition check passed:47 editions,799 poems,848 source hashes',f'{h["baseline_files"]} baseline paths checked; changed only portrait map and separately authorized concurrent edition art mapping',f'All{h["source_records"]} source records and recorded master hashes match','All five64/128px circular thumbnails visually inspected',f'{rep} desktop1280px and mobile360px profile crop inspected; mobile scroll width360px']
review=dict(recorded_at=now,batch=batch['id'],writer_ids=ids,integrated_writer_ids=ids,held_writer_ids=[],verification='passed',checks=checks,independent=False,human_natural='Editorial Natural applied to all five; individual source limitations and visual comparisons recorded in portrait-edits.',limitations=['Independent author/editor likeness review pending','Watercolor pigment, hair, jewelry and garment detail remain interpretive as recorded',f'{holds} likeness holds retain photos;3 missing-photo records remain open with generic artwork','Concurrent work preserved; no publication in this batch'])
write(b/'review.json',review);write(b/'progress.json',dict(batch=batch['id'],integrated_writer_ids=ids,held_writer_ids=[],verification='passed',resume_writer_id=None))
for path in ['kb/research/writers/portrait-batches.json','kb/records/poet-watercolor-loop.json','kb/records/poet-watercolor-rollout.json']:
 q=read(path);q['counts'].update(newly_verified=art-4,newly_integrated_pending_verification=0,pending_photographs=pending);q['updated_at']=now
 if 'batches'in q:next(x for x in q['batches'] if x['id']==batch['id']).update(status='integrated',verification='passed',integrated_writer_ids=ids,held_writer_ids=[],resume_writer_id=None)
 if 'resume_batch'in q:q.update(resume_batch=nextname,resume_writer_id=nextid)
 else:q.update(next_batch=nextname,next_writer_id=nextid)
 if q.get('user_review_application'):q['user_review_application']['resume']=f'Review application verified; normal queue now {nextname or "final deployment verification"} writer{nextid}. Do not regenerate saved review work.'
 if path.endswith('poet-watercolor-rollout.json'):q.update(review,status='ready_for_final_deployment' if pending==0 else 'rollout_in_progress')
 if pending==0:q['deployment_resume']='All actionable photographs processed; reconcile authorized portrait-only final release against latest remote main, preserving concurrent edition releases; verify build/CI, push and manual public-only Pages deploy, live-check, then pause heartbeat. Existing holds stay open.'
 write(path,q)
edits=read('kb/research/writers/portrait-edits.json')
for x in edits:
 if x['writer_id'] in ids and x.get('status')=='integrated_pending_build':x.update(status='integrated_verified_locally',verification='passed',verification_batch=batch['id'],independent_likeness_review='pending',human_natural='Editorial Natural; individual limitations recorded.')
write('kb/research/writers/portrait-edits.json',edits)
f=Path('kb/registers/activity.jsonl');rows=[json.loads(x) for x in f.read_text().splitlines()];n=max(int(x['id'].split('-')[-1]) for x in rows)+1
with f.open('a') as out:out.write(json.dumps(dict(id=f'KBL-EVT-{n:03d}',recorded_at=now,actor={'kind':'ai_assistant','name':'Current assistant; Samanta implementation and Drishti self-review'},summary=f'{batch["id"]} verified locally: five portraits{ids} integrated. {art} artistic portraits,{pending} actionable photographs,{holds} likeness holds and3 generic placeholders. Build, source/master/content hashes and thumbnails/desktop/mobile checks passed. Originals/concurrent work preserved; no publication.',refs=['KBL-WORK-004'],evidence=[f'research/writers/portrait-batches/{batch["id"]}/review.json'],next_action=f'Resume {nextname} writer{nextid}; active heartbeat retained.' if pending else 'Carry out authorized final portrait deployment from latest remote main; keep heartbeat active until live verification.'),ensure_ascii=False)+'\n')
print(n,art,pending)
