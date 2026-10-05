"""Deterministic, server-rendered sharing metadata from each page's actual artwork."""
import hashlib
import html
import json
import os
import re
from html.parser import HTMLParser
from urllib.parse import urlsplit

FALLBACK = 'assets/home/life-after-rain-poetic-natural.webp'
VOID = {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr','image'}

class Page(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.stack=[]; self.images=[]; self.links=[]; self.title=[]; self.byline=[]
        self.feed(text)
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        classes=set(' '.join(d.get('class','') for _,d in self.stack).split()) | set(a.get('class','').split())
        if tag in {'img','image'}:
            src=a.get('src') or a.get('href') or a.get('xlink:href','')
            if src.startswith('assets/') and src.lower().endswith(('.webp','.jpg','.jpeg','.png')):
                self.images.append({'source':src,'alt':a.get('alt',''),'classes':classes})
        if tag=='a': self.links.append((a.get('href',''),classes))
        if tag not in VOID:self.stack.append((tag,a))
    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag,attrs)
        if tag not in VOID:self.handle_endtag(tag)
    def handle_endtag(self,tag):
        for n in range(len(self.stack)-1,-1,-1):
            if self.stack[n][0]==tag:
                del self.stack[n:];break
    def handle_data(self,data):
        if any(t=='title' for t,_ in self.stack):self.title.append(data)
        if any('poem-byline' in a.get('class','').split() for _,a in self.stack):self.byline.append(data)


def clean(value): return ' '.join(value.split())

def choose_image(name, page, pages):
    def match(classes):return next((i for i in page.images if i['classes'] & classes),None)
    reason='page_artwork'; image=None
    if name.startswith('poem-'):
        image=match({'poem-art'})
        reason='poem_illustration'
        if not image:
            issue=next((href for href,classes in page.links if re.fullmatch(r'issue-\d+\.html',href) and 'reader-meta' in classes),None)
            if issue and issue in pages:
                image=next((i for i in pages[issue].images if 'edition-cover' in i['classes']),None)
                reason='text_poem_edition_cover'
    elif name.startswith(('poet-','editor-')) or name=='ahimanikya-satapathy.html':
        image=match({'author-portrait','editor-portrait'})
        reason='poet_portrait'
    elif re.fullmatch(r'issue-\d+\.html',name):
        image=match({'edition-cover'}); reason='edition_cover'
    elif name=='index.html':
        image=next((i for i in page.images if i['source']==FALLBACK),None); reason='stable_homepage'
    else:
        image=next((i for i in page.images if i['source'].startswith(('assets/section-art/','assets/home/'))),None)
    if not image:
        image={'source':FALLBACK,'alt':'An imagined rain-washed courtyard beside an indigo doorway, opening onto a pond and green fields.'}
        reason='journal_fallback'
    return image,reason


def public_base(environ):
    origin=environ.get('SITE_URL','https://ahimanikya.github.io').rstrip('/')
    parts=urlsplit(origin)
    if parts.scheme not in {'http','https'} or not parts.netloc or parts.path not in {'','/'} or parts.query or parts.fragment:
        raise ValueError('SITE_URL must be an absolute HTTP(S) origin without a path')
    base=environ.get('SITE_BASE','/kabita-live' if 'SITE_URL' not in environ else '/')
    if '?' in base or '#' in base or '..' in base.split('/'):
        raise ValueError('Invalid SITE_BASE')
    return origin+'/'+base.strip('/')+'/' if base.strip('/') else origin+'/'


def inject(text, entry):
    # Idempotent if an already prepared page is passed through this stage again.
    text=re.sub(r'<!-- social-preview:start -->.*?<!-- social-preview:end -->','',text,flags=re.S)
    values=[('property','og:type',entry['type']),('property','og:site_name','Kabita Live'),
            ('property','og:title',entry['title']),('property','og:description',entry['description']),
            ('property','og:url',entry['url']),('property','og:image',entry['image_url']),
            ('property','og:image:type','image/jpeg'),('property','og:image:width','1200'),
            ('property','og:image:height','630'),('property','og:image:alt',entry['alt']),
            ('name','twitter:card','summary_large_image'),('name','twitter:title',entry['title']),
            ('name','twitter:description',entry['description']),('name','twitter:image',entry['image_url']),
            ('name','twitter:image:alt',entry['alt'])]
    tags=''.join(f'<meta {attr}="{key}" content="{html.escape(value,quote=True)}">' for attr,key,value in values)
    tags+=f'<link rel="canonical" href="{html.escape(entry["url"],quote=True)}">'
    return text.replace('</head>','<!-- social-preview:start -->'+tags+'<!-- social-preview:end --></head>',1)


def prepare(root, names, environ=None):
    base=public_base(os.environ if environ is None else environ)
    parsed={name:Page((root/name).read_text()) for name in names}
    entries={}
    for name,page in parsed.items():
        image,reason=choose_image(name,page,parsed)
        source=root/image['source']
        if not source.is_file():raise ValueError('Missing sharing image: '+str(source))
        # Digest protects social caches when an assigned image is revised.
        digest=hashlib.sha256(b'social-jpeg-contain-1200x630-v1\0'+source.read_bytes()).hexdigest()[:20]
        asset='assets/social/'+digest+'.jpg'
        title=clean(''.join(page.title)) or 'Kabita Live'
        short=title.removesuffix(' · Kabita Live')
        if name.startswith('poem-'):
            byline=clean(''.join(page.byline))
            description=f'{short}'+(f' — {byline}' if byline else '')+'. Read the poem on Kabita Live.'
        elif reason=='poet_portrait':description=f'Poetry, biography and contributions by {short} on Kabita Live.'
        elif reason=='edition_cover':description=f'Read {short}: poetry in Odia, Hindi and English.'
        else:description=f'{short} — Kabita Live, a journal of poetry in Odia, Hindi and English.'
        if len(description)>240: description=description[:237].rsplit(' ',1)[0]+'…'
        entries[name]={'title':title,'description':description,'type':'article' if name.startswith('poem-') else 'profile' if reason=='poet_portrait' else 'website','url':base+('' if name=='index.html' else name),'image_url':base+asset,'asset':asset,'source':image['source'],'alt':image['alt'] or f'Artwork accompanying {short}','reason':reason}
    return entries


def robots_text(release=False,base='/'):
    if release:return 'User-agent: *\nAllow: /\n'
    # Sharing access does not remove the general indexing gate or page noindex.
    base='/'+base.strip('/')+'/' if base.strip('/') else '/'
    return ''.join(f'User-agent: {bot}\nAllow: {base}\nDisallow: /\n\n' for bot in ['facebookexternalhit','Twitterbot','LinkedInBot','WhatsApp'])+'User-agent: *\nDisallow: /\n'
