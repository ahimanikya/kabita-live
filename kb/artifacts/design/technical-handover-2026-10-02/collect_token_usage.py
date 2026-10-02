"""Reproduce the dated, metadata-only Kabita Live usage snapshot.

Reads session metadata and token_count events only; exports no conversation text.
Requires the original machine's local Codex logs. An absent log is not zero usage.
Run from any directory; supply --output to avoid replacing the delivered snapshot.
"""
from pathlib import Path
import argparse, collections, json
ROOTS={
 '01a0f159-e48e-7071-a26f-300966922b0c':'Social pages, editorial content and handover',
 '01a0ee81-0265-7673-a63c-04f6bf884d2d':'Magazine redesign and implementation'
}
def main():
 ap=argparse.ArgumentParser()
 ap.add_argument('--cutoff',default='2026-10-02T18:25:00.000Z')
 ap.add_argument('--log-root',type=Path,default=Path.home()/'.codex')
 ap.add_argument('--output',type=Path,required=True)
 args=ap.parse_args();sessions={}
 for folder in ['sessions','archived_sessions']:
  for path in (args.log_root/folder).rglob('*.jsonl'):
   try:
    with path.open() as f:meta=json.loads(next(f))['payload']
   except (ValueError,KeyError,StopIteration,OSError):continue
   # Prefer the active-session copy if an archive copy repeats its ID.
   sessions.setdefault(meta['id'],(path,meta))
 missing_roots=set(ROOTS)-sessions.keys()
 if missing_roots:raise SystemExit('Required project logs missing: '+', '.join(sorted(missing_roots)))
 rows=[]
 for sid,(path,meta) in sessions.items():
  ancestor=sid;seen=set()
  while ancestor not in ROOTS and ancestor in sessions and ancestor not in seen:
   seen.add(ancestor);m=sessions[ancestor][1];src=m.get('source')
   nested=src.get('subagent',{}).get('thread_spawn',{}) if isinstance(src,dict) else {}
   ancestor=m.get('parent_thread_id') or nested.get('parent_thread_id')
  if ancestor not in ROOTS:continue
  events=[]
  with path.open() as f:
   for line in f:
    try:r=json.loads(line)
    except ValueError:continue
    if r.get('timestamp','')>args.cutoff:continue
    p=r.get('payload',{})
    if r.get('type')=='event_msg' and p.get('type')=='token_count' and p.get('info'):
     events.append((r['timestamp'],p['info']))
  src=meta.get('source');guardian=isinstance(src,dict) and src.get('subagent',{}).get('other')=='guardian'
  row={'session_id':sid,'root_id':ancestor,'kind':'main' if sid in ROOTS else 'automatic_review' if guardian else 'other','usage_events':len(events)}
  if events:
   usage=events[-1][1]['total_token_usage']
   assert usage['input_tokens']+usage['output_tokens']==usage['total_tokens']
   assert 0<=usage.get('cached_input_tokens',0)<=usage['input_tokens']
   assert 0<=usage.get('reasoning_output_tokens',0)<=usage['output_tokens']
   resets=sum(events[i][1]['total_token_usage']['total_tokens']<events[i-1][1]['total_token_usage']['total_tokens'] for i in range(1,len(events)))
   first_equal=events[0][1]['total_token_usage']==events[0][1]['last_token_usage']
   if resets or not first_equal:raise SystemExit('Manual counter/inheritance review required: '+sid)
   row.update(first_event=events[0][0],last_event=events[-1][0],usage=usage,resets=resets,first_equals_last_usage=first_equal)
  rows.append(row)
 summary={}
 for kind in ['main','automatic_review','other']:
  group=[r for r in rows if r['kind']==kind and r.get('usage')]
  summary[kind]={'sessions':len(group),'usage':dict(sum((collections.Counter(r['usage']) for r in group),collections.Counter())),'resets':sum(r['resets'] for r in group)}
 result={'cutoff_utc':args.cutoff,'scope':'Two identified Kabita Live chats and descendants identified by parent-thread metadata; local usage logs only. No raw conversation text copied.','roots':ROOTS,'summary':summary,'sessions':rows,'missing_usage_sessions':sum(not r.get('usage') for r in rows)}
 args.output.write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({'cutoff':args.cutoff,'summary':summary,'unmeasured_sessions':result['missing_usage_sessions']},indent=2))
if __name__=='__main__':main()
