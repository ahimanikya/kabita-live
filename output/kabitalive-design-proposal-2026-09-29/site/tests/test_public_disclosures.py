import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location('disclosures', Path(__file__).parents[1] / 'tools/check_public_disclosures.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class PublicDisclosures(unittest.TestCase):
    def check(self, filename, content):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'about.html').write_text('<section id="creative-process"><h2>How we use AI</h2><p>AI assists with artwork.</p></section>')
            (root / filename).write_text(content)
            return module.audit(root)['violations']

    def test_production_copy_and_inline_markup(self):
        for text in ['AI-generated picture', 'AI&#8209;assisted text', 'AI <em>created</em> illustration', 'Prepared with artificial intelligence', 'Translated using ChatGPT']:
            with self.subTest(text=text):
                self.assertTrue(self.check('poem.html', '<p>' + text + '</p>'))

    def test_metadata_and_accessible_descriptions(self):
        self.assertTrue(self.check('poem.html', '<meta property="og:image:alt" content="AI-created scene"><img alt="AI-assisted portrait">'))

    def test_external_reader_data(self):
        self.assertTrue(self.check('reader.json', json.dumps({'illustration': {'alt': 'AI-created scene'}})))

    def test_embedded_reader_data(self):
        self.assertTrue(self.check('poem.html', '<script type="application/json">{"credit":"AI-assisted translation"}</script>'))

    def test_poetry_and_topic_discussion_are_preserved(self):
        self.assertFalse(self.check('poem.html', '<p>How far can AI advance?</p><p>What people teach AI about a language</p>'))

    def test_code_and_comments_are_not_reader_copy(self):
        self.assertFalse(self.check('poem.html', '<!-- AI-generated --><script>const example="AI-assisted";</script><p>Illustration</p>'))

    def test_central_disclosure_is_required(self):
        self.assertTrue(self.check('about.html', '<h1>Our Story</h1>'))

    def test_central_disclosure_allowed(self):
        self.assertFalse(self.check('article.html', '<p>Artistic adaptation of a supplied photograph.</p>'))

    def test_plain_text_download(self):
        self.assertTrue(self.check('reading.txt', 'Written by AI'))

    def test_invalid_reader_json_fails(self):
        self.assertTrue(self.check('reader.json', '{broken'))
