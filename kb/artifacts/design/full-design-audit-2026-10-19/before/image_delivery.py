"""Static, native image delivery: preserve sources, semantics and no-script access."""
import json
import re
from html import escape
from html.parser import HTMLParser

class Tag(HTMLParser):
    def handle_starttag(self, tag, attrs):
        self.attrs = dict(attrs)

def enhance(text, manifest):
    def image(match):
        parser = Tag(); parser.feed(match[0]); a = parser.attrs
        source = a.get('src', '')
        data = manifest.get(source)
        if not data or a.get('class') == 'home-view-fallback':
            return match[0]
        a['decoding'] = 'async'
        a['width'] = a.get('width') or str(data['width'])
        a['height'] = a.get('height') or str(data['height'])
        # Existing art direction and responsive choices take precedence.
        if 'srcset' not in a and '/articles/' not in source:
            width = int(a['width'])
            variants = data['variants']
            if width <= 96:
                variants = [v for v in variants if v['width'] <= 480]
                a['sizes'] = f'{width}px'
            elif '/writers/' in source or '/editors/' in source:
                a['sizes'] = '(max-width:760px) 80vw, 360px'
            else:
                a['sizes'] = '(max-width:760px) calc(100vw - 40px), (max-width:1224px) 45vw, 560px'
            a['srcset'] = ', '.join(f'{v["src"]} {v["width"]}w' for v in variants) + f', {source} {data["width"]}w'
        if int(a['width']) > 96:
            a['class'] = ' '.join(dict.fromkeys((a.get('class','')+' progressive-art').split()))
            # A tiny static image is visible before the full image arrives; no animation.
            a['style'] = a.get('style','').rstrip(';') + f';background-image:url({data["preview"]})'
        return '<img ' + ' '.join(f'{k}="{escape(v or "",quote=True)}"' for k,v in a.items()) + '>'
    text = re.sub(r'<img\b[^>]*>', image, text)
    if 'progressive-art' in text:
        text = text.replace('</head>', '<link rel="stylesheet" href="assets/image-delivery.css?v=1"><script defer src="assets/image-delivery.js?v=1"></script></head>')
    return text

def apply_image_delivery(site):
    manifest = json.loads((site/'data/image-delivery.json').read_text())
    for page in site.glob('*.html'):
        if page.is_symlink(): continue
        text = page.read_text()
        page.write_text(enhance(text,manifest))
