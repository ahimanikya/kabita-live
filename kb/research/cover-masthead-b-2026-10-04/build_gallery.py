"""Build a local, source-preserving 47-edition masthead B review."""
from pathlib import Path
import base64, hashlib, html, json, re, shutil
R=Path(__file__).resolve().parents[3]; S=R/'projects/site'
O=R/'kb/artifacts/artwork/home-natural-2026-10-04/covers-b';O.mkdir(exist_ok=True)
Q=[x for x in json.loads((R/'kb/research/poetic-natural/queue.json').read_text())['items'] if x['id'].startswith('cover-')]
ISS={int(re.search(r'\d+',x['title']).group()):x['label'].split()[-2:] for x in json.loads((S/'data/issues.json').read_text())}
# Individual art-direction choices after contact-sheet review; all retain original framing.
IVORY={45,44,40,35,33,31,29,26,21,19,17,13,10,2}
INK='#243A38'; PAPER='#F5EFDF'
fontcss="@font-face{font-family:'Cormorant Garamond';src:url('../../assets/fonts/CormorantGaramond-Variable.ttf');font-weight:300 700}@font-face{font-family:'Noto Serif Oriya';src:url('../../assets/fonts/NotoSerifOriya-Variable.ttf');font-weight:100 900}"
css=fontcss+"""*{box-sizing:border-box}body{margin:0;background:#f5efdf;color:#243a38;font:16px/1.5 Georgia,serif}main{max-width:1440px;margin:auto;padding:32px}h1{font:600 clamp(34px,4vw,54px)/1.05 'Cormorant Garamond',serif;margin:12px 0}h2{font:600 25px 'Cormorant Garamond',serif;margin:0 0 5px}header p{max-width:760px;margin:12px 0 24px}.eyebrow{font:11px/1.5 Arial,sans-serif;letter-spacing:2px;color:#87553f}a{color:inherit;text-underline-offset:4px}a:focus-visible,button:focus-visible,select:focus-visible{outline:3px solid #963f28;outline-offset:4px}.tools{display:flex;flex-wrap:wrap;gap:12px;align-items:center;margin:22px 0 30px}button,select,.nav a{font:14px Arial,sans-serif;min-height:44px;border:1px solid #a89d87;border-radius:0;background:transparent;color:inherit;padding:10px 14px;cursor:pointer}button[aria-pressed=true]{background:#243a38;color:#f5efdf}.grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:32px 24px}.grid.small{grid-template-columns:repeat(8,minmax(0,1fr));gap:24px 16px}svg{display:block;width:100%;height:auto;background:#eae1cd;box-shadow:0 2px 12px #243a3818}.cover-link{display:block;text-decoration:none}.caption{margin:12px 0 0;font:13px/1.5 Arial,sans-serif}.title{font:500 21px/1.2 'Cormorant Garamond',serif;margin-top:5px}.small .title{font-size:17px}.flag{display:block;color:#963f28;font:12px/1.5 Arial,sans-serif;margin-top:5px}footer{border-top:1px solid #d2c6ac;margin-top:40px;padding-top:20px;font-size:13px}.pair{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:32px;max-width:1100px}.nav{display:flex;gap:12px;flex-wrap:wrap;margin:24px 0}.nav a{text-decoration:none}.detail-note{max-width:760px}.count{font:13px Arial,sans-serif}.grid article[hidden]{display:none}@media(max-width:850px){.grid{grid-template-columns:repeat(2,minmax(0,1fr))}.grid.small{grid-template-columns:repeat(4,minmax(0,1fr))}}@media(max-width:520px){main{padding:22px 18px}.grid{grid-template-columns:1fr;gap:30px}.grid.small{grid-template-columns:repeat(2,minmax(0,1fr));gap:24px 16px}.pair{grid-template-columns:1fr}.pair .proposed{grid-row:1}.tools{gap:8px}}"""
def page(title,body,script=''):
 return '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>'+html.escape(title)+' · Kabita Live</title><style>'+css+'</style></head><body><main>'+body+'</main>'+script+'</body></html>'
def svg(n,src,proposed=True):
 template=S/f'assets/covers/editions/issue-{n}-cover.svg'
 if not template.exists():template=S/f'assets/covers/editions/issue-{n:02}-cover.svg'
 old=template.read_text()
 old=re.sub(r'<image[^>]+/>',f'<image href="{src}" width="1024" height="1536" preserveAspectRatio="xMidYMid slice"/>',old)
 if not proposed:
  return old.replace('id="shade"',f'id="old-{n}"').replace('url(#shade)',f'url(#old-{n})')
 month,year=ISS[n]
 old=re.sub(r'(<text x="64" y="1400"[^>]*>).*?(</text>)',lambda m:m[1]+f'ISSUE {n} · {month.upper()} {year}'+m[2],old)
 tone=PAPER if n in IVORY else INK; wash=INK if n in IVORY else PAPER
 opacity=.64 if n in IVORY else .58
 if n==47:opacity=.72
 old=re.sub(r'<defs>.*?</defs>','',old,flags=re.S)
 old=re.sub(r'<path fill="url\(#shade\)"[^>]*/>','',old)
 old=re.sub(r'<g transform="translate\(64 80\) scale\(\.26\)">.*?</g>','',old,flags=re.S)
 overlays=f'<defs><linearGradient id="top-{n}" x1="0" y1="0" x2="0" y2="1"><stop stop-color="{wash}" stop-opacity="{opacity}"/><stop offset=".62" stop-color="{wash}" stop-opacity="{opacity*.84:.2f}"/><stop offset="1" stop-color="{wash}" stop-opacity="0"/></linearGradient><linearGradient id="foot-{n}" x1="0" y1="0" x2="0" y2="1"><stop stop-color="{INK}" stop-opacity="0"/><stop offset=".6" stop-color="{INK}" stop-opacity=".68"/><stop offset="1" stop-color="{INK}" stop-opacity=".84"/></linearGradient></defs><path fill="url(#top-{n})" d="M0 0h1024v460H0z"/><path fill="url(#foot-{n})" d="M0 1190h1024v346H0z"/>'
 old=old.replace('<text x="166"',overlays+'<text x="166"',1)
 old=re.sub(r'<text x="166" y="166"[^>]*>Kabita Live</text>',f'<text x="64" y="184" font-family="Cormorant Garamond,Georgia,serif" font-weight="600" font-size="138" fill="{tone}">Kabita Live</text>',old)
 old=re.sub(r'(<text x="64" y="262"[^>]*?)fill="[^"]+"',r'\1fill="'+tone+'"',old)
 return old
