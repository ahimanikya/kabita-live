"""Durable per-image checkpoints for one edition batch; generation stays in built-in tool."""
import argparse,json,hashlib,shutil
from pathlib import Path
from datetime import datetime,timezone
R=Path(__file__).resolve().parents[3];K=Path(__file__).resolve().parent
p=argparse.ArgumentParser();p.add_argument('edition',type=int);p.add_argument('action',choices=['claim','save','review']);p.add_argument('id');p.add_argument('value',nargs='?');a=p.parse_args()
path=K/f'batches/edition-{a.edition}/batch.json';b=json.loads(path.read_text());i=next(x for x in b['items'] if x['id']==a.id);now=datetime.now(timezone.utc).isoformat()
if a.action=='claim':
 assert i['status']=='pending';i.update(status='in_progress',started_at=now);b['status']='in_progress'
elif a.action=='save':
 assert i['status']=='in_progress';i['tool_output']=a.value;path.write_text(json.dumps(b,ensure_ascii=False,indent=2)+'\n')
 target=R/i['output'];assert not target.exists();target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(a.value,target)
 i.update(status='generated',output_sha256=hashlib.sha256(target.read_bytes()).hexdigest(),saved_at=now)
 i['attempts'].append({'version':1,'prompt':i['prompt'],'tool_output':a.value,'output':i['output'],'sha256':i['output_sha256']})
else:
 assert i['status']=='generated';i.update(status='verified',review={'independent':False,'at':now,'outcome':'pass','notes':a.value})
b['updated_at']=now;path.write_text(json.dumps(b,ensure_ascii=False,indent=2)+'\n')
qpath=K/'queue.json';q=json.loads(qpath.read_text());ed=next(x for x in q['editions'] if x['edition']==a.edition);ed.update(status='in_progress',next_artwork=next((x['id'] for x in b['items'] if x['status'] in ['pending','in_progress','generated']),None));q['updated_at']=now;qpath.write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n');print(i['id'],i['status'])
