import json
import unittest
from html.parser import HTMLParser
from pathlib import Path
from cover_layout import render_cover, render_cover_pair
from social_metadata import Page, choose_image

ROOT = Path(__file__).resolve().parents[1]


class Links(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.links = []
        self.depth = 0
        self.nested = False
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            self.nested |= self.depth > 0
            self.depth += 1
            self.links.append(dict(attrs))

    def handle_endtag(self, tag):
        if tag == 'a':
            self.depth -= 1


class MagazineCovers(unittest.TestCase):
    def test_every_edition_has_two_named_entry_links_and_preserves_share_source(self):
        for row in json.loads((ROOT / 'cover-catalogue.json').read_text()):
            with self.subTest(edition=row['number']):
                n = row['number']
                pair = render_cover_pair(ROOT, n, row['alt'], row['title'], row['story'], row['date'], local=True)
                links = Links(pair)
                self.assertFalse(links.nested)
                self.assertEqual(len(links.links), 2)
                for side, link in zip(('front', 'back'), links.links):
                    self.assertEqual(link['href'], f'issue-{n}.html?focus=1')
                    self.assertIn(side, link['aria-label'])
                    self.assertIn('data-open-edition-reader', link)
                    self.assertEqual('hidden' in link, side == 'back')
                page = Page('<figure class="edition-cover">' + pair + '</figure>')
                image, reason = choose_image(f'issue-{n}.html', page, {})
                self.assertEqual(reason, 'edition_cover')
                original = Page(render_cover(ROOT, n, row['alt']))
                self.assertEqual(image['source'], original.images[0]['source'])

    def test_listing_covers_keep_normal_navigation_and_escape_source_copy(self):
        pair = render_cover_pair(ROOT, 48, 'Artwork', '<A & B>', 'A "quiet" <beginning>. More.', 'October 2026', card=True)
        self.assertNotIn('data-open-edition-reader', pair)
        self.assertEqual(len(Links(pair).links), 1)
        self.assertNotIn('data-back-cover-edition', pair)
        pair = render_cover_pair(ROOT, 48, 'Artwork', '<A & B>', 'A \"quiet\" <beginning>. More.', 'October 2026', local=True)
        self.assertNotIn('<A & B>', pair)
        self.assertIn('&lt;A &amp; B&gt;', pair)
        self.assertIn('preserveAspectRatio="xMidYMid meet"', pair)


if __name__ == '__main__':
    unittest.main()
