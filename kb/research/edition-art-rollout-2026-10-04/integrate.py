"""Merge a reviewed edition locally; preserve prior entries and original assets."""
import json,sys,hashlib
from pathlib import Path
from PIL import Image
from datetime import datetime,timezone
R=Path(__file__).resolve().parents[3];K=Path(__file__).resolve().parent;S=R/'projects/site';ed=int(sys.argv[1]);p=K/f'batches/edition-{ed}/batch.json';b=json.loads(p.read_text());now=datetime.now(timezone.utc).isoformat()
manifest=S/'data/edition-art-direction.json';d=json.loads(manifest.read_text());generic=json.loads((S/'data/poem-art-assignments.json').read_text())['assignments']
for i in b['items']:
 if i['status']=='held':continue
 assert i['status'] in ['verified','integrated_local'],i['id']
 source=R/i['output'];assert hashlib.sha256(source.read_bytes()).hexdigest()==i['output_sha256']
 assert i.get('alt'),'Write a reviewed descriptive alt before integration'
 key=str(i['poem_id']);old=d['poems'].get(key)
 assert old is None or old.get('artwork_id')==i['id'],'Existing explicit art must not be silently replaced'
 target=S/f'assets/poem-art/editions/{ed}/{i["id"]}-v1.webp';target.parent.mkdir(parents=True,exist_ok=True)
 im=Image.open(source).convert('RGB');im.thumbnail((1536,1024))
 if not target.exists():im.save(target,'WEBP',quality=90,method=6)
 i.update(status='integrated_local',public_asset=str(target.relative_to(S)),public_sha256=hashlib.sha256(target.read_bytes()).hexdigest(),previous_assignment=generic.get(key),integrated_at=now)
 d['poems'][key]={'edition':ed,'mode':'illustrated','artwork_id':i['id'],'src':i['public_asset'],'alt':i['alt'],'caption':i['title']+' · An AI-assisted '+i.get('medium_label','watercolor')+' interpretation for this poem.','width':im.width,'height':im.height}
for i in b['text_led']:
 key=str(i['poem_id']);old=d['poems'].get(key);assert old is None or old['mode']=='text','Preserve existing explicit illustration'
 d['poems'][key]={'edition':ed,'mode':'text'};i['status']='integrated_local'
manifest.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n');b.update(status='integrated_pending_verification',updated_at=now);p.write_text(json.dumps(b,ensure_ascii=False,indent=2)+'\n')
qp=K/'queue.json';q=json.loads(qp.read_text());entry=next(x for x in q['editions'] if x['edition']==ed);entry.update(status=b['status'],next_artwork=None);qp.write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n');print(f'Edition{ed}: local integration complete; build/visual checks still required.')
