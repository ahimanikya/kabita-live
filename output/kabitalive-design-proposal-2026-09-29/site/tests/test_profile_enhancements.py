import ast
import json
import re
import unittest
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def function_scope(path, names, **scope):
    tree = ast.parse(path.read_text())
    selected = ast.Module(body=[n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in names], type_ignores=[])
    exec(compile(selected, str(path), 'exec'), scope)
    return scope


class ProfileEnhancements(unittest.TestCase):
    def setUp(self):
        self.bio = function_scope(ROOT/'author-pages.py', {'author_biography_sections'}, e=escape)['author_biography_sections']
        self.work = function_scope(ROOT/'standalone-pages.py', {'writer_work'}, e=escape, catalogue={1: {'reader': 'poem-1.html', 'lang': 'or'}})['writer_work']

    def test_short_or_single_paragraph_biography_never_folds(self):
        for paragraphs in [['one two', 'three four'], ['word ' * 130]]:
            html = self.bio([{'heading': 'Life', 'paragraphs': paragraphs}])
            self.assertNotIn('<details', html)
            for p in paragraphs: self.assertIn(escape(p), html)

    def test_long_biography_preserves_order_language_and_no_js_content(self):
        sections = [{'heading': 'Life & writing', 'language': 'or', 'paragraphs': ['ଶବ୍ଦ ' * 60, 'ଅନ୍ୟ ' * 60]}, {'heading': 'Later', 'language': 'hi', 'paragraphs': ['कविता & जीवन']}]
        html = self.bio(sections)
        self.assertEqual(html.count('<details class="profile-more" open>'), 1)
        self.assertIn('<summary><span', html)
        self.assertLess(html.index('</section>'), html.index('<details'))
        self.assertEqual(re.findall(r'<p lang="([^"]+)">(.*?)</p>', html), [('or',escape(sections[0]['paragraphs'][0])),('or',escape(sections[0]['paragraphs'][1])),('hi',escape(sections[1]['paragraphs'][0]))])
        self.assertEqual(html.count('<section'), html.count('</section>'))
        self.assertIn('<h2>Later</h2>', html)

    def test_unenriched_mixed_script_paragraphs_retain_languages(self):
        html = self.bio([{'heading': 'Life', 'paragraphs': ['English ' * 60, 'ଓଡ଼ିଆ ' * 60], 'paragraph_languages': ['en', 'or']}])
        self.assertIn('<p lang="en">English', html)
        self.assertIn('<p lang="or">ଓଡ଼ିଆ', html)

    def test_compact_metadata_preserves_desktop_cells_and_actual_destinations(self):
        writer={'name':'Poet','works':[{'id':1,'title':'କବିତା & title','month':'November','year':'2026','issue':49}]}
        classic=self.work(writer)
        compact=self.work(writer,compact_profile=True)
        self.assertIn('class="contribution-mobile-date"', classic)
        self.assertNotIn('profile-mobile-meta', classic)
        self.assertIn('href="issue-49.html" class="profile-mobile-edition">Issue 49 · November 2026</a>', compact)
        self.assertEqual(re.findall(r'<td data-label=.*?</tr>',classic),re.findall(r'<td data-label=.*?</tr>',compact))
        self.assertEqual(set(re.findall(r'href="([^"]+)"',classic)),set(re.findall(r'href="([^"]+)"',compact)))

    def test_sparse_profile_has_no_fabricated_work_or_edition_link(self):
        self.assertNotIn('<table', self.work({'name':'Poet','works':[]},compact_profile=True))
        html=self.work({'name':'Poet','works':[{'id':1,'title':'Title','issue':None}]},compact_profile=True)
        self.assertIn('Edition not recorded · Date not recorded',html)
        self.assertNotIn('href="issue-',html)


if __name__ == '__main__': unittest.main()
