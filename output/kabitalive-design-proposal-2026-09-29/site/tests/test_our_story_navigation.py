import json
import unittest
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class Page(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.ids = {}; self.links = []; self.details = []; self.in_summary = 0
        self.summary_headings = []; self.feed(text)
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:self.ids.setdefault(attrs['id'], []).append((tag, attrs))
        if tag == 'a':self.links.append(attrs.get('href', ''))
        if tag == 'details':self.details.append(attrs)
        if tag == 'summary':self.in_summary += 1
        if self.in_summary and tag in ('h1','h2','h3'):self.summary_headings.append(tag)
    def handle_endtag(self, tag):
        if tag == 'summary':self.in_summary -= 1

class StoryNavigation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = (ROOT/'about.html').read_text()
        cls.page = Page(cls.text)
    def test_contents_targets_are_unique_and_sections_are_in_reading_order(self):
        targets = ['story','editors','creative-process','editorial-policies','design','credits','privacy']
        positions = []
        for target in targets:
            self.assertEqual(len(self.page.ids.get(target, [])), 1, target)
            self.assertIn('#'+target, self.page.links)
            positions.append(self.text.index('id="'+target+'"'))
        self.assertEqual(positions, sorted(positions))
        self.assertIn('aria-label="On this page"', self.text)
    def test_native_supplements_and_privacy_start_collapsed(self):
        self.assertFalse(self.page.summary_headings)
        self.assertEqual(self.page.ids['privacy'][0][0], 'details')
        self.assertNotIn('open', self.page.ids['privacy'][0][1])
        for name in ['story-design-details','story-team-details']:
            rows = [x for x in self.page.details if name in x.get('class','').split()]
            self.assertEqual(len(rows),1);self.assertNotIn('open',rows[0])
    def test_policy_words_and_fragments_survive_reordering(self):
        from html import escape
        for section in json.loads((ROOT/'data/editorial-policies.json').read_text())['sections']:
            self.assertIn('policy-'+section['id'],self.page.ids)
            for paragraph in section['paragraphs']:self.assertIn(escape(paragraph),self.text)
    def test_retired_essay_and_repeated_labels_are_removed(self):
        self.assertNotIn('story-language-essay',self.page.ids)
        self.assertNotIn('thirty-languages-and-the-journey-of-a-poem.html', self.page.links)
        self.assertNotIn('The editorial desk</span>',self.text)
        self.assertNotIn('Artwork and image sources',self.text)
        self.assertEqual(len(self.page.ids.get('credits-editors',[])),1)
        self.assertIn('The care behind these pages.',self.text)
        self.assertIn('not human staff',self.text)

    def test_existing_disclosure_and_human_portrait_links_remain(self):
        for fragment in ['credits-writers','credits-translations','credits-ahimanikya','creative-process-title','story-design-title']:
            self.assertIn(fragment,self.page.ids)
        for profile in ['editor-pradeep.html','editor-paresh.html','ahimanikya-satapathy.html']:
            self.assertIn(profile,self.page.links)
        self.assertIn('How we use AI',self.text)
        self.assertNotIn('What people teach AI about a language',self.text)

if __name__ == '__main__':unittest.main()
