import unittest
from retired_external_links import remove_retired_links
class RetiredLinks(unittest.TestCase):
 def test_only_exact_confirmed_link_is_removed(self):
  text='<a href="https://example.org/old" target="_blank">Source ↗</a><a href="https://example.org/new">New</a>'
  result=remove_retired_links(text,{'https://example.org/old'})
  self.assertIn('<span class="unavailable-reference">Source</span>',result)
  self.assertIn('<a href="https://example.org/new">New</a>',result)
 def test_encoded_urls_preserve_label_markup(self):
  self.assertEqual(remove_retired_links('<a href="https://example.org/?a=1&amp;b=2"><em>Book</em></a>',{'https://example.org/?a=1&b=2'}),'<span class="unavailable-reference"><em>Book</em></span>')
 def test_unlisted_links_and_poetry_unchanged(self):
  text='<p>Words about AI</p><a href="poem-1.html">Poem</a>'
  self.assertEqual(remove_retired_links(text,{'https://example.org/old'}),text)
