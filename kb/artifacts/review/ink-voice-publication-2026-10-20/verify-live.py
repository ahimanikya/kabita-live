from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from urllib.request import urlopen, Request
from urllib.error import HTTPError
import hashlib,json,re
ROOT=Path('/Users/ahimanikya/Projects/Kabita Live')
SITE=Path('/Users/ahimanikya/.codex/worktrees/ink-voice-publication/Kabita Live/projects/site/dist')
EVIDENCE=ROOT/'kb/artifacts/review/ink-voice-publication-2026-10-20'
paths=['index.html','issue-48.html','poem-826.html','poem-827.html','poem-834.html','poets.html','poems.html','about.html','contact.html','translation-review.html','assets/ink-voice.css','assets/kabita-live-symbol-ink-voice.svg','assets/reader-language.mjs','assets/poem-experience.js','assets/poem-reader.js','assets/home-featured.js','assets/app.js','runtime-config.json','assets/fonts/Newsreader-Variable.woff2','assets/fonts/Newsreader-Italic-Variable.woff2','assets/fonts/Literata-Variable.woff2','assets/fonts/Literata-Italic-Variable.woff2','sitemap.xml','robots.txt']
hashdata=lambda b:hashlib.sha256(b).hexdigest()
def fetch(rel):
 url='https://kabitalive.com/'+('' if rel=='index.html' else rel)
 try:
  with urlopen(Request(url,headers={'User-Agent':'KabitaLiveReleaseVerification/1.0'}),timeout=45) as res:b=res.read();status=res.status
 except HTTPError as e:b=e.read();status=e.code
 result={'path':rel,'url':url,'status':status,'sha256':hashdata(b)}
 if (SITE/rel).is_file():result['expected_sha256']=hashdata((SITE/rel).read_bytes());result['matches_release']=result['sha256']==result['expected_sha256']
 if rel=='index.html' and status==200:
  text=b.decode();result['ink_voice']='ink-opening' in text;result['current_cover']='ink-edition-cover' in text
  (EVIDENCE/'live-home.html').write_bytes(b)
  match=re.search(r'<meta property="og:image" content="([^"]+)"',text)
  if match:result['sharing_image']=match.group(1)
 if rel=='translation-review.html' and status==200:result['noindex']='noindex' in b.decode()
 return result
with ThreadPoolExecutor(max_workers=4) as pool:rows=list(pool.map(fetch,paths))
for rel in ['branding-guide.html','design-system-review.html','kb/index.md']:rows.append(fetch(rel))
home=rows[0]
if home.get('sharing_image'):
 rel=home['sharing_image'].split('https://kabitalive.com/',1)[1];image=fetch(rel);image['note']='Raster bytes may differ between Linux CI and macOS; browser image checked separately.';rows.append(image)
result={'checks':rows,'all_expected_pages_and_assets_200':all(r['status']==200 for r in rows if r['path'] not in ['branding-guide.html','design-system-review.html','kb/index.md']),'internal_paths_404':all(r['status']==404 for r in rows if r['path'] in ['branding-guide.html','design-system-review.html','kb/index.md']),'exact_mismatches':[r['path'] for r in rows if r.get('matches_release') is False and not r['path'].startswith('assets/social/')]}
(EVIDENCE/'live-http-checks.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='checks'},indent=2))
