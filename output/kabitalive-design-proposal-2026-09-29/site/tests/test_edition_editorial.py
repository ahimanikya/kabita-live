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
    def test_only_existing_variants_have_links_and_original_badge(self):
        html=self.render({'or':{'title':'Original','paragraphs':['One']}},translationException='Private reason')
        self.assertIn('href="#editorial-or"',html);self.assertNotIn('href="#editorial-en"',html);self.assertNotIn('href="#editorial-hi"',html)
        self.assertIn('Original</span>',html);self.assertIn('data-editorial-original="or"',html);self.assertNotIn('Private reason',html)
    def test_studio_paragraph_counts_can_differ_and_credits_are_escaped(self):
        html=self.render({'or':{'title':'Original','paragraphs':['One']},'en':{'title':'English','paragraphs':['First','Second'],'credit':'Translated by A & B <script>alert(1)</script>'}},quotes=[],paragraph_poem_ids=[[]])
        self.assertIn('<p>Second</p>',html);self.assertIn('A &amp; B &lt;script&gt;',html);self.assertNotIn('<script>alert',html)
    def test_ai_production_credit_is_held_not_silently_rewritten(self):
        with self.assertRaises(ValueError):self.render({'en':{'title':'Translation','paragraphs':['Text'],'credit':'Translated by ChatGPT; reviewed by Editor'}})
    def test_legacy_creditless_variants_still_render(self):
        html=self.render({'or':{'title':'Original','paragraphs':['One']},'en':{'title':'English','paragraphs':['Two']}})
        self.assertIn('href="#editorial-en"',html);self.assertNotIn('class="editorial-status"',html)
