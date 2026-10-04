#!/usr/bin/env python3
"""Validate author identity assets, source biography retention and contribution joins."""
import collections
import hashlib
import json
import html as html_module
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

ROOT=Path(__file__).resolve().parents[1]
SITE=ROOT/'projects/site'

class Profile(HTMLParser):
    def __init__(self,html):
        super().__init__();self.ids=[];self.links=[];self.images=[];self.text=[];self.h1=0;self.contributions=0
        self.feed(html)
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.append(a['id'])
        if tag=='a' and 'href' in a:self.links.append(a['href'])
        if tag=='img':self.images.append(a.get('src',''))
        if tag=='h1':self.h1+=1
        if 'data-contribution' in a:self.contributions+=1
    def handle_data(self,data):self.text.append(data)

def main():
    load=lambda p:json.loads(p.read_text())
    profiles={p['id']:p for p in load(SITE/'data/writer-profiles.json')}
    poems=[d for p in (SITE/'content/editions').glob('*/poem-*.json') for d in [load(p)] if d.get('status')!='archived']
    expected=collections.Counter(p['writer_id'] for p in poems if p['writer_id'])
    identity_groups=load(SITE/'data/writer-identities.json')['groups']
    for group in identity_groups:
        count=sum(expected[i] for i in group['member_ids'])
        for ident in group['member_ids']:expected[ident]=count
    for p in poems:
        if p['writer_id'] and p['writer_id'] not in profiles:
            profiles[p['writer_id']]={'id':p['writer_id'],'name':p['author'],'biography':''}
    quotes=load(SITE/'data/writer-quotes.json');poems_by_id={p['id']:p for p in poems}
    portraits=load(SITE/'data/writer-portraits.json');enriched=load(SITE/'data/writer-enrichment.json')
    aliases={82:'poet-dokana.html',337:'poet-kshanika.html',257:'poet-drink.html',1:'editor-pradeep.html',43:'editor-paresh.html'}
    sources=load(ROOT/'kb/research/writers/portrait-sources.json')
    source_by_id={p['writer_id']:p for p in sources}
    errors=[]
    def need(ok,message):
        if not ok:errors.append(message)
    name_corrections=load(SITE/'data/writer-name-corrections.json')
    directory=(SITE/'poets.html').read_text()
    for key,correction in name_corrections.items():
        ident=int(key);name=correction['display_name']
        need(profiles[ident]['name']==correction['captured_name'],f'{ident}: captured name changed')
        profile_html=(SITE/f'poet-{ident}.html').read_text()
        need(bool(re.search(r'<h1[^>]*>'+re.escape(html_module.escape(name))+r'</h1>',profile_html)),f'{ident}: corrected profile heading missing')
        card=re.search(r'<article class="poet-card"[^>]*data-writer="'+key+r'".*?</article>',directory,re.S)
        need(bool(card) and name in html_module.unescape(card[0]) and correction['captured_name'] in html_module.unescape(card[0]),f'{ident}: directory name/search alias missing')
        for poem in poems:
            if poem['writer_id']!=ident:continue
            reader_html=(SITE/f'poem-{poem["id"]}.html').read_text()
            share=re.search(r'<script type="application/json" id="poem-data">(.*?)</script>',reader_html,re.S)
            need(bool(share) and json.loads(share[1])[0]['author']==name,f'{ident}: reader sharing byline mismatch')
    cache={}
    for ident,p in profiles.items():
        route=aliases.get(ident,f'poet-{ident}.html');html=(SITE/route).read_text();doc=Profile(html);cache[route]=doc
        need(doc.h1==1,f'{ident}: expected one identity heading')
        need(len(doc.ids)==len(set(doc.ids)),f'{ident}: duplicate element IDs')
        need(doc.contributions==expected[ident],f'{ident}: contribution count differs from publication')
        if ident in {1,43}:need(any(x.startswith('about.html#credits-') for x in doc.links),f'{ident}: editor credit link missing')
        else:need('about.html' in doc.links,f'{ident}: Our Story route missing')
        if ident not in {1,43}:
            need('author-profile-opening' in html,f'{ident}: editor-style opening missing')
            selection=quotes.get(str(ident))
            need(bool(selection)==bool(expected[ident]),f'{ident}: quote coverage differs from poem availability')
            need('class="signature"' not in html,f'{ident}: repeated signature remains')
            if selection:
                poem=poems_by_id.get(selection['poem_id'])
                need(bool(poem) and poem['writer_id']==ident,f'{ident}: quote belongs to another writer')
                need(poem['text'][selection['text_start']:selection['text_end']]==selection['text'],f'{ident}: quote is not source exact')
                match=re.search(r'<figure class="author-quote"[^>]*><blockquote lang="([^"]+)">(.*?)</blockquote><figcaption>— <a href="([^"]+)"',html,re.S)
                need(bool(match),f'{ident}: quote missing from rendered page')
                if match:
                    need(html_module.unescape(match[2])==selection['text'],f'{ident}: rendered quote changed')
                    need(match[1]==poem['language'],f'{ident}: quote language differs')
                    route={809:'poem-dokana.html',810:'poem-kshanika.html',814:'poem-drink.html'}.get(poem['id'],f'poem-{poem["id"]}.html')
                    need(match[3]==route and (SITE/route).is_file(),f'{ident}: incorrect quote citation')
            asset=portraits.get(str(ident))
            if asset:
                need(asset['src'] in doc.images and (SITE/asset['src']).is_file(),f'{ident}: portrait missing')
                if asset['kind']=='generic_artwork':
                    need('Generic artwork · photograph unavailable' in html and 'not a likeness of ' in html,f'{ident}: generic artwork disclosure missing')
                if asset['kind']=='journal_photo':
                    original=ROOT/'kb'/source_by_id[ident]['file']
                    need(original.read_bytes()==(SITE/asset['src']).read_bytes(),f'{ident}: original portrait altered')
            else:need('author-initials' in html,f'{ident}: missing image fallback')
            if str(ident) not in enriched:
                for paragraph in p['biography'].split('\n'):
                    if paragraph.strip():need(paragraph.strip() in doc.text,f'{ident}: source biography paragraph changed')
    for route,doc in cache.items():
        for link in doc.links:
            url=urlsplit(link)
            if url.scheme or not url.fragment:continue
            dest=url.path or route
            if dest not in cache:cache_doc=Profile((SITE/dest).read_text())
            else:cache_doc=cache[dest]
            need(url.fragment in cache_doc.ids,f'{route}: missing anchor {link}')
    for item in load(ROOT/'kb/research/writers/portrait-edits.json'):
        need(hashlib.sha256((ROOT/'kb'/item['master']).read_bytes()).hexdigest()==item['master_sha256'],f'{item["writer_id"]}: master changed')
    report={'result':'PASS' if not errors else 'FAIL','profiles':len(profiles),'adapted_authors':len(profiles)-2,'preserved_editor_profiles':2,
            'source_photo_profiles':sum(p['kind']=='journal_photo' for p in portraits.values()),
            'new_artistic_portraits':sum(p['kind']=='generated_portrait' for p in portraits.values()),
            'ai_edited_photographic_portraits':sum(p['kind']=='generated_photo' for p in portraits.values()),
            'generic_artwork_profiles':sum(p['kind']=='generic_artwork' for p in portraits.values()),
            'initials_profiles':len(profiles)-2-len(portraits),'expanded_narratives':len(enriched),
            'quote_profiles':len(quotes),'profiles_without_poems':sum(not expected[i] for i in profiles if i not in {1,43}),'contribution_links_checked':sum(bool(p['writer_id']) for p in poems),'unique_writer_identities':len(profiles)-sum(len(g['member_ids'])-1 for g in identity_groups),'errors':errors}
    (ROOT/'kb/records/author-page-verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False,indent=2));return bool(errors)

if __name__=='__main__':raise SystemExit(main())
