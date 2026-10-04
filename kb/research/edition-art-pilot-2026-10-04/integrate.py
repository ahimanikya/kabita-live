"""Locally integrate one reviewed edition, retaining the generic library unchanged."""
import json,sys,hashlib,re
from pathlib import Path
from html import escape as e
from PIL import Image
from datetime import datetime,timezone
R=Path(__file__).resolve().parents[3];K=Path(__file__).resolve().parent;S=R/'projects/site';A=R/'kb/artifacts/artwork/edition-art-pilot-2026-10-04'
edition=int(sys.argv[1]);q=json.loads((K/'queue.json').read_text());now=datetime.now(timezone.utc).isoformat()
def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
alts={'threshold-memory':'Watercolor of a meal on a steel plate beside a shaded room and a warm red threshold.','oleander-walkway':'Yellow funnel flowers and narrow leaves hang over a sunlit walkway in watercolor.','breath-in-bamboo':'A plain bamboo flute rests on cotton beside a softly lit open window.','room-for-a-tree':'A leafy sapling in a small clay pot beside a paved yard with little planting space.','pondside-warmth':'A small brown lizard warms itself on a stone beside quiet pond water.','mind-orbits':'Uneven translucent blue and earth-coloured watercolor arcs meet on open ivory paper.','two-petals':'Two unequal pale petals meet on a cool stone sill in a spare watercolor study.','shutter-morning':'A neighbourhood tea shop begins its morning under a partly raised shutter.','city-at-night':'Quiet low rooftops at night with one small warm window beyond a cropped balcony.'}
path=S/'data/edition-art-direction.json';direction=json.loads(path.read_text()) if path.exists() else {'version':1,'policy':'Explicit poem-and-edition commissions; excluded from generic artwork assignment. Text-led openings retain reader and edition controls.','poems':{}}
if not (K/'reader-baseline.json').exists():
 variants={}
 for p in S.glob('poem-*.html'):
  m=re.search(r'<script type="application/json" id="reading-data">(.*?)</script>',p.read_text(),re.S)
  if m:variants[p.name]=json.loads(m[1])['variants']
 save(K/'reader-baseline.json',variants)
for i in q['items']:
 if i['edition']!=edition:continue
 if i['status']=='held':continue
 assert i['status'] in ('verified','integrated_local'),i['id']
 assert hashlib.sha256((R/i['output']).read_bytes()).hexdigest()==i['output_sha256']
 target=S/f'assets/poem-art/editions/{edition}/{i["id"]}-v1.webp';target.parent.mkdir(parents=True,exist_ok=True)
 im=Image.open(R/i['output']).convert('RGB');im.thumbnail((1536,1024))
 if not target.exists():im.save(target,'WEBP',quality=90,method=6)
 direction['poems'][str(i['poem_id'])]={'edition':edition,'mode':'illustrated','artwork_id':i['id'],'src':str(target.relative_to(S)),'alt':alts[i['id']],'caption':i['title']+' · An AI-assisted watercolor interpretation for this poem.','width':im.width,'height':im.height}
 i.update(status='integrated_local',public_asset=str(target.relative_to(S)),public_sha256=hashlib.sha256(target.read_bytes()).hexdigest(),integrated_at=now)
for i in q['text_led']:
 if i['edition']==edition:
  direction['poems'][str(i['poem_id'])]={'edition':edition,'mode':'text'};i['status']='integrated_local'
