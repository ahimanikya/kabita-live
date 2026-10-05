import unittest
from image_delivery import enhance
from social_metadata import Page
D={'assets/poem-art/example.webp':{'width':1536,'height':1024,'preview':'data:image/webp;base64,eA==','variants':[{'src':'assets/responsive/test-480.webp','width':480}]}}
class Delivery(unittest.TestCase):
 def test_native_fallback_and_source_identity(self):
  result=enhance('<head></head><figure class="poem-art"><img src="assets/poem-art/example.webp" alt="A tree" width="1536" height="1024"></figure>',D)
  self.assertIn('src="assets/poem-art/example.webp"',result)
  self.assertIn('assets/responsive/test-480.webp 480w',result)
  self.assertIn('background-image:url(data:image/webp;',result)
  self.assertEqual(Page(result).images[0]['source'],'assets/poem-art/example.webp')
 def test_existing_direction_and_lazy_loading_survive(self):
  result=enhance('<img src="assets/poem-art/example.webp" srcset="special.webp 800w" sizes="50vw" loading="lazy" alt="Tree">',D)
  for item in ['srcset="special.webp 800w"','sizes="50vw"','loading="lazy"','alt="Tree"']:self.assertIn(item,result)
 def test_icons_unchanged(self):
  image='<img src="assets/icon.svg" alt="">'
  self.assertEqual(enhance(image,D),image)
