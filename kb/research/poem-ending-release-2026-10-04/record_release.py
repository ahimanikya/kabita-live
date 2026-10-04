from pathlib import Path
from datetime import datetime,timezone
import json,shutil,sys
R=Path('/Users/ahimanikya/Projects/Kabita Live');C=Path(sys.argv[1]);K=R/'kb/research/poem-ending-release-2026-10-04';now=datetime.now(timezone.utc).isoformat()
roots=[R,C];data=[json.loads((r/'kb/registers/records.json').read_text()) for r in roots];did='KBL-DEC-'+str(max(int(d['id'].split('-')[-1]) for x in data for d in x['decisions'])+1).zfill(3)
record={'recorded_at':now,'status':'verified_ready_to_publish','user_quote':'apply','context':'User requested application after reviewing the locally applied ending refinement; prior instruction in this conversation requested pushing fixes and updating the website.','scope':'Publish only approved closing marks and ending refinement using the established manual public-only Pages preview workflow. Preserve current portraits, artwork, poem text, consent, runtime, noindex and DNS.','independent':False,'base_commit':json.loads((K/'baseline.json').read_text())['base'],'release_checkout':str(C),'verification':'research/poem-ending-release-2026-10-04/verification.json','checks':'28 application tests passed;10 emulator-dependent rules tests run in mandatory publication CI. Build and all3218protected input hashes pass;799poems/2373language variants preserved;1502neighbouring titles verified.'}
decision={'id':did,'title':'Publish the approved poem closing marks and ending refinement','status':'approved','actor':{'kind':'human','name':'Ahimanikya Satapathy'},'quote':'apply','scope':record['scope'],'evidence':['records/poem-ending-deployment-2026-10-04.json']}
for x in data:
 for d in data[0]['decisions']:
  if d['id'] in ['KBL-DEC-047','KBL-DEC-048'] and not any(a['id']==d['id'] for a in x['decisions']):x['decisions'].append(d.copy())
 x['decisions'].append(decision)
events=[[json.loads(l) for l in (r/'kb/registers/activity.jsonl').read_text().splitlines() if l.strip()] for r in roots];eid='KBL-EVT-'+str(max(int(e['id'].split('-')[-1]) for es in events for e in es)+1).zfill(3)
event={'id':eid,'recorded_at':now,'actor':{'kind':'ai_assistant','name':'Current assistant; Samanta implementation and Drishti self-review'},'summary':'Prepared approved closing marks and ending refinements for publication from the latest portrait release.799poems/2373variants,3218protected inputs and1502navigation titles pass;28 application tests and public build pass. Manual Pages preview deployment next.','refs':['KBL-WORK-004',did],'evidence':['records/poem-ending-deployment-2026-10-04.json'],'next_action':'Commit, push, dispatch manual preview workflow and verify live closing marks, titles and preserved runtime.'}
for r,x in zip(roots,data):
 (r/'kb/records/poem-ending-deployment-2026-10-04.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
 (r/'kb/registers/records.json').write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
 with (r/'kb/registers/activity.jsonl').open('a') as f:f.write(json.dumps(event,ensure_ascii=False)+'\n')
p=C/'kb/review/index.md';p.write_text(p.read_text()+'\n- [Approved poem ending refinement](../records/poem-ending-refinement-2026-10-04.json): varied botanical marks, neighbouring poem titles, compact spacing and quieter footer. [Publication verification](../records/poem-ending-deployment-2026-10-04.json).\n')
shutil.copytree(K,C/'kb/research/poem-ending-release-2026-10-04',dirs_exist_ok=True)
print(did,eid)
