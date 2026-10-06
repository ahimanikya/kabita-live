"""Approved masthead B; exact reviewed SVG composition scales at every cover size."""
import json,re
from functools import lru_cache
from html import escape
from itertools import count
_sequence=count()
@lru_cache(maxsize=1)
def catalogue(root):
    return json.loads((root/'data/cover-layout-b.json').read_text())
def render_cover(root,number,alt):
    svg='\n'.join(line.rstrip() for line in catalogue(root)[str(number)]['svg'].splitlines() if line.strip())
    token=f'cover-b-{number}-{next(_sequence)}-'
    svg=re.sub(r'id="([^"]+)"',lambda m:'id="'+token+m[1]+'"',svg)
    svg=re.sub(r'url\(#([^\)]+)\)',lambda m:'url(#'+token+m[1]+')',svg)
    svg=re.sub(r'aria-label="[^"]+"',lambda m:'aria-label="'+escape(f'Kabita Live issue {number}. {alt}',quote=True)+'"',svg,count=1)
    return f'<div class="cover photo-cover cover-b cover-{number}" data-cover-edition="{number}">'+svg+'</div>'
def apply_cover_styles(root):
    for path in root.glob('*.html'):
        if path.is_symlink():continue
        text=path.read_text()
        if 'data-cover-edition=' in text:
            text=text.replace('</head>','<link rel="stylesheet" href="assets/cover-layout-b.css?v=20261004"></head>')
            if path.name in ('index.html','archive.html') or re.fullmatch(r'(?:issue-\d+|archive-\d{4})\.html',path.name):
                text=re.sub(r'class="(cover photo-cover cover-b cover-\d+)(?: magazine-object)?"',r'class="\1 magazine-object"',text)
                text=text.replace('</head>','<link rel="stylesheet" href="assets/magazine-covers.css?v=1"></head>')
            path.write_text(text)
