"""Inventory image files, uses and preserved variants; generate a local review catalogue."""
from pathlib import Path
from collections import Counter,defaultdict
import os,json,hashlib,re,html
from PIL import Image
R=Path(__file__).resolve().parents[1];S=(R/'projects/site').resolve();exts={'.png','.webp','.jpg','.jpeg','.svg','.gif','.avif'}
exclude={'audit-images','.git','node_modules','.generated','.public','.astro','dist','kabita-live-project','__pycache__'}
files=[];aliases=[]
for base,dirs,names in os.walk(R,followlinks=False):
 dirs[:]=[n for n in dirs if n not in exclude and not (Path(base)/n).is_symlink()]
 for n in names:
  p=Path(base)/n
  if p.suffix.lower() not in exts:continue
  if p.is_symlink():
   aliases.append({'path':str(p.relative_to(R)),'target':str(p.resolve().relative_to(R)) if p.resolve().is_relative_to(R) else str(p.resolve()),'valid':p.exists()});continue
  files.append(p)
usage=defaultdict(set)
for p in [x for x in S.glob('*.html') if not x.is_symlink()]+list((S/'assets').glob('*.css')):
 text=p.read_text()
 for ref in re.findall(r'(?:src|href)=[\"\']([^\"\']+)|url\([\"\']?([^\)\"\']+)',text):
  value=next((x for x in ref if x),'').split('?')[0].split('#')[0]
  if not value or value.startswith(('data:','http:','https:')):continue
  q=(p.parent/value).resolve()
  if q.suffix.lower() in exts and q.exists():usage[str(q)].add(p.name)
 for srcset in re.findall(r'srcset="([^"]+)"',text):
  for entry in srcset.split(','):
   q=(p.parent/entry.strip().split()[0]).resolve()
   if q.exists():usage[str(q)].add(p.name)
cover_data=json.loads((S/'cover-catalogue.json').read_text());active_covers={str((S/x['artwork']).resolve()):x for x in cover_data}
poem_data=json.loads((S/'data/poem-art-library.json').read_text())['artworks'];poem_paths={str((S/x['src']).resolve()):x for x in poem_data}
def role(p):
 t=str(p.relative_to(R));name=p.name
 if '/reserved/' in t:return 'Reserved'
 if '/recovered-studies/' in t:return 'Historical studies'
 if '/portrait-sources/' in t:return 'Portrait sources'
 if '/covers/' in t or '/edition-sources/' in t:return 'Edition covers'
 if '/poem-library-' in t or '/poem-art/' in t:return 'Poem illustrations'
 if '/section-art/' in t:return 'Inner-page illustrations'
 if '/home/' in t:return 'Homepage artwork'
 if '/writers/' in t or '/writer-portraits/' in t or '/editors/' in t:return 'Portraits'
 if '/backgrounds/' in t:return 'Paper textures'
 if '/icons/' in t:return 'Icons'
 if '/history/' in t:return 'Historical studies'
 if '/evidence/' in t or '/review/' in t:return 'Review evidence'
 if p.suffix=='.svg':return 'Brand and interface'
 return 'Other preserved material'
records=[];duplicates=defaultdict(list)
for p in files:
 digest=hashlib.sha256(p.read_bytes()).hexdigest();dimensions=None
 if p.suffix.lower()!='.svg':
  try:
   with Image.open(p) as im:dimensions=list(im.size)
  except Exception:pass
 category=role(p);uses=sorted(usage.get(str(p),[]));status='active' if uses else 'preserved'
 if category=='Reserved':status='reserved'
 if str(p) in active_covers:status='active edition identity'
 if str(p) in poem_paths:status='active poem library'
 rec={'path':str(p.relative_to(R)),'category':category,'status':status,'bytes':p.stat().st_size,'dimensions':dimensions,'sha256':digest,'public_reference_count':len(uses),'reference_examples':uses[:6]}
 records.append(rec);duplicates[digest].append(rec['path'])
