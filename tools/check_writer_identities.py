#!/usr/bin/env python3
"""Check grouped writer journeys against the preserved publication assignments."""
from pathlib import Path
from html.parser import HTMLParser
import json,re
R=Path(__file__).resolve().parents[1];S=R/'projects/site'
load=lambda p:json.loads(p.read_text())
class Markup(HTMLParser):
    def __init__(self,text):super().__init__();self.tags=[];self.feed(text)
    def handle_starttag(self,tag,attrs):self.tags.append((tag,dict(attrs)))
def main():
    groups=load(S/'data/writer-identities.json')['groups']
    sources=[load(p) for p in (S/'content/editions').glob('*/poem-*.json') if load(p).get('status')!='archived']
    routes=load(S/'data/local-routes.json');library=load(S/'assets/reading-library.json')
    directory=Markup((S/'poets.html').read_text());cards=[int(a['data-writer']) for _,a in directory.tags if 'data-writer' in a]
    finder=Markup((S/'poems.html').read_text());poet_rows=[a['data-poet'] for _,a in finder.tags if 'data-poet' in a]
    menu=re.search(r'<select id="poem-poet-filter".*?</select>',(S/'poems.html').read_text(),re.S)[0]
    enrichment=load(S/'data/writer-enrichment.json');seen=set();result=[]
    for group in groups:
        canonical=group['canonical_id'];members=set(group['member_ids'])
        assert canonical in members and not seen.intersection(members)
        seen.update(members)
        poem_ids={p['id'] for p in sources if p['writer_id'] in members}
        expected_routes={routes[str(i)] for i in poem_ids}
        assert cards.count(canonical)==1
        assert poet_rows.count(str(canonical))==len(poem_ids)
        assert f'value="{canonical}"' in menu
        payload=load(S/f'assets/reading-authors/poet-{canonical}.json')
        assert {p['id'] for p in payload['poems']}==poem_ids
        assert len(payload['poems'])==len(poem_ids)
        assert sum(x['id']==canonical for x in library['poets'])==1
        for member in members:
            text=(S/f'poet-{member}.html').read_text();doc=Markup(text)
            linked={a['href'] for tag,a in doc.tags if tag=='a' and 'contribution-title' in a.get('class','')}
            assert linked==expected_routes,(member,linked,expected_routes)
            assert enrichment[str(member)]==enrichment[str(canonical)]
            if member!=canonical:
                assert member not in cards
                assert str(member) not in poet_rows
                assert f'value="{member}"' not in menu
                assert all(x['id']!=member for x in library['poets'])
                assert any(tag=='link' and a.get('rel')=='canonical' and a.get('href')==f'poet-{canonical}.html' for tag,a in doc.tags)
                assert any(a.get('data-pagefind-ignore')=='all' for tag,a in doc.tags if tag=='main')
                assert load(S/f'assets/reading-authors/poet-{member}.json')==payload
        for ident in poem_ids:
            doc=Markup((S/routes[str(ident)]).read_text())
            assert any(a.get('href')==f'poet-{canonical}.html' for tag,a in doc.tags if tag=='a')
        result.append({'canonical_id':canonical,'member_ids':sorted(members),'poem_ids':sorted(poem_ids)})
    report={'result':'PASS','groups':result,'directory_entries':len(cards),'reader_library_poets':len(library['poets']),'checks':['Complete contribution union on every preserved profile URL','One directory/search/reader-library entry per confirmed identity','Canonical byline destinations','Old reader payload URLs retain complete collections','Alias pages excluded from search indexing']}
    (R/'kb/records/writer-identity-verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
