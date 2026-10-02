import json,sys
from pathlib import Path
from datetime import datetime,timezone
batch=sys.argv[1];n=int(batch.rsplit('-',1)[1]);root=Path.cwd();now=datetime.now(timezone.utc).isoformat();r=json.loads((root/f'kb/research/writers/batches/{batch}/review.json').read_text());total=len(json.load(open('projects/site/data/writer-enrichment.json')));limited=sum(json.loads(p.read_text()).get('status')=='source_limited_local_draft' for p in Path('kb/research/writers/enrichment').glob('*.json'));nxt=f'research-{n+1:03}'
p=Path('kb/records/writer-enrichment-loop.json');d=json.loads(p.read_text());d.update(foreground_progress=f'research-002 through {batch} integrated and verified; {total} drafts processed, including {limited} source-limited cases.',next_batch=nxt,updated_at=now);p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
p=Path('kb/registers/records.json');d=json.loads(p.read_text());evidence=f'research/writers/batches/{batch}/review.json'
for w in d['work']:
 if w['id']=='KBL-WORK-012':
  w['next_action']=f'Resume {nxt}; {total}/427 drafts processed, {limited} source-limited. Independent review pending. Preserve source flags:535 self-translation,699 duplicate,682/708 conflict,727 wrong-source archive,294 award wording; memorial writer67; source-limited389 and contribution mapping382.'
  if evidence not in w['evidence']:w['evidence'].append(evidence)
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
p=Path('kb/registers/activity.jsonl');events=[json.loads(l) for l in p.read_text().splitlines() if l.strip()];num=max(int(e['id'].rsplit('-',1)[1]) for e in events)+1
names={p['id']:p['name'] for p in json.load(open('projects/site/data/writer-profiles.json'))}
e=dict(id=f'KBL-EVT-{num:03}',recorded_at=now,actor=dict(kind='ai_assistant',name='Current assistant; Anvesha research and Drishti self-review'),summary=f"Integrated and verified {batch}: "+', '.join(names[i] for i in r['writer_ids'])+f". {total}/427 drafts processed; {r['externally_corroborated']} externally corroborated and {len(r['source_limited'])} source-limited this batch. Public build and author/edition checks passed; {r['checks']['preserved_source_files']} inputs and {r['checks']['existing_narratives_preserved']} earlier narratives unchanged. No publication.",refs=['KBL-WORK-012'],evidence=[evidence],next_action=f'Resume {nxt}; loop ACTIVE. {limited} source-limited cases and independent author/editor review remain open.')
with p.open('a') as f:f.write(json.dumps(e,ensure_ascii=False)+'\n')
print(total,limited,nxt)
