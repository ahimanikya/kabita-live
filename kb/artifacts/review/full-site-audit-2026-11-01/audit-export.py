"""Read-only static audit of an exported journal; no service mutations."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json,sys,collections
root=Path(sys.argv[1]);out=Path(sys.argv[2])
class Page(HTMLParser):
 def __init__(self,text):
  super().__init__();self.ids=[];self.refs=[];self.h1=0;self.images=[];self.lang=None;self.title=False;self.feed(text)
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if a.get('id'):self.ids.append(a['id'])
  if tag=='html':self.lang=a.get('lang')
  if tag=='h1':self.h1+=1
  if tag=='title':self.title=True
  if tag=='img':self.images.append(a)
  for k in ['href','src','poster']:
   if a.get(k):self.refs.append(a[k])
  if a.get('srcset'):
   self.refs.extend(x.strip().split()[0] for x in a['srcset'].split(',') if x.strip())
pages={p.relative_to(root).as_posix():Page(p.read_text()) for p in root.rglob('*.html')};findings=[];checks=0
for name,p in pages.items():
 for kind,condition in [('missing_language',not p.lang),('missing_title',not p.title),('heading_count',p.h1!=1),('duplicate_ids',len(p.ids)!=len(set(p.ids)))]:
  if condition:findings.append({'page':name,'kind':kind,'detail':p.h1 if kind=='heading_count' else ''})
 for img in p.images:
  if 'alt' not in img:findings.append({'page':name,'kind':'missing_image_alt','src':img.get('src')})
 for ref in p.refs:
  u=urlsplit(ref)
  if u.scheme or u.netloc:continue
  target=(root/u.path.lstrip('/')) if u.path.startswith('/') else root/Path(name).parent/unquote(u.path or Path(name).name)
  if not u.path:target=root/name
  if target.is_dir():target=target/'index.html'
  checks+=1
  if not target.exists():findings.append({'page':name,'kind':'missing_local_target','target':ref})
  elif u.fragment and target.suffix=='.html' and ':~:text=' not in u.fragment:
   dest=pages.get(target.relative_to(root).as_posix())
   if dest and unquote(u.fragment) not in dest.ids:findings.append({'page':name,'kind':'missing_anchor','target':ref})
report={'pages':len(pages),'local_references_checked':checks,'images':sum(len(p.images) for p in pages.values()),'findings_by_kind':dict(collections.Counter(f['kind'] for f in findings)),'findings':findings,'limitations':['Static HTML, not accessibility certification','Runtime-generated anchors require manual classification','No signed-in reviewer, email or submission writes tested']}
out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='findings'}))
