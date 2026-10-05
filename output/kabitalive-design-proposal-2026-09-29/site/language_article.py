"""Render the supplied language essay in the existing journal shell."""
from html import escape
import json
import re

ROUTE = 'thirty-languages-and-the-journey-of-a-poem.html'


def render_language_article(site):
    source = site / 'content/articles'
    metadata = json.loads((source / 'thirty-languages.json').read_text())
    dimensions = json.loads((source / 'thirty-languages-images.json').read_text())
    body = (source / 'thirty-languages.html').read_text()
    body = body.replace('<article>', '<article class="language-essay" aria-labelledby="article-title">', 1)
    body = body.replace('<h1>', '<h1 id="article-title">', 1)
    body = body.replace('class="lead"', 'class="lead article-lead"', 1)
    for name, size in dimensions.items():
        original = 'images/' + name + '.png'
        image = 'assets/articles/thirty-languages/' + name + '.webp'
        body = body.replace(original, image)
        pattern = r'<img\b[^>]*src="' + re.escape(image) + r'"[^>]*>'
        def image_tag(match):
            tag = re.sub(r' (?:width|height)="[^"]*"', '', match[0])
            attrs = f' width="{size["width"]}" height="{size["height"]}" decoding="async"'
            if name == 'poetry-across-languages-hero':
                attrs += f' fetchpriority="high" srcset="assets/articles/thirty-languages/{name}-800.webp 800w, {image} {size["width"]}w" sizes="(max-width: 760px) calc(100vw - 40px), 960px"'
            return tag[:-1] + attrs + '>'
        body = re.sub(pattern, image_tag, body)
    # Keep the supplied prose, sources, image disclosures and both semantic tables.
    # The narrow-screen table regions are keyboard-scrollable and named.
    table_number = 0
    def table_region(match):
        nonlocal table_number
        table_number += 1
        label = 'India population data' if table_number == 1 else 'Worldwide population data'
        return f'<div class="table-wrap" tabindex="0" role="region" aria-label="{label}">'
    body = re.sub(r'<div class="(?:table-wrap|table-scroll)">', table_region, body)
    body = body.replace('<footer class="article-notes">', '<section class="article-notes" aria-labelledby="article-notes-title">')
    body = body.replace('<h2>Data and image notes</h2>', '<h2 id="article-notes-title">Data and image notes</h2>')
    body = body.replace('</footer>', '</section>')
    body = '<link rel="stylesheet" href="assets/language-essay.css?v=1">' + body
    return metadata, body


def finish_language_article(site, metadata):
    path = site / ROUTE
    text = path.read_text()
    description = escape(metadata['excerpt'], quote=True)
    text = text.replace('</head>', f'<meta name="description" content="{description}"></head>', 1)
    path.write_text(text)
