from pathlib import Path
import json,urllib.request,hashlib,re,datetime
root=Path('/private/tmp/kbl-selective-portraits-20261003/projects/site')
base='https://ahimanikya.github.io/kabita-live/'
route='thirty-languages-and-the-journey-of-a-poem.html'
files=['index.html','about.html',route,'assets/article-links.css','assets/language-essay.css','runtime-config.json','assets/analytics.js','assets/engagement.js','robots.txt']
files += [str(p.relative_to(root/'dist')) for p in (root/'dist/assets/articles/thirty-languages').glob('*')]
evidence=[]
for file in files:
 req=urllib.request.Request(base+file+'?verify=69132222',headers={'User-Agent':'facebookexternalhit/1.1'})
 live=urllib.request.urlopen(req,timeout=40).read()
 expected=(root/'dist'/file).read_bytes()
 if file=='runtime-config.json':
  runtime=json.loads(expected)
  assert runtime['analytics']['basePath']=='/'
  runtime['analytics']['basePath']='/kabita-live/'
  runtime['analytics']['publicPages']={'/kabita-live'+k:v for k,v in runtime['analytics']['publicPages'].items()}
  assert json.loads(live)==runtime,file
 elif file=='robots.txt':
  assert live==expected.replace(b'Allow: /\n',b'Allow: /kabita-live/\n'),file
 else:
  assert live==expected,file
 if file.endswith('.html'):
  assert b'noindex' in live,file
 if file in ['index.html','about.html']:
  assert live.count(('href="'+route+'"').encode())==1,file
 if file=='index.html':
  assert live.index(b'id="home-language-essay"') < live.index(b'class="section home-editors"')
 evidence.append({'path':file,'sha256':hashlib.sha256(live).hexdigest(),'exact_build_match':file not in ['runtime-config.json','robots.txt'],'note':'Only expected hosted URL prefix differs' if file in ['runtime-config.json','robots.txt'] else None})
meta=json.loads((root/'.generated/social-previews.json').read_text())[route]
image=urllib.request.urlopen(meta['image_url']+'?verify=69132222',timeout=40).read()
Path('/private/tmp/kbl-essay-live-social.jpg').write_bytes(image)
print(json.dumps({'result':'PASS','verified_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'release_commit':'69132222','files':evidence,'sharing':{'url':meta['image_url'],'source':meta['source'],'sha256':hashlib.sha256(image).hexdigest(),'local_sha256':hashlib.sha256((root/'dist'/meta['asset']).read_bytes()).hexdigest()},'scope':'HTTP checks with sharing crawler user-agent; not an actual social-platform scrape.'},indent=2))
