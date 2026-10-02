#!/usr/bin/env python3
"""Check captured publication membership, text fidelity and reciprocal reader links."""
import hashlib
from collections import defaultdict
import json
import re
from html import unescape
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'projects/site'
CONTENT = SITE / 'content/editions'
SPACING = json.loads((SITE/'data/poem-spacing.json').read_text())
ENDINGS = json.loads((SITE/'data/poem-endings.json').read_text())
ENDING_EVIDENCE = {str(e['poem_id']):e for e in json.loads((ROOT/'kb/records/poem-ending-migration.json').read_text())['entries']}

class Reader(HTMLParser):
    def __init__(self, text):
        super().__init__(); self.links=[]; self.stanzas=[]; self.in_verse=False; self.in_stanza=False
        self.feed(text)
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if tag=='a' and 'href' in a: self.links.append(a['href'])
        if tag=='div' and 'verse' in a.get('class','').split(): self.in_verse=True
        if self.in_verse and tag=='p': self.in_stanza=True; self.stanzas.append('')
        if self.in_stanza and tag=='br': self.stanzas[-1]+='\n'
    def handle_endtag(self, tag):
        if tag=='p': self.in_stanza=False
        if tag=='div': self.in_verse=False
    def handle_data(self, data):
        if self.in_stanza: self.stanzas[-1]+=data

