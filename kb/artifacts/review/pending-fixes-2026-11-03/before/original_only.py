"""Fail public export if additional website translations return.

Submitted works (including credited human translations) remain canonical originals.
Historical translation drafts are preserved in source/KB but are not public assets.
"""
import json
from html.parser import HTMLParser


def check_reader(data, label):
    if not isinstance(data, dict):
        raise ValueError(f'{label}: malformed reader payload')
    if 'variants' in data:
        source = data.get('source_language')
        if not source or set(data['variants']) != {source}:
            raise ValueError(f'{label}: reader must contain only its submitted language')
    for poem in data.get('poems', []):
        check_reader(poem, label)


class OriginalOnlyHTML(HTMLParser):
    def __init__(self, label):
        super().__init__(convert_charrefs=True)
        self.label = label
        self.reading = False
        self.payload = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        for control in ('data-reading-language', 'data-focus-language', 'data-collection-language', 'data-editorial-language'):
            if control in attrs:
                raise ValueError(f'{self.label}: removed translation control {control} returned')
        if 'data-reading-titles' in attrs:
            titles = json.loads(attrs['data-reading-titles'])
            if set(titles) != {attrs.get('data-lang')}:
                raise ValueError(f'{self.label}: translated listing titles returned')
        if 'excerpt-translation' in attrs.get('class', '').split():
            raise ValueError(f'{self.label}: translated editorial excerpt returned')
        if tag == 'script' and attrs.get('id') in ('reading-data', 'focus-entry-data'):
            self.reading = True
            self.payload = []

    def handle_data(self, data):
        if self.reading:
            self.payload.append(data)

    def handle_endtag(self, tag):
        if tag == 'script' and self.reading:
            check_reader(json.loads(''.join(self.payload)), self.label)
            self.reading = False


def check_public_originals(root, pages, assets):
    for name, html in pages.items():
        if name == 'translation-review.html':
            raise ValueError('Translation review material must stay outside public export')
        OriginalOnlyHTML(name).feed(html)
    for relative in assets:
        if 'poem-translations' in relative or 'translation-review' in relative:
            raise ValueError(f'Private translation data in public assets: {relative}')
        if relative.startswith(('assets/reading-editions/', 'assets/reading-authors/')) or relative == 'assets/reading-all.json':
            check_reader(json.loads((root / relative).read_text()), relative)
