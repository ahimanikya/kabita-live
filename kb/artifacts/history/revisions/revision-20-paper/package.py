from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
import json,shutil
r=Path(__file__).resolve().parents[1];p=r.parent/'kabita-live-project';v=r/'revision-20-paper'
for folder in ['site','brand-guide','revision-20-paper']:shutil.copytree(r/folder,p/folder,dirs_exist_ok=True)
for f in ['DESIGN-PROPOSAL.md','DESIGN-PROPOSAL.html','build-report.py']:shutil.copy2(r/f,p/f)
f=p/'README.md';s=f.read_text();addition='\nRevision 20: warm ivory paper texture across journal pages; off in night reading and print. Pipili Chandua is preserved in site/assets/art-library for future use. Issue 34 returns to Rain on the tiles. Current cover stories and generation provenance: revision-20-paper.\n'
if 'Revision 20:' not in s:f.write_text(s+addition)
c=json.loads((r/'site/cover-catalogue.json').read_text())
with ZipFile(r/'Kabita-Live-All-47-Covers.zip','w',ZIP_DEFLATED) as z:
 prefix='Kabita-Live-47-Covers/'
 for x in c:
  for suffix in ['.png','.webp','-480.webp','-cover.svg']:
   f=r/'site'/x['artwork'].replace('.webp',suffix);z.write(f,prefix+'artwork/'+f.name)
 for f in [v/'README.md',v/'COVER-STORIES.md',v/'current-47-manifest.json',r/'site/cover-catalogue.json',r/'site/assets/header-separator.svg',r/'revision-19-cover-stories/EDITOR-COVER-CARD.md']:z.write(f,prefix+f.name)
 for f in (r/'site/assets/art-library').iterdir():z.write(f,prefix+'reserved/'+f.name)
 z.write(v/'reserved-pipili-chandua.json',prefix+'reserved/provenance.json')
for name in ['Kabita-Live-Page-Designs.zip','Kabita-Live-Design-Proposal.zip','Kabita-Live-Project-Starter.zip','Kabita-Live-Branding-Guide.zip']:
 path=r/name;temp=path.with_suffix('.tmp.zip');root=p if 'Starter' in name else r
 with ZipFile(path) as old,ZipFile(temp,'w',ZIP_DEFLATED) as new:
  prefix=old.namelist()[0].split('/')[0]+'/';seen=set()
  for info in old.infolist():
   if info.is_dir():continue
   rel=info.filename[len(prefix):];f=root/rel;new.writestr(info.filename,f.read_bytes() if f.exists() else old.read(info.filename));seen.add(rel)
  extras=[root/'revision-20-paper',root/'site/assets/art-library',root/'site/assets/paper-grain.svg']
  for folder in extras:
   files=[folder] if folder.is_file() else folder.rglob('*')
   for f in files:
    if not f.is_file() or 'before' in f.parts or '__pycache__' in f.parts:continue
    rel=str(f.relative_to(root))
    if rel not in seen:new.write(f,prefix+rel);seen.add(rel)
 temp.replace(path)
print('Portable project and five download packages refreshed.')