def main():
    errors=[]
    def need(condition, message):
        if not condition: errors.append(message)
    load=lambda p: json.loads(p.read_text())
    issues=load(CONTENT/'index.json'); poems=[load(p) for p in CONTENT.glob('*/poem-*.json')]
    routes=load(SITE/'data/local-routes.json'); by_id={p['id']:p for p in poems}
    profiles={82:'poet-dokana.html',337:'poet-kshanika.html',257:'poet-drink.html',1:'editor-pradeep.html',43:'editor-paresh.html'}
    for group in load(SITE/'data/writer-identities.json')['groups']:
        profiles.update({i:f'poet-{group["canonical_id"]}.html' for i in group['member_ids']})
    archived={p['id'] for p in poems if p.get('status')=='archived'}
    rules=load(SITE/'data/poem-reconciliation.json')['rules']
    need(archived=={int(i) for i,r in rules.items() if r['action']=='archive'},'Archive status differs from approved corrections')
    need(sorted(i['number'] for i in issues)==list(range(1,48)), 'Expected all 47 edition numbers')
    need(len(poems)==len(by_id)==801, 'Expected 801 unique captured poems')
    memberships=[pid for i in issues for pid in i['poem_ids']]
    need(len(memberships)==len(set(memberships))==800-len(archived), 'Edition membership must exclude archived records')
    need(set(by_id)-set(memberships)=={645}|archived, 'Unexpected unassigned or archived poem')
    listed=sum(len(i['listed_poem_ids']) for i in issues)
    need(listed==796-len(archived), 'Unexpected contents-listed poem count')
    for issue in issues:
        n=issue['number']; html=(SITE/f'issue-{n}.html').read_text()
        need(load(CONTENT/f'issue-{n:02d}/edition.json')==issue,f'Issue {n}: manifest mismatch')
        targets=[unescape(m) for m in re.findall(r'<h3[^>]*><a href="([^"]+)"',html)]
        need(targets==[routes[str(pid)] for pid in issue['poem_ids']],f'Issue {n}: reader order mismatch')
        for pid in issue['poem_ids']:
            need(by_id[pid]['edition']==n,f'Poem {pid}: edition mismatch')
    for p in poems:
        ident=p['id']
        if ident in archived:
            route=f'poem-{ident}.html';html=(SITE/route).read_text()
            need('The poem text is currently unavailable.' in html and 'id="reading-data"' not in html,f'Poem {ident}: archive notice missing or invalid verse exposed')
            need(route not in Reader((SITE/'archive.html').read_text()).links,f'Poem {ident}: unavailable entry exposed in archive index')
            need(str(ident) not in routes,f'Poem {ident}: still in reading routes')
            continue
        route=routes[str(ident)]; reader=Reader((SITE/route).read_text())
        expected=p['stanzas']
        ending=ENDINGS.get(str(ident))
        if ending:
            count=ending['verse_line_count'];flat=[line for stanza in expected for line in stanza]
            need(hashlib.sha256(p['text'].encode()).hexdigest()==ending['source_sha256'],f'Poem {ident}: ending source changed')
            need(flat[count:]==ENDING_EVIDENCE[str(ident)]['source_tail'],f'Poem {ident}: reviewed tail changed')
            expected=[];remaining=count
            for stanza in p['stanzas']:
                if remaining<=0:break
                expected.append(stanza[:remaining]);remaining-=len(stanza)
        spacing=SPACING.get(str(ident),{})
        if spacing:
            need(hashlib.sha256(p['text'].encode()).hexdigest()==spacing['source_sha256'],f'Poem {ident}: spacing source changed')
            groups=[];index=0
            for stanza in expected:
                group=[]
                for line in stanza:
                    if index in spacing['before_lines'] and group:groups.append(group);group=[]
                    group.append(line);index+=1
                if group:groups.append(group)
            expected=groups
        need(reader.stanzas==['\n'.join(s) for s in expected],f'Poem {ident}: rendered stanza mismatch')
        need('\n\n'.join(reader.stanzas)=='\n\n'.join('\n'.join(s) for s in expected),f'Poem {ident}: rendered verse mismatch')
        need('\ufffd' not in p['text']+p['title']+p['author'],f'Poem {ident}: damaged Unicode')
        if p['edition']:
            need(f'issue-{p["edition"]}.html' in reader.links,f'Poem {ident}: missing return link')
            siblings=next(i['poem_ids'] for i in issues if i['number']==p['edition'])
            pos=siblings.index(ident)
            if pos<len(siblings)-1: need(routes[str(siblings[pos+1])] in reader.links,f'Poem {ident}: missing next link')
        if p['writer_id']:
            profile=profiles.get(p['writer_id'],f'poet-{p["writer_id"]}.html')
            need(profile in reader.links,f'Poem {ident}: missing writer link')
            need(route in Reader((SITE/profile).read_text()).links,f'Poem {ident}: missing reciprocal contribution')
    receipts=load(ROOT/'kb/research/editions/source-receipts.json')
    for r in receipts:
        raw=(ROOT/'kb/artifacts/content-import/editions'/r['path']).read_bytes()
        need(hashlib.sha256(raw).hexdigest()==r['sha256'],f'Source hash mismatch: {r["path"]}')
    need(len(receipts)==848,'Expected 848 source receipts')
    text_groups=defaultdict(list)
    for p in poems: text_groups[p['text']].append(p['id'])
    duplicate_groups=sorted(sorted(ids) for ids in text_groups.values() if len(ids)>1)
    result={'result':'PASS' if not errors else 'FAIL','editions':len(issues),'complete_poems':len(poems)-len(archived),'archived_poems':sorted(archived),
            'edition_assigned':len(memberships),'listed_poems':listed,'supplementary_assigned_poems':4,
            'source_hashes_verified':len(receipts),'reciprocal_writer_links_checked':sum(bool(p['writer_id']) for p in poems if p['id'] not in archived),
            'checks':['Unique edition membership','Published contents order','Original capture integrity and reviewed reader verse parity',
                      'Return and next-poem links','Reciprocal writer contribution links','Raw source SHA-256'],
            'known_gaps':{'unassigned_poems':[645],'missing_author':[30],
                          'identical_text_groups_for_editorial_review':duplicate_groups},'errors':errors}
    (ROOT/'kb/records/edition-content-verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(result,ensure_ascii=False,indent=2)); return bool(errors)

if __name__=='__main__': raise SystemExit(main())
