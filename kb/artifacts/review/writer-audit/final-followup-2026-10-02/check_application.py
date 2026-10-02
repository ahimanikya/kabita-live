"""Check research drafts against site inputs and rendered biography/book/reference content."""
import hashlib,json
from pathlib import Path
from html.parser import HTMLParser
ROOT=Path(__file__).resolve().parents[5]
SITE=ROOT/'projects/site'
class Text(HTMLParser):
    def __init__(self,s):
        super().__init__();self.out=[];self.links=[];self.feed(s)
    def handle_data(self,s):self.out.append(s)
    def handle_starttag(self,tag,attrs):
        if tag=='a':self.links.append(dict(attrs).get('href',''))
def norm(s):return ' '.join(s.split())
data=json.loads((SITE/'data/writer-enrichment.json').read_text())
aliases={'82':'poet-dokana.html','337':'poet-kshanika.html','257':'poet-drink.html','1':'editor-pradeep.html','43':'editor-paresh.html'}
errors=[];paragraphs=0;books=0;sources=0;legacy_intros=[]
for key,draft in data.items():
    dossier=json.loads((ROOT/f'kb/research/writers/enrichment/{key}.json').read_text())
    if dossier.get('reader_draft')!=draft:errors.append(f'{key}: research draft differs from site input')
    paragraphs+=sum(len(s['paragraphs']) for s in draft.get('sections',[]))
    books+=len(draft.get('books',[]));sources+=len(draft.get('sources',[]))
    if draft.get('intro'):legacy_intros.append(int(key))
    for surface in [SITE,SITE/'dist']:
        route=aliases.get(key,f'poet-{key}.html')
        doc=Text((surface/route).read_text());text=norm(' '.join(doc.out))
        for section in draft.get('sections',[]):
            for paragraph in section['paragraphs']:
                if norm(paragraph) not in text:errors.append(f'{surface.name}/{route}: missing narrative paragraph')
        for book in draft.get('books',[]):
            if norm(book['title']) not in text or book['url'] not in doc.links:errors.append(f'{surface.name}/{route}: missing book/link')
        colophon=Text((surface/'about.html').read_text())
        for source in draft.get('sources',[]):
            if source['url'] not in colophon.links:errors.append(f'{surface.name}/{key}: missing research reference in colophon')
report={'result':'PASS' if not errors else 'FAIL','profiles_checked':len(data),'biography_paragraphs_checked_per_surface':paragraphs,'book_links_checked_per_surface':books,'source_links_checked_per_surface':sources,'surfaces':['local preview HTML','public build HTML'],'legacy_intro_fields':{'writer_ids':legacy_intros,'handling':'Retained historical introductory labels are intentionally omitted by the approved own-poem quotation opening; all biography sections are rendered.'},'site_input_sha256':hashlib.sha256((SITE/'data/writer-enrichment.json').read_bytes()).hexdigest(),'independent':False,'errors':errors}
Path(__file__).with_name('application-verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False,indent=2))
raise SystemExit(bool(errors))
