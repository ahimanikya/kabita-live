from pathlib import Path
import json,datetime,shutil
R=Path('/Users/ahimanikya/Projects/Kabita Live');C=Path('/private/tmp/kbl-final-portraits-20261004');B=Path(__file__).resolve().parent;now=datetime.datetime.now(datetime.timezone.utc).isoformat();rel='kb/records/accepted-candidate-two-2026-10-04.json'
live=json.loads((B/'live-verification.json').read_text());w=json.loads((B/'workflow.json').read_text());assert live['result']=='PASS' and w['conclusion']=='success' and w['headSha']=='d86bb1bfefd4ef11f1bd2ca848123bcc3868863b'
d=json.loads((R/rel).read_text());d.update(status='deployed_and_live_verified',deployed_at=now,live_verification={'profiles':8,'asset_hashes':24,'noindex':True,'services_preserved':True},url=live['url'],resume='All8 remaining saved candidates accepted, applied and live verified.424 artistic portraits and3 generic artworks; no active likeness holds. Source photographs remain missing for233,258,416. Portrait automation remains paused.',independent_author_editor_review='User acceptance recorded; independent author/editor confirmation not claimed')
for root in [R,C]:
 (root/rel).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
 for name in ['kb/research/writers/portrait-batches.json','kb/records/poet-watercolor-loop.json','kb/records/poet-watercolor-rollout.json']:
  p=root/name;q=json.loads(p.read_text());q['deployment_resume']=d['resume'];q['latest_acceptance_record']=rel.removeprefix('kb/');q['updated_at']=now
  if 'held_writer_ids' in q:q['held_writer_ids']=[]
  if name.endswith('poet-watercolor-loop.json'):q.update(setup_status='PAUSED',completion_status='deployed_verified_user_accepted_likenesses')
  if name.endswith('poet-watercolor-rollout.json'):q['status']='deployed_user_accepted_likenesses'
  p.write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n')
 f=root/'kb/registers/activity.jsonl';rows=[json.loads(x) for x in f.read_text().splitlines()];n=max(int(x['id'].split('-')[-1]) for x in rows)+1
 with f.open('a') as out:out.write(json.dumps(dict(id=f'KBL-EVT-{n:03}',recorded_at=now,actor={'kind':'ai_assistant','name':'Current assistant; implementation and self-review'},summary='Eight remaining likeness candidates accepted by Ahimanikya are published and live verified: six Candidate2 artworks and the two existing retries.424 artistic portraits,0 active likeness holds,3 labelled generic placeholders with source-photo records open. All8 hosted profiles and24 asset hashes passed; commitd86bb1bf, manual Pages workflow37192800491 succeeded. Concurrent artwork and poem-ending releases preserved; portrait automation stays paused.',refs=['KBL-WORK-004'],evidence=[rel.removeprefix('kb/')],next_action='No further portrait generation; preserve source-photo holds for233,258,416 and review provenance.'),ensure_ascii=False)+'\n')
shutil.copytree(B,C/'kb/research/writers/accepted-candidate-two-2026-10-04',dirs_exist_ok=True)
print('Recorded published acceptance of all8 remaining candidates')
