#!/usr/bin/env python3
"""Audit the exported website's shared Ink & Voice contract.

Checks every route, not just a sample. Browser evidence remains necessary for
computed styles, interaction states and visual quality. Historical cover art
and KB design studies are outside the website-theme contract.
"""
import argparse
from collections import Counter
from hashlib import sha256
from html.parser import HTMLParser
import json
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.scripts, self.headers, self.body = [], [], [], {}

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'link':
            self.links.append(attrs)
        elif tag == 'script' and attrs.get('src'):
            self.scripts.append(attrs['src'])
        elif tag == 'body':
            self.body = attrs
        elif tag == 'header' and 'site-header' in attrs.get('class', '').split():
            self.headers.append(attrs)


def audit(site):
    errors, routes, styles, families = [], [], Counter(), Counter()
    logo = 'assets/kabita-live-symbol-ink-voice.svg'
    if not (site / logo).exists():
        return {'result': 'FAIL', 'errors': ['Current logo missing'], 'pages': 0}
    logo_hash = sha256((site / logo).read_bytes()).hexdigest()[:12]
    for path in sorted(site.glob('*.html')):
        text = path.read_text()
        page = Page()
        page.feed(text)
        css = [x['href'] for x in page.links if x.get('rel') == 'stylesheet']
        css_paths = [urlsplit(x).path for x in css]
        issues = []
        if 'site-theme' not in page.body.get('class', '').split():
            issues.append('Missing shared theme class')
        if css_paths.count('assets/ink-voice.css') != 1:
            issues.append('Expected exactly one Ink & Voice stylesheet')
        if len(css_paths) != len(set(css_paths)):
            issues.append('Duplicate stylesheet inclusion')
        icons = [x for x in page.links if x.get('rel') == 'icon']
        if len(icons) != 1 or icons[0].get('href') != f'{logo}?v={logo_hash}' or icons[0].get('type') != 'image/svg+xml':
            issues.append('Favicon differs from current versioned logo')
        if 'assets/appearance.js' not in page.scripts:
            issues.append('Shared saved/system theme support missing')
        if path.name != 'search.html' and len(page.headers) != 1:
            issues.append('Expected one shared header')
        if path.name != 'search.html' and 'class="brand-symbol"' not in text:
            issues.append('Current theme-aware masthead symbol missing')
        for asset in css_paths + [urlsplit(x).path for x in page.scripts]:
            if asset and not urlsplit(asset).scheme and not (site / asset).is_file():
                issues.append(f'Missing asset {asset}')
        if 'assets/kabita-live-symbol.svg' in text:
            issues.append('Historical logo still referenced by page markup')
        styles.update(css_paths)
        family = 'poem' if 'poem-page' in page.body.get('class', '') else 'profile' if path.name.startswith('poet-') else 'edition' if path.name.startswith('issue-') else 'other'
        families[family] += 1
        routes.append({'route': path.name, 'family': family, 'styles': css_paths, 'issues': issues})
        errors.extend(f'{path.name}: {issue}' for issue in issues)
    for font in ['Newsreader-Variable.woff2', 'Newsreader-Italic-Variable.woff2', 'Literata-Variable.woff2', 'Literata-Italic-Variable.woff2', 'NotoSerifOriya-Variable.woff2', 'TiroDevanagariHindi-Regular.woff2']:
        if not (site / 'assets/fonts' / font).exists():
            errors.append(f'Missing approved local font {font}')
    return {'result': 'FAIL' if errors else 'PASS', 'pages': len(routes), 'families': dict(families), 'stylesheets': dict(styles), 'errors': errors, 'routes': routes,
            'limits': 'Static export contract. Computed type/colour, modal states, responsive layout and artwork exceptions require browser review.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--site', type=Path, default=ROOT / 'projects/site/dist')
    parser.add_argument('--out', type=Path)
    args = parser.parse_args()
    result = audit(args.site)
    if args.out:
        args.out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k not in ('routes', 'stylesheets')}, ensure_ascii=False, indent=2))
    raise SystemExit(bool(result['errors']))
