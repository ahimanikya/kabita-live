import json
from html import escape
import unittest
from pathlib import Path
from writer_names import writer_search_names, writer_aliases, load_writer_profiles
from poet_directory import render_poet_directory

ROOT = Path(__file__).resolve().parents[1]

class WriterSearchAliases(unittest.TestCase):
    def test_search_alias_does_not_merge_distinct_people(self):
        self.assertEqual(writer_search_names(ROOT)[478], ['Sasmita Rout'])
        self.assertNotIn(478, writer_aliases(ROOT))
        profiles = {p['id']: p for p in load_writer_profiles(ROOT)}
        self.assertEqual(profiles[478]['name'], 'ସସ୍ମିତା ରାଉତ')
        self.assertNotEqual(profiles[478]['name'], profiles[235]['name'])
        html = render_poet_directory(ROOT, [profiles[235], profiles[478]], {}, {}, {})
        self.assertIn('href="poet-478.html"', html)
        self.assertIn('href="poet-235.html"', html)
        from html.parser import HTMLParser
        class Cards(HTMLParser):
            entries = {}
            def handle_starttag(self, tag, attrs):
                attrs = dict(attrs)
                if 'data-writer' in attrs: self.entries[attrs['data-writer']] = attrs['data-search']
        cards = Cards(); cards.feed(html)
        self.assertIn('Sasmita Rout', cards.entries['478'])
        self.assertIn('Sasmita Rout', cards.entries['235'])

    def test_alias_has_existing_editorial_source(self):
        item = json.loads((ROOT/'data/writer-search-aliases.json').read_text())['478']
        source = (ROOT/item['source']).read_text()
        self.assertIn('Sasmita Rout', source)

    def test_poem_search_includes_alias_without_changing_credit(self):
        # Execute renderer definitions only; no site build or generated writes.
        source = (ROOT/'edition-pages.py').read_text().split('def collection_languages_markup')[0]
        scope = dict(R=ROOT, publication_issues=[], load_writer_profiles=load_writer_profiles,
                     e=escape, json=json, sample_routes={}, profile_routes={})
        exec(compile(source, 'edition-pages.py', 'exec'), scope)
        scope['edition_poet'] = lambda poem, show_issue=False: ''
        poem = dict(id=835, writer_id=478, language='or', title='ନିରବ ଆଳାପ',
                    author='ସସ୍ମିତା ରାଉତ', text='Original', edition=49)
        html = scope['edition_rows']([poem])
        self.assertIn('Sasmita Rout', html)
        self.assertIn('data-poet="478"', html)
        self.assertIn('href="poem-835.html"', html)
        self.assertEqual(poem['author'], 'ସସ୍ମିତା ରାଉତ')
