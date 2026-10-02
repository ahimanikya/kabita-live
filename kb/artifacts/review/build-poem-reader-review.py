"""Review-only poem layouts; preserve live reader files and verse markup."""
from pathlib import Path
import json,re,os,hashlib
root=Path(__file__).resolve().parents[3];site=(root/'projects/site').resolve();review=root/'kb/artifacts/review/site'
shell=(review/'home-atmosphere-review.html').read_text()
shell=re.sub(r'<aside class="wrap notice".*?</aside>','',shell,flags=re.S)
shell=shell.replace('Homepage atmosphere ·','Poem reader options ·').replace('Homepage atmosphere choices','Poem reader choices').replace('Homepage · final touches','Poem pages · review').replace('Paper, light and evening.','Room for the poem.')
shell=shell.replace('Two small decisions, considered separately: the edge of the artwork and a choice of reading light.','Two quieter reading layouts, using the same poems, artwork and approved typography.')
shell=re.sub(r'<p class="review-explainer">.*?</p>','<p class="review-explainer">Compare Current, A and B in Odia, Hindi and English. Try text sizing, sharing and the 360px view. These are mockups; the live poem pages stay unchanged. Underlining and language-sensitive audio remain a separate interaction review.</p>',shell,count=1,flags=re.S)
shell=shell.replace('Isolated homepage preview','Poem preview').replace('assets/home-atmosphere-review.js?v=1','assets/poem-reader-review.js?v=1').replace('home-atmosphere-sample.html','poem-reader-sample-or.html')
shell=shell.replace('<div class="review-preview-bar">','<div class="review-preview-bar"><label class="review-language">Poem language <select id="poem-preview-language"><option value="or">ଓଡ଼ିଆ · Odia</option><option value="hi">हिन्दी · Hindi</option><option value="en">English</option></select></label>',1)
shell=shell.replace('</style>','.review-language{display:flex;align-items:center;gap:10px;font-size:14px}.review-language select{width:auto;max-width:210px;min-height:44px}.review-preview-bar{flex-wrap:wrap}</style>',1)
home=(site/'index.html').read_text();shell=re.sub(r'<header.*?</header>',re.search(r'<header.*?</header>',home,re.S).group(),shell,count=1,flags=re.S)
shell=shell.replace('<body class="journal-paper cotton-paper">','<body class="journal-paper cotton-paper site-theme"><script src="assets/appearance.js"></script>')
(review/'poem-reader-review.html').write_text(shell)
data={'version':1,'title':'Kabita Live poem reader review','groups':[{'id':'reader','title':'Poem reader','status':'unreviewed','heading':'The poem comes into focus.','description':'A keeps the 60/40 illustrated opening, with one line of edition/language information and a single poet byline. B brings the first verse closer to the title, with artwork in the right margin on desktop and after the poem on phones. Both remove the repeated information sidebar and large repeated poet block.','variants':['Current · Existing reader','A · Quiet illustrated opening — recommended','B · The poem first'],'checks':['Poem wording, punctuation, authored line breaks and stanza order remain unchanged.','One edition link above the title; one author byline. No repeated metadata sidebar.','Text sizing and Share remain visible; appearance stays in the shared masthead.','After the poem: More by this poet, the next poem, and a quiet correction link.','Compare all three languages at desktop and 360px. A keeps artwork in the opening; B moves it after the poem on phones.','Underlining and audio are not implemented in this layout mockup.']}]}
(review/'poem-reader-catalogue.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
s=(review/'assets/home-atmosphere-review.js').read_text().replace('home-atmosphere-catalogue.json','poem-reader-catalogue.json').replace('kabita-live-home-atmosphere-review-v1','kabita-live-poem-reader-review-v1').replace('kabita-live-home-atmosphere-decisions.json','kabita-live-poem-reader-decisions.json')
s=s.replace("s.variant:0", "s.variant:1")
s=s.replace("frame.src='home-atmosphere-sample.html?element='+encodeURIComponent(g.id)+'&variant='+d.variant", "frame.src='poem-reader-sample-'+$('#poem-preview-language').value+'.html?variant='+d.variant")
s=s.replace('storageMessage();render();', "$('#poem-preview-language').onchange=preview;\nstorageMessage();render();")
(review/'assets/poem-reader-review.js').write_text(s)
records=[]
for lang,slug in [('or','dokana'),('hi','kshanika'),('en','drink')]:
 source=site/f'poem-{slug}.html';s=source.read_text();records.append({'file':source.name,'sha256':hashlib.sha256(s.encode()).hexdigest()})
 s=re.sub(r'<script[^>]*src="assets/analytics.js"[^>]*></script>','',s)
 s=s.replace('</head>','<link rel="stylesheet" href="assets/poem-reader-sample.css"><script defer src="assets/poem-reader-sample.js"></script></head>')
 (review/f'poem-reader-sample-{lang}.html').write_text(s)
for name in ['poem-reader-review.html','poem-reader-catalogue.json','assets/poem-reader-review.js','assets/poem-reader-sample.js','assets/poem-reader-sample.css']+[f'poem-reader-sample-{l}.html' for l in ['or','hi','en']]:
 p=site/name
 if not p.exists() and not p.is_symlink():p.symlink_to(os.path.relpath(review/name,p.parent))
(root/'kb/records/poem-reader-mockup-source.json').write_text(json.dumps({'scope':'Review-only layouts; no applied reader change','baselines':records,'deferred':['Poem underlining interaction','Language-sensitive poetry audio']},indent=2)+'\n')
print('Poem reader comparison desk and three source-exact sample snapshots created.')
