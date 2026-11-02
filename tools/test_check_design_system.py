"""Regression checks for reader and explicitly approved private-shell contracts."""
import tempfile
import unittest
from pathlib import Path
from hashlib import sha256
from check_design_system import audit


class DesignContractTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.site = Path(self.temp.name)
        assets = self.site / 'assets'
        (assets / 'fonts').mkdir(parents=True)
        for name in ['ink-voice.css', 'editor-workspace.css', 'editorial-desk.css', 'appearance.js']:
            (assets / name).touch()
        for name in ['Newsreader-Variable', 'Newsreader-Italic-Variable', 'Literata-Variable', 'Literata-Italic-Variable', 'NotoSerifOriya-Variable', 'TiroDevanagariHindi-Regular']:
            (assets / 'fonts' / (name + '.woff2')).touch()
        logo = assets / 'kabita-live-symbol-ink-voice.svg'
        logo.write_text('<svg/>')
        key = sha256(logo.read_bytes()).hexdigest()[:12]
        self.icon = f'<link rel="icon" type="image/svg+xml" sizes="any" href="assets/{logo.name}?v={key}">'
        self.reader = self.icon + '<link rel="stylesheet" href="assets/ink-voice.css"><script src="assets/appearance.js"></script><body class="site-theme"><header class="site-header"><svg class="brand-symbol"></svg></header></body>'
        self.studio = self.icon + '<meta name="robots" content="noindex,nofollow"><link rel="stylesheet" href="assets/editor-workspace.css"><link rel="stylesheet" href="assets/editorial-desk.css"><body></body>'

    def test_empty_export_fails_even_when_assets_exist(self):
        self.assertIn('No exported HTML routes found', audit(self.site)['errors'])

    def test_reader_and_named_studio_have_distinct_checked_contracts(self):
        (self.site / 'index.html').write_text(self.reader)
        (self.site / 'author-proof.html').write_text(self.studio)
        result = audit(self.site)
        self.assertEqual(result['result'], 'PASS', result['errors'])
        self.assertEqual(result['families'], {'studio': 1, 'other': 1})

    def test_new_route_cannot_inherit_studio_exemption(self):
        (self.site / 'other-editor.html').write_text(self.studio)
        self.assertTrue(any('Missing shared theme class' in e for e in audit(self.site)['errors']))

    def test_studio_does_not_bypass_brand_privacy_or_asset_checks(self):
        for missing, expected in [(self.icon, 'Favicon'), ('noindex,', 'missing noindex'), ('<link rel="stylesheet" href="assets/editor-workspace.css">', 'Studio stylesheet')]:
            with self.subTest(missing=missing):
                (self.site / 'author-proof.html').write_text(self.studio.replace(missing, ''))
                self.assertTrue(any(expected in e for e in audit(self.site)['errors']))
        (self.site / 'author-proof.html').write_text(self.studio)
        (self.site / 'assets/editorial-desk.css').unlink()
        self.assertTrue(any('Missing asset assets/editorial-desk.css' in e for e in audit(self.site)['errors']))

    def test_reader_theme_regression_still_fails(self):
        (self.site / 'index.html').write_text(self.reader.replace('site-theme', ''))
        self.assertTrue(any('Missing shared theme class' in e for e in audit(self.site)['errors']))

    def test_component_reference_has_explicit_safe_shell_contract(self):
        (self.site/'assets/author-profile.js').touch()
        reference = self.reader.replace('site-theme', 'site-theme lib-page').replace('assets/appearance.js', 'assets/author-profile.js')
        reference += '<meta name="robots" content="noindex,nofollow"><html data-pagefind-ignore="all"><meta http-equiv="Content-Security-Policy" content="connect-src \'none\'; form-action \'none\'">'
        reference += ''.join(f'<button data-mode="{mode}"></button>' for mode in ['light','dark','system'])
        path = self.site/'component-library.html'; path.write_text(reference)
        self.assertEqual(audit(self.site)['result'], 'PASS')
        for original, replacement, expected in [('noindex,nofollow','index,follow','noindex'), ('connect-src', 'other-src', 'simulation boundary'), ('data-mode="dark"', 'data-mode="other"', 'theme controls')]:
            with self.subTest(expected=expected):
                path.write_text(reference.replace(original,replacement))
                self.assertTrue(any(expected in e for e in audit(self.site)['errors']))


if __name__ == '__main__':
    unittest.main()
