import json, struct, unittest
from pathlib import Path
from urllib.parse import urljoin, urlparse
from html.parser import HTMLParser

SITE = Path(__file__).resolve().parents[1]
class Links(HTMLParser):
    def __init__(self, source):
        super().__init__(); self.links=[]; self.feed(source)
    def handle_starttag(self, tag, attrs):
        if tag=='link': self.links.append(dict(attrs))

class EditorApp(unittest.TestCase):
    def test_manifest_starts_in_studio_on_custom_domain_and_project_path(self):
        manifest=json.loads((SITE/'assets/editor-app.webmanifest').read_text())
        self.assertEqual(manifest['display'],'standalone')
        # Omitted id defaults to the resolved, query-free start_url. Relative id
        # values resolve from the origin and would break project-base identity.
        self.assertNotIn('id',manifest)
        self.assertFalse(urlparse(manifest['start_url']).query)
        for base in ['https://example.com/','https://example.github.io/journal/']:
            location=base+'assets/editor-app.webmanifest'
            self.assertEqual(urljoin(location,manifest['start_url']),base+'editor-workspace.html')
            self.assertEqual(urljoin(location,manifest['scope']),base+'editor-workspace.html')
            for icon in manifest['icons']:
                self.assertEqual(urljoin(location,icon['src']),base+'assets/'+icon['src'])
    def test_icons_are_real_pngs_at_declared_sizes(self):
        manifest=json.loads((SITE/'assets/editor-app.webmanifest').read_text())
        sizes={int(i['sizes'].split('x')[0]) for i in manifest['icons']}
        self.assertTrue({192,512}.issubset(sizes))
        for size in sizes|{180}:
            data=(SITE/f'assets/editor-app-{size}.png').read_bytes()
            self.assertEqual(data[:8],b'\x89PNG\r\n\x1a\n')
            self.assertEqual(struct.unpack('>II',data[16:24]),(size,size))
    def test_template_has_manifest_and_ios_icon(self):
        links=Links((SITE/'data/editor-workspace.html.template').read_text()).links
        self.assertEqual([l['href'] for l in links if l.get('rel')=='manifest'],['assets/editor-app.webmanifest'])
        self.assertEqual([l['href'] for l in links if l.get('rel')=='apple-touch-icon'],['assets/editor-app-180.png'])
    def test_public_export_contains_manifest_resources(self):
        export=SITE/'.public'
        self.assertTrue(export.is_dir(),'Run python3 build.py and build-public.py first')
        manifest=json.loads((export/'assets/editor-app.webmanifest').read_text())
        for icon in manifest['icons']:
            self.assertEqual((export/'assets'/icon['src']).read_bytes(),(SITE/'assets'/icon['src']).read_bytes())
        for name in ['editor-app-180.png','editor-install.mjs','editor-install.css']:
            self.assertEqual((export/'assets'/name).read_bytes(),(SITE/'assets'/name).read_bytes())
        self.assertIn('assets/editor-app.webmanifest',(SITE/'.generated/pages/editor-workspace.html').read_text())
