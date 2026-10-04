"""Merge the five approved local refinements onto the latest clean release."""
from pathlib import Path
import json,shutil,hashlib,sys
source=Path(sys.argv[1]); target=Path(sys.argv[2]);s=source/'projects/site';t=target/'projects/site'
evidence=source/'kb/artifacts/review/website-refinements-publication-2026-10-04'
baseline={str(p.relative_to(t)):hashlib.sha256(p.read_bytes()).hexdigest() for folder in ['data','assets/covers','assets/portraits','assets/poem-art/editions'] for p in (t/folder).rglob('*') if p.is_file()}
for f in ['runtime-config.json','assets/analytics.js','cover_layout.py','assets/cover-layout-b.css','assets/feedback.js']:
 p=t/f
 if p.exists():baseline[f]=hashlib.sha256(p.read_bytes()).hexdigest()
(evidence/'baseline.json').write_text(json.dumps(baseline,indent=2)+'\n')
files=['build.py','build-public.py','edition-pages.py','standalone-pages.py','archive_directory.py','home_artistic.py','poem_experience.py','poet_directory.py','submission_polish.py','human_natural.py','home_views.py','assets/human-natural.css','assets/home-views.css','assets/home-views.js','assets/cover-story.js','assets/footer-art-trial.css','assets/poet-directory.css','assets/poem-experience.js','data/home-views.json']
for f in files:
 (t/f).parent.mkdir(parents=True,exist_ok=True);shutil.copy2(s/f,t/f)
p=t/'assets/style.css';v=p.read_text();old='.footer-simple .earth-edge{width:125px;height:42px;top:-42px;background-size:310px auto}';assert old in v;p.write_text(v.replace(old,'.footer-simple .earth-edge{display:none}',1))
for v in json.loads((s/'data/home-views.json').read_text()):
 for k in ['src','small']:shutil.copy2(s/v[k],t/v[k])
lib=json.loads((t/'data/poem-art-library.json').read_text()); local=json.loads((s/'data/poem-art-library.json').read_text())
assign=json.loads((t/'data/poem-art-assignments.json').read_text())
for ident,poem in [('gift-of-dates','724'),('river-return','786')]:
 art=next(x for x in local['artworks'] if x['id']==ident);assert not any(x['id']==ident for x in lib['artworks']);lib['artworks'].append(art);assign['assignments'][poem]=ident;shutil.copy2(s/art['src'],t/art['src'])
for f,d in [('poem-art-library.json',lib),('poem-art-assignments.json',assign)]: (t/'data'/f).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
# The site catalogue is a relative link to this canonical KB file.
f='kb/assets/imagery-catalogue.json'
metadata=json.loads((target/f).read_text()); known={x['src'] for x in metadata['artworks']}
for x in json.loads((source/f).read_text())['artworks']:
 if x['src'] not in known and any(k in x['src'] for k in ['gift-of-dates','river-return']):metadata['artworks'].append(x)
(target/f).write_text(json.dumps(metadata,indent=2,ensure_ascii=False)+'\n')
print('Merged approved refinements; preserved current edition overrides, covers and runtime settings.')
