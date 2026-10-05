import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from social_metadata import Page, choose_image, inject, prepare, public_base, robots_text

class SocialMetadataTests(unittest.TestCase):
    def test_poem_art_beats_small_poet_portrait(self):
        page=Page('<img class="poem-poet-portrait" src="assets/face.webp"><figure class="poem-art"><img src="assets/poem.webp" alt="A river"></figure>')
        image,reason=choose_image('poem-1.html',page,{})
        self.assertEqual(image['source'],'assets/poem.webp');self.assertEqual(reason,'poem_illustration')
    def test_text_poem_gets_its_own_edition(self):
        poem=Page('<p class="reader-meta"><a href="issue-4.html">Issue 4</a></p><img class="poem-poet-portrait" src="assets/face.webp">')
        edition=Page('<figure class="edition-cover"><svg><image href="assets/cover.webp" /></svg></figure>')
        image,reason=choose_image('poem-2.html',poem,{'issue-4.html':edition})
        self.assertEqual(image['source'],'assets/cover.webp');self.assertEqual(reason,'text_poem_edition_cover')
    def test_profile_retains_generic_artwork_disclosure(self):
        page=Page('<figure class="editor-portrait author-portrait"><img src="assets/generic.webp" alt="Generic artwork, not a likeness"></figure>')
        image,reason=choose_image('poet-233.html',page,{})
        self.assertEqual(image['alt'],'Generic artwork, not a likeness');self.assertEqual(reason,'poet_portrait')
    def test_navigation_images_are_not_used_as_page_art(self):
        page=Page('<header><img src="assets/logo.png"></header><img src="assets/writers/face.webp">')
        _,reason=choose_image('contact.html',page,{})
        self.assertEqual(reason,'journal_fallback')
    def test_base_handles_current_host_and_future_root(self):
        self.assertEqual(public_base({}),'https://ahimanikya.github.io/kabita-live/')
        self.assertEqual(public_base({'SITE_URL':'https://example.org','SITE_BASE':'/'}),'https://example.org/')
        self.assertEqual(public_base({'SITE_URL':'https://example.org','SITE_BASE':'journal'}),'https://example.org/journal/')
        with self.assertRaises(ValueError):public_base({'SITE_URL':'example.org'})
    def test_static_tags_escaped_unique_and_noindex_retained(self):
        entry={'type':'article','title':'A "poem" & <rain>','description':'Some words','url':'https://example.org/poem.html','image_url':'https://example.org/image.jpg','alt':'Rain'}
        text='<head><meta name="robots" content="noindex,nofollow"></head><body>Original verse</body>'
        once=inject(text,entry); twice=inject(once,entry)
        self.assertEqual(once,twice);self.assertEqual(once.count('property="og:image"'),1)
        self.assertIn('&quot;poem&quot; &amp; &lt;rain&gt;',once);self.assertIn('noindex,nofollow',once)
        self.assertIn('<body>Original verse</body>',once)
    def test_changed_source_changes_cache_key(self):
        with TemporaryDirectory() as tmp:
            root=Path(tmp);(root/'assets').mkdir(); source=root/'assets/art.png'; source.write_bytes(b'original')
            (root/'poem-1.html').write_text('<title>Test</title><figure class="poem-art"><img src="assets/art.png"></figure>')
            before=prepare(root,['poem-1.html'],{})['poem-1.html'];source.write_bytes(b'revision')
            after=prepare(root,['poem-1.html'],{})['poem-1.html'];self.assertNotEqual(before['asset'],after['asset'])
            self.assertTrue(before['image_url'].startswith('https://ahimanikya.github.io/kabita-live/assets/social/'))
    def test_preview_does_not_enable_general_crawling(self):
        text=robots_text(False,'/kabita-live/');self.assertTrue(text.endswith('User-agent: *\nDisallow: /\n'))
        self.assertIn('User-agent: facebookexternalhit\nAllow: /kabita-live/\nDisallow: /',text)
        self.assertEqual(robots_text(True),'User-agent: *\nAllow: /\n')

if __name__=='__main__':unittest.main()
