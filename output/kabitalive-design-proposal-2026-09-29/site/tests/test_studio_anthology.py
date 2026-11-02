import unittest, tempfile, json
from pathlib import Path
from studio_anthology import render_studio_anthologies
class StudioAnthology(unittest.TestCase):
 def test_sanitized_submitted_poem_renders_without_added_translations(self):
  with tempfile.TemporaryDirectory() as folder:
   root=Path(folder);(root/'content/anthologies').mkdir(parents=True)
   (root/'content/anthologies/toshali-2027.json').write_text(json.dumps({'title':'Anthology','cover':'assets/cover.webp','poems':[{'id':900,'title':'<script>','author':'Writer','writer_id':1,'language':'or','stanzas':[['line one','line two']], 'translations':{'en':{'title':'Translated','stanzas':[['English stanza']], 'credit':'Translator'}}}]}))
   pages=[];render_studio_anthologies(root,lambda *a,**k:pages.append(a));self.assertEqual(pages[0][0],'toshali-book-2027.html');self.assertIn('&lt;script&gt;',pages[0][2]);self.assertIn('lang="or"',pages[0][2]);self.assertNotIn('lang="en"',pages[0][2]);self.assertNotIn('English stanza',pages[0][2]);self.assertNotIn('Translated',pages[0][2]);self.assertNotIn('Translator',pages[0][2]);self.assertIn('line one<br>line two',pages[0][2]);self.assertNotIn('<script>',pages[0][2])
