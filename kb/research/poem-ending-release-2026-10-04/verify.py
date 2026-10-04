from pathlib import Path
import hashlib,json,re,sys
from html.parser import HTMLParser
R=Path('/Users/ahimanikya/Projects/Kabita Live');K=R/'kb/research/poem-ending-release-2026-10-04';C=Path(sys.argv[1]);S=C/'projects/site';B=json.loads((K/'baseline.json').read_text())
for p,h in B['protected'].items():assert hashlib.sha256((C/p).read_bytes()).hexdigest()==h,p
new=json.loads((S/'assets/reading-all.json').read_text())['poems'];assert len(new)==len(B['readers'])
class Nav(HTMLParser):
 def __init__(self):super().__init__();self.active=False;self.dest=None;self.count=0
 def handle_starttag(self,t,a):
  a=dict(a)
  if t=='a' and 'poem-step' in a.get('class',''):self.dest=a['aria-label'].split(': ',1)[1]
  if t=='span' and a.get('class')=='poem-step-title':self.active=True;self.text=''
 def handle_data(self,d):
  if self.active:self.text+=d
 def handle_endtag(self,t):
  if t=='span' and self.active:assert self.text==self.dest,(self.text,self.dest);self.active=False;self.count+=1
count=0;pages=[];langs=0
for before,after in zip(B['readers'],new):
 assert before=={k:v for k,v in after.items() if k!='end_mark'},after['id']
 langs+=len(after['variants']);assert after['end_mark'] in ['leaf','paired','sprig']
 html=(S/'dist'/after['route']).read_text();assert 'noindex,nofollow' in html
 data=json.loads(re.search(r'id="reading-data">(.*?)</script>',html,re.S)[1]);assert data['variants']==before['variants'];assert data['end_mark']==after['end_mark']
 marks=re.findall(r'class="poem-closing-mark" data-end-mark="(.*?)"',html);assert marks==([] if after.get('availability') else [after['end_mark']]),after['id']
 nav=Nav();nav.feed(html);count+=nav.count;pages.append(after['route'])
assert not (S/'dist/kb').exists()
runtime=json.loads((S/'dist/runtime-config.json').read_text());runtime['analytics'].pop('basePath',None);runtime['analytics'].pop('publicPages',None);assert runtime==json.loads((S/'runtime-config.json').read_text())
assets={}
for f in ['poem-end-leaf.svg','poem-end-paired.svg','poem-end-sprig.svg','poem-experience.js','poem-experience.css']:
 p='assets/'+f;assert (S/'dist'/p).read_bytes()==(S/p).read_bytes();assets[p]=hashlib.sha256((S/'dist'/p).read_bytes()).hexdigest()
result={'result':'PASS','base':B['base'],'protected_files':len(B['protected']),'poems':len(new),'unchanged_language_variants':langs,'neighbouring_titles':count,'noindex':True,'runtime_preserved':True,'assets':assets,'pages':pages}
(K/'verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print({k:v for k,v in result.items() if k not in ['pages','assets']})
