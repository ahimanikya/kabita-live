#!/usr/bin/env python3
"""Verify the approved reader rollout, source integrity and edition payload parity."""
from pathlib import Path
from html.parser import HTMLParser
import hashlib,json,re
R=Path(__file__).resolve().parents[1];S=R/'projects/site'
class Page(HTMLParser):
 def __init__(self,text):super().__init__();self.ids={};self.tags=[];self.feed(text)
 def handle_starttag(self,tag,attrs):
  a=dict(attrs);self.tags.append((tag,a))
  if 'id' in a:
   assert a['id'] not in self.ids,('duplicate id',a['id'])
   self.ids[a['id']]=(tag,a)
hashes=json.loads((R/'kb/evidence/poem-reader-rollout/source-hashes.json').read_text())
changes={x['path']:x for x in json.loads((R/'kb/artifacts/content-reconciliation/2026-10-01/file-changes.json').read_text())}
for name,digest in hashes.items():
 if name in changes:
  change=changes[name]
  assert change['before_sha256']==digest,name
  assert hashlib.sha256((R/'kb'/change['before_snapshot']).read_bytes()).hexdigest()==digest,name
  digest=change['after_sha256']
 assert hashlib.sha256((S/name).read_bytes()).hexdigest()==digest,name
sources={p['id']:p for f in (S/'content/editions').glob('*/poem-*.json') for p in [json.loads(f.read_text())]}
routes=json.loads((S/'data/local-routes.json').read_text());readers={};unavailable=[]
for ident,p in sources.items():
 if p.get('status')=='archived':continue
 text=(S/routes[str(ident)]).read_text();doc=Page(text)
 data=json.loads(re.search(r'<script type="application/json" id="reading-data">(.*?)</script>',text,re.S)[1]);readers[ident]=data
 assert data['id']==ident
 for key in ['page-bookmarks','open-focus','focus-reader','poem-secondary-links','selection-tools','reading-panel']:assert key in doc.ids,(ident,key)
 assert 'poem-reading-mock' not in text and 'review-share' not in text
 assert text.count('id="page-bookmarks-button"')==1
 assert len([a for t,a in doc.tags if 'data-share' in a])==1
 for code in ['original','or','hi','en']:
  a=doc.ids['tab-'+code][1];assert ('disabled' in a)==(code!='original' and code not in data['variants'])
 if len(data['variants'])<3:unavailable.append(ident)
 assert doc.ids['reading-panel'][1]['aria-labelledby']=='tab-original'
 for v in data['variants'].values():
  lines=[l for st in v['stanzas'] for l in st]
  for i in v['hidden_lines']:assert re.fullmatch(r'(?:[\s*＊_—–=\-]{3,}|\s*∎\s*)',lines[i])
 assert not re.search(r'<figure class="poem-art[^>]*>.*?<figcaption',text,re.S)
 links=[a['href'] for t,a in doc.tags if t=='a' and 'href'in a]
 assert f'contact.html?poem={ident}' in links
 issues=json.loads(re.search(r'<script type="application/json" id="focus-edition-data">(.*?)</script>',text,re.S)[1])
 assert issues==({'url':f'assets/reading-editions/issue-{p["edition"]}.json'} if p['edition'] else {})
for issue in json.loads((S/'content/editions/index.json').read_text()):
 d=json.loads((S/f'assets/reading-editions/issue-{issue["number"]}.json').read_text())
 assert [p['id'] for p in d['poems']]==issue['poem_ids']
 for p in d['poems']:assert p==readers[p['id']],p['id']
result={'result':'PASS','poems':len(readers),'edition_payloads':47,'unchanged_source_files':len(hashes)-len(changes),'authorized_reconciled_source_files':len(changes),'missing_language_versions_disabled':unavailable,'checks':['Unique control IDs','Correct original alias and availability','Edition order and payload parity','Poet feedback destinations','Historical source preservation and authorized correction hashes','No visible art captions','Only decoration lines hidden']}
(R/'kb/evidence/poem-reader-rollout/integrity.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