summary={'file_count':len(records),'exact_unique_files':len(duplicates),'aliases':len(aliases),'broken_aliases':[x for x in aliases if not x['valid']],'files_by_role':dict(Counter(x['category'] for x in records)),'active_edition_covers':47,'earlier_section_illustrations':14,'dedicated_poem_illustrations':9,'earlier_generation_outputs':96,'cache_outputs_already_preserved':95,'recovered_historical_output':1,'scope':'Canonical workspace including KB history and website assets. Portable, build outputs and dependency folders excluded as copies; archived ZIP contents not unpacked. File counts include formats, sizes, proof images and preserved variants, not unique artworks.'}
result={'summary':summary,'images':records,'aliases':aliases,'exact_duplicate_groups':[v for v in duplicates.values() if len(v)>1]}
(R/'kb/assets/image-inventory.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
# Catalogue: use logical collections first; all physical files remain available in the second view.
preview=S/'audit-images';preview.mkdir(exist_ok=True)
def url(p):
 p=p.resolve();key=hashlib.sha256(str(p).encode()).hexdigest()[:20]+p.suffix;link=preview/key
 if not link.exists():link.symlink_to(os.path.relpath(p,preview))
 return 'audit-images/'+key
caption_records={a['src']:a for a in json.loads((R/'kb/assets/imagery-catalogue.json').read_text())['artworks']}
caption_paths={str((S/src).resolve()):a for src,a in caption_records.items()}
cards=[]
def card(path,title,category,note):
 p=Path(path).resolve();a=caption_paths.get(str(p),{});cards.append({'src':url(p),'title':title,'category':category,'note':note,'caption':a.get('caption',''),'tags':a.get('tags',[]),'filename':p.name})
for c in sorted(cover_data,key=lambda x:x['number'],reverse=True):card(S/c['artwork'],f'Edition {c["number"]:03d} · {c["date"]}','Edition covers',c['title']+' · Exclusive edition identity; never a poem illustration.')
for a in poem_data:
 card(S/a['src'],a['caption'],'Poem illustrations',('Earlier inner-page art, reused when text motifs match.' if a['usage']=='section-and-poem' else 'Dedicated poem illustration.'))
for slug in ['dokana','kshanika','drink']:card(S/f'assets/poem-art/{slug}.webp',slug.title(),'Poem illustrations','Bespoke illustration, retained with its original poem.')
for p in sorted((S/'assets/section-art').glob('*.webp')):
 if '-640' not in p.stem:card(p,p.stem.replace('-',' ').title(),'Inner-page illustrations','Existing section opening; available for relevant poem motifs, never a cover.')
card(S/'assets/home/life-after-rain.webp','LIFE AS IT IS','Homepage artwork','Homepage identity; retain separately from cover and poem libraries.')
card(R/'kb/artifacts/artwork/reserved/pipili-chandua.webp','Pipili Chandua','Reserved','Reserved for future use, as requested. Not in the poem pool.')
# Historical cover alternatives identified by the preserved cover filename mapping.
active_sources={Path(x['previous']).stem for x in json.loads((R/'kb/records/edition-cover-filenames.json').read_text())}
for p in sorted((R/'kb/artifacts/artwork/masters/covers/editions').glob('*.png')):
 if p.stem not in active_sources:card(p,p.stem,'Historical studies','Earlier cover version. Preserve as history; excluded from poem library.')
for p in sorted((R/'kb/artifacts/history/revisions/revision-05').glob('*.png')):card(p,p.stem.replace('-',' ').title(),'Historical studies','Earlier photographic cover concept; not a poem asset.')
card(R/'kb/artifacts/artwork/recovered-studies/evening-water-earlier-output.png','Evening water · earlier output','Historical studies','Recovered from this chat’s generated-image cache. Near-duplicate historical variant.')
portraits=json.loads((S/'data/writer-portraits.json').read_text());writers={str(x['id']):x['name'] for x in json.loads((S/'data/writer-profiles.json').read_text())}
for ident,a in portraits.items():card(S/a['src'],writers.get(ident,'Writer '+ident),'Portraits',f'Writer {ident} · {a["kind"]} · Identity-bound; never random scenery.')
for ed in json.loads((S/'editor-profiles.json').read_text()):card(S/ed['portrait'],ed['name'],'Portraits',ed['role']+' · Identity-bound portrait.')
for p in sorted((S/'assets/backgrounds').glob('*')):
 if p.suffix in exts:card(p,p.stem.replace('-',' ').title(),'Paper textures','Background texture; not a content illustration.')
all_cards=[{'src':url(R/x['path']),'title':Path(x['path']).name,'category':x['category'],'note':x['status']+' · '+str(x['public_reference_count'])+' public references · '+x['path'],'filename':Path(x['path']).name} for x in records]
data=json.dumps({'collections':cards,'files':all_cards,'summary':summary},ensure_ascii=False).replace('<','\\u003c')
html_doc='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>Image library · Kabita Live</title><link rel="stylesheet" href="assets/style.css"><style>main{padding:32px 0}h1{font-size:48px;margin:20px 0}.intro{font:18px/1.7 var(--ui);max-width:850px}.controls{display:flex;gap:16px;flex-wrap:wrap;margin:26px 0}.controls label{font:15px var(--ui)}.controls select,.controls input{min-height:48px;max-width:280px}.gallery{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:30px}.gallery figure{margin:0;min-width:0}.gallery img{width:100%;height:220px;object-fit:contain;background:color-mix(in srgb,var(--panel) 30%,transparent)}.gallery h2{font-size:25px;margin:14px 0 8px}.gallery p{font:14px/1.6 var(--ui);overflow-wrap:anywhere}.gallery code{font-size:12px;overflow-wrap:anywhere}.pagination{display:flex;align-items:center;gap:20px;margin:32px 0}.pagination button{min-height:48px;padding:12px;border:1px solid var(--line)}@media(max-width:760px){.gallery{grid-template-columns:1fr}.gallery img{height:auto;max-height:340px}h1{font-size:38px}}</style></head><body class="journal-paper cotton-paper site-theme"><script src="assets/appearance.js"></script><main class="wrap"><a href="index.html">Kabita Live</a><p>Captions follow the shared artwork record. Search by artwork name, edition or filename.</p><h1>A place for every image.</h1><p class="intro">47 edition identities, 14 earlier section illustrations, 9 dedicated poem artworks, portraits, textures and preserved studies. Covers remain with their editions. Poem illustrations now follow textual motifs. Pipili Chandua stays reserved.</p><p class="intro">Collection view groups assets by their purpose. The complete file view includes original masters, sizes, formats and historical evidence. This is a local knowledge-base catalogue.</p><div class="controls"><label>View<select id="view"><option value="collections">Art collections</option><option value="files">Every image file</option></select></label><label>Use<select id="category"><option value="all">All uses</option></select></label><label>Find<input id="query" type="search" placeholder="Edition, motif, caption or file"></label></div><p id="count" role="status"></p><div id="gallery" class="gallery"></div><div class="pagination"><button id="previous">Previous</button><span id="page"></span><button id="next">Next</button></div><script id="catalogue" type="application/json">'''+data+'''</script><script>const data=JSON.parse(document.querySelector('#catalogue').textContent);let page=0;const batch=24;const categories=[...new Set(data.files.concat(data.collections).map(x=>x.category))].sort();for(const c of categories){let o=document.createElement('option');o.value=c;o.textContent=c;document.querySelector('#category').append(o)}function render(){let list=data[document.querySelector('#view').value],cat=document.querySelector('#category').value,q=document.querySelector('#query').value.toLowerCase();list=list.filter(x=>(cat==='all'||x.category===cat)&&[x.title,x.note,x.filename,x.caption,...(x.tags||[])].join(' ').toLowerCase().includes(q));page=Math.min(page,Math.max(0,Math.ceil(list.length/batch)-1));let g=document.querySelector('#gallery');g.replaceChildren();for(const x of list.slice(page*batch,(page+1)*batch)){let f=document.createElement('figure'),a=document.createElement('a'),im=document.createElement('img'),h=document.createElement('h2'),p=document.createElement('p'),code=document.createElement('code');a.href=x.src;im.src=x.src;im.alt=x.title;im.loading='lazy';a.append(im);h.textContent=x.title;p.textContent=x.category+' · '+x.note;code.textContent=x.filename;f.append(a,h,p,code);g.append(f)}document.querySelector('#count').textContent=list.length+' entries';document.querySelector('#page').textContent='Page '+(page+1)+' of '+Math.max(1,Math.ceil(list.length/batch));document.querySelector('#previous').disabled=page===0;document.querySelector('#next').disabled=(page+1)*batch>=list.length}for(const id of ['view','category','query'])document.querySelector('#'+id).addEventListener(id==='query'?'input':'change',()=>{page=0;render()});document.querySelector('#previous').onclick=()=>{page--;render()};document.querySelector('#next').onclick=()=>{page++;render()};render();</script></main></body></html>'''
p=R/'kb/artifacts/review/site/image-library-audit.html';p.write_text(html_doc);alias=S/'image-library-audit.html'
if not alias.exists():alias.symlink_to(os.path.relpath(p,S))
report='''---
type: "Asset audit"
title: "Image inventory and usage plan"
---

# Image inventory and usage plan

[Imagery finder and canonical captions](imagery.md) · [Open the visual catalogue](http://127.0.0.1:8771/image-library-audit.html) · [Complete file inventory](image-inventory.json) · [Cover filename mapping](../records/edition-cover-filenames.json) · [Poem matching evidence](../records/poem-art-match-evidence.json)

'''
report+=f"Inventoried **{len(records)} physical image files**, **{len(duplicates)} exact unique file contents**, and **{len(aliases)} compatibility aliases**. These counts include masters, delivery formats, thumbnails and evidence screenshots; they are not counts of unique artworks. The portable handoff and generated/dependency directories are excluded as copies. Historical ZIP contents were not unpacked.\n\n"
report+='| Intended role | Policy |\n|---|---|\n| Edition covers | 47 active identities, named `edition-NNN-YYYY-MM.webp`; `-480.webp` thumbnails; matching named master aliases. Each belongs to its own edition. Never selected for poems. |\n| Poem artwork | 9 dedicated images, plus 14 previously generated inner-page illustrations reused where text motifs support them. Preserve original captions and provenance. |\n| Inner pages | 14 existing watercolor openings. Can support related poem motifs; no cover reuse. |\n| Homepage | LIFE AS IT IS remains the homepage identity. |\n| People | Identity-bound writer/editor portraits and original reference photographs; never randomized. |\n| Reserved | Pipili Chandua retained for future use, excluded from all automatic selection. |\n| Textures, icons and brand | Interface assets, separate from editorial illustrations. |\n| History and evidence | Alternate covers, early photographic concepts, superseded treatments and screenshots retained unchanged. |\n\n'
report+='## Earlier generations\n\nAll 96 image outputs in this chat’s generation folder were compared by SHA-256: 95 already had an exact copy in the project. The remaining early evening-water output is now preserved under `artifacts/artwork/recovered-studies/`. It closely resembles the earlier photographic cover concept; it is retained as a historical variant, not introduced as poem art.\n\n## Poem connections\n\nTitle and body motifs are matched in Odia, Hindi and English, with evidence stored per poem. The current issue has targeted context-reviewed overrides, including rain → wet courtyard, a departed poet → empty chair, writing → notebook/pen, and freedom → open window. The remaining automated links are assisted suggestions, not a claim of full native-language editorial review. Neutral reading imagery is used where no clear motif is found. Relevant imagery takes priority over avoiding repeats.\n\n## Preservation and review\n\nNo historical originals, portrait sources, cover studies or generation outputs were deleted. Exact duplicates are reported, not destructively deduplicated. Active cover delivery names changed with compatibility aliases retained. This is current-assistant self-review (`independent: false`), not publication approval.\n'
report+='\n## File counts by role\n\n| Role | Files |\n|---|---:|\n'+''.join(f'| {k} | {v} |\n' for k,v in summary['files_by_role'].items())
(R/'kb/assets/image-usage-plan.md').write_text(report)
print(json.dumps(summary,indent=2))
