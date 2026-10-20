"""Local export audit: routes, fragment targets, assets, labels and design delivery."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
from collections import Counter
import json,hashlib
ROOT=Path(__file__).resolve().parents[4];SITE=ROOT/'projects/site';DIST=SITE/'dist';OUT=Path(__file__).parent
class Page(HTMLParser):
 def __init__(self):
  super().__init__(convert_charrefs=True);self.ids=[];self.links=[];self.assets=[];self.images=[];self.labels=[];self.theme=False;self.robots=[];self.title=False;self.in_template=0
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='template':self.in_template+=1
  if a.get('id') and not self.in_template:self.ids.append(a['id'])
  if tag=='a' and a.get('href'):self.links.append(a['href'])
  if tag in ('img','script','source') and a.get('src'):self.assets.append(a['src'])
  if tag=='link' and a.get('rel') in ('stylesheet','icon','preload'):self.assets.append(a.get('href',''))
  if tag in ('img','source') and a.get('srcset'):self.assets.extend(v.strip().split(' ')[0] for v in a['srcset'].split(','))
  if tag=='img':self.images.append(a)
  if tag=='meta' and a.get('name')=='robots':self.robots.append(a.get('content',''))
  if tag=='link' and 'ink-voice.css' in a.get('href',''):self.theme=True
  if tag=='title':self.title=True
 def handle_endtag(self,tag):
  if tag=='template':self.in_template-=1
pages={p.relative_to(DIST).as_posix():Page() for p in DIST.rglob('*.html')}
for name,p in pages.items():p.feed((DIST/name).read_text())
missing=[];fragments=[];dupes=[];alt=[];no_theme=[];no_title=[];robots=[];checked_links=0;checked_assets=0
for name,p in pages.items():
 if not p.title:no_title.append(name)
 if name not in {'search.html'} and not p.theme:no_theme.append(name)
 if not any('noindex' in r for r in p.robots):robots.append(name)
 for ident,n in Counter(p.ids).items():
  if n>1:dupes.append([name,ident,n])
 for img in p.images:
  if 'alt' not in img:alt.append([name,img.get('src')])
 for kind,urls in [('link',p.links),('asset',p.assets)]:
  for raw in urls:
   u=urlsplit(raw)
   if u.scheme or u.netloc or raw.startswith('data:'):continue
   if kind=='link':checked_links+=1
   else:checked_assets+=1
   target=unquote(u.path)
   if target.startswith('/kabita-live/'):target=target[len('/kabita-live/'):]
   elif target.startswith('/'):target=target[1:]
   else:target=(Path(name).parent/target).as_posix() if target else name
   f=DIST/target
   if f.is_dir():f=f/'index.html'
   if not f.is_file():missing.append([name,kind,raw]);continue
   rel=f.relative_to(DIST).as_posix()
   if kind=='link' and u.fragment and rel in pages and unquote(u.fragment) not in pages[rel].ids:fragments.append([name,raw])
result={'intentional_unthemed_redirects':['search.html redirects to poems.html, retaining its no-JavaScript link'], 'html_pages':len(pages),'checked_local_links':checked_links,'checked_asset_references':checked_assets,'missing_files':missing,'missing_fragments':fragments,'duplicate_ids':dupes,'missing_image_alt':alt,'missing_theme':no_theme,'missing_title':no_title,'missing_noindex':robots}
(OUT/'export-audit.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:(len(v) if isinstance(v,list) else v) for k,v in result.items()},indent=2))
for k in ['missing_files','missing_fragments','duplicate_ids','missing_image_alt','missing_theme']:print(k,result[k][:12])
