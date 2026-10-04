from apply_decisions import *
from collections import Counter
now=datetime.datetime.now(datetime.timezone.utc).isoformat();rp='kb/records/likeness-decisions-2026-10-04.json';r=read(rp)
assert all(d['status'] in ['applied_pending_verification','retry_integrated_pending_verification','retry_hold'] for d in r['decisions'])
base=read(str(B.relative_to(ROOT)/'baseline.json'));changed=[p for p,h in base.items() if not (ROOT/p).exists() or sha(ROOT/p)!=h]
assert set(changed)<= {'projects/site/data/writer-portraits.json','projects/site/data/edition-art-direction.json'},changed
edits=read('kb/research/writers/portrait-edits.json');checked=0
for e in edits:
 if e.get('source_sha256') and e.get('source',{}).get('file'):
  assert sha(ROOT/'kb'/e['source']['file'])==e['source_sha256'];checked+=1
 if e.get('master_sha256') and e.get('master'):assert sha(ROOT/'kb'/e['master'])==e['master_sha256']
write(str(B.relative_to(ROOT)/'hash-check.json'),dict(result='PASS',baseline_files=len(base),changed_files=changed,source_records_verified=checked,note='Only authorized portrait mapping and separately authorized concurrent edition art mapping changed. All earlier source photos, writer assets, masters and content hashes preserved.'))
assert read(str(B.relative_to(ROOT)/'author-check.json'))['result']=='PASS'
assert read(str(B.relative_to(ROOT)/'edition-check.json'))['result']=='PASS'
accepted=[d['writer_id'] for d in r['decisions'] if d['status']!='retry_hold'];held=[d['writer_id'] for d in r['decisions'] if d['status']=='retry_hold']
for d in r['decisions']:
 if d['status']=='applied_pending_verification':d['status']='user_selected_verified_locally'
 elif d['status']=='retry_integrated_pending_verification':d['status']='retry_verified_locally'
 d['verification']='passed' if d['writer_id'] in accepted else 'candidate_saved_photo_retained'
r.update(status='applied_with_two_retry_holds',verification='passed',verified_at=now,counts=dict(user_selected_applied=23,requested_retries=12,retries_applied=10,retry_holds=2,total_applied=33),results_page='artifacts/review/likeness-decisions-2026-10-04/index.html');write(rp,r)
for e in edits:
 if e.get('verification_batch')=='likeness-decisions-2026-10-04' and e['writer_id'] in accepted:
  e['status']='user_approved_integrated_verified_locally' if e.get('user_review') else 'integrated_verified_locally';e['verification']='passed';e['verified_at']=now
write('kb/research/writers/portrait-edits.json',edits)
mapcounts=Counter(x['kind'] for x in read('projects/site/data/writer-portraits.json').values());assert mapcounts['generated_portrait']==402
for path in ['kb/research/writers/portrait-batches.json','kb/records/poet-watercolor-loop.json','kb/records/poet-watercolor-rollout.json']:
 q=read(path);resolved=[dict(h,resolved_at=now,resolution_record='records/likeness-decisions-2026-10-04.json',resolution='User-selected saved attempt' if any(d['writer_id']==h['writer_id'] and 'attempt' in d for d in r['decisions']) else 'Requested soft source-limited retry passed local review; independent confirmation pending') for h in q['likeness_holds'] if h['writer_id'] in accepted]
 q.setdefault('resolved_likeness_holds',[]).extend(resolved);q['likeness_holds']=[h for h in q['likeness_holds'] if h['writer_id'] not in accepted]
 for h in q['likeness_holds']:
  if h['writer_id'] in held:
   d=next(d for d in r['decisions'] if d['writer_id']==h['writer_id']);h['prior_reason']=h['reason'];h['reason']=d['review'];h['retry_master']=d['master'];h['retry_record']='records/likeness-decisions-2026-10-04.json'
 assert len(q['likeness_holds'])==7
 q['counts'].update(newly_verified=398,newly_integrated_pending_verification=0,likeness_holds=7,pending_photographs=15);q['updated_at']=now
 q['user_review_application']={'record':'records/likeness-decisions-2026-10-04.json','status':'applied_with_two_retry_holds','resume':'portrait-082, writer210; do not regenerate saved review retries or user-selected masters.'}
 if path.endswith('poet-watercolor-rollout.json'):
  q['latest_review_application']='records/likeness-decisions-2026-10-04.json';q['limitations']=[x.replace('40 likeness holds','7 likeness holds') for x in q['limitations']];q['checks'].append('Subsequent user review application:23 selections and10 retries verified locally; see linked record for33 new integrations. Historical081 checks above are retained as recorded.')
 write(path,q)
review=dict(recorded_at=now,result='PASS',independent=False,applied_ids=accepted,held_ids=held,checks=['Node24 public Astro build passed','429 author profiles:402 artistic,22 photos,3 generic; author and edition checks passed','All33 circular thumbnails inspected at normal size','Mahua partial-source crop and Raja Rajeswari full-face profile checked at desktop1280 and mobile360; source crop preserved','3341 baseline paths checked: only portrait map and concurrent edition artwork map changed',f'{checked} source records and all recorded master hashes verified'],limitations=['23 explicit user acceptances recorded; author confirmation not claimed','10 new retries have source-limited detail and pending independent likeness review','150 and227 remain held with original photos and saved retry candidates','Five other holds outside this review export remain unchanged'],results_page='http://127.0.0.1:8771/portrait-review-results.html',publication='No push or deployment in this task;15 normal portrait photographs remain actionable.')
write(str(B.relative_to(ROOT)/'review.json'),review)
activity=ROOT/'kb/registers/activity.jsonl';rows=[json.loads(x) for x in activity.read_text().splitlines() if x.strip()];n=max(int(x['id'].split('-')[-1]) for x in rows)+1
entry=dict(id=f'KBL-EVT-{n:03d}',recorded_at=now,actor={'kind':'ai_assistant','name':'Current assistant; Samanta implementation and Drishti self-review'},summary='Applied imported human portrait review:23 exact saved attempts selected by Ahimanikya, plus12 requested targeted retries. Ten retries integrated;150 Sutanuka and227 Sweety remain held.33 total new integrations verified;402 artistic,15 pending photographs,7 likeness holds,3 generic placeholders. Originals and all earlier masters preserved; results review page created. No publication.',refs=['KBL-WORK-004'],evidence=['records/likeness-decisions-2026-10-04.json','research/writers/likeness-decisions-2026-10-04/review.json'],next_action='Resume portrait082 writer210 through active portrait heartbeat; do not regenerate saved review work.')
with activity.open('a') as f:f.write(json.dumps(entry,ensure_ascii=False)+'\n')
print(entry['id'],r['counts'],mapcounts)
