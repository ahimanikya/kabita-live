"""Local archive simplification and companion directory copy study."""
from pathlib import Path
import json,re,os
ROOT=Path(__file__).resolve().parents[4];SITE=ROOT/'projects/site';OUT=Path(__file__).parent
shell=(OUT/'source-archive.html').read_text();poet=(SITE/'poets.html').read_text()
if not (OUT/'source-archive.html').exists(): (OUT/'source-archive.html').write_text(shell)
issues={x['number']:x for x in json.loads((SITE/'content/editions/index.json').read_text())}
icon=(SITE/'assets/icons/earth-voice-v1/ink/footer-story.svg').read_text()
leaf=(SITE/'assets/icons/earth-voice-v1/ink/kendu.svg').read_text().replace('role="img" aria-label="In the kendu shade"','aria-hidden="true" focusable="false"')
cards=[]
for raw in re.findall(r'<article class="issue-card".*?</article>',shell,re.S):
 n=int(re.search(r'aria-label="Open issue (\d+)"',raw).group(1));issue=issues[n]
 raw=re.sub(r'<details class="cover-story">.*?</details>','',raw,flags=re.S)
 raw=re.sub(r'<h3>.*?</h3><p>.*?</p>',f'<div class="edition-identity"><h2><a href="issue-{n}.html">{issue["month"]} {issue["year"]}</a></h2><p>Issue {n} · {len(issue["poem_ids"])} poems</p></div>',raw,flags=re.S)
 cards.append(raw)
assert len(cards)==47
filters='<div class="archive-years" role="group" aria-label="Choose a year"><button type="button" data-archive-year="all" aria-pressed="true">All years</button>'+''.join(f'<button type="button" data-archive-year="{y}" aria-pressed="false">{y}</button>' for y in sorted({i['year'] for i in issues.values()},reverse=True))+'</div>'
main='<main id="main" class="wrap archive-mock" tabindex="-1"><div class="review-note">Archive · Design preview <a href="archive.html">Compare current page</a></div><section class="archive-opening"><div><span class="eyebrow artistic-eyebrow">'+icon+' The archive</span><h1>Every issue,<br>another beginning.</h1><p>Forty-seven gatherings of words.<br>Open a cover; let a poem find you.</p></div><img src="assets/section-art/archive-640.webp" width="640" height="427" alt=""></section>'+filters+'<p id="archive-results" role="status" aria-live="polite"></p><div class="cover-grid archive-gallery">'+''.join(cards)+'</div><div class="archive-more"><button type="button" class="btn" id="archive-more">Show more editions</button><p id="archive-progress"></p></div>'+'</main>'
html=re.sub(r'<main\b.*?</main>',lambda m:main,shell,count=1,flags=re.S).replace('<title>Archive · Kabita Live</title>','<title>Archive · Design preview</title>')
html=html.replace('<script defer src="assets/analytics.js"></script>','').replace('</head>','<style>'+(OUT/'mock.css').read_text()+'</style></head>').replace('</body>','<script>'+(OUT/'mock.js').read_text()+'</script></body>')
(OUT/'archive-polish-mock.html').write_text(html)
poet=poet.replace('<span class="eyebrow">The writers of Kabita Live</span>','<span class="eyebrow artistic-eyebrow">'+leaf+' The writers of Kabita Live</span>').replace('Meet the poets. Find a voice that stays with you.','Behind every poem, a voice. Find one that stays with you.')
poet=poet.replace('<div class="poets-directory">','<div class="review-note">Poet directory · Copy preview <a href="poets.html">Compare approved page</a></div><div class="poets-directory">').replace('<script defer src="assets/analytics.js"></script>','')
poet=poet.replace('</head>','<style>'+ (OUT/'mock.css').read_text().split('/* ARCHIVE */')[0]+'</style></head>')
(OUT/'poets-copy-mock.html').write_text(poet)
for filename in ['archive-polish-mock.html','poets-copy-mock.html']:
 p=SITE/filename
 if not p.exists():p.symlink_to(os.path.relpath(OUT/filename,p.parent.resolve()))
 assert p.is_symlink()
print('Created archive47-cover preview and companion poet-copy preview; reader pages unchanged.')
