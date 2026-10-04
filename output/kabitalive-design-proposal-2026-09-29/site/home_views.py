"""Approved quiet homepage views; covers retain stable edition identities."""
import json
import re
from html import escape


def apply_home_views(site):
    views = json.loads((site / 'data/home-views.json').read_text())
    path = site / 'index.html'
    text = path.read_text()
    first = views[0]
    figure = ('<figure class="home-art home-views">'
              f'<img id="home-view-image" src="{first["src"]}" srcset="{first["small"]} 768w, {first["src"]} 1536w" '
              'sizes="(max-width:760px) calc(100vw - 40px), (max-width:1224px) 55vw, 640px" '
              f'alt="{escape(first["alt"])}" width="1536" height="1024" fetchpriority="high" decoding="async">'
              f'<figcaption><span id="home-view-title">{escape(first["title"])}</span></figcaption></figure>')
    text, count = re.subn(r'<figure class="home-art">.*?</figure>', lambda _: figure, text, count=1, flags=re.S)
    assert count == 1, 'Homepage artwork missing'
    payload = json.dumps(views, ensure_ascii=False).replace('<', '\\u003c')
    text = text.replace('</head>', '<link rel="stylesheet" href="assets/home-views.css?v=2"></head>')
    text = text.replace('</body>', f'<script type="application/json" id="home-view-data">{payload}</script><script defer src="assets/home-views.js?v=2"></script></body>')
    path.write_text(text)
    about = site / 'about.html'
    text = about.read_text()
    credit = ('<p id="home-view-sources">The homepage field, flower-in-palm and rainy-street paintings are AI-assisted Poetic Natural interpretations of Odisha photographs by Ahimanikya Satapathy. '
              'They are artistic adaptations, not documentary photographs. The courtyard is an AI-assisted imagined scene.</p>')
    marker = '<details><summary>Artwork and image sources</summary>'
    assert marker in text, 'Artwork credits missing'
    start = text.index(marker)
    end = text.index('</summary>', start) + len('</summary>')
    text = text[:end] + credit + text[end:]
    about.write_text(text)
