"""Permanent Our Story link for the language essay."""
from language_article import ROUTE


def apply_article_links(site):
    story = site / 'about.html'
    text = story.read_text()
    if 'id="story-language-essay"' not in text:
        start = text.index('<div class="story-invitations">')
        end = text.index('</div>', start) + len('</div>')
        section = f'''<section class="story-language-essay" id="story-language-essay" aria-labelledby="story-language-essay-title">
<h2 id="story-language-essay-title">Poetry across languages</h2>
<p>Our magazine focuses on Odia, Hindi and English. Explore how a poem’s voice, cultural detail and feeling can travel between these three languages.</p>
<a class="text-link" href="{ROUTE}">Read the essay</a></section>'''
        text = text[:end] + section + text[end:]
        text = text.replace('</head>', '<link rel="stylesheet" href="assets/article-links.css?v=1"></head>', 1)
        story.write_text(text)
