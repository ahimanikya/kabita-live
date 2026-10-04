from pathlib import Path
from datetime import datetime,timezone
import json,shutil,sys
R=Path('/Users/ahimanikya/Projects/Kabita Live');C=Path(sys.argv[1]);K=R/'kb/research/poem-ending-release-2026-10-04';now=datetime.now(timezone.utc).isoformat();live=json.loads((K/'live-verification.json').read_text());assert live['result']=='PASS'
p=R/'kb/records/poem-ending-deployment-2026-10-04.json';d=json.loads(p.read_text());d.update(status='published_and_verified',deployed_at=now,url=live['url'],live_verification='research/poem-ending-release-2026-10-04/live-verification.json',checks='GitHub build, application tests, Firebase rules tests and Pages deployment passed. Live asset/payload hashes match;799poems present in the all-poem reader; five representative page endings, navigation and existing art verified.');p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n');shutil.copy2(p,C/'kb/records'/p.name)
roots=[R,C];events=[[json.loads(l) for l in (r/'kb/registers/activity.jsonl').read_text().splitlines() if l.strip()] for r in roots];eid='KBL-EVT-'+str(max(int(e['id'].split('-')[-1]) for es in events for e in es)+1).zfill(3)
event={'id':eid,'recorded_at':now,'actor':{'kind':'ai_assistant','name':'Current assistant; publication and self-review'},'summary':'Published approved poem ending refinements at48934b0e via successful manual Pages workflow37192467335. Three original botanical closing marks, stable per-poem assignment, final-line grouping, neighbouring navigation titles, compact spacing and quieter footer verified live. All799reader poems present; five sample pages and nine assets/payloads match. Published portraits/art, runtime, consent and noindex retained.','refs':['KBL-WORK-004','KBL-DEC-049'],'evidence':['records/poem-ending-deployment-2026-10-04.json'],'next_action':'Publication complete; continue future changes from current approved state.'}
for r in roots:
 with (r/'kb/registers/activity.jsonl').open('a') as f:f.write(json.dumps(event,ensure_ascii=False)+'\n')
shutil.copytree(K,C/'kb/research/poem-ending-release-2026-10-04',dirs_exist_ok=True)
print(eid)
