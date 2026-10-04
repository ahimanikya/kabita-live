"""Refresh the human-readable gallery from durable batch state."""
import json
from pathlib import Path
from html import escape as e
R=Path(__file__).resolve().parents[3];K=Path(__file__).resolve().parent;A=R/'kb/artifacts/artwork/edition-art-rollout-2026-10-04';S=R/'projects/site';q=json.loads((K/'queue.json').read_text());routes=json.loads((S/'data/local-routes.json').read_text())
parts=['<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Every edition, its own atmosphere · Kabita Live</title><style>body{background:#f8f4e9;color:#303a37;font:18px/1.65 Georgia,serif;margin:0}main{max-width:1120px;margin:auto;padding:40px 24px}h1{font-size:clamp(36px,6vw,60px);line-height:1.1}h2{font-size:30px}a{color:#356368}section{border-top:1px solid #ccc1ad;padding:28px 0}.grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:24px}img{max-width:100%;height:auto}.status,small{font:14px/1.5 system-ui;color:#56625c}li{margin:10px 0}@media(max-width:760px){.grid{grid-template-columns:1fr}}</style><main><h1>Every edition,<br>its own atmosphere.</h1><p>Human Natural in Poetic Natural mode: imagery chosen after reading the poems, with selective detail, plausible materials and room for interpretation.</p><p><a href="../edition-art-pilot-2026-10-04/index.html">Explore the original nine-image pilot</a> · <a href="https://ahimanikya.github.io/kabita-live/">Visit the website</a></p><p>Existing covers and poems stay. New images belong to their own poems and editions. Verification is by the creating assistant; independent editorial review remains separate.</p>']
for ed in q['editions']:
 n=ed['edition']
 if n>=45:continue
 parts.append(f'<section id="edition-{n}"><h2>Issue {n} · {e(ed["label"])}</h2><p class="status">{e(ed["status"].replace("_"," "))}</p>')
 if not ed.get('batch'):parts.append('<p>Queued for poem reading and art direction.</p></section>');continue
 b=json.loads((R/ed['batch']).read_text());parts.append(f'<p>{e(b["direction"])}</p><div class="grid">')
 for i in b['items']:
  poem=json.loads((R/i['poem_evidence']).read_text());ready=(R/i['output']).exists();img=f'<a href="/{i["output"]}"><img src="/{i["output"]}" alt="{e(i.get("alt",i["title"]))}"></a>' if ready else '<p>Awaiting generation</p>'
  prompts=' · '.join(f'<a href="/{a["prompt"]}">Prompt {a["version"]}</a>' for a in i['attempts'])
  parts.append(f'<article>{img}<h3>{e(i["title"])}</h3><p><a href="/projects/site/{routes[str(i["poem_id"])]}">{e(poem["title"])}</a><br><small>{e(poem["author"])}</small></p><p>{e(i["rationale"])}</p><p class="status">{e(i["status"].replace("_"," "))}</p><p class="status">{prompts}</p></article>')
 parts.append('</div><h3>Room for the words</h3><ul>')
 for i in b['text_led']:
  parts.append(f'<li><a href="/projects/site/{routes[str(i["poem_id"])]}">Poem {i["poem_id"]}</a> — {e(i["rationale"])}</li>')
 parts.append('</ul></section>')
parts.append('</main></html>');(A/'index.html').write_text(''.join(parts));print('Rollout gallery refreshed.')
