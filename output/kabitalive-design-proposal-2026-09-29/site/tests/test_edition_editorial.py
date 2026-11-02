import json
import tempfile
import unittest
from pathlib import Path
from edition_editorial import render_editorial


class EditorialReader(unittest.TestCase):
    def render(self, variants, poems=None, **extra):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);p=root/'content/editorials/issue-50.json';p.parent.mkdir(parents=True)
            p.write_text(json.dumps(dict(status='user_reviewed',original_language='or',variants=variants,**extra)))
            return render_editorial(root,50,poems or {}, {})

    def test_single_version_remains_readable_without_unnecessary_controls(self):
        html=self.render({'or':{'title':'Original','paragraphs':['One']}},translationException='Private reason')
        self.assertIn('id="editorial-or"',html)
        self.assertIn('<p>One</p>',html)
        self.assertNotIn('data-editorial-language',html)
        self.assertNotIn('Private reason',html)

    def test_three_versions_are_readable_without_script_english_first(self):
        html=self.render({lang:{'title':lang,'paragraphs':[lang+' prose']} for lang in ['or','hi','en']})
        self.assertLess(html.index('id="editorial-en"'),html.index('id="editorial-or"'))
        self.assertLess(html.index('id="editorial-or"'),html.index('id="editorial-hi"'))
        for lang in ['en','or','hi']:
            self.assertIn(f'data-editorial-language="{lang}"',html)
            self.assertIn(f'href="#editorial-{lang}"',html)
            self.assertIn(f'<p>{lang} prose</p>',html)
        self.assertNotIn(' hidden',html)
        self.assertIn('assets/edition-editorial.js?v=5',html)

    def test_human_translation_credit_escapes_markup(self):
        html=self.render({'or':{'title':'Original','paragraphs':['One']},'en':{'title':'English','paragraphs':['First','Second'],'credit':'Translated by A & B <script>alert(1)</script>'}},quotes=[],paragraph_poem_ids=[[]])
        self.assertIn('<p>Second</p>',html)
        self.assertIn('Translated by A &amp; B &lt;script&gt;',html)
        self.assertNotIn('<script>alert',html)

    def test_all_editorial_languages_quote_same_original_not_renderings(self):
        variants={lang:{'title':lang,'paragraphs':['Prose']} for lang in ['or','hi','en']}
        quote={'after':0,'poem_id':1,'language':'hi','original':'पहली पंक्ति\nदूसरी पंक्ति','renderings':{'or':'WITHHELD_ODIA','en':'WITHHELD_ENGLISH'}}
        poems={1:{'writer_id':2,'author':'Poet','title':'कविता','language':'hi'}}
        html=self.render(variants,poems=poems,quotes=[quote])
        self.assertEqual(html.count('<blockquote lang="hi"><p>पहली पंक्ति<br>दूसरी पंक्ति</p></blockquote>'),3)
        self.assertEqual(html.count('<figcaption lang="hi">'),3)
        self.assertNotIn('WITHHELD',html)
        self.assertNotIn('excerpt-translation',html)

    def test_inline_quotes_keep_source_language_and_escape_all_text(self):
        html=self.render({'or':{'title':'Original','paragraphs':['ପ୍ରସଙ୍ଗ “A & B <line>” <script>after</script>'],'inline_quotes':[{'text':'A & B <line>','language':'en'}]}})
        self.assertIn('“<span lang="en">A &amp; B &lt;line&gt;</span>” &lt;script&gt;after&lt;/script&gt;',html)
        self.assertNotIn('<script>after',html)

    def test_invalid_inline_quote_metadata_fails(self):
        for quote in [{'text':'','language':'en'},{'text':'missing','language':'en'},{'text':'Text','language':'bad" onclick="x'}]:
            with self.subTest(quote=quote),self.assertRaisesRegex(ValueError,'invalid inline quotation'):
                self.render({'or':{'title':'Original','paragraphs':['Text'],'inline_quotes':[quote]}})

    def test_inline_verse_line_breaks_are_preserved(self):
        html=self.render({'or':{'title':'Original','paragraphs':['ପ୍ରସଙ୍ଗ “First line\nSecond line”'],'inline_quotes':[{'text':'First line\nSecond line','language':'en'}]}})
        self.assertIn('<span lang="en">First line<br>Second line</span>',html)

    def test_missing_original_fails_closed(self):
        with self.assertRaisesRegex(ValueError,'verified original language'):
            self.render({'en':{'title':'Translation','paragraphs':['Text']}})

    def test_original_prose_is_escaped(self):
        html=self.render({'or':{'title':'A & B','paragraphs':['<script>example</script>']}})
        self.assertIn('A &amp; B',html)
        self.assertIn('&lt;script&gt;example&lt;/script&gt;',html)
        self.assertNotIn('<script>example',html)
