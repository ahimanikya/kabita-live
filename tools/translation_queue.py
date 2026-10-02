#!/usr/bin/env python3
"""Index translation drafts in edition order, preserving source identity and review status."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[1]
SITE=ROOT/'projects/site'
if not SITE.exists(): SITE=ROOT/'site'
content=SITE/'content/editions'
issues=json.loads((content/'index.json').read_text())
catalog=json.loads((SITE/'data/poem-translations.json').read_text())
holds_path=ROOT/'kb/production/translations/source-holds.json'
holds=json.loads(holds_path.read_text()) if holds_path.exists() else {}
paths={d['id']:p for p in content.glob('*/poem-*.json') for d in [json.loads(p.read_text())] if d.get('status')!='archived'}
ordered=[pid for i in sorted(issues,key=lambda x:x['number'],reverse=True) for pid in i['poem_ids']]
ordered+=sorted(set(paths)-set(ordered))
tasks=[]
for ident in ordered:
 source=json.loads(paths[ident].read_text())
 digest=hashlib.sha256(source['text'].encode()).hexdigest()
 entry=catalog.get(str(ident),{})
 if entry: assert entry['source_sha256']==digest,f'Stale translation source: {ident}'
 for lang in ['or','hi','en']:
  if lang==source['language']:continue
  version=entry.get('variants',{}).get(lang)
  if version:
   assert version['kind']=='Translation' and version['title'] and version['stanzas']
   assert [len(s) for s in version['stanzas']]==[len(s) for s in source['stanzas']],f'Stanza/line coverage: {ident}/{lang}'
  tasks.append({'poem_id':ident,'edition':source['edition'],'source_language':source['language'],'target_language':lang,'source':str(paths[ident].relative_to(ROOT)),'source_sha256':digest,'status':('reviewed' if version.get('status')=='reviewed' else 'draft-ready') if version else 'pending'})
  if not version and lang in holds.get(str(ident),{}).get('targets',[]):
   tasks[-1]['status']='needs-source'
   tasks[-1]['hold_reason']=holds[str(ident)]['reason']
out={'mode':'Small batches in this chat, edition order newest first; continue after checks without repeated approval','total':len(tasks),'draft_ready':sum(t['status']=='draft-ready' for t in tasks),'reviewed':sum(t['status']=='reviewed' for t in tasks),'pending':sum(t['status'] in ['pending','needs-source'] for t in tasks),'ready_to_translate':sum(t['status']=='pending' for t in tasks),'needs_source':sum(t['status']=='needs-source' for t in tasks),'tasks':tasks}
(ROOT/'kb/production/translations/queue.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(f"Translation queue: {out['total']} total; {out['draft_ready']} drafts; {out['reviewed']} reviewed; {out['pending']} pending.")
