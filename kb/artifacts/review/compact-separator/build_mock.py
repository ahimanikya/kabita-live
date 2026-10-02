"""Local-only trials of the existing short poetic-waterline ornament."""
from pathlib import Path
import re,os,json,hashlib
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[3];SITE=ROOT/'projects/site'
# Match the existing Search opening exactly; never redraw or stretch the asset.
css='''
.compact-trial-nav{display:flex;gap:12px 24px;flex-wrap:wrap;padding:12px 0;margin-bottom:18px;border-bottom:1px solid var(--line);font:13px/1.5 var(--ui)}
.compact-trial-nav a{text-decoration:underline;text-underline-offset:4px;color:var(--rust)}
.compact-trial .submission-review{display:none}
.compact-trial .page-head-copy:after,.compact-trial .submission-opening>div:after{content:'';display:block;width:115px;height:23px;margin-top:24px;background:url('assets/poetic-waterline.svg') left center/115px 23px no-repeat}
'''
items=[('search','Search','search.html'),('editors','Editors','editorial-team.html'),('submit','Send a poem','submit-polish-mock.html'),('story','Our Story','about.html')]
checks=[]
for key,label,source in items:
 original=(SITE/source).read_text();s=original
 s=re.sub(r'(<main\b[^>]*class=")([^"]*)',lambda m:m[1]+m[2]+' compact-trial',s,count=1)
 nav='<nav class="compact-trial-nav" aria-label="Compact separator preview"><span>Small separator · Preview only</span>'+''.join('<a href="compact-separator-'+k+'-mock.html">'+l+'</a>' for k,l,_ in items)+'</nav>'
 s=re.sub(r'(<main\b[^>]*>)',lambda m:m[1]+nav,s,count=1)
 s=s.replace('</head>','<style>'+css+'</style></head>').replace('<script defer src="assets/analytics.js"></script>','')
 name='compact-separator-'+key+'-mock.html';(OUT/name).write_text(s)
 p=SITE/name
 if not p.exists():p.symlink_to(os.path.relpath(OUT/name,p.parent.resolve()))
 checks.append({'source':source,'sha256':hashlib.sha256(original.encode()).hexdigest(),'preview':name,'status':'existing placement retained' if key in ('search','story') else 'new placement trial'})
(OUT/'sources.json').write_text(json.dumps(checks,indent=2)+'\n')
print('Four compact separator previews ready; source asset unchanged.')
