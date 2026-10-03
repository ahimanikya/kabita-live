"""Verify originals, unrelated mappings, inputs and published page text."""
from pathlib import Path
from html.parser import HTMLParser
import json,hashlib,sys
ROOT=Path(__file__).resolve().parents[4]
RELEASE=Path('/private/tmp/kbl-selective-portraits-20261003')
HERE=Path(__file__).resolve().parent
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
class Text(HTMLParser):
 def __init__(self):super().__init__();self.bits=[];self.skip=0
 def handle_starttag(self,t,a):
  if t in ('script','style'):self.skip+=1
 def handle_endtag(self,t):
  if t in ('script','style'):self.skip=max(0,self.skip-1)
 def handle_data(self,d):
  if not self.skip:self.bits.append(d)
def text_sha(p):
 parser=Text();parser.feed(p.read_text());return hashlib.sha256(' '.join(' '.join(parser.bits).split()).encode()).hexdigest()
baseline=read(HERE/'release-baseline.json')
if '--capture-text' in sys.argv:
 assert all(sha(RELEASE/'projects/site'/p)==v['hash'] for p,v in baseline['pages'].items())
 (HERE/'release-visible-text-baseline.json').write_text(json.dumps({p:text_sha(RELEASE/'projects/site'/p) for p in baseline['pages']},indent=2)+'\n')
 print('Captured normalized text of unchanged baseline pages');sys.exit()
q=read(ROOT/'kb/records/selective-portrait-fixes-2026-10-03.json');ids={str(x) for x in q['writer_ids']}
preserve=read(HERE/'preservation.json');errors=[]
for p,h in preserve['files'].items():
 if not (ROOT/p).exists() or sha(ROOT/p)!=h:errors.append('original changed: '+p)
current=read(ROOT/'projects/site/data/writer-portraits.json')
if {k:v for k,v in current.items() if k not in ids}!=preserve['non_shortlisted_mapping']:errors.append('unrelated local mapping changed')
if '--local-only' not in sys.argv:
 release_map=read(RELEASE/'projects/site/data/writer-portraits.json')
 if {k:v for k,v in release_map.items() if k not in ids}!={k:v for k,v in baseline['mapping'].items() if k not in ids}:errors.append('unrelated published mapping changed')
 for p,h in baseline['preserved_inputs'].items():
  if sha(RELEASE/p)!=h:errors.append('published input changed: '+p)
 for p,h in read(HERE/'release-visible-text-baseline.json').items():
  if text_sha(RELEASE/'projects/site'/p)!=h:errors.append('published text changed: '+p)
result={'result':'FAIL' if errors else 'PASS','original_files_checked':len(preserve['files']),'selected_ids':q['writer_ids'],'published_pages_text_checked':0 if '--local-only' in sys.argv else len(baseline['pages']),'errors':errors,'independent':False}
(HERE/('local-preservation-check.json' if '--local-only' in sys.argv else 'release-scope-check.json')).write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result));sys.exit(bool(errors))
