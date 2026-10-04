from pathlib import Path
import json,datetime,shutil
R=Path('/Users/ahimanikya/Projects/Kabita Live');C=Path('/private/tmp/kbl-final-portraits-20261004');K=R/'kb/research/writers/final-portrait-release-2026-10-04';now=datetime.datetime.now(datetime.timezone.utc).isoformat()
live=json.loads((K/'live-verification.json').read_text());assert live['result']=='PASS'
workflow=json.loads((K/'workflow.json').read_text());assert workflow['conclusion']=='success' and workflow['headSha']=='c7ad97794e3dc02c2558de12777d065c3f11e07b'
for root in [R,C]:
 p=root/'kb/records/final-portrait-deployment-2026-10-04.json';d=json.loads((R/'kb/records/final-portrait-deployment-2026-10-04.json').read_text());d.update(status='deployed_and_live_verified',deployed_at=now,workflow_id=37191215799,workflow_url='https://github.com/ahimanikya/kabita-live/actions/runs/37191215799',url=live['url'],live_checks={k:v for k,v in live.items() if k not in ['assets','pages']},independent_likeness_review='pending',evidence='research/writers/final-portrait-release-2026-10-04/live-verification.json',resume='Deployment and live verification complete; no generation remains actionable. Retain8 likeness holds and3 missing-source holds with generic artwork. Pause portrait heartbeat.');p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
 for rel in ['kb/records/poet-watercolor-loop.json','kb/records/poet-watercolor-rollout.json','kb/research/writers/portrait-batches.json']:
  p=root/rel;q=json.loads(p.read_text());q['updated_at']=now;q['deployment_record']='records/final-portrait-deployment-2026-10-04.json';q['deployment_resume']='Final rollout deployed and live verified;8 likeness holds and3 missing-source records remain open. Independent author/editor likeness review pending.'
  if 'resume_batch' in q:q.update(resume_batch=None,resume_writer_id=None)
  if rel.endswith('poet-watercolor-rollout.json'):q['status']='deployed_with_holds'
  p.write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n')
 p=root/'kb/registers/activity.jsonl';rows=[json.loads(x) for x in p.read_text().splitlines()];eid=max(int(x['id'].split('-')[-1]) for x in rows)+1
 with p.open('a') as f:f.write(json.dumps(dict(id=f'KBL-EVT-{eid:03}',recorded_at=now,actor={'kind':'ai_assistant','name':'Current assistant; deployment and self-review'},summary=f'Final portrait rollout published at commitc7ad977 through successful manual Pages workflow37191215799. Live checks passed for{live["verified_profile_pages"]} profile pages and{live["verified_asset_hashes"]} asset hashes.416 artistic portraits,8 likeness holds retaining originals,3 labelled generic artworks with source holds open. Imported35 decisions applied; independent author/editor review pending. Existing edition art, active services, consent and noindex preserved.',refs=['KBL-WORK-004'],evidence=['records/final-portrait-deployment-2026-10-04.json'],next_action='Pause completed portrait automation; resolve held likenesses only with further review or better identified sources.'),ensure_ascii=False)+'\n')
shutil.copytree(K,C/'kb/research/writers/final-portrait-release-2026-10-04',dirs_exist_ok=True)
print('Recorded successful final deployment')
