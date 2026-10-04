"""Verify exact public refinements and preserved service assets after Pages publication."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import urllib.request,json,hashlib,sys
root=Path(sys.argv[1]);site=root/'projects/site';dist=site/'dist';base='https://ahimanikya.github.io/kabita-live/'
paths=['index.html','about.html','archive.html','poems.html','poets.html','contact.html','submit.html','feedback.html','issue-47.html','poem-724.html','poem-786.html','poem-644.html','runtime-config.json','assets/analytics.js','assets/private-feedback.js','assets/human-natural.css','assets/home-views.js','assets/home-views.css','assets/cover-story.js','assets/footer-art-trial.css','assets/style.css','assets/cover-layout-b.css','assets/poem-experience.js','assets/poem-art/gift-of-dates-poetic-natural-v1.webp','assets/poem-art/river-return-poetic-natural-v1.webp']
for view in json.loads((site/'data/home-views.json').read_text()):paths.extend([view['src'],view['small']])
def check(path):
 try:
  with urllib.request.urlopen(base+path,timeout=40) as r:body=r.read();status=r.status
 except Exception as exc:raise RuntimeError(path) from exc
 assert body==(dist/path).read_bytes(), 'Live content mismatch: '+path
 return {'path':path,'status':status,'sha256':hashlib.sha256(body).hexdigest()}
with ThreadPoolExecutor(max_workers=5) as pool:checks=list(pool.map(check,paths))
print(json.dumps({'result':'PASS','assets_and_pages':checks},indent=2))