manifest=[];cards=[]
for i,x in enumerate(Q):
 n=int(x['id'][-3:]); month,year=ISS[n]
 src=R/x['delivery_source'];pn=src.with_name(src.stem+'-poetic-natural.webp');current=pn if pn.exists() else src
 selected=R/'kb/artifacts/artwork/home-natural-2026-10-04/cover-subtle-v2.webp' if n==47 else current
 shutil.copyfile(selected,O/f'art-{n:02}.webp')
 if n==47:shutil.copyfile(current,O/'current-47.webp')
 new=svg(n,f'art-{n:02}.webp');old=svg(n,'current-47.webp' if n==47 else f'art-{n:02}.webp',False)
 note='Existing artwork retained; the portrait reference remains unresolved.' if n==16 else ('Refined photographic study from the masthead B preview.' if n==47 else 'Existing Poetic Natural artwork retained. Framing and central scene preserved.')
 tone='Ivory' if n in IVORY else 'Dark ink'
 nav='<nav class="nav" aria-label="Cover navigation"><a href="index.html#issue-'+str(n)+'">All covers</a>'
 if i>0:nav+=f'<a href="issue-{int(Q[i-1]["id"][-3:]):02}.html">← Newer edition</a>'
 if i<len(Q)-1:nav+=f'<a href="issue-{int(Q[i+1]["id"][-3:]):02}.html">Older edition →</a>'
 nav+='</nav>'
 title=f'Issue {n} · {month} {year}'
 body=f'<header><div class="eyebrow">MAGAZINE COVER REVIEW</div><h1>{title}</h1><p>{html.escape(x["title"])}. {note}</p></header>'+nav+'<section class="pair"><article><h2>Previous masthead</h2>'+old+'</article><article class="proposed"><h2>Masthead B</h2>'+new+'</article></section>'+f'<p class="detail-note">{tone} lettering with a local wash behind the masthead; full-bleed artwork and the Odia signature retained.</p>'+nav+'<footer>Local review · AI-assisted imagery. Historical originals are preserved. Nothing in this gallery is published automatically.</footer>'
 (O/f'issue-{n:02}.html').write_text(page(title,body))
 flag='<span class="flag">Portrait reference still open</span>' if n==16 else ''
 cards.append(f'<article id="issue-{n}" data-year="{year}"><a class="cover-link" href="issue-{n:02}.html" aria-label="Compare issue {n}, {month} {year}">{new}<div class="caption">ISSUE {n} · {month.upper()} {year}</div><div class="title">{html.escape(x["title"])}</div>{flag}</a></article>')
 manifest.append({'edition':n,'date':f'{month} {year}','title':x['title'],'source':str(selected.relative_to(R)),'source_sha256':hashlib.sha256(selected.read_bytes()).hexdigest(),'retained_current_sha256':hashlib.sha256(current.read_bytes()).hexdigest(),'tone':tone,'crop':'unchanged full frame','note':note,'page':f'issue-{n:02}.html'})
script='''<script>const grid=document.querySelector('.grid'),year=document.querySelector('#year'),button=document.querySelector('#size'),count=document.querySelector('#count');year.addEventListener('change',()=>{let n=0;for(const card of grid.children){card.hidden=year.value!=='all'&&card.dataset.year!==year.value;if(!card.hidden)n++}count.textContent=n+' covers'});button.addEventListener('click',()=>{const small=grid.classList.toggle('small');button.setAttribute('aria-pressed',String(small));button.textContent=small?'Larger covers':'Thumbnail view'});</script>'''
body='<header><div class="eyebrow">KABITA LIVE · 47 EDITIONS · COVER REVIEW</div><h1>One name. Forty-seven beginnings.</h1><p>Masthead B across the collection: a stronger literary wordmark, the Odia signature and full-bleed artwork. Open any cover to compare it with the current treatment.</p></header><div class="tools"><label for="year">Year</label><select id="year"><option value="all">All years</option>'+''.join(f'<option>{y}</option>' for y in range(2026,2021,-1))+'</select><button id="size" aria-pressed="false">Thumbnail view</button><span class="count" id="count" role="status">47 covers</span></div><section class="grid" aria-label="Magazine cover collection">'+''.join(cards)+'</section><footer>Local review only · Edition 47 uses the refined photographic study; other cover artwork is retained. Edition 16 keeps its existing portrait while its reference is unresolved. Historical originals and previous designs remain preserved. <a href="../mastheads.html">Masthead studies</a></footer>'
(O/'index.html').write_text(page('All 47 covers · Masthead B',body,script))
(O/'manifest.json').write_text(json.dumps({'masthead':'B','status':'local_review','independent':False,'covers':manifest},ensure_ascii=False,indent=2)+'\n')
print(f'Built {len(manifest)} comparison pages and collection gallery; reader assets unchanged.')
