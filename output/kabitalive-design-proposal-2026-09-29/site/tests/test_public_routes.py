import sys, unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from public_routes import is_reader_page

class PublicationBoundary(unittest.TestCase):
    def test_development_pages_never_become_reader_pages(self):
        for name in ['design-system-review.html','all-pages.html','poem-final-check.html',
                     'poet-profile-review-257.html','homepage-polish-current.html',
                     'new-review.html','new-prototype.html','credits-content.html','reviews.html','review-10.html']:
            with self.subTest(name=name): self.assertFalse(is_reader_page(name))
    def test_reader_families_and_explicit_review_exception(self):
        for name in ['index.html','poem-809.html','poet-82.html','issue-48.html','archive-2026.html',
                     'poem-dokana.html','translation-review.html']:
            with self.subTest(name=name): self.assertTrue(is_reader_page(name))
