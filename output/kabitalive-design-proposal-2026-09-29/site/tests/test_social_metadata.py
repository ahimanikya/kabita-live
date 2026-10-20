import unittest
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from social_metadata import Page, choose_image, inject, prepare, public_base, robots_text

class SocialMetadataTests(unittest.TestCase):
    def home_fixture(self, root, number=48):
        (root/'content/editions').mkdir(parents=True,exist_ok=True)
        (root/'data').mkdir(exist_ok=True)
        (root/'assets/fonts').mkdir(parents=True,exist_ok=True)
        for name in ['CormorantGaramond-Variable.ttf','NotoSerifOriya-Variable.ttf']:
            (root/'assets/fonts'/name).write_bytes(b'font')
        (root/'assets/current.webp').write_bytes(b'current cover art')
        (root/'content/editions/index.json').write_text(json.dumps([{'number':number},{'number':47}]))
        svg=f'<svg><image href="assets/current.webp"/><text>Issue {number}</text></svg>'
        (root/'data/cover-layout-b.json').write_text(json.dumps({str(number):{'artwork':'assets/current.webp','date':'October 2026','svg':svg}}))
        (root/'index.html').write_text(f'<head><title>Home</title></head><img src="assets/portrait.webp"><div class="ink-current-edition"><div data-cover-edition="{number}"><image href="assets/responsive-copy.webp"/></div></div><div data-cover-edition="47"><image href="assets/older.webp"/></div>')

    def test_home_uses_complete_current_cover_and_updates_on_next_edition(self):
        with TemporaryDirectory() as tmp:
            root=Path(tmp);self.home_fixture(root)
            before=prepare(root,['index.html'],{})['index.html']
            self.assertEqual(before['edition'],48)
            self.assertEqual(before['reason'],'current_edition_front_cover')
            self.assertEqual(before['source'],'assets/current.webp')
            self.assertIn('<text>Issue 48</text>',before['cover_svg'])
            self.assertIn('Issue 48',before['alt'])
            self.home_fixture(root,49)
            after=prepare(root,['index.html'],{'SITE_URL':'https://kabitalive.com'})['index.html']
            self.assertEqual(after['edition'],49)
            self.assertNotEqual(before['asset'],after['asset'])
            self.assertTrue(after['image_url'].startswith('https://kabitalive.com/assets/social/'))
            self.assertEqual(after['url'],'https://kabitalive.com/')

    def test_home_rejects_missing_or_stale_visible_cover_instead_of_generic_fallback(self):
        with TemporaryDirectory() as tmp:
            root=Path(tmp);self.home_fixture(root)
            for markup in ['<img src="assets/home/life-after-rain-poetic-natural.webp">','<div class="ink-current-edition"><div data-cover-edition="47"></div></div>']:
                (root/'index.html').write_text(markup)
                with self.assertRaisesRegex(ValueError,'visible cover'):
                    prepare(root,['index.html'],{})
        with self.assertRaisesRegex(ValueError,'current edition front cover'):
            choose_image('index.html',Page(''),{})

    def test_essay_uses_lead_art_and_supplied_description(self):
        with TemporaryDirectory() as tmp:
            root=Path(tmp);(root/'assets').mkdir()
            (root/'assets/lead.webp').write_bytes(b'lead')
            name='language-essay.html'
            (root/name).write_text('<title>Language essay · Kabita Live</title><meta name="description" content="A supplied essay."><img src="assets/logo.png"><figure class="article-lead"><img src="assets/lead.webp" alt="Readers at a table"></figure><img src="assets/chart.png">')
            result=prepare(root,[name],{})[name]
            self.assertEqual(result['source'],'assets/lead.webp')
            self.assertEqual(result['type'],'article')
            self.assertEqual(result['description'],'A supplied essay.')
            self.assertEqual(result['alt'],'Readers at a table')

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
    def test_alias_canonical_preserved_once_and_injection_idempotent(self):
        with TemporaryDirectory() as tmp:
            root=Path(tmp);(root/'assets/home').mkdir(parents=True)
            (root/'assets/home/life-after-rain-poetic-natural.webp').write_bytes(b'art')
            text='<head><title>Alias</title><link rel="canonical" href="poet-192.html"></head>'
            (root/'poet-224.html').write_text(text)
            entry=prepare(root,['poet-224.html'],{})['poet-224.html']
            self.assertEqual(entry['canonical_url'],'https://ahimanikya.github.io/kabita-live/poet-192.html')
            once=inject(text,entry)
            self.assertEqual(once,inject(once,entry))
            self.assertEqual(once.count('rel="canonical"'),1)
            self.assertIn('href="'+entry['canonical_url']+'"',once)
            self.assertEqual(entry['url'],'https://ahimanikya.github.io/kabita-live/poet-224.html')

    def test_external_source_canonical_rejected(self):
        with TemporaryDirectory() as tmp:
            root=Path(tmp);(root/'assets/home').mkdir(parents=True)
            (root/'assets/home/life-after-rain-poetic-natural.webp').write_bytes(b'art')
            (root/'contact.html').write_text('<head><link rel="canonical" href="https://elsewhere.test/"></head>')
            with self.assertRaisesRegex(ValueError,'Invalid source canonical'):
                prepare(root,['contact.html'],{})

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
