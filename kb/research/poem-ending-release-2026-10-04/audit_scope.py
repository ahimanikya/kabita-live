"""Prove every modified generated file contains only the approved ending delta."""
from pathlib import Path
from html.parser import HTMLParser
import json,subprocess,sys,re,collections
R=Path('/Users/ahimanikya/Projects/Kabita Live');K=R/'kb/research/poem-ending-release-2026-10-04';C=Path(sys.argv[1]);base=json.loads((K/'baseline.json').read_text())['base']
def git(*args):return subprocess.check_output(['git','-C',str(C),*args])
def old(p):return git('show',base+':'+p).decode()
def strip_mark(x):
 if isinstance(x,dict):return {k:strip_mark(v) for k,v in x.items() if k!='end_mark'}
 if isinstance(x,list):return [strip_mark(v) for v in x]
 return x
class Page(HTMLParser):
 def __init__(self,text):super().__init__(convert_charrefs=True);self.tokens=[];self.nav=[];self.skip=None;self.depth=0;self.json=False;self.feed(text)
 def handle_starttag(self,t,a):
  a=dict(a);cls=a.get('class','')
  if 'poem-step ' in cls:self.nav.append((t,a))
  if self.skip:
   if t==self.skip:self.depth+=1
   return
  if cls in ['poem-reading-end','poem-closing-mark']:
   self.skip=t;self.depth=1;return
  for k,v in list(a.items()):
   if k in ['src','href']:
    v=re.sub(r'poem-experience.css\?v=(?:9|12)\b','poem-experience.css?v=ENDING',v)
    a[k]=re.sub(r'poem-experience.js\?v=(?:7|9)\b','poem-experience.js?v=ENDING',v)
  self.json=t=='script' and a.get('type')=='application/json';self.tokens.append(('start',t,sorted(a.items())))
 def handle_endtag(self,t):
  if self.skip:
   if t==self.skip:
    self.depth-=1
    if not self.depth:self.skip=None
   return
  self.tokens.append(('end',t));self.json=False
 def handle_data(self,d):
  if self.skip or not d.strip():return
  self.tokens.append(('data',json.dumps(strip_mark(json.loads(d)),ensure_ascii=False,sort_keys=True) if self.json else d))
 def handle_comment(self,d):
  if not self.skip:self.tokens.append(('comment',d))
changes=[l.split('\t',1) for l in git('diff','--name-status',base,'HEAD').decode().splitlines()];counts=collections.Counter();errors=[]
site='output/kabitalive-design-proposal-2026-09-29/site/'
source={'assets/poem-experience.css','assets/poem-experience.js','build.py','edition-pages.py','poem_reader.py','tests/reader-pagination.test.mjs'}
newsource={'assets/poem-end-leaf.svg','assets/poem-end-paired.svg','assets/poem-end-sprig.svg','poem_end_marks.py','data/poem-end-mark-overrides.json'}
kb_existing={'kb/artifacts/design/brand-guide/DESIGN-SYSTEM.md','kb/reference/design-system.md','kb/registers/DASHBOARD.md','kb/registers/activity.jsonl','kb/registers/records.json','kb/review/index.md'}
for status,p in changes:
 new=(C/p).read_bytes()
 if p.startswith(site):
  rel=p[len(site):]
  if status=='A':assert rel in newsource,p;counts['new_closing_mark_sources']+=1
  elif rel.endswith('.html'):
   a,b=Page(old(p)),Page(new.decode())
   if a.tokens!=b.tokens or a.nav!=b.nav:
    mismatch=next(((i,str(x)[:250],str(y)[:250]) for i,(x,y) in enumerate(zip(a.tokens,b.tokens)) if x!=y),None);errors.append({'path':p,'mismatch':mismatch,'lengths':[len(a.tokens),len(b.tokens)],'nav_equal':a.nav==b.nav})
   counts['html_only_approved_ending_markup_and_asset_versions']+=1
  elif rel.startswith('assets/reading-') and rel.endswith('.json'):
   assert json.loads(old(p))==strip_mark(json.loads(new)),p;counts['reader_json_only_end_mark_added']+=1
  else:assert rel in source,p;counts['reviewed_source_files']+=1
 else:
  assert p.startswith('kb/'),p
  if status=='M':assert p in kb_existing,p;counts['existing_kb_files']+=1
  else:assert any(p.startswith(prefix) for prefix in ['kb/artifacts/review/poem-end-marks-2026-10-04/','kb/research/poem-ending-release-2026-10-04/','kb/records/poem-end-marks-','kb/records/poem-ending-']),p;counts['new_task_only_evidence_files']+=1
old_records=json.loads(old('kb/registers/records.json'));new_records=json.loads((C/'kb/registers/records.json').read_text());added=[x for x in new_records['decisions'] if x not in old_records['decisions']]
assert {x['id'] for x in added}=={'KBL-DEC-047','KBL-DEC-048','KBL-DEC-049'}
new_records['decisions']=[x for x in new_records['decisions'] if x not in added];assert new_records==old_records
old_events=old('kb/registers/activity.jsonl');new_events=(C/'kb/registers/activity.jsonl').read_text();assert new_events.startswith(old_events);extra=new_events[len(old_events):].strip().splitlines();assert len(extra)==1 and json.loads(extra[0])['evidence']==['records/poem-ending-deployment-2026-10-04.json']
for p in ['kb/artifacts/design/brand-guide/DESIGN-SYSTEM.md','kb/reference/design-system.md','kb/review/index.md']:assert (C/p).read_text().startswith(old(p)),p
result={'result':'PASS' if not errors else 'FAIL','commit':git('rev-parse','HEAD').decode().strip(),'base':base,'total_changed_files':len(changes),'categories':dict(counts),'generated_html_semantics':'Only closing-mark nodes, approved previous/next presentation, end_mark JSON fields and reader asset cache versions differ. All navigation targets and other DOM tokens preserved.','knowledge_records':'Existing records unchanged; only DEC047/048/049 and one deployment event added; design/review references append-only.','errors':errors}
(K/'scope-audit.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False,indent=2));assert not errors
