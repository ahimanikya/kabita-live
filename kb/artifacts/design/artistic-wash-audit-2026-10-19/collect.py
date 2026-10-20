"""Read-only source inventory for the artistic audit; not browser/render verification."""
from pathlib import Path
from html.parser import HTMLParser
from collections import Counter
import hashlib,json
ROOT=Path(__file__).resolve().parents[4]
SITE=ROOT/'projects/site'
OUT=Path(__file__).parent
ROUTES=['index.html','issue-48.html','issue-47.html','poem-824.html','poem-831.html','poet-476.html','poems.html','poets.html','archive.html','about.html','editorial-team.html','contact.html','feedback.html','submit.html','thirty-languages-and-the-journey-of-a-poem.html']
class Page(HTMLParser):
 def __init__(self): super().__init__();self.body='';self.css=[];self.images=[];self.classes=Counter()
 def handle_starttag(self,tag,attrs):
  d=dict(attrs)
  if tag=='body':self.body=d.get('class','')
  if tag=='link' and d.get('rel')=='stylesheet':self.css.append(d['href'].split('?')[0])
  if tag=='img':self.images.append({k:d[k] for k in ['src','alt'] if k in d})
  self.classes.update(d.get('class','').split())
def hash_file(p):return hashlib.sha256(p.read_bytes()).hexdigest()
pages={};files=set()
for route in ROUTES:
 p=Page();p.feed((SITE/route).read_text());files.add(route);files.update(p.css)
 pages[route]={'body':p.body,'stylesheet_order':p.css,'art_classes':{k:v for k,v in p.classes.items() if any(t in k for t in ['art','cover','vignette','portrait','waterline','opening','feature'])},'images':p.images,'duplicate_stylesheets':[k for k,v in Counter(p.css).items() if v>1]}
files.update(['assets/poetic-waterline.svg','assets/header-separator-connected.svg','assets/odisha-watercolour-poetic-natural.webp'])
all_pages=list(SITE.glob('*.html'));themes=Counter()
for path in all_pages:
 p=Page();p.feed(path.read_text());
 if 'site-theme' in p.body.split():themes['site_theme']+=1
 if 'site-theme' in p.body.split() and 'journal-paper' in p.body.split():themes['theme_with_disabled_body_paper_layer']+=1
hashes={f:hash_file(SITE/f) for f in sorted(files) if (SITE/f).is_file()}
(OUT/'source-inventory.json').write_text(json.dumps({'scope':'Static source inventory only; no DOM/computed style or browser rendering inspected in this run.','top_level_html_files':len(all_pages),'theme_counts':dict(themes),'representative_routes':pages,'source_sha256':hashes},ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'representative_routes':len(pages),'hashed_source_files':len(hashes),'theme_counts':dict(themes)},indent=2))
