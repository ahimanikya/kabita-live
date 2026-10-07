"""Approved homepage feature and permanent Our Story link for the language essay."""
from language_article import ROUTE


def apply_article_links(site):
    home = site / 'index.html'
    text = home.read_text()
    if 'id="home-language-essay"' not in text:
        marker = '<section class="section home-editors"'
        assert marker in text and text.index('Recent editions') < text.index(marker)
        feature = f'''<section class="section home-language-essay" id="home-language-essay" aria-labelledby="home-language-essay-title">
<figure><img src="assets/articles/thirty-languages/poetry-across-languages-hero-800.webp" width="1672" height="941" loading="lazy" decoding="async" alt="Two readers comparing a book and a sheet of writing at a shared table."></figure>
<div><span class="eyebrow">Poetry across languages</span><h2 id="home-language-essay-title">Thirty languages and the journey of a poem</h2>
<p>Population can guide a multilingual poetry collection. Literary traditions and thoughtful translation shape what reaches the reader.</p>
<a class="text-link" href="{ROUTE}">Read the essay</a></div></section>'''
        text = text.replace(marker, feature + marker, 1)
        text = text.replace('</head>', '<link rel="stylesheet" href="assets/article-links.css?v=1"></head>', 1)
        home.write_text(text)
    story = site / 'about.html'
    text = story.read_text()
    if 'id="story-language-essay"' not in text:
        start = text.index('<div class="story-invitations">')
        end = text.index('</div>', start) + len('</div>')
        section = f'''<section class="story-language-essay" id="story-language-essay" aria-labelledby="story-language-essay-title">
<h2 id="story-language-essay-title">Poetry across languages</h2>
<p>What should a poem carry with it when it enters another language? Explore how population, literary traditions and close attention to meaning can guide a multilingual collection.</p>
<a class="text-link" href="{ROUTE}">Read the essay</a></section>'''
        text = text[:end] + section + text[end:]
        text = text.replace('</head>', '<link rel="stylesheet" href="assets/article-links.css?v=1"></head>', 1)
        story.write_text(text)
