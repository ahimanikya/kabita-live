#!/usr/bin/env python3
"""Maintain the OKF image finder and validate one caption per artwork identity."""
from pathlib import Path
from html.parser import HTMLParser
from collections import defaultdict
import json,re,argparse
ROOT=Path(__file__).resolve().parents[1]
S=(ROOT/'projects/site').resolve() if (ROOT/'projects/site').exists() else ROOT/'site'
K=ROOT/'kb'
rows=json.loads((K/'assets/imagery-catalogue.json').read_text())['artworks']
by_src={a['src']:a for a in rows}
by_resolved={}
for a in rows:
 src=S/a['src']
 for ext in ['.png','.webp','.jpg','.jpeg']:
  for suffix in ['', '-480', '-640', '-768']:
   candidate=src.with_name(src.stem+suffix).with_suffix(ext)
   if candidate.exists():by_resolved[str(candidate.resolve())]=a

def identify(src):return by_src.get(src) or by_resolved.get(str((S/src).resolve()))


def normalize(t):return ' '.join(t.split())
class Figures(HTMLParser):
 def __init__(self):super().__init__();self.figure=None;self.caption=False;self.supplement=0;self.found=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='figure':self.figure={'src':None,'caption':''}
  if self.figure is None:return
  if tag=='img' and self.figure['src'] is None:self.figure['src']=a.get('src')
  if tag=='figcaption':self.caption=True
  if self.caption and tag=='span' and 'edition-cover-sources' in a.get('class',''):self.supplement=1
  elif self.supplement:self.supplement+=1
 def handle_data(self,text):
  if self.caption and not self.supplement:self.figure['caption']+=text
 def handle_endtag(self,tag):
  if self.supplement:self.supplement-=1
  if tag=='figcaption':self.caption=False;self.supplement=0
  if tag=='figure' and self.figure is not None:self.found.append(self.figure);self.figure=None

def scan():
 errors=[];uses=defaultdict(list);checked=0;pages=0
 assert len(by_src)==len(rows) and len({a['id'] for a in rows})==len(rows)
 for a in rows:
  if not (S/a['src']).exists():errors.append('Missing delivery: '+a['src'])
  if a.get('master') and not (K/a['master']).exists():errors.append('Missing master: '+a['master'])
 for p in S.glob('*.html'):
  if p.is_symlink() or p.name=='credits-content.html':continue
  pages+=1;text=p.read_text();parser=Figures();parser.feed(text)
  for src in set(re.findall(r'<img[^>]+src="([^"]+)"',text)):
   if identify(src):uses[identify(src)['src']].append(p.name)
  for f in parser.found:
   if not f['src'] or not identify(f['src']) or not normalize(f['caption']):continue
   checked+=1
   if normalize(f['caption'])!=normalize(identify(f['src'])['caption']):errors.append(p.name+': '+str(f))
 return {'artwork_identities':len(rows),'public_pages_checked':pages,'captions_checked':checked,'asset_paths_recognized':len(by_resolved),'errors':errors},uses

