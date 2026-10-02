#!/usr/bin/env python3
"""Derive edition work batches from the authoritative translation queue."""
from pathlib import Path
from collections import OrderedDict
import json
ROOT=Path(__file__).resolve().parents[1]
folder=ROOT/'kb/production/translations'
queue=json.loads((folder/'queue.json').read_text())
groups=OrderedDict()
for task in queue['tasks']:
 key=task['edition']
 group=groups.setdefault(key,{'id':f'edition-{key:02d}' if key is not None else 'unassigned','edition':key,'poem_ids':[],'translations':[]})
 if task['poem_id'] not in group['poem_ids']:group['poem_ids'].append(task['poem_id'])
 group['translations'].append({k:task[k] for k in ['poem_id','source_language','target_language','source','source_sha256','status']})
for group in groups.values():
 counts={status:sum(t['status']==status for t in group['translations']) for status in ['pending','needs-source','draft-ready','reviewed']}
 group['counts']=counts
 group['status']='pending' if counts['pending'] else 'needs-source' if counts['needs-source'] else 'draft-complete'
 group['remaining_poem_ids']=list(dict.fromkeys(t['poem_id'] for t in group['translations'] if t['status']=='pending'))
active=next((g['id'] for g in groups.values() if g['status']=='pending'),None)
result={'schema_version':1,'mode':'Sequential editions, newest first; original publication order inside each edition','completion_definition':'All requested target versions drafted, integrated and checked; independent linguistic approval remains separate','next_batch':active,'batch_count':len(groups),'actionable_batches':sum(g['status']=='pending' for g in groups.values()),'source_hold_batches':sum(g['status']=='needs-source' for g in groups.values()),'draft_complete_batches':sum(g['status']=='draft-complete' for g in groups.values()),'draft_translations':queue['draft_ready'],'remaining_translations':queue['pending'],'source_held_translations':queue['needs_source'],'batches':list(groups.values())}
assert sum(len(g['translations']) for g in groups.values())==queue['total']
assert len({(t['poem_id'],t['target_language']) for g in groups.values() for t in g['translations']})==queue['total']
(folder/'edition-batches.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='batches'}))
