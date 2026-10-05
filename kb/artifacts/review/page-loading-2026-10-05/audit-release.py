from pathlib import Path
import subprocess,json,sys,re,collections,hashlib
root=Path('/private/tmp/kbl-selective-portraits-20261003');site=root/'projects/site';sys.path.insert(0,str(site))
from image_delivery import enhance
manifest=json.loads((site/'data/image-delivery.json').read_text())
files=subprocess.check_output(['git','diff','--name-only','e837063223310742d97e28610e945b889f8f5e05','fc7a72813a6d2e953f3b5789b7d8265157eb7042'],cwd=root,text=True).splitlines()
prefix='output/kabitalive-design-proposal-2026-09-29/site/'
classes=collections.Counter();unknown=[];mismatches=[];exact=0
allowed={'assets/fonts/README.md','assets/home-views.js','assets/style.css','build.py','home_views.py','package.json','data/image-delivery.json','image_delivery.py','assets/image-delivery.css','assets/image-delivery.js','tests/home-views.test.mjs','tests/test_image_delivery.py','tools/prepare-font-delivery.py','tools/prepare-image-delivery.mjs'}
def strip_home(text,after=False):
 text=re.sub(r'<figure class="home-art home-views">.*?</figure>','',text,flags=re.S)
 text=re.sub(r'<script type="application/json" id="home-view-data">.*?</script>','',text,flags=re.S)
 text=re.sub(r'<script defer src="assets/home-views.js\?v=2"></script>','',text)
 if after:text=text.replace('<script>'+(site/'assets/home-views.js').read_text()+'</script>','')
 return text
for path in files:
 if path.startswith('kb/artifacts/review/page-loading-2026-10-05/') or path=='kb/records/page-loading-2026-10-05.json':classes['scoped_evidence']+=1;continue
 if not path.startswith(prefix):unknown.append(path);continue
 rel=path[len(prefix):]
 if rel.endswith('.html'):
  classes['generated_html']+=1
  old=subprocess.check_output(['git','show','e837063223310742d97e28610e945b889f8f5e05:'+path],cwd=root).decode()
  new=(root/path).read_text()
  old=old.replace('NotoSerifOriya-Variable.ttf','NotoSerifOriya-Variable.woff2').replace('type="font/ttf"','type="font/woff2"').replace('style.css?revision=mobile-footer-20261004','style.css?revision=delivery-20261005')
  if rel=='index.html':old=strip_home(old);new=strip_home(new,True)
  expected=enhance(old,manifest)
  if expected!=new:mismatches.append(rel)
  else:exact+=1
 elif rel.startswith('assets/responsive/') and rel.endswith('.webp'):classes['responsive_image_copies']+=1
 elif rel.startswith('assets/fonts/') and rel.endswith('.woff2'):classes['compressed_existing_fonts']+=1
 elif rel in allowed:classes['loading_source_and_tests']+=1
 else:unknown.append(path)
assert not unknown,unknown
assert not mismatches,mismatches
protected=json.loads((root/'kb/artifacts/review/page-loading-2026-10-05/release-protected.json').read_text());assert all(hashlib.sha256((root/p).read_bytes()).hexdigest()==h for p,h in protected.items())
variants={v['src'] for x in manifest.values() for v in x['variants']};assert all((site/p).exists() for p in variants)
report={'result':'PASS','release_commit':subprocess.check_output(['git','rev-parse','fc7a72813a6d2e953f3b5789b7d8265157eb7042'],cwd=root,text=True).strip(),'baseline':subprocess.check_output(['git','rev-parse','e837063223310742d97e28610e945b889f8f5e05'],cwd=root,text=True).strip(),'changed_file_count':len(files),'categories':dict(classes),'unknown_paths':unknown,'generated_html_exact_transform_matches':exact,'generated_html_mismatches':mismatches,'html_check':'Every changed HTML file equals old live HTML transformed only by approved font URL/version replacements and the exact image-delivery renderer. For homepage only, old/new approved home-art figure and selector scripts are removed before the same exact comparison. All remaining HTML must match byte-for-byte.','protected_content_service_records_unchanged':len(protected),'notes':'No changes to poem text, translations, runtime configuration, analytics/engagement code, cover styling, templates outside declared loading source, KB registers, publication workflow, or DNS.'}
print(json.dumps(report,indent=2))
