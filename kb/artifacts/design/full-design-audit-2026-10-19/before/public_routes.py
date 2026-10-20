"""Explicit reader route boundary; development material is local-only."""
import re

READER_PAGES = {
    'index.html', 'about.html', 'archive.html', 'poems.html', 'poets.html',
    'contact.html', 'submit.html', 'search.html', 'not-found.html', '404.html',
    'editorial-team.html', 'editor-pradeep.html', 'editor-paresh.html',
    'ahimanikya-satapathy.html', 'thirty-languages-and-the-journey-of-a-poem.html',
    'highlight.html', 'highlights.html', 'feedback.html', 'upcoming.html',
    'current-contributors.html', 'translation-review.html',
    'poem-dokana.html', 'poem-kshanika.html', 'poem-drink.html',
    'poet-dokana.html', 'poet-kshanika.html', 'poet-drink.html',
}

def is_reader_page(name):
    return name in READER_PAGES or bool(re.fullmatch(r'(?:poem|poet|issue|archive)-[0-9]+\.html', name))