save(path,direction)
q['counts']={s:sum(i['status']==s for i in q['items']) for s in ['pending','in_progress','generated','verified','held','integrated_local']};q['updated_at']=now
save(K/'queue.json',q)
record=json.loads((R/'kb/records/edition-art-pilot-2026-10-04.json').read_text());routes=json.loads((S/'data/local-routes.json').read_text());lib={i['id']:i for i in json.loads((S/'data/poem-art-library.json').read_text())['artworks']}
replacements=json.loads((S/'artwork-replacements.json').read_text())
for previous in lib.values():previous['src']=replacements.get(previous['src'],previous['src'])
parts=['<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Each edition, its own atmosphere · Kabita Live</title><style>body{margin:0;background:#f8f4e9;color:#303a37;font:18px/1.65 Georgia,serif}main{max-width:1120px;margin:auto;padding:40px 24px}h1{font-size:clamp(34px,6vw,64px);line-height:1.1;max-width:800px}h2{font-size:32px}h3{font-size:24px;margin:12px 0}a{color:#356368}header{border-bottom:1px solid #ccc1ad;padding-bottom:28px}section{padding:28px 0;border-bottom:1px solid #ccc1ad}.grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:24px}img{max-width:100%;height:auto;display:block}.status,small{font:14px/1.5 system-ui;color:#54645e}.pending{aspect-ratio:3/2;display:grid;place-items:center;background:#ede7da}summary{cursor:pointer}details img{max-width:260px;margin:12px 0}li{margin:12px 0}footer{margin:32px 0} @media(max-width:760px){.grid{grid-template-columns:1fr}main{padding:24px 18px}}</style><main><header><p>KABITA LIVE · LOCAL DESIGN PILOT</p><h1>Each edition,<br>its own atmosphere.</h1><p>Nine new interior illustrations across three recent issues. A few poems receive a deliberate visual companion; others gain room to speak through type and space.</p><p class="status">'+str(q['counts'].get('integrated_local',0))+' of 9 integrated locally · '+str(q['counts'].get('held',0))+' held · Covers and poem texts preserved · Not published</p></header>']
for ed in [47,46,45]:
 parts.append(f'<section id="edition-{ed}"><h2>Issue {ed}</h2><p>{e(record["edition_directions"][str(ed)])}</p><p><a href="/projects/site/issue-{ed}.html">Browse this edition</a></p><div class="grid">')
 for i in [x for x in q['items'] if x['edition']==ed]:
  poem=json.loads((R/i['poem_evidence']).read_text());ready=i['status'] in ['verified','integrated_local'];img=f'<a href="{i["id"]}/{Path(i["output"]).name}"><img src="{i["id"]}/{Path(i["output"]).name}" alt="{e(alts[i["id"]])}"></a>' if ready else '<div class="pending">'+e(i['status'].replace('_',' '))+'</div>'
  old=lib.get(i['previous_assignment']);before=f'<details><summary>Previous shared image</summary><img src="/projects/site/{old["src"]}" alt="{e(old["alt"])}"><small>{e(i["previous_assignment"])}</small></details>' if old else ''
  prompts=' · '.join(f'<a href="/{attempt["prompt"]}">Prompt {attempt["version"]}</a>' for attempt in i['attempts'])
  parts.append(f'<article>{img}<h3>{e(i["title"])}</h3><p><a href="/projects/site/{routes[str(i["poem_id"])]}">{e(poem["title"])}</a><br><small>{e(poem["author"])}</small></p><p>{e(i["rationale"])}</p><p class="status">{e(i["status"].replace("_"," "))}</p>{before}<p class="status">{prompts}</p></article>')
 parts.append('</div><h3>Room for the words</h3><ul>')
 for i in [x for x in q['text_led'] if x['edition']==ed]:
  poem=json.loads((K/f'poem-{i["poem_id"]}.json').read_text());parts.append(f'<li><a href="/projects/site/{routes[str(i["poem_id"])]}">{e(poem["title"])}</a> — {e(i["rationale"])} <small>({e(i["status"].replace("_"," "))})</small></li>')
 parts.append('</ul></section>')
parts.append('<footer><p>Art direction is a new interpretation drawn from selected poems, not a claim about the editors’ original issue themes. Existing bespoke illustrations are retained. AI-assisted artwork with Human Natural / Poetic Natural direction; visual review by the creating assistant, not independent editorial approval.</p><p>The nine edition images are reserved for their own poems and issues. They are not added to the generic shared-art pool.</p></footer></main></html>')
(A/'index.html').write_text(''.join(parts));print(json.dumps(q['counts']))
