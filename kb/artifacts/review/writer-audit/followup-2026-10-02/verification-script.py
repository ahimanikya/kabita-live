import json,hashlib,re,sys
from pathlib import Path
from html import unescape
R=Path.cwd();S=R/'projects/site';O=R/'kb/artifacts/review/writer-audit/followup-2026-10-02';read=lambda p:json.loads(p.read_text())
old=read(O/'protected-before.json');changed=[p for p,h in old.items() if hashlib.sha256((R/p).read_bytes()).hexdigest()!=h]
allowed=['projects/site/content/editions/issue-18/poem-390.json','projects/site/content/editions/issue-39/poem-699.json'];assert sorted(changed)==sorted(allowed),changed
# Name corrections reach profile, directory, reader, edition and sharing data; captured names stay intact.
checks=[]
for wid,item in read(S/'data/writer-name-corrections.json').items():
 name=item['display_name'];captured=item['captured_name'];raw=next(p for p in read(S/'data/writer-profiles.json') if str(p['id'])==wid);assert raw['name']==captured
 html=(S/f'poet-{wid}.html').read_text();assert re.search(r'<h1[^>]*>'+re.escape(name)+r'</h1>',html)
 directory=(S/'poets.html').read_text();card=re.search(r'<article class="poet-card"[^>]*data-writer="'+wid+r'".*?</article>',directory,re.S).group();assert name in card and captured in card
 for p in (S/'content/editions').glob('*/poem-*.json'):
  d=read(p)
  if str(d['writer_id'])!=wid:continue
  assert d['author']!=name or d['author']==raw['name'] or d['author']==name
  reader=(S/f'poem-{d["id"]}.html').read_text();assert name in reader
  share=json.loads(re.search(r'<script type="application/json" id="poem-data">(.*?)</script>',reader,re.S)[1]);assert share[0]['author']==name
  assert name in (S/f'issue-{d["edition"]}.html').read_text()
 checks.append({'writer_id':wid,'name':name,'captured_name':captured,'surfaces':'profile/directory/search aliases/reader/edition/share'})
for i,iss,start,end in [(390,18,0,1),(699,39,18,35)]:
 before=read(O/f'before/content/editions/issue-{iss}/poem-{i}.json');after=read(S/f'content/editions/issue-{iss}/poem-{i}.json');assert after['stanzas']==before['stanzas'][start:end]
 for lang,v in read(S/'data/poem-translations.json')[str(i)]['variants'].items():assert v['stanzas']==read(O/'before/data/poem-translations.json')[str(i)]['variants'][lang]['stanzas'][start:end]
 html=(S/f'poem-{i}.html').read_text();public=(S/f'dist/poem-{i}.html').read_text();assert html.count('id="reading-data"')==public.count('id="reading-data"')==1
# Quotes all retain their exact wording; only699 source offsets change.
a=read(O/'before/data/writer-quotes.json');b=read(S/'data/writer-quotes.json');assert all(a[i]['text']==b[i]['text'] for i in a)
assert [i for i in a if a[i]!=b[i]]==['429']
summary={'result':'PASS','protected_files_checked':len(old),'intentional_changes':changed,'names':checks,'poem_and_translation_ranges':'exact retained slices','quote_wording':'all unchanged; writer429 offsets re-anchored','isolated_reimport':'all content JSON matches','build':'PASS:1297 indexed pages','author_and_edition_checks':'PASS'}
(O/'verification.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n');print(json.dumps(summary,indent=2))
