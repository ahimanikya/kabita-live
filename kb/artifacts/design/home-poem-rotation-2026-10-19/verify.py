"""Task-scoped exported homepage/source verification; no browser claim."""
from pathlib import Path
from html import unescape
import hashlib, json, re, sys

root=Path.cwd(); site=root/'projects/site'; evidence=root/'kb/artifacts/design/home-poem-rotation-2026-10-19'
html=(site/'dist/index.html').read_text()
old=(root/'kb/artifacts/design/current-edition-home-2026-10-19/home-after.html').read_text()
pattern=r'<template data-featured-language="([^"]+)" data-poem-id="(\d+)" data-pagefind-ignore>(.*?)</template>'
current={ident:(lang,card) for lang,ident,card in re.findall(pattern,html,re.S)}
prior={ident:(lang,card) for lang,ident,card in re.findall(pattern,old,re.S)}
assert len(current)==13, len(current)
assert len(prior)==11, len(prior)
assert all(current[ident]==value for ident,value in prior.items()), 'Existing poem card changed'
assert set(current)-set(prior)=={'810','812'}
assert 'data-rotation="visit" data-edition="48"' in html
assert 'assets/home-featured.js?v=visit-20261019' in html
assert (site/'dist/assets/home-featured.js').read_bytes()==(site/'assets/home-featured.js').read_bytes()
sys.path.insert(0,str(site.resolve()))
from writer_names import load_writer_profiles
names={p['id']:p['name'] for p in load_writer_profiles(site)}
approved=json.loads((site/'data/home-featured.json').read_text())
titles=json.loads((site/'data/poem-title-overrides.json').read_text())
issues=json.loads((site/'content/editions/index.json').read_text())
poems={str(ident):json.loads((site/f'content/editions/issue-{issue["number"]:02d}/poem-{ident}.json').read_text()) for issue in issues for ident in issue['poem_ids']}
groups={lang:[] for lang in ['or','hi','en']}; detail=[]
for ident,(lang,card) in current.items():
    poem=poems[ident]; assert poem['status']=='captured_full_text'; assert poem['language']==lang
    groups[lang].append(ident)
    title=unescape(re.search(r'<h3\b.*?<a[^>]+>(.*?)</a>',card,re.S)[1])
    byline=unescape(re.search(r'class="byline"[^>]+>(.*?)</a>',card,re.S)[1])
    excerpt=unescape(re.search(r'<p class="excerpt[^>]+>(.*?)</p>',card,re.S)[1])
    if ident in titles:assert titles[ident]['source_title']==poem['title']
    assert title==unescape(titles.get(ident,{}).get('display_title',poem['title']))
    assert byline==names.get(poem['writer_id'],poem['author']).split('/')[0].strip()
    source=unescape(approved.get(ident,{}).get('excerpt',poem['text']))
    expected=[line.strip() for line in source.splitlines() if line.strip()][:4]
    if lang=='or':expected=[line.translate(str.maketrans('', '', '।॥|')).rstrip() for line in expected]
    assert excerpt=='\n'.join(expected), ident
    links=re.findall(r'href="([^"]+)"',card)
    assert all((site/'dist'/link).is_file() for link in links), links
    detail.append({'poem_id':int(ident),'language':lang,'title':title,'writer_id':poem['writer_id'],'byline':byline,'excerpt':excerpt,'links':links})
assert groups=={'or':['826','829','833'],'hi':['827','810','812'],'en':['824','825','828','830','831','832','834']}, groups
baseline=json.loads((root/'kb/artifacts/design/ink-and-voice-reader-2026-10-19/preserved-before.json').read_text())
changed=[name for name,sha in baseline.items() if hashlib.sha256((root/name).read_bytes()).hexdigest()!=sha]
assert not changed, changed
local=json.loads((evidence/'protected-before.json').read_text())
local_changed=[name for name,sha in local.items() if hashlib.sha256((site/name).read_bytes()).hexdigest()!=sha]
assert not local_changed, local_changed
(evidence/'candidate-groups.json').write_text(json.dumps(groups,ensure_ascii=False,indent=2)+'\n')
(evidence/'source-card-evidence.json').write_text(json.dumps(detail,ensure_ascii=False,indent=2)+'\n')
(evidence/'home-after.html').write_text(html)
result={'status':'pass','candidate_counts':{lang:len(ids) for lang,ids in groups.items()},'unchanged_current_edition_cards':len(prior),'added_recent_originals':[810,812],'source_excerpts_byline_title_and_links_checked':len(current),'protected_files':{'checked':len(baseline),'changed':changed},'local_protected_files':{'checked':len(local),'changed':local_changed},'exported_script_matches_source':True,'edition':48,'source_display_format':'Existing four-line format retained, including the previously approved Odia display-only punctuation handling.'}
(evidence/'export-verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False))
