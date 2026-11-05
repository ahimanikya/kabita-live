import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location('check_audience_pages', Path(__file__).resolve().parents[1] / 'check_audience_pages.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class AudienceCatalogueTests(unittest.TestCase):
    def test_missing_new_issue_detected_and_history_preserved(self):
        old = {'/issue-48.html': 'October', '/poem-old.html': 'Earlier poem'}
        public = {'/issue-48.html': 'October corrected title', '/issue-49.html': 'November', '/poem-835.html': 'New poem'}
        missing, merged = module.reconcile(old, public)
        self.assertEqual(missing, ['/issue-49.html', '/poem-835.html'])
        self.assertEqual(merged['/poem-old.html'], 'Earlier poem')
        self.assertEqual(merged['/issue-48.html'], 'October corrected title')
        self.assertEqual(module.reconcile(merged, public)[0], [])

    def test_private_unbounded_and_noncanonical_paths_rejected(self):
        for path in ['/editor-workspace.html', '/author-proof.html', '/monthly-review.html', '/poem-1.html?email=x', '/issue-49.html#editorial', 'https://example.org/issue-49.html', '/poem-../private.html']:
            with self.subTest(path=path), self.assertRaises(ValueError):
                module.validate_pages({path: 'Title'})

    def test_invalid_titles_and_empty_catalogue_rejected(self):
        for pages in [{}, [], {'/issue-49.html': ''}, {'/issue-49.html': 1}, {'/issue-49.html': 'private\nvalue'}]:
            with self.subTest(pages=pages), self.assertRaises(ValueError):
                module.validate_pages(pages)

if __name__ == '__main__':
    unittest.main()
