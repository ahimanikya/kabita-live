from pathlib import Path
import re,os,json,hashlib
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[3];SITE=ROOT/'projects/site'
css='''
.waterline-preview{position:relative;width:100%;height:34px;margin:28px 0;pointer-events:none;scroll-margin-top:180px}
.waterline-preview .waterline-wave{display:block;width:100%;height:34px;overflow:visible}
.waterline-preview .waterline-leaf{position:absolute;width:24px;height:28px;left:calc(50% - 12px);top:-1px}
.separator-preview-nav{display:flex;align-items:center;flex-wrap:wrap;gap:10px 22px;font:13px/1.5 var(--ui);padding:16px 0;border-bottom:1px solid var(--line);margin-bottom:20px}
.separator-preview-nav a{color:var(--rust);text-decoration:underline;text-underline-offset:4px}
.separator-preview-nav .current{font-weight:bold;text-decoration:none;color:var(--ink)}
.separator-preview .editorial-invitation{margin-top:0;border-top:0}
.separator-preview .submission-opening{margin-bottom:0}
.separator-preview .waterline-preview+.writer-work{margin-top:0;border-top:0}
.separator-preview .waterline-preview+.colophon{margin-top:0;padding-top:0;border-top:0}
.separator-preview .editorial-review-bar,.separator-preview .submission-review{display:none}
.separator-intro{max-width:680px;margin:34px 0}
.separator-intro h1{font:500 clamp(36px,4vw,56px)/1.15 'Cormorant Garamond',serif;margin-bottom:18px}
.separator-intro p{font:19px/1.7 var(--serif);color:var(--muted)}
.separator-options{display:grid;grid-template-columns:1fr 1fr;gap:24px;margin:30px 0}
.separator-option{border:1px solid var(--line);padding:26px;background:var(--panel)}
.separator-option h2{font:500 30px/1.2 'Cormorant Garamond',serif;margin:0 0 12px}
.separator-option p{font:17px/1.6 var(--serif);color:var(--muted);margin:0 0 20px}
.separator-option a{font:15px var(--ui);text-decoration:underline;text-underline-offset:4px}
@media(max-width:700px){.waterline-preview{margin:20px 0;height:28px;scroll-margin-top:100px}.waterline-preview .waterline-wave{height:28px}.separator-preview-nav{gap:10px 16px;font-size:12px}.separator-options{grid-template-columns:1fr;gap:16px}.separator-option{padding:22px}}
'''
# The original waterline's two colours and small leaf are retained. Only the
# waves stretch; the leaf keeps a fixed size at every viewport width.
divider='''<div class="waterline-preview" id="signature-divider" aria-hidden="true"><svg class="waterline-wave" viewBox="0 0 1000 34" preserveAspectRatio="none" fill="none"><path d="M1 22 C95 12 155 13 245 21 S405 29 488 20 M512 20 C600 11 654 14 745 21 S900 26 999 18" stroke="#983e30" stroke-width="1.2" stroke-linecap="round" opacity=".62" vector-effect="non-scaling-stroke"/><path d="M18 28 C135 21 197 23 282 28 S421 26 475 23 M525 26 C620 20 711 26 793 28 S932 23 982 24" stroke="#263d4b" stroke-width=".7" opacity=".34" vector-effect="non-scaling-stroke"/></svg><svg class="waterline-leaf" viewBox="0 0 24 28" fill="none"><path d="M14 15C7 14 3 9 4 3c7 1 11 5 10 12Z" fill="#65665d" opacity=".62"/><path d="M15 19 8 8" stroke="#65665d" stroke-width=".9" opacity=".7"/></svg></div>'''
items=[('editors','Editors','../editorial-polish/editorial-team-mock.html','<section class="editorial-strip editorial-invitation"','Before the invitation to share a poem.'),('submit','Send a poem','../submission-polish/submit-polish-mock.html','<div class="submission-layout"','Between the opening invitation and the practical next steps.'),('profile','Writer profile','../editorial-polish/editor-pradeep-mock.html','<section class="writer-work" id="contributions"','Between life and writing, and poems in the journal.'),('story','Our Story',str(SITE/'about.html'),'<section class="colophon" id="credits"','Before the credits: a quiet transition to the people behind the pages.')]
def nav(active):
 return '<nav class="separator-preview-nav" aria-label="Separator preview"><a href="separator-placement-mock.html">Overview</a>'+''.join('<a '+('class="current" aria-current="page" ' if k==active else '')+'href="separator-'+k+'-mock.html#signature-divider">'+label+'</a>' for k,label,*_ in items)+'</nav>'
def save(name,html):
 (OUT/name).write_text(html)
 p=SITE/name
 if not p.exists():p.symlink_to(os.path.relpath(OUT/name,p.parent.resolve()))
checks=[]
for key,label,source,marker,description in items:
 path=(OUT/source).resolve();original=path.read_text();assert original.count(marker)==1,(key,original.count(marker))
 s=original.replace(marker,divider+marker,1)
 s=re.sub(r'(<main\b[^>]*class=")([^"]*)',lambda m:m[1]+m[2]+' separator-preview',s,count=1)
 s=re.sub(r'(<main\b[^>]*>)',lambda m:m[1]+nav(key),s,count=1)
 s=s.replace('</head>','<style>'+css+'</style></head>')
 s=s.replace('<script defer src="assets/analytics.js"></script>','')
 save('separator-'+key+'-mock.html',s)
 checks.append({'source':str(path.relative_to(ROOT)),'sha256':hashlib.sha256(original.encode()).hexdigest(),'preview':'separator-'+key+'-mock.html','placement':description})
base=(SITE/'submit.html').read_text()
main='<main id="main" class="wrap separator-preview" tabindex="-1">'+nav('')+'<section class="separator-intro"><span class="eyebrow">A small pause between chapters</span><h1>Let the page breathe.</h1><p>One wave, one leaf, across the content width. Four places where the page changes purpose—each shown in context before we decide where to keep it.</p></section>'+divider+'<div class="separator-options">'+''.join('<section class="separator-option"><h2>'+label+'</h2><p>'+description+'</p><a href="separator-'+key+'-mock.html#signature-divider">Preview this placement →</a></section>' for key,label,_,_,description in items)+'</div><p class="muted">Preview only. The existing reader pages are unchanged.</p></main>'
s=re.sub(r'<main\b.*?</main>',lambda m:main,base,count=1,flags=re.S).replace('</head>','<style>'+css+'</style></head>').replace('<script defer src="assets/analytics.js"></script>','')
save('separator-placement-mock.html',s)
(OUT/'sources.json').write_text(json.dumps(checks,indent=2)+'\n')
(OUT/'mock.css').write_text(css)
print('Four contextual previews and overview created.')
