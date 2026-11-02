import hashlib,json,unittest
from pathlib import Path
SITE=Path(__file__).resolve().parents[1]
ROOT=SITE.parents[2]
class RetiredTranslations(unittest.TestCase):
    def test_archived_material_is_exact_and_outside_site(self):
        archive=ROOT/'kb/history/retired-poem-translations-2026-11-03'
        for item in json.loads((archive/'manifest.json').read_text()):
            saved=ROOT/item['archive']
            self.assertEqual(hashlib.sha256(saved.read_bytes()).hexdigest(),item['sha256'])
            if item['source'].startswith('projects/site/'):
                self.assertFalse((ROOT/item['source']).exists())
    def test_public_export_contains_no_retired_translation_data(self):
        dist=SITE/'dist'
        self.assertTrue(dist.is_dir(),'Build before checking public export')
        self.assertFalse((dist/'translation-review.html').exists())
        for name in ['poem-translations.json','translation-review.json','translation_review.py']:
            self.assertFalse(list(dist.rglob(name)))
