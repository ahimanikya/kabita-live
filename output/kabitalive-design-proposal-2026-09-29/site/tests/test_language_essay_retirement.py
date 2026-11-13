"""Retirement excludes reader output without deleting source or response history."""
import sys
import tempfile
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from article_links import apply_article_links
from public_routes import is_reader_page
ROUTE='thirty-languages-and-the-journey-of-a-poem.html'
class LanguageEssayRetirement(unittest.TestCase):
    def test_route_excluded_and_source_preserved(self):
        self.assertFalse(is_reader_page(ROUTE))
        self.assertTrue((ROOT/'content/articles/thirty-languages.json').is_file())
        self.assertTrue((ROOT/'language_article.py').is_file())
        self.assertIn('kabita:article:language-journey',(ROOT/'src/article-responses.mjs').read_text())
    def test_teaser_removed_idempotently_without_other_content_loss(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);page=root/'about.html'
            page.write_text('<main><p>Keep story</p><section class="story-language-essay" id="story-language-essay"><h3>Further reading</h3><a href="'+ROUTE+'">Essay</a></section><details id="privacy">Keep choices</details></main>')
            expected='<main><p>Keep story</p><details id="privacy">Keep choices</details></main>'
            for _ in range(2):apply_article_links(root);self.assertEqual(page.read_text(),expected)
    def test_public_export_excludes_page_and_discovery(self):
        self.assertFalse((ROOT/'dist'/ROUTE).exists())
        self.assertFalse((ROOT/'.generated/pages'/ROUTE).exists())
        for name in ['about.html','sitemap.xml','llms.txt']:
            path=ROOT/'dist'/name
            if path.exists():self.assertNotIn(ROUTE,path.read_text(),name)
if __name__=='__main__':unittest.main()
