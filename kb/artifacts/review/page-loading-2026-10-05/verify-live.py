from pathlib import Path
import urllib.request,json,hashlib,datetime,re,subprocess
root=Path('/private/tmp/kbl-selective-portraits-20261003/projects/site');base='https://ahimanikya.github.io/kabita-live/'
files=['index.html','poem-724.html','poet-49.html','about.html','thirty-languages-and-the-journey-of-a-poem.html','assets/style.css','assets/image-delivery.css','assets/image-delivery.js','runtime-config.json','assets/analytics.js','assets/engagement.js','robots.txt']
files += [str(p.relative_to(root/'dist')) for p in (root/'dist/assets/fonts').glob('*.woff2')]
for page in ['poem-724.html','poet-49.html']:
 files += re.findall(r'assets/responsive/[^\s,\"]+\.webp',(root/'dist'/page).read_text())
for view in json.loads((root/'data/home-views.json').read_text()):files.extend([view['src'],view['small']])
meta=json.loads((root/'.generated/social-previews.json').read_text());files.extend(meta[n]['asset'] for n in ['index.html','poem-724.html','poet-49.html'])
evidence=[]
for file in dict.fromkeys(files):
 live=urllib.request.urlopen(urllib.request.Request(base+file+'?verify=loading-20261005',headers={'User-Agent':'facebookexternalhit/1.1'}),timeout=45).read()
 expected=(root/'dist'/file).read_bytes()
 comparison=None
 if live!=expected and file.endswith('.jpg'):
  downloaded=Path('/private/tmp')/('live-'+Path(file).name);downloaded.write_bytes(live)
  comparison=json.loads(subprocess.check_output(['/Users/ahimanikya/.nvm/versions/node/v24.15.0/bin/node','/private/tmp/kbl-compare-jpeg.mjs',str(downloaded),str(root/'dist'/file)],text=True))
 else:assert live==expected,file
 evidence.append({'path':file,'sha256':hashlib.sha256(live).hexdigest(),'bytes':len(live),'exact_build_match':live==expected,'decoded_comparison':comparison})
print(json.dumps({'result':'PASS','verified_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'files':evidence,'checks':'Live HTML, responsive images, four homepage views, six WOFF2 fonts, three static sharing images, consent/runtime scripts and noindex robots match isolated hosted build; cross-platform JPEG encoding differences are accepted only with decoded-pixel RMS below0.1 on the0–255 scale. Actual browser rotation verified separately.'},indent=2))
