#!/usr/bin/env python3
"""Check edition navigation against publication order and local reader routes."""
from pathlib import Path
from html.parser import HTMLParser
import json,re
R=Path(__file__).resolve().parents[1];S=R/'projects/site'
class Links(HTMLParser):
 def __init__(self,text):super().__init__();self.links=[];self.feed(text)
 def handle_starttag(self,tag,attrs):
  if tag=='a':self.links.append(dict(attrs))
routes=json.loads((S/'data/local-routes.json').read_text());count=0
for path in (S/'assets/reading-editions').glob('issue-*.json'):
 edition=json.loads(path.read_text());poems=edition['poems'];ids=[p['id'] for p in poems]
 for position,p in enumerate(poems):
  page=(S/p['route']).read_text();assert page.count('class="edition-glance"')==1,p['id']
  match=re.search(r'<section class="edition-glance"><nav.*?</nav>',page,re.S);assert match,p['id']
  links=Links(match[0]).links;nearby=links[:-1]
  assert len(nearby)==min(5,len(poems)),p['id']
  actual=[next(x['id'] for x in poems if x['route']==a['href']) for a in nearby]
  assert p['id'] in actual and [ids.index(i) for i in actual]==list(range(ids.index(actual[0]),ids.index(actual[0])+len(actual))),p['id']
  assert [a['href'] for a in nearby if a.get('aria-current')=='page']==[p['route']],p['id']
  assert links[-1]['href']==f'issue-{edition["edition"]}.html#edition-poems',p['id']
  panel=re.search(r'<section class="edition-glance">.*?</section>',page,re.S)[0]
  assert 'id="poem-secondary-links"' in panel and f'contact.html?poem={p["id"]}' in panel,p['id']
  assert 'poem-space-' not in page,p['id']
  for a in links:assert (S/a['href'].split('#')[0]).exists(),a
  count+=1
unassigned=(S/routes['645']).read_text();assert 'edition-glance related-only' in unassigned and 'In this edition' not in unassigned
result={'result':'PASS','edition_poems':count,'unassigned_poems':1,'edition_link_order_current_poem_destinations_and_related_links':'PASS'}
(R/'kb/evidence/poem-panel-rollout/integrity.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
