"""Checkpoint a claimed generation; never overwrite a retained candidate."""
import argparse,json,hashlib,shutil
from pathlib import Path
from datetime import datetime,timezone
R=Path(__file__).resolve().parents[3];K=Path(__file__).resolve().parent
p=argparse.ArgumentParser();p.add_argument('action',choices=['claim','save','review']);p.add_argument('id');p.add_argument('value',nargs='?');a=p.parse_args()
path=K/'queue.json';q=json.loads(path.read_text());item=next(i for i in q['items'] if i['id']==a.id);now=datetime.now(timezone.utc).isoformat()
if a.action=='claim':
 assert item['status']=='pending',item['status']
 item.update(status='in_progress',started_at=now)
 q['active_batch']={'id':item['batch'],'owner':'current-chat-assistant','started_at':now,'status':'running'}
elif a.action=='save':
 assert item['status']=='in_progress',item['status']
 item['tool_output']=a.value
 # Persist the tool evidence before any filesystem copy.
 path.write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n')
 target=R/item['output'];target.parent.mkdir(exist_ok=True,parents=True)
 assert not target.exists(),target
 shutil.copy2(a.value,target)
 item.update(status='generated',output_sha256=hashlib.sha256(target.read_bytes()).hexdigest(),saved_at=now)
 item['attempts'].append({'version':1,'prompt':item['prompt'],'tool_output':a.value,'output':item['output'],'sha256':item['output_sha256']})
elif a.action=='review':
 assert item['status']=='generated',item['status']
 item.update(status='verified',review={'independent':False,'reviewed_at':now,'outcome':'pass','notes':a.value})
q['updated_at']=now;q['counts']={s:sum(i['status']==s for i in q['items']) for s in ['pending','in_progress','generated','verified','held','integrated_local']}
q['next_id']=next((i['id'] for i in q['items'] if i['status'] in ['pending','in_progress','generated']),None)
path.write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'item':item['id'],'status':item['status'],'counts':q['counts'],'next':q['next_id']}))
