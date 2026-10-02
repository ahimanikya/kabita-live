"""Local-only card directory proposal; source text and production pages stay unchanged."""
from pathlib import Path
from html import escape
from html.parser import HTMLParser
import json,re,os,hashlib
ROOT=Path(__file__).resolve().parents[4]; SITE=ROOT/'projects/site'; OUT=Path(__file__).parent
class Entries(HTMLParser):
 def __init__(self):super().__init__();self.rows=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='a' and a.get('class')=='directory-entry':self.rows.append(a)
shell=(OUT/'source-directory.html').read_text(); parser=Entries();parser.feed(shell)
portraits=json.loads((SITE/'data/writer-portraits.json').read_text());quotes=json.loads((SITE/'data/writer-quotes.json').read_text());routes=json.loads((SITE/'data/local-routes.json').read_text())
poems={p['id']:p for path in (SITE/'content/editions').glob('*/poem-*.json') for p in [json.loads(path.read_text())] if p.get('status')!='archived'}
profiles=json.loads((SITE/'data/writer-profiles.json').read_text());names={p['name']:str(p['id']) for p in profiles}
cards=[];evidence=[]
for row in sorted(parser.rows,key=lambda x:x['data-directory-name'].split('/')[0].strip().casefold()):
 raw=row['data-directory-name'];name=raw.split('/')[0].strip();wid={'poet-dokana.html':'82','poet-kshanika.html':'337','poet-drink.html':'257','editor-pradeep.html':'1','editor-paresh.html':'43'}.get(row['href']) or re.search(r'poet-(\d+)\.html',row['href']).group(1)
 if wid=='1':name='Pradeep Biswal'
 if wid=='43':name='Paresh Kumar Pattnaik'
 works=sorted([p for p in poems.values() if str(p.get('writer_id'))==wid],key=lambda p:p['id'])
 q=quotes.get(wid); selected=None;text=''
 if q:
  selected=poems.get(q['poem_id'])
  if selected:
   assert str(selected['writer_id'])==wid
   assert selected['text'][q['text_start']:q['text_end']]==q['text'],wid
   text='\n'.join(q['text'].strip().splitlines()[:2])
 elif works:
  selected=works[0]; text='\n'.join(selected['text'].strip().splitlines()[:2])
 portrait=portraits.get(wid,{}).get('src') or {'1':'assets/editors/pradeep-biswal-artistic-v1.webp','43':'assets/editors/paresh-kumar-pattnaik-artistic-v1.webp'}.get(wid); initials=''.join(x[0] for x in name.split()[:2]).upper()
 if portrait:assert (SITE/portrait).exists()
 pic=(f'<img src="{escape(portrait)}" alt="" width="64" height="64" loading="lazy" decoding="async">' if portrait else f'<span class="poet-initials" aria-hidden="true">{escape(initials)}</span>')
 body=f'<blockquote lang="{selected["language"]}">{escape(text)}</blockquote>' if text else '<p class="no-excerpt">Meet this writer in their profile.</p>'
 poem_route=routes.get(str(selected['id']),f"poem-{selected['id']}.html") if text else ''
 citation=f'<a class="poet-source" href="{escape(poem_route)}" title="{escape(selected["title"])}" aria-label="Read the quoted poem: {escape(selected["title"])}">From a poem ↗</a>' if text else ''
 count=f'{len(works)} poem'+('' if len(works)==1 else 's') if works else 'Writer profile'
 cards.append(f'<article class="poet-card" data-search="{escape(raw)}" data-writer="{wid}"><div class="poet-card-identity">{pic}<h2><a class="poet-profile" href="{escape(row["href"])}">{escape(name)}</a></h2></div>{body}<div class="poet-card-meta"><span>{count}</span>{citation}</div></article>')
 evidence.append({'id':wid,'name':name,'profile':row['href'],'portrait':portrait,'poem_count':len(works),'quote_poem':selected['id'] if text else None,'excerpt':text})
main='''<main id="main" class="wrap poets-mock" tabindex="-1"><div class="mock-note">Poet directory · Design preview <a href="poets.html">Compare current page</a></div><section class="poets-opening"><div><span class="eyebrow">The writers of Kabita Live</span><h1>A gathering of voices.</h1><p>Meet the poets. Find a voice that stays with you.</p></div><img src="assets/section-art/voices-640.webp" alt="" width="640" height="427"></section><div class="poets-search"><label for="poet-find">Find a poet</label><div class="poets-search-field"><input type="search" id="poet-find" placeholder="Search a name in any script" autocomplete="off"><button type="button" id="poet-clear" hidden>Clear</button></div></div><p id="poet-results" class="poet-results" role="status" aria-live="polite"></p><div class="poet-cards" id="poet-cards">'''+''.join(cards)+'''</div><div id="poet-empty" hidden><h2>No poets found.</h2><p>Try another spelling, or clear your search to browse everyone.</p></div><div class="poets-more"><button type="button" class="btn" id="poet-more">Show more poets</button><p id="poet-progress"></p></div><noscript><p>All poets are shown below when JavaScript is unavailable.</p></noscript></main>'''
html=re.sub(r'<main\b.*?</main>',lambda m:main,shell,count=1,flags=re.S)
html=html.replace('<title>Poets · Kabita Live</title>','<title>Poet cards · Kabita Live design preview</title>')
html=html.replace('<script defer src="assets/analytics.js"></script>','')
html=html.replace('</head>','<style>'+(OUT/'mock.css').read_text()+'</style></head>')
html=html.replace('</body>','<script>'+(OUT/'mock.js').read_text()+'</script></body>')
(OUT/'poets-card-mock.html').write_text(html)
p=SITE/'poets-card-mock.html'
if not p.exists():p.symlink_to(os.path.relpath(OUT/'poets-card-mock.html',p.parent.resolve()))
assert p.is_symlink()
assert len({x['id'] for x in evidence})==len(evidence), 'Duplicate directory IDs'
(OUT/'sources.json').write_text(json.dumps({'reader_source_sha256':hashlib.sha256(shell.encode()).hexdigest(),'cards':evidence},ensure_ascii=False,indent=2)+'\n')
print(f'Generated {len(cards)} source-linked cards; {sum(bool(x["portrait"]) for x in evidence)} existing portraits; {sum(bool(x["excerpt"]) for x in evidence)} excerpts.')
