from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
import json,shutil,hashlib
r=Path(__file__).resolve().parents[1]; p=r.parent/'kabita-live-project'
revision=r/'revision-19-cover-stories'
c=json.loads((r/'site/cover-catalogue.json').read_text())
m={x['issue']:x for x in json.loads((r/'revision-18-covers/manifest.json').read_text())}
m.update({x['issue']:x for x in json.loads((revision/'manifest.json').read_text())})
for x in c:m[x['number']].update(title=x['title'],theme=x['theme'],master=x['artwork'].replace('.webp','.png'))
(revision/'current-47-manifest.json').write_text(json.dumps([m[x['number']] for x in c],ensure_ascii=False,indent=2))
readme='''# Kabita Live · 47 covers with stories

Revision 19 · 29 September 2026

All 47 proposed covers have original poetic narratives and separate cultural notes. Ten new artworks broaden the collection with Sambalpuri sari, Puri gamucha, kendu woodland generally, Similipal, Deomali, Fakir Mohan Senapati, Pipili appliqué, Raghurajpur painting, Kantilo bell-metal and Konark. The existing loom artwork has an imaginative Gangadhar Meher tribute.

Use the site cover gallery to view each story in an optional disclosure. Historical dates and issue links remain; these newly imagined covers do not describe the original contents. The previous 47 artwork masters remain intact in the project. The active cover catalogue selects 37 previous artworks and 10 new versioned artworks.

Generation: built-in image generation tool, one image per prompt. Exact new prompts and source provenance: manifest.json. All active prompts: current-47-manifest.json. Cover stories: COVER-STORIES.md. Editor guidance: EDITOR-COVER-CARD.md. Master PNGs, responsive WebP and separately editable masthead SVGs are included in the cover package. The SVGs retain live type and require the indicated fonts for intended shaping.

The images are cultural interpretations, not documentary photographs. The Fakir Mohan likeness was guided by the portrait published on Srujanee (linked in manifest.json), with literary context from Government of Odisha. The reference is research material, not a newly commissioned source photograph. Future portrait directions are planning only.

The one-page branding PDF is unchanged; the cover-story card is its new companion.
'''
(revision/'README.md').write_text(readme)
# Regenerate the narrative document from the authoritative catalogue, including latest sources.
doc='# Kabita Live · Forty-seven stories of home\n\nମାଟିର ମହକ · ମନର ସ୍ୱର\n\nOriginal narratives for newly proposed cover art; these are not historical issue summaries.\n\n'
for x in c:
 doc+=f"## Issue {x['number']} · {x['date']} — {x['title']}\n\n**{x['theme']}**\n\n{x['story']}\n\nCultural connection: {x['cultural_connection']}\n\n"
 for s in x['sources']:doc+=f"Reference: [{s['label']}]({s['url']})\n\n"
(revision/'COVER-STORIES.md').write_text(doc)
checks={'covers':len(c),'stories':len({x['story'] for x in c}),'titles':len({x['title'] for x in c}),'masters':len({hashlib.sha256((r/'site'/x['artwork'].replace('.webp','.png')).read_bytes()).hexdigest() for x in c}),'new_artworks':10,'files_missing':[]}
for x in c:
 for suffix in ['.png','.webp','-480.webp','-cover.svg']:
  f=r/'site'/x['artwork'].replace('.webp',suffix)
  if not f.exists():checks['files_missing'].append(str(f))
assert checks['covers']==checks['stories']==checks['titles']==checks['masters']==47 and not checks['files_missing']
(revision/'file-checks.json').write_text(json.dumps(checks,indent=2))
# Sync portable project without removing previous work.
for folder in ['site','brand-guide','revision-19-cover-stories']:
 shutil.copytree(r/folder,p/folder,dirs_exist_ok=True)
for file in ['DESIGN-PROPOSAL.md','DESIGN-PROPOSAL.html','build-report.py']:shutil.copy2(r/file,p/file)
f=p/'README.md';s=f.read_text();line='\nRevision 19: all 47 covers have distinct poetic stories and cultural notes. Ten new heritage, craft, ecology and literary artworks replace repeated motifs in the active catalogue. Editor cover-story card: site/editor-cover-card.html. Sources, prompts and provenance: revision-19-cover-stories.\n'
if 'Revision 19:' not in s:f.write_text(s+line)
f=p/'build-all.py';s=f.read_text().replace("print('Complete: 37 designs and three companion documents. Serve the site directory to preview.')", "shutil.copy2(root/'brand-guide/editor-cover-card.html',root/'site/editor-cover-card.html')\n(root/'site/editor-cover-card.html').write_text((root/'site/editor-cover-card.html').read_text().replace('EDITORS-CHEAT-SHEET.html','editors-cheat-sheet.html'))\nprint('Complete: 37 designs and four companion documents. Serve the site directory to preview.')");f.write_text(s)
with ZipFile(r/'Kabita-Live-All-47-Covers.zip','w',ZIP_DEFLATED) as z:
 prefix='Kabita-Live-47-Covers/'
 for x in c:
  for suffix in ['.png','.webp','-480.webp','-cover.svg']:
   f=r/'site'/x['artwork'].replace('.webp',suffix);z.write(f,prefix+'artwork/'+f.name)
 for f in [revision/'README.md',revision/'COVER-STORIES.md',revision/'EDITOR-COVER-CARD.md',revision/'current-47-manifest.json',revision/'manifest.json',revision/'new-art-review.jpg',r/'site/cover-catalogue.json',r/'site/assets/header-separator.svg']:z.write(f,prefix+f.name)
# Refresh existing distribution archives while retaining their intended scope.
for name in ['Kabita-Live-Page-Designs.zip','Kabita-Live-Design-Proposal.zip','Kabita-Live-Project-Starter.zip','Kabita-Live-Branding-Guide.zip']:
 path=r/name;temp=path.with_suffix('.tmp.zip');root=p if 'Starter' in name else r
 with ZipFile(path) as old, ZipFile(temp,'w',ZIP_DEFLATED) as new:
  prefix=old.namelist()[0].split('/')[0]+'/';seen=set()
  for info in old.infolist():
   if info.is_dir():continue
   rel=info.filename[len(prefix):];f=root/rel
   new.writestr(info.filename,f.read_bytes() if f.exists() else old.read(info.filename));seen.add(rel)
  additions=[root/'revision-19-cover-stories',root/'brand-guide']
  if 'Branding' not in name:additions.append(root/'site')
  for folder in additions:
   for f in folder.rglob('*'):
    if not f.is_file() or 'before' in f.parts or '__pycache__' in f.parts:continue
    rel=str(f.relative_to(root))
    if rel not in seen:new.write(f,prefix+rel);seen.add(rel)
 temp.replace(path)
print(json.dumps(checks));print('Updated cover collection, portable project and four distribution archives.')
