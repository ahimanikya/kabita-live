import json,html,hashlib
from pathlib import Path
from collections import Counter
from datetime import datetime,timezone
root=Path(__file__).resolve().parents[5];site=root/'projects/site';home=root/'kb/research/writers';now=datetime.now(timezone.utc).isoformat()
load=lambda p:json.loads(p.read_text())
save=lambda p,d:p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
en=load(site/'data/writer-enrichment.json');plan=load(home/'enrichment-batches.json');progress=load(home/'enrichment-progress.json');aliases={82:'poet-dokana.html',337:'poet-kshanika.html',257:'poet-drink.html'}
assert len(en)==427 and plan['next_batch'] is None
assert len(plan['batches'])==83 and all(b['verification']=='passed' and b['status']=='verified' for b in plan['batches'])
dossiers=[];legacy=[]
for ident,reader in en.items():
 d=load(home/'enrichment'/f'{ident}.json');dossiers.append(d)
 if 'reader_draft' in d:assert d['reader_draft']==reader,ident
 else:legacy.append(int(ident))
 route=aliases.get(int(ident),f'poet-{ident}.html')
 for section in reader.get('sections',[]):
  for paragraph in section.get('paragraphs',[]):
   for location in [site,site/'dist']:assert html.escape(paragraph) in (location/route).read_text(),(ident,location)
assert set(legacy)=={82,337,257}
base=home/'batches/research-079';hashes=load(base/'preserved-inputs.json')
for p,h in hashes.items():assert hashlib.sha256((site/p).read_bytes()).hexdigest()==h,p
before=load(base/'enrichment-before.json')
for i,d in before.items():assert en[i]==d,i
states=Counter(d['status'] for d in dossiers);limited=sorted([d for d in dossiers if d['status']=='source_limited_local_draft'],key=lambda d:d['name'].casefold())
assert states=={'source_checked_local_draft':336,'source_limited_local_draft':91}
audit=dict(recorded_at=now,status='draft_enrichment_complete',independent=False,reader_drafts=427,externally_corroborated_drafts=336,source_limited_drafts=91,previously_enriched_preserved=15,new_batch_writers=412,verified_batches=83,next_batch=None,automation_status='PAUSED',checks=dict(public_node24_build='passed',author_pages='PASS',edition_integrity='PASS',original_capture_hashes_verified=848,all_preview_and_public_narratives_verified=427,current_run_preserved_inputs=len(hashes),current_run_earlier_narratives_preserved=len(before),dossier_reader_snapshots_equal=424,legacy_dossiers_without_embedded_snapshot=legacy),limitations=['Source-checked means supporting external evidence was found; it does not certify every biographical statement or resolve all discrepancies.','All427 drafts require independent author/editor factual review.','91 source-limited records retain their precise next actions; they are not externally verified biographies.','Three legacy dossiers lack an embedded reader_draft field; their existing reader text is unchanged and rendered correctly.','Known edition gaps remain: unassigned645, missing author30, duplicate-text groups268/304 and645/650; archived385 and727 unchanged.','No new portraits, layout changes, publication, push or deployment.'],source_limited=[dict(writer_id=d['writer_id'],name=d['name'],next_action=d.get('next_action','Author/editor factual review.'),limitations=d.get('limitations',[]),dossier=f"research/writers/enrichment/{d['writer_id']}.json") for d in limited],batch_evidence='research/writers/enrichment-batches.json',last_batch='research/writers/batches/research-084/review.json')
save(home/'completion-review.json',audit)
lines=['---','type: "Research completion review"','title: "Writer enrichment completion and editorial follow-up"','---','','# Writer enrichment: draft pass complete','','All **427 writer profiles** now have enriched local drafts. The83 sequential batches covering412 writers are verified;15 earlier profiles remain preserved.','','- **336** drafts have supporting external evidence.','- **91** drafts remain source-limited.','- All427 still need independent author/editor factual review.','- The background research automation is paused. Nothing was published.','','## Verification','','The Node24 public build, author-page checks and47-edition integrity checks passed. All427 narratives match both the preview and public build;848 original capture hashes passed. This final run preserved805 inputs and400 earlier narratives. Three legacy dossiers (82,337,257) use an older schema without an embedded reader snapshot; their existing text is preserved.','','## Editorial follow-up','','The complete evidence, contradictions and next actions remain in each dossier, including externally corroborated profiles. Recent specific questions include the possible255/449 duplicate identity,423’s possible Ma Yongbo spelling match, and precise award wording for152 and258. No identities were merged.','','### Source-limited profiles','','| Writer | Next action |','| --- | --- |']
for d in limited:
 name=d['name'].replace('|','/');action=d.get('next_action','Author/editor factual review.').replace('|','/').replace('\n',' ')
 lines.append(f"| [{name} ({d['writer_id']})](enrichment/{d['writer_id']}.json) | {action} |")
lines+=['','Existing edition-source questions remain separate from profile enrichment. See [completion evidence](completion-review.json) and [batch register](ENRICHMENT-BATCHES.md).']
(home/'ENRICHMENT-COMPLETION.md').write_text('\n'.join(lines)+'\n')
p=root/'kb/records/writer-enrichment-loop.json';d=load(p);d.update(setup_status='PAUSED',completion_status='draft_enrichment_complete',foreground_progress='All427 writer profiles have enriched local drafts:336 source-checked and91 source-limited. All83 sequential batches verified;15 earlier profiles preserved. Independent author/editor review remains pending.',next_batch=None,updated_at=now,completed_at=now,completion_evidence='research/writers/completion-review.json');save(p,d)
p=root/'kb/registers/records.json';d=load(p)
for w in d['work']:
 if w['id']=='KBL-WORK-012':
  w['next_action']='Review enriched author pages together, then obtain independent author/editor factual review. All427 drafts processed;91 source-limited. Background enrichment loop PAUSED. Preserve source flags:535 self-translation,699 duplicate,682/708 conflict,727 wrong-source archive,294 award wording; memorial writer67; source-limited389 and contribution mapping382. See completion-review.json for all follow-ups.'
  for e in ['research/writers/batches/research-084/review.json','research/writers/completion-review.json','research/writers/ENRICHMENT-COMPLETION.md']:
   if e not in w['evidence']:w['evidence'].append(e)
save(p,d)
p=root/'kb/registers/activity.jsonl';events=[json.loads(x) for x in p.read_text().splitlines() if x.strip()];num=max(int(e['id'].rsplit('-',1)[1]) for e in events)+1
e=dict(id=f'KBL-EVT-{num:03}',recorded_at=now,actor=dict(kind='ai_assistant',name='Current assistant; Anvesha research and Drishti self-review'),summary='Completed and verified research-084: Gargi Sarkhel Bagchi and Nutan Sarawagi. All427 writer profiles now have enriched local drafts:336 source-checked,91 source-limited. All83 batches verified and15 earlier profiles preserved. Public build, author and edition checks passed; all427 preview/public narratives compared. Automation confirmed PAUSED. Independent author/editor review remains pending; no publication.',refs=['KBL-WORK-012'],evidence=['research/writers/batches/research-084/review.json','research/writers/completion-review.json'],next_action='Review enriched pages with user; resolve source-limited and factual questions through independent author/editor review. Research loop remains paused.')
with p.open('a') as f:f.write(json.dumps(e,ensure_ascii=False)+'\n')
print(json.dumps({k:audit[k] for k in ['status','reader_drafts','externally_corroborated_drafts','source_limited_drafts','verified_batches','automation_status']}))
