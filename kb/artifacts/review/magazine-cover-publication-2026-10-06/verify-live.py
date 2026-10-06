"""Verify the cover-only release against its isolated public build."""
import hashlib,json,re,urllib.request
from pathlib import Path

BASE='https://ahimanikya.github.io/kabita-live/'
DIST=Path('/Users/ahimanikya/.codex/worktrees/magazine-cover-release/Kabita Live/projects/site/dist')
sha=lambda b:hashlib.sha256(b).hexdigest()
routes=['index.html','archive.html','archive-2026.html','issue-47.html','issue-1.html','assets/magazine-covers.css']
rows=[]
for route in routes:
    with urllib.request.urlopen(BASE+route,timeout=40) as response:
        body=response.read()
        assert response.status==200
    expected=(DIST/route).read_bytes()
    assert body==expected,route+' live bytes differ'
    row={'route':route,'sha256':sha(body),'matches_release':True}
    if route.endswith('.html'):
        text=body.decode()
        assert 'magazine-object' in text and 'magazine-covers.css?v=1' in text
        assert 'noindex' in text
        og=re.findall(r'<meta property="og:image" content="([^"]+)"',text)
        tw=re.findall(r'<meta name="twitter:image" content="([^"]+)"',text)
        assert len(og)==1 and og==tw
        with urllib.request.urlopen(og[0],timeout=40) as response:
            assert response.status==200
            row['sharing_image']={'url':og[0],'sha256':sha(response.read())}
    rows.append(row)
report={'result':'PASS','files':rows,'independent':False}
Path(__file__).with_name('live-verification.json').write_text(json.dumps(report,indent=2)+'\n')
print('PASS:',len(rows),'exact live page/stylesheet comparisons; static sharing images reachable; preview gates retained.')
