"""Check published cover markup, exact image/CSS hashes and unchanged runtime config."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import urllib.request,json,hashlib,re,sys
ROOT=Path(sys.argv[1]);S=ROOT/'projects/site';BASE='https://ahimanikya.github.io/kabita-live/'
def get(path):
 with urllib.request.urlopen(BASE+path,timeout=40) as r:return r.status,r.read()
def check(n):
 status,b=get(f'issue-{n}.html');s=b.decode();assert status==200 and f'data-cover-edition="{n}"' in s
 assert 'font-weight="600" font-size="138"' in s and 'noindex' in s and 'cover-layout-b.css' in s
 images=re.findall(r'<image href="([^"]+)"',s);assert len(images)==1
 p=images[0];status,image=get(p);expected=(S/p).read_bytes();assert image==expected,p
 return {'edition':n,'status':status,'image':p,'sha256':hashlib.sha256(image).hexdigest(),'masthead':'B'}
with ThreadPoolExecutor(max_workers=6) as pool:checks=list(pool.map(check,range(1,48)))
for page in ['index.html','archive.html']+[f'archive-{year}.html' for year in range(2022,2027)]:
 status,b=get(page);assert status==200 and 'data-cover-edition=' in b.decode(),page
for path in ['assets/cover-layout-b.css','runtime-config.json','assets/analytics.js']:
 status,b=get(path);assert b==(S/'dist'/path).read_bytes(),path
out={'result':'PASS','editions':checks,'homepage_archive_year_routes':'PASS','cover_css_exact_hash':'PASS','runtime_and_analytics_exact_hash':'PASS'}
print(json.dumps(out,indent=2))
