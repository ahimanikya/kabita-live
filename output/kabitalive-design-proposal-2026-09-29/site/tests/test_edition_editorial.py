import json
import tempfile
import unittest
from pathlib import Path
from edition_editorial import render_editorial

class EditorialReader(unittest.TestCase):
    def render(self, variants, **extra):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);p=root/'content/editorials/issue-50.json';p.parent.mkdir(parents=True)
            p.write_text(json.dumps(dict(status='user_reviewed',original_language='or',variants=variants,**extra)))
            return render_editorial(root,50,{}, {})

    def test_original_prose_has_no_translation_controls(self):
        html=self.render({'or':{'title':'Original','paragraphs':['One']}},translationException='Private reason')
        self.assertIn('id="editorial-or"',html)
        self.assertIn('<p>One</p>',html)
        self.assertNotIn('data-editorial-language',html)
        self.assertNotIn('Private reason',html)

    def test_additional_variants_and_their_credits_are_not_exported(self):
        html=self.render({'or':{'title':'Original','paragraphs':['One']},'en':{'title':'English','paragraphs':['First','Second'],'credit':'Translated by A & B <script>alert(1)</script>'}},quotes=[],paragraph_poem_ids=[[]])
        self.assertIn('<p>One</p>',html)
        self.assertNotIn('<p>Second</p>',html)
        self.assertNotIn('Translated by',html)
        self.assertNotIn('id="editorial-en"',html)

    def test_missing_original_fails_closed(self):
        with self.assertRaisesRegex(ValueError,'verified original language'):
            self.render({'en':{'title':'Translation','paragraphs':['Text']}})

    def test_original_prose_is_escaped(self):
        html=self.render({'or':{'title':'A & B','paragraphs':['<script>example</script>']}})
        self.assertIn('A &amp; B',html)
        self.assertIn('&lt;script&gt;example&lt;/script&gt;',html)
        self.assertNotIn('<script>example',html)
