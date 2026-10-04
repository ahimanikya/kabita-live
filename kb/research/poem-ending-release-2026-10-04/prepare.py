from pathlib import Path
import json,hashlib,sys,difflib,subprocess,shutil,re
R=Path('/Users/ahimanikya/Projects/Kabita Live');C=Path(sys.argv[1]);S=C/'projects/site';L=R/'projects/site';K=R/'kb/research/poem-ending-release-2026-10-04';B=R/'kb/artifacts/review/poem-end-marks-2026-10-04/application/before'
assert not subprocess.check_output(['git','-C',str(C),'status','--porcelain']).strip()
base=subprocess.check_output(['git','-C',str(C),'rev-parse','HEAD'],text=True).strip()
protected={str(p.relative_to(C)):hashlib.sha256(p.read_bytes()).hexdigest() for directory in [S/'content',S/'data',S/'assets'] for p in directory.rglob('*') if p.is_file() and (directory!=S/'assets' or p.suffix in {'.png','.jpg','.jpeg','.webp','.woff2'})}
protected[str((S/'runtime-config.json').resolve().relative_to(C))]=hashlib.sha256((S/'runtime-config.json').read_bytes()).hexdigest()
old=json.loads((S/'assets/reading-all.json').read_text())['poems']
baseline={'base':base,'protected':protected,'readers':old}
(K/'baseline.json').write_text(json.dumps(baseline,ensure_ascii=False)+'\n')
# Apply only the reviewed source changes; keep other unpublished local work out.
for name,before_name in [('poem_reader.py','poem_reader.py'),('edition-pages.py','edition-pages.py'),('assets/poem-experience.js','poem-experience.js')]:
 oldtext=(B/before_name).read_text();newtext=(L/name).read_text()
 # Runtime defaults were not part of the closing-mark change.
 if name.endswith('.js'):
  oldline=next(x for x in oldtext.splitlines() if x.startswith('const storedEffects='));newtext=re.sub(r'^const storedEffects=.*$',oldline,newtext,flags=re.M)
 rel=str((S/name).resolve().relative_to(C));patch=''.join(difflib.unified_diff(oldtext.splitlines(True),newtext.splitlines(True),fromfile='a/'+rel,tofile='b/'+rel))
 patch_path=K/(Path(name).name+'.patch');patch_path.write_text(patch)
 if patch:subprocess.run(['git','-C',str(C),'apply','--check',str(patch_path)],check=True);subprocess.run(['git','-C',str(C),'apply',str(patch_path)],check=True)
css=(L/'assets/poem-experience.css').read_text();addition=css[css.index('/* Approved closing marks:'):]
p=S/'assets/poem-experience.css';assert 'Approved closing marks:' not in p.read_text();p.write_text(p.read_text()+'\n'+addition)
p=S/'build.py';t=p.read_text();t,n=re.subn(r'poem-experience.css\?v=\d+','poem-experience.css?v=12',t);assert n==1;t,n=re.subn(r'poem-experience.js\?v=\d+','poem-experience.js?v=9',t);assert n==1;p.write_text(t)
for name in ['poem_end_marks.py','data/poem-end-mark-overrides.json','assets/poem-end-leaf.svg','assets/poem-end-paired.svg','assets/poem-end-sprig.svg']:
 shutil.copy2(L/name,S/name)
p=S/'tests/reader-pagination.test.mjs';tests=(L/'tests/reader-pagination.test.mjs').read_text();extra=tests[tests.index("test('closing mark stays"):];assert 'closing mark stays' not in p.read_text();p.write_text(p.read_text()+'\n'+extra)
for name in ['poem-end-marks-options-2026-10-04.json','poem-end-marks-applied-2026-10-04.json','poem-ending-refinement-2026-10-04.json']:
 shutil.copy2(R/'kb/records'/name,C/'kb/records'/name)
source=R/'kb/artifacts/review/poem-end-marks-2026-10-04';shutil.copytree(source,C/'kb/artifacts/review/poem-end-marks-2026-10-04',dirs_exist_ok=True)
# Document final approved behaviour without importing unrelated local brand edits.
p=C/'kb/artifacts/design/brand-guide/DESIGN-SYSTEM.md';t=p.read_text();assert '## Poem closing marks' not in t;p.write_text(t+'\n'+(R/'kb/artifacts/design/brand-guide/DESIGN-SYSTEM.md').read_text().split('## Poem closing marks',1)[1].join(['## Poem closing marks','']))
if not (S/'node_modules').exists():(S/'node_modules').symlink_to(L/'node_modules',target_is_directory=True)
print(json.dumps({'checkout':str(C),'base':base,'protected_files':len(protected),'poems':len(old)},indent=2))
