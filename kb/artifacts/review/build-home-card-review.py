"""Build review-only poem-card choices against the current homepage."""
from pathlib import Path
import json,re,os
root=Path(__file__).resolve().parents[3]
review=root/'kb/artifacts/review/site';site=(root/'projects/site').resolve()
shell=(review/'home-review.html').read_text()
shell=shell.replace('Homepage review ·','Poem-card choices ·').replace('Homepage · review desk','Poem cards · revised choices').replace('One change at a time.','A face beside the words.')
shell=shell.replace('Compare each suggestion independently. Choose Current, A or B, add notes, then approve the direction you prefer.','Three variations on your requested layout: portrait left, poem title and poet right, with aligned excerpts underneath.')
shell=shell.replace('Nothing here changes the homepage. Decisions are saved only in this browser; download them when you are ready. Each sample isolates one suggestion, so you can mix your choices later.','Your seven approved homepage directions have been applied locally. Option A was selected in our discussion and is now applied to the homepage; B and C remain comparison studies. All three use laterite language labels and a four-line excerpt area with ellipsis for overflow.')
shell=shell.replace('assets/home-review.js?v=1','assets/home-card-review.js?v=1').replace('Homepage choices','Poem-card choices').replace('home-review-sample.html','home-card-sample.html')
# Shared current masthead, including the approved icon button.
shell=re.sub(r'<header.*?</header>',re.search(r'<header.*?</header>',(site/'index.html').read_text(),re.S).group(),shell,count=1,flags=re.S)
(review/'home-card-review.html').write_text(shell)
data={'version':1,'title':'Kabita Live poem-card revision','groups':[{'id':'cards','title':'Poem cards','status':'locked','heading':'The poet and the poem, together.','description':'A keeps the portrait small and round. B uses a taller artistic portrait. C gives the face more space beside a quieter title. Each keeps the same four-line excerpt area and aligns the reading links.','variants':['A · Small round portrait — recommended','B · Upright artistic portrait','C · A larger portrait, quieter title'],'checks':['The portrait is on the left; poem title and author are on the right.','All three scripts start their excerpts at the same height in the wide layout.','Overflow ends with an ellipsis; Read the poem opens the complete source text.','Use 360px to inspect long Odia and Hindi lines. No verse is rewritten.']}]}
(review/'home-card-catalogue.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
s=(review/'assets/home-review.js').read_text().replace('home-review-catalogue.json','home-card-catalogue.json').replace('kabita-live-homepage-review-v1','kabita-live-home-cards-v1').replace('home-review-sample.html','home-card-sample.html').replace('kabita-live-homepage-decisions.json','kabita-live-home-card-decisions.json')
(review/'assets/home-card-review.js').write_text(s)
baseline=(site/'index.html').read_text()
if 'home-poem-cards' in baseline:
 baseline=(review/'home-card-sample.html').read_text()
 baseline=re.sub(r'<link rel="stylesheet" href="assets/home-card-sample.css"><script defer src="assets/home-card-sample.js"></script>','',baseline)
 baseline=re.sub(r'<script type="application/json" id="home-review-data">.*?</script>','',baseline,flags=re.S)
html=baseline.replace('</head>','<link rel="stylesheet" href="assets/home-card-sample.css"><script defer src="assets/home-card-sample.js"></script></head>')
# Retain source-exact excerpts and portrait references from the previous study.
old=(review/'home-review-sample.html').read_text();payload=re.search(r'<script type="application/json" id="home-review-data">(.*?)</script>',old,re.S).group(1)
html=html.replace('</body>',f'<script type="application/json" id="home-review-data">{payload}</script></body>')
(review/'home-card-sample.html').write_text(html)
for name in ['home-card-review.html','home-card-catalogue.json','home-card-sample.html','assets/home-card-review.js','assets/home-card-sample.js','assets/home-card-sample.css']:
 p=site/name
 if p.is_symlink():p.unlink()
 if not p.exists():p.symlink_to(os.path.relpath(review/name,p.parent))
print('Revised card study built; public homepage cards remain unchanged.')
