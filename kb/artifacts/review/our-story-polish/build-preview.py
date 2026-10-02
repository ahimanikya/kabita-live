from pathlib import Path
import re,json,hashlib
R=Path(__file__).resolve().parents[4]
site=R/'projects/site';out=Path(__file__).parent
original=(site/'about.html').read_text()
(out/'before.html').write_text(original)
s=original.replace('<title>About · Kabita Live</title>','<title>Our Story · Proposed refinement · Kabita Live</title>')
old=re.search(r'<div class="side-layout"><div class="prose">(.*?)</div><aside',s,re.S).group(1)
new='''<h2 class="or" lang="or">ମାଟିର ମହକ · ମନର ସ୍ୱର</h2>
<p class="story-signature">The fragrance of earth. The voice of the heart.</p>
<p>Rooted in Odia, Kabita Live brings poetry in Odia, Hindi and English into a shared literary home. Each language has its own music; each poem offers another way of seeing.</p>
<h2>Room for another voice.</h2>
<p>We welcome original poems and translations, established writers and younger voices, and readers across places and generations. A poem begins with its writer and continues with everyone who reads it.</p>
<p>Read an edition, share a poem with its poet’s name, or write to the editorial desk. Your responses are private, and always welcome.</p>
<div class="story-invitations"><a class="text-link" href="submit.html">Send a poem</a><a class="text-link" href="feedback.html">Write to the editors</a></div>'''
s=s.replace(old,new,1)
start=s.index('<section class="colophon" id="credits-writers">');end=s.index('<section class="colophon" id="privacy">',start)
writers=s[start:end]
s=s[:start]+s[end:]
inside=writers.removeprefix('<section class="colophon" id="credits-writers">').removesuffix('</section>')
inside=inside.replace('<h2>The voices in these pages.</h2>','',1)
credit_details='<details id="credits-writers"><summary>Poets, portraits and biography references</summary><div class="colophon-details">'+inside+'</div></details>'
marker='</section>\n<section class="journal-paths">'
assert marker in s
s=s.replace(marker,credit_details+'</section>\n<section class="journal-paths">',1)
# Keep privacy alongside credits; journal navigation follows both.
a=s.index('<section class="journal-paths">');b=s.index('<section class="colophon" id="privacy">',a)
paths=s[a:b];s=s[:a]+s[b:];s=s.replace('</main>',paths+'</main>',1)
style='''<style id="our-story-proposal-style">
.review-strip{font:13px/1.5 var(--sans,Arial,sans-serif);padding:12px 0;border-bottom:1px solid var(--line,#D2C6AC);display:flex;gap:20px;align-items:center;flex-wrap:wrap}.review-strip a{padding:8px 0}.review-strip strong{margin-right:auto;font-weight:500}.story-proposal .page-head{margin-bottom:24px;padding-bottom:20px}.story-proposal .side-layout{align-items:start;margin-bottom:48px}.story-proposal .prose h2:first-child{margin-top:0}.story-signature{font-size:17px;color:var(--muted,#655F51);margin-top:8px!important}.story-proposal .prose h2:not(:first-child){margin-top:28px}.story-invitations{display:flex;flex-wrap:wrap;gap:12px 28px;margin-top:24px}.story-proposal .side-panel{background:transparent;border:0;border-left:1px solid var(--line,#D2C6AC);padding:0 0 0 32px}.story-proposal #credits{margin-top:0}.story-proposal #credits>p{max-width:760px}.story-proposal #credits>details{border-top:1px solid var(--line,#D2C6AC);margin:0;padding:0}.story-proposal #credits>details:last-child{border-bottom:1px solid var(--line,#D2C6AC)}.story-proposal #credits>details>summary{padding:18px 0;min-height:44px;font-size:19px}.story-proposal .colophon-details{overflow-wrap:anywhere}.story-proposal #privacy{margin-top:36px;padding-top:24px}.story-proposal .journal-paths{margin-top:32px}.story-proposal #credits-writers .profile-footnote{max-width:800px}.story-proposal .credit-source{scroll-margin-top:24px}
@media(max-width:760px){.review-strip{gap:8px 20px}.review-strip strong{width:100%}.story-proposal .page-head{padding-bottom:8px;margin-bottom:16px;gap:16px}.story-proposal .opening-art{margin-bottom:0}.story-proposal .side-layout{gap:32px;margin-bottom:32px}.story-proposal .side-panel{padding:24px 0 0;border-left:0;border-top:1px solid var(--line,#D2C6AC)}.story-proposal #credits>details>summary{font-size:18px}.story-proposal #credits{padding-top:28px}.story-proposal .prose h2.or{font-size:24px;line-height:1.7}}
</style>'''
s=s.replace('</head>',style+'</head>')
s=s.replace('class="wrap inner-artistic"','class="wrap inner-artistic story-proposal"',1)
s=s.replace('<header class="wrap site-header">','<div class="wrap review-strip"><strong>Design review · Our Story</strong><a href="about.html">Current page</a><a href="#credits">Proposed credits</a></div><header class="wrap site-header">',1)
s=s.replace('</body>','''<script>function revealCredit(){let id;try{id=decodeURIComponent(location.hash.slice(1))}catch{return}const target=document.getElementById(id);if(!target)return;for(let el=target;el;el=el.parentElement)if(el.tagName==='DETAILS')el.open=true;target.scrollIntoView()}window.addEventListener('hashchange',revealCredit);if(location.hash)revealCredit();</script></body>''')
(out/'proposed.html').write_text(s)
link=site/'our-story-polish-review.html'
if not link.exists():link.symlink_to('../../../kb/artifacts/review/our-story-polish/proposed.html')
# Preserve exact credit content/IDs and reference destinations in this candidate.
ids=lambda t:set(re.findall(r'id="(credits[^\"]*)"',t))
assert ids(original)<=ids(s)
hrefs=lambda t:set(re.findall(r'href="(https?[^\"]*)"',t))
assert hrefs(original)==hrefs(s)
assert 'Sonu Swayin and Versatile IT Services Pvt. Ltd.' in s
(out/'source-check.json').write_text(json.dumps({'about_sha256':hashlib.sha256(original.encode()).hexdigest(),'credit_ids_preserved':len(ids(s)),'external_destinations_preserved':len(hrefs(s)),'reader_page_unchanged':True,'changes':['Shorter journal narrative; removed unattributed quotation in candidate only','Grouped author and portrait provenance with existing credits','Privacy followed by journal navigation','Reduced opening/body spacing and lighter editorial sidebar']},indent=2)+'\n')
print('Created isolated Our Story candidate; preserved all credit anchors and external references.')
