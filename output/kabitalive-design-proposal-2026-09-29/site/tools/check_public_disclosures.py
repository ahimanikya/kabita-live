"""Check exported reader copy; AI production disclosures belong in Our Story."""
import argparse
import html
import json
import re
from html.parser import HTMLParser
from pathlib import Path

LABEL = re.compile(
    r'\bAI[\s\u2010-\u2015-]+(?:generated|created|assisted|assistance|adaptation|assistants?|researchers?)\b'
    r'|\bAI\s+assists?\s+with\b'
    r'|\b(?:prepared|drafted|written|created|generated|produced|developed|researched|designed|translated)'
    r'\s+(?:with|by|using)\s+(?:an?\s+)?(?:AI|artificial intelligence|ChatGPT|OpenAI)\b', re.I)


def strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, list):
        for item in value:
            yield from strings(item)
    elif isinstance(value, dict):
        for item in value.values():
            yield from strings(item)


class ReaderCopy(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []
        self.attributes = []
        self.suppressed = None
        self.json_script = False
        self.script_parts = []
        self.central = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in ('script', 'style'):
            self.suppressed = tag
            self.json_script = tag == 'script' and attrs.get('type', '').lower() in ('application/json', 'application/ld+json')
            self.script_parts = []
            return
        if self.suppressed:
            return
        if tag == 'section' and attrs.get('id') == 'creative-process':
            self.central = True
        for key in ('alt', 'title', 'aria-label', 'aria-description', 'placeholder', 'content'):
            if attrs.get(key):
                self.attributes.append(attrs[key])
        if tag in ('p', 'div', 'section', 'br', 'li', 'h1', 'h2', 'h3'):
            self.parts.append(' ')

    def handle_endtag(self, tag):
        if tag == self.suppressed:
            if self.json_script:
                self.attributes.extend(strings(json.loads(''.join(self.script_parts))))
            self.suppressed = None
            self.json_script = False
        elif not self.suppressed and tag in ('p', 'div', 'section', 'li', 'h1', 'h2', 'h3'):
            self.parts.append(' ')

    def handle_data(self, data):
        if self.suppressed:
            if self.json_script:
                self.script_parts.append(data)
        else:
            self.parts.append(data)


def labels(text):
    return sorted(set(m.group() for m in LABEL.finditer(html.unescape(text))))


def audit(root):
    root = Path(root)
    violations = []
    count = 0
    central = False
    for path in sorted(root.rglob('*')):
        if not path.is_file() or path.suffix.lower() not in ('.html', '.json', '.txt', '.md'):
            continue
        if 'pagefind' in path.relative_to(root).parts:
            continue  # Derived search index; its input pages are checked.
        count += 1
        route = path.relative_to(root).as_posix()
        try:
            text = path.read_text(encoding='utf-8')
            if path.suffix.lower() == '.html':
                parser = ReaderCopy()
                parser.feed(text)
                content = [''.join(parser.parts), *parser.attributes]
                if route == 'about.html':
                    central = parser.central and 'How we use AI' in content[0] and 'AI assists with' in content[0]
                    continue
            elif path.suffix.lower() == '.json':
                content = list(strings(json.loads(text)))
            else:
                content = [text]
            found = sorted(set(match for value in content for match in labels(value)))
            if found:
                violations.append({'path': route, 'labels': found})
        except (ValueError, UnicodeError) as error:
            violations.append({'path': route, 'error': str(error)})
    if not central:
        violations.append({'path': 'about.html', 'error': 'Central creative-process disclosure is missing or empty.'})
    return {'files_checked': count, 'violations': violations}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root', nargs='?', default='dist')
    args = parser.parse_args()
    result = audit(args.root)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(bool(result['violations']))
