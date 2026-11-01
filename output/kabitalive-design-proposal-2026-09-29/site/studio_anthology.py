"""Render a reviewed Studio anthology from sanitized Git content only."""
import json
from hashlib import sha256
from html import escape

def render_studio_anthologies(root, page):
    source=root/'content/anthologies/toshali-2027.json'
    if not source.exists(): return
    d=json.loads(source.read_text());e=escape
    parts=[f'<!-- studio-content-sha256:{sha256(source.read_bytes()).hexdigest()} -->',f'<header class="page-head"><h1>{e(d["title"])}</h1></header>',f'<img src="{e(d["cover"],quote=True)}" alt="Complete Toshali Anthology 2027 front cover" style="max-width:100%;max-height:80vh;object-fit:contain">']
    intro=d.get('introduction',{})
    if intro.get('text'):
        parts.append(f'<section class="prose" lang="{e(intro.get("language","or"),quote=True)}"><h2>{e(intro["title"])}</h2><p>{e(intro.get("byline",""))}</p>')
        parts.extend('<p>'+e(p).replace('\n','<br>')+'</p>' for p in intro['text'].split('\n\n'));parts.append('</section>')
    parts.append('<nav aria-label="Anthology contents"><ol>')
    parts.extend(f'<li><a href="#poem-{p["id"]}">{e(p["title"])} — {e(p["author"])}</a></li>' for p in d['poems']);parts.append('</ol></nav>')
    for p in d['poems']:
        parts.append(f'<article class="section" id="poem-{p["id"]}"><h2>{e(p["title"])}</h2><p><a href="poet-{p["writer_id"]}.html">{e(p["author"])}</a></p>')
        art=p.get('artwork',{})
        if art.get('mode')=='illustrated':parts.append(f'<figure><img src="{e(art["src"],quote=True)}" alt="{e(art["alt"],quote=True)}" width="{art["width"]}" height="{art["height"]}" loading="lazy" style="max-width:100%;height:auto"><figcaption>{e(art["caption"])}</figcaption></figure>')
        versions={p['language']:{'title':p['title'],'stanzas':p['stanzas'],'credit':''},**p.get('translations',{})}
        for lang,v in versions.items():
            parts.append(f'<section lang="{lang}"><h3>{e(v["title"])}</h3>')
            parts.extend('<p class="verse">'+'<br>'.join(e(line) for line in stanza)+'</p>' for stanza in v['stanzas'])
            parts.append('<p>'+e(v.get('credit',''))+'</p></section>')
        parts.append('</article>')
    page('toshali-book-2027.html',d['title'],''.join(parts),desc='Toshali Anthology of Poetry 2027: poems and their language editions.')
