"""The approved reference publishes only rendered specimens, never its KB tree."""
import base64
import hashlib
import json
import re
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from html import unescape
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from component_library import render_component_library, ROUTE
from public_routes import is_reader_page

SITE=Path(__file__).resolve().parents[1]
PROJECT=next(p for p in SITE.parents if (p/'utkal.config.json').is_file())

class ComponentReferenceExport(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        project=Path(self.temp.name);(project/'utkal.config.json').write_text('{}')
        self.site=project/'site';self.site.mkdir();(self.site/'assets').mkdir()
        self.library=project/'kb/artifacts/design/component-library';self.library.mkdir(parents=True)
        for name in ['build.py','template.html','library.css','library.js']:
            shutil.copyfile(PROJECT/'kb/artifacts/design/component-library'/name,self.library/name)
        for name in ['index.html','poets.html','poem-835.html','assets/kabita-live-symbol-ink-voice.svg']:
            shutil.copyfile(SITE/name,self.site/name)

    def test_public_render_ignores_preview_alias_and_needs_no_manifest(self):
        secret=self.library/'private-review.txt';secret.write_text('PRIVATE REVIEW DO NOT EXPORT')
        (self.site/ROUTE).symlink_to(secret)
        html=render_component_library(self.site)
        self.assertNotIn('PRIVATE REVIEW',html)
        self.assertNotIn('kb/',html)
        self.assertNotIn('127.0.0.1',html)
        self.assertNotIn('LOCAL DESIGN REFERENCE',html)
        self.assertIn('About this reference',html)
        self.assertIn('data-pagefind-ignore="all"',html)
        self.assertIn('content="noindex,nofollow"',html)
        self.assertFalse(is_reader_page(ROUTE))
        self.assertEqual(secret.read_text(),'PRIVATE REVIEW DO NOT EXPORT')
        self.assertFalse((self.library/'index.html').exists())
        self.assertFalse((self.library/'manifest.json').exists())

    def test_public_script_hash_and_no_service_boundary_survive_copy_changes(self):
        html=render_component_library(self.site)
        script=re.search(r'<script>(.*?)</script>',html,re.S)[1]
        digest=base64.b64encode(hashlib.sha256(script.encode()).digest()).decode()
        self.assertIn('sha256-'+digest,html)
        self.assertIn("connect-src 'none'",unescape(html))
        self.assertIn("form-action 'none'",unescape(html))
        self.assertEqual(re.findall(r'<script[^>]+src="([^"]+)"',html),['assets/author-profile.js'])
        self.assertNotIn('runtime-config.json',html)
        self.assertIn('sandbox="allow-same-origin"',html)
        self.assertIn('sizes="any"',html)
        self.assertIn('assets/kabita-live-symbol-ink-voice.svg?v=',html)

    def test_missing_canonical_source_fails_closed(self):
        (self.library/'build.py').unlink()
        with self.assertRaisesRegex(ValueError,'source missing'):
            render_component_library(self.site)

if __name__=='__main__':unittest.main()
