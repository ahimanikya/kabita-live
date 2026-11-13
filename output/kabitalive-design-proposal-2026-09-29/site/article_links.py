"""Retire the language-essay teaser; preserve its archived source separately."""
import re


def apply_article_links(site):
    story = site / 'about.html'
    text = story.read_text()
    # Also cleans an already-generated local page without reintroducing the link.
    text = re.sub(r'<section\b[^>]*\bid="story-language-essay"[^>]*>.*?</section>', '', text, flags=re.S)
    text = re.sub(r'<link\b[^>]*href="assets/article-links\.css(?:\?[^"]*)?"[^>]*>', '', text)
    story.write_text(text)
