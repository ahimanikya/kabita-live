"""Publication boundary regression checks for additional website translations."""
import json
from pathlib import Path
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from original_only import check_reader, OriginalOnlyHTML
from poem_reader import render_reader


class OriginalOnlyTests(unittest.TestCase):
    def test_submitted_translation_is_preserved_as_source(self):
        source = {'id': 999999, 'language': 'en', 'title': 'A submitted work',
                  'text': 'Line one\nLine two', 'stanzas': [['Line one', 'Line two']]}
        html = render_reader(source)
        payload = json.loads(html.split('id="reading-data">', 1)[1].split('</script>', 1)[0])
        self.assertEqual(payload['variants']['en']['stanzas'], source['stanzas'])
        self.assertEqual(set(payload['variants']), {'en'})
        OriginalOnlyHTML('fixture').feed(html)

    def test_translated_reader_asset_is_rejected(self):
        with self.assertRaisesRegex(ValueError, 'submitted language'):
            check_reader({'poems': [{'source_language':'or', 'variants': {'or':{}, 'en':{}}}]}, 'fixture')

    def test_translated_embedded_payload_is_rejected(self):
        data = {'source_language':'hi', 'variants': {'hi':{}, 'en':{}}}
        with self.assertRaises(ValueError):
            OriginalOnlyHTML('fixture').feed('<script id="focus-entry-data" type="application/json">'+json.dumps(data)+'</script>')

    def test_translation_controls_and_hidden_titles_are_rejected(self):
        for html in ['<button data-focus-language="en">A</button>',
                     '<div data-lang="or" data-reading-titles=\'{"or":"x","en":"y"}\'></div>',
                     '<p class="excerpt-translation">Removed excerpt</p>']:
            with self.subTest(html=html), self.assertRaises(ValueError):
                OriginalOnlyHTML('fixture').feed(html)


if __name__ == '__main__':
    unittest.main()