def sync():
 # These older data files remain compatibility projections, not caption authorities.
 p=S/'data/poem-art-library.json';d=json.loads(p.read_text())
 for a in d['artworks']:a['caption']=by_src[a['src']]['caption']
 p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
 p=S/'data/poem-art-captions.json';p.write_text(json.dumps({str(a['poem_id']):a['caption'] for a in rows if 'poem_id' in a},ensure_ascii=False,indent=2)+'\n')
 p=S/'cover-catalogue.json';d=json.loads(p.read_text())
 for a in d:a['cultural_connection']=by_src[a['artwork']]['caption']
 p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
 report,uses=scan()
 text='''---
type: "Asset knowledge"
title: "Imagery finder, canonical captions and reuse"
---

# Find and reuse an image

Start here when looking for earlier artwork. [Visual catalogue](http://127.0.0.1:8771/image-library-audit.html) · [Canonical image records](imagery-catalogue.json) · [Every file, alias and hash](image-inventory.json) · [Usage plan](image-usage-plan.md).

## Choose by purpose

- **Edition covers:** `cover-001` through `cover-047`, with edition/date filenames. Covers stay with their edition; never use them as poem scenery.
- **Poem illustrations:** 23 artworks. Search the caption, multilingual tags or artwork ID below. Match the poem’s imagery; consult [assignment evidence](../records/poem-art-match-evidence.json). Automatic suggestions still need editorial judgment.
- **Inner-page openings:** the 14 records tagged `section-opening`; these watercolor images may also accompany related poems.
- **Homepage:** `home-life-as-it-is`, reserved for the home identity.
- **Portraits:** use the identity map in the [writer system](../research/author-page-system.md) and [portrait source archive](../artifacts/artwork/portrait-sources/). Never select a portrait by visual similarity or generic theme.
- **Reserved:** [Pipili Chandua](../artifacts/artwork/reserved/) is preserved for future use and excluded from the automatic pool.
- **Earlier studies:** [artwork masters](../artifacts/artwork/masters/), [revision history](../history/index.md) and [recovered generation](../artifacts/artwork/recovered-studies/). These are historical, not automatic replacements.
- **Interface:** [icons](icon-catalogue.md) and [design reference](../reference/design-system.md) cover ornaments, background textures and branding.

## One image, one caption

`imagery-catalogue.json` is the caption authority. Its stable image IDs connect delivery files, master files, roles, themes, provenance and the current caption. A thumbnail, alternate format or compatibility filename is still the same artwork. Reused images keep the same caption, punctuation and capitalization. No per-page caption rewrites. Visible homepage, edition and poem artwork captions align right, with a 12px gap beneath the image on desktop and phones. Decorative placements may omit a caption; there is no need to add labels everywhere. Alt text describes what is visible; poem interpretation and cover stories remain separate contextual prose. Historical studies preserve their original wording and are not rewritten to match current records.

Edit a caption once in the canonical record. Run `python3 tools/imagery.py`, rebuild with `python3 projects/site/build.py`, then run `python3 tools/imagery.py --check`. Refresh the finder after the build to update page locations. The compatibility caption files are generated projections. `tools/audit_images.py` refreshes the complete file inventory and visual catalogue; it does not overwrite canonical captions. Sync the portable package after all checks.

## Border or paper edge

Current treatment: watercolor openings with soft paper edges blend into the background. All inner-page artwork, including edition covers and poem illustrations, is borderless under the user’s latest instruction. Only homepage artwork retains the approved fine warm keyline. Preserve the original bitmap; presentation belongs in CSS.

## Artwork records

Search this page for a place, motif, caption, edition, or image ID. Page locations below are discovered from current public HTML, not guessed from filenames. The full inventory also lists unused files and historical aliases.

'''
 for a in rows:
  locations=uses.get(a['src'],[])
  text+=f'### {a["id"]} · {a["title"]}\n\n'
  text+='- Caption: '+a['caption']+'\n- Roles: '+', '.join(a['roles'])+'; treatment: '+a['treatment']+'.\n'
  text+='- Find by: '+', '.join(a['tags'])+'.\n- Delivery: `'+a['src']+'`.\n'
  if a.get('master'):text+='- [Original master](../'+a['master']+').\n'
  text+='- [Provenance](../'+a['provenance']+').\n'
  text+='- Used on '+str(len(locations))+' pages: '+', '.join('['+n+'](http://127.0.0.1:8771/'+n+')' for n in sorted(locations))+'.\n\n'
 (K/'assets/imagery.md').write_text(text)
 (K/'records/imagery-usage.json').write_text(json.dumps({by_src[src]['id']:sorted(v) for src,v in uses.items()},ensure_ascii=False,indent=2)+'\n')
 return report

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');args=p.parse_args()
 report=scan()[0] if args.check else sync()
 if args.check:(K/'records/imagery-caption-verification.json').write_text(json.dumps({**report,'independent':False,'scope':'Current public figures; historical review snapshots excluded.'},indent=2)+'\n')
 print(json.dumps(report,indent=2))
 if args.check and report['errors']:raise SystemExit(1)
