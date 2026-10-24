"""Approved masthead B; exact reviewed SVG composition scales at every cover size."""
import json,re
from functools import lru_cache
from html import escape, unescape
from itertools import count
from textwrap import wrap, shorten
_sequence=count()
@lru_cache(maxsize=1)
def catalogue(root):
    return json.loads((root/'data/cover-layout-b.json').read_text())
@lru_cache(maxsize=1)
def delivery(root):
    path=root/'data/cover-delivery.json'
    return json.loads(path.read_text()) if path.exists() else {}
def render_cover(root,number,alt,*,card=False):
    svg='\n'.join(line.rstrip() for line in catalogue(root)[str(number)]['svg'].splitlines() if line.strip())
    if card:
        source=catalogue(root)[str(number)]['artwork']
        variant=delivery(root).get(source)
        if variant:
            svg=svg.replace('href="'+source+'"','href="'+variant['src']+'"')
    token=f'cover-b-{number}-{next(_sequence)}-'
    svg=re.sub(r'id="([^"]+)"',lambda m:'id="'+token+m[1]+'"',svg)
    svg=re.sub(r'url\(#([^\)]+)\)',lambda m:'url(#'+token+m[1]+')',svg)
    svg=re.sub(r'aria-label="[^"]+"',lambda m:'aria-label="'+escape(f'Kabita Live issue {number}. {alt}',quote=True)+'"',svg,count=1)
    return f'<div class="cover photo-cover cover-b cover-{number}" data-cover-edition="{number}">'+svg+'</div>'

def render_back_cover(root,number,title,story,date,*,card=False):
    """A new companion design, never a reconstruction of a historical back cover."""
    source=catalogue(root)[str(number)]['artwork']
    if card:source=delivery(root).get(source,{}).get('src',source)
    title_lines=wrap(title,30,break_long_words=False,break_on_hyphens=False)
    # An exact opening extract from the existing cover narrative, not a poem quote.
    excerpt=shorten(story.split('. ')[0].rstrip('.')+'.',width=175,placeholder='…')
    story_lines=wrap(excerpt,45,break_long_words=False,break_on_hyphens=False)
    def lines(values,y,step):
        return ''.join(f'<tspan x="512" y="{y+i*step}">{escape(line)}</tspan>' for i,line in enumerate(values))
    svg=(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1536" width="1024" height="1536" role="img" aria-label="{escape(f"Issue {number} back cover: {title}. {excerpt}",quote=True)}">'
        '<path fill="#F5EFDF" d="M0 0h1024v1536H0z"/>'
        f'<text x="512" y="98" text-anchor="middle" font-family="Arial,sans-serif" font-size="28" fill="#655F51">{escape(f"ISSUE {number} · {date.upper()}")}</text>'
        f'<image href="{escape(source,quote=True)}" x="112" y="174" width="800" height="540" preserveAspectRatio="xMidYMid meet"/>'
        '<g text-anchor="middle" fill="#263C3C">'
        '<text font-family="Cormorant Garamond,Georgia,serif" font-size="64" font-weight="500">'+lines(title_lines,808,70)+'</text>'
        '<text font-family="Source Serif 4,Georgia,serif" font-size="34">'+lines(story_lines,1000,48)+'</text>'
        '<text x="512" y="1330" font-family="Cormorant Garamond,Georgia,serif" font-size="72" font-weight="600">Kabita Live</text>'
        '<text x="512" y="1400" font-family="Noto Serif Oriya,serif" font-size="40" lang="or">ମାଟିର ମହକ · ହୃଦୟର ସ୍ବର</text>'
        '<text x="512" y="1470" font-family="Arial,sans-serif" font-size="28">kabitalive.com</text></g></svg>')
    return f'<div class="cover magazine-back" data-back-cover-edition="{number}">{svg}</div>'

def cover_link_label(markup, number, side):
    """Keep visible cover lettering in the link name for speech navigation."""
    lettering = ' '.join(' '.join(unescape(re.sub(r'<[^>]+>', ' ', text)).split())
                         for text in re.findall(r'<text\b[^>]*>(.*?)</text>', markup, re.S))
    return escape(f'Read issue {number} — {side} cover: {lettering}', quote=True)

def render_cover_pair(root,number,alt,title,story,date,*,card=False,local=False):
    href=f'issue-{number}.html'
    front=render_cover(root,number,alt,card=card)
    if not local:
        return f'<a class="magazine-cover-link" href="{href}" aria-label="{cover_link_label(front,number,"front")}">{front}</a>'
    token=f'cover-view-{number}-{next(_sequence)}'
    sides=[('front',front),('back',render_back_cover(root,number,title,story,date,card=card))]
    return (f'<div class="magazine-view" data-cover-view role="group" aria-label="Issue {number} cover">'+''.join(
        f'<a id="{token}-{side}" class="magazine-cover-link" data-cover-face="{side}"'+(' hidden' if side=='back' else '')+f' href="{href}" aria-label="{cover_link_label(art,number,side)}">{art}</a>'
        for side,art in sides)+f'<button type="button" class="magazine-cover-toggle" data-cover-toggle aria-controls="{token}-front {token}-back" aria-label="View back cover of issue {number}" hidden>View back cover</button></div>')
def apply_cover_styles(root):
    for path in root.glob('*.html'):
        if path.is_symlink():continue
        text=path.read_text()
        if 'data-cover-edition=' in text:
            text=text.replace('</head>','<link rel="stylesheet" href="assets/cover-layout-b.css?v=20261004"></head>')
            if path.name in ('index.html','archive.html') or re.fullmatch(r'(?:issue-\d+|archive-\d{4})\.html',path.name):
                text=re.sub(r'class="(cover photo-cover cover-b cover-\d+)(?: magazine-object)?"',r'class="\1 magazine-object"',text)
                text=text.replace('</head>','<link rel="stylesheet" href="assets/magazine-covers.css?v=3"></head>')
            path.write_text(text)
