"""Catch missing transitive modules in the actual public build."""
import re
import unittest
from pathlib import Path


class ToshaliExportTests(unittest.TestCase):
    def test_public_modules_and_dependencies_are_exported(self):
        public = Path(__file__).resolve().parents[1] / 'dist'
        pending = ['assets/toshali-invitation.mjs', 'assets/toshali-review.mjs']
        checked = set()
        while pending:
            relative = pending.pop()
            if relative in checked:
                continue
            checked.add(relative)
            path = public / relative
            self.assertTrue(path.is_file(), f'Missing public module: {relative}')
            for ref in re.findall(r'''(?:from\s*|import\s*\(\s*)['"](\./[^'"]+)['"]''', path.read_text()):
                pending.append(str(Path(relative).parent / ref))
        self.assertIn('assets/toshali-policy.mjs', checked)
        self.assertIn('assets/toshali-review-service.js', checked)

