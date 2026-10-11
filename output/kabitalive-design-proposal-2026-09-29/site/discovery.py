"""Search discovery for public reader pages; independent of editorial certification."""
import html
import json
import re
from html.parser import HTMLParser
from urllib.parse import urljoin, urlsplit
from xml.etree import ElementTree as ET

VOID = {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}

class ReaderPage(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.stack=[]; self.heading=[]; self.authors=[]; self.language='en'; self.redirect=False
        self.feed(text)
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if tag=='meta' and a.get('http-equiv','').lower()=='refresh': self.redirect=True
        if a.get('id')=='experience-verse': self.language=a.get('lang','en')
        if tag not in VOID: self.stack.append((tag,a))
    def handle_endtag(self, tag):
        for i in range(len(self.stack)-1,-1,-1):
            if self.stack[i][0]==tag: del self.stack[i:]; break
    def handle_data(self, data):
        if any(t=='h1' for t,a in self.stack): self.heading.append(data)
        if any('poem-byline' in a.get('class','').split() for t,a in self.stack):
            anchor=next((a for t,a in reversed(self.stack) if t=='a'),None)
            if anchor and re.fullmatch(r'(?:poet|editor)-[\w-]+\.html',anchor.get('href','')):
                self.authors.append((anchor['href'],data))

def eligible(name, entry, page, status):
    if name in {'404.html','search.html','contact.html','submit.html','translation-review.html'} or page.redirect: return False
    if entry.get('canonical_url',entry['url']) != entry['url']: return False
    held=set(status.get('archived_poem_records',[])+status.get('unassigned_poems',[])+status.get('missing_author_names',[]))
    match=re.fullmatch(r'poem-(\d+)\.html',name)
    return not (match and int(match[1]) in held)

def safe_json(value):
    return json.dumps(value,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c').replace('>','\\u003e').replace('&','\\u0026')

def enrich(text, name, entry, status, enabled):
    """Use the same HTML for readers and crawlers; never fabricate dates or credits."""
    page=ReaderPage(text)
    indexable=enabled and eligible(name,entry,page,status)
    text=re.sub(r'<!-- discovery:start -->.*?<!-- discovery:end -->','',text,flags=re.S)
    text=re.sub(r'''<meta\b(?=[^>]*\bname\s*=\s*["']robots["'])[^>]*>''','',text,flags=re.I)
    robots='index,follow,max-image-preview:large' if indexable else 'noindex,follow'
    if not enabled: robots='noindex,nofollow'
    tags=f'<meta name="robots" content="{robots}">'
    if indexable:
        url=entry['canonical_url']; base=urljoin(url,'./')
        title=entry['title'].removesuffix(' · Kabita Live')
        heading=' '.join(''.join(page.heading).split())
        webpage={'@type':'WebPage','@id':url+'#webpage','url':url,'name':title,
                 'description':entry['description'],'isPartOf':{'@id':base+'#website'},
                 'primaryImageOfPage':{'@type':'ImageObject','url':entry['image_url']}}
        graph=[{'@type':'WebSite','@id':base+'#website','url':base,'name':'Kabita Live',
                'inLanguage':['or','hi','en']},webpage]
        if name.startswith('poem-'):
            work={'@type':'CreativeWork','@id':url+'#poem','url':url,'name':heading or title,
                  'genre':'Poetry','inLanguage':page.language,'mainEntityOfPage':{'@id':url+'#webpage'}}
            authors={}
            for href,label in page.authors: authors[href]=authors.get(href,'')+label
            if authors: work['author']=[{'@type':'Person','name':' '.join(label.split()),'url':urljoin(url,href)} for href,label in authors.items()]
            webpage['mainEntity']={'@id':url+'#poem'}; graph.append(work)
        elif name.startswith(('poet-','editor-')):
            webpage['@type']='ProfilePage'
            webpage['mainEntity']={'@type':'Person','name':heading or title,'url':url}
        elif name.startswith(('issue-','archive')) or name in {'poems.html','poets.html'}:
            webpage['@type']='CollectionPage'
        tags+='<script type="application/ld+json">'+safe_json({'@context':'https://schema.org','@graph':graph})+'</script>'
    return text.replace('</head>','<!-- discovery:start -->'+tags+'<!-- discovery:end --></head>',1),indexable

def crawler_policy(base, training=False):
    parts=urlsplit(base)
    if parts.scheme!='https' or not parts.netloc: raise ValueError('Discovery requires an HTTPS origin')
    # robots.txt is a voluntary crawl policy, never an authentication or rate limit.
    text='# Public reading is open to search and citation. Forms are not crawl targets.\n'
    if not training:
        for bot in ['GPTBot','ClaudeBot','Google-Extended','CCBot']:
            text+=f'User-agent: {bot}\nDisallow: /\n\n'
    text+='User-agent: *\nAllow: /\n\nSitemap: '+base+'sitemap.xml\n'
    return text

def write_discovery(root, entries, base, training=False):
    ET.register_namespace('','http://www.sitemaps.org/schemas/sitemap/0.9')
    tree=ET.Element('{http://www.sitemaps.org/schemas/sitemap/0.9}urlset')
    for url in sorted({e['canonical_url'] for e in entries.values()}):
        node=ET.SubElement(tree,'{http://www.sitemaps.org/schemas/sitemap/0.9}url')
        ET.SubElement(node,'{http://www.sitemaps.org/schemas/sitemap/0.9}loc').text=url
    (root/'sitemap.xml').write_bytes(ET.tostring(tree,encoding='utf-8',xml_declaration=True))
    (root/'robots.txt').write_text(crawler_policy(base,training))
    lines=['# Kabita Live','', '> A monthly poetry journal in Odia, Hindi and English.','',
           '## Reading and citation','',
           'Use each page’s canonical URL. Credit the named poet and any named translator. Preserve original language, line breaks and stanza boundaries when quoting.',
           'Consult the original poem and its visible attribution alongside additional language versions. Poetry belongs to its respective authors; this guide does not grant republication or training rights.',
           'This file is a navigation aid. The linked HTML pages are authoritative; no login or JavaScript is required to read their original text.','', '## Journal','']
    for name,label in [('index.html','Home'),('poems.html','Poems'),('poets.html','Poets'),('archive.html','Edition archive'),('editorial-team.html','Editors'),('about.html','Our story and credits')]:
        if name in entries: lines.append(f'- [{label}]({entries[name]["canonical_url"]})')
    lines+=['','## Editions','']
    for name in sorted((n for n in entries if re.fullmatch(r'issue-\d+\.html',n)),key=lambda n:int(n[6:-5]),reverse=True):
        e=entries[name]; label=e['title'].removesuffix(' · Kabita Live').replace('[','').replace(']','')
        lines.append(f'- [{label}]({e["canonical_url"]})')
    lines+=['','## Complete public URL catalogue','',f'- [XML sitemap]({base}sitemap.xml)','']
    (root/'llms.txt').write_text('\n'.join(lines))
