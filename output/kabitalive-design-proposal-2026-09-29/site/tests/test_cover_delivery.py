import json,tempfile,unittest,re
from pathlib import Path
from cover_layout import render_cover,catalogue,delivery
from social_metadata import Page
class CoverDelivery(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name);(self.root/'data').mkdir()
  self.source='assets/covers/editions/example.webp'
  self.svg='<svg viewBox="0 0 1024 1536" aria-label="Old"><image href="'+self.source+'" width="1024" height="1536" preserveAspectRatio="xMidYMid slice"/><defs><linearGradient id="top"/></defs><path fill="url(#top)"/><text lang="or">ମାଟିର ମହକ</text></svg>'
  (self.root/'data/cover-layout-b.json').write_text(json.dumps({'1':{'svg':self.svg,'artwork':self.source}}))
 def tearDown(self):
  catalogue.cache_clear();delivery.cache_clear();self.temp.cleanup()
 def test_only_card_raster_changes_with_full_svg_geometry_and_lettering_preserved(self):
  (self.root/'data/cover-delivery.json').write_text(json.dumps({self.source:{'src':'assets/responsive/cover.webp'}}))
  native=render_cover(self.root,1,'Original & artwork');card=render_cover(self.root,1,'Original & artwork',card=True)
  normalize=lambda s:re.sub(r'cover-b-1-\d+-','cover-b-1-',s)
  self.assertEqual(normalize(card.replace('assets/responsive/cover.webp',self.source)),normalize(native))
  self.assertEqual(Page('<figure class="edition-cover">'+native+'</figure>').images[0]['source'],self.source)
  self.assertIn('Original &amp; artwork',card)
  self.assertNotEqual(re.findall(r'id="([^"]+)"',card),re.findall(r'id="([^"]+)"',native))
 def test_missing_manifest_retains_original(self):
  self.assertIn('href="'+self.source+'"',render_cover(self.root,1,'Art',card=True))
