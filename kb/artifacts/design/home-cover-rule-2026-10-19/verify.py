from pathlib import Path
import json,hashlib,re
root=Path.cwd();r=root/'projects/site';e=root/'kb/artifacts/design/home-cover-rule-2026-10-19'
old=json.loads((e/'before-social-previews.json').read_text());new=json.loads((r/'.generated/social-previews.json').read_text())
changed=[name for name in old if old[name]!=new[name]]
assert changed==['index.html'],changed
home=new['index.html'];current=max(i['number'] for i in json.loads((r/'content/editions/index.json').read_text()))
cover=json.loads((r/'data/cover-layout-b.json').read_text())[str(current)]
assert home['edition']==current
assert home['reason']=='current_edition_front_cover'
assert home['source']==cover['artwork']
assert home['cover_svg']==cover['svg']
assert home['image_url']!=old['index.html']['image_url']
html=(r/'dist/index.html').read_text()
for tag in ['og:image','twitter:image']:
    matches=re.findall(r'<meta (?:property|name)="'+tag+r'" content="([^"]+)"',html)
    assert matches==[home['image_url']],(tag,matches)
assert f'data-cover-edition="{current}"' in html
asset=r/'dist'/home['asset'];assert asset.is_file();assert asset.stat().st_size<5_000_000
baseline=json.loads((e/'protected-before.json').read_text())
changed_protected=[name for name,sha in baseline.items() if hashlib.sha256((r/name).read_bytes()).hexdigest()!=sha]
assert not changed_protected,changed_protected
other=json.loads((e/'before-other-preview-hashes.json').read_text())
changed_images=[name for name,sha in other.items() if hashlib.sha256((r/'dist'/name).read_bytes()).hexdigest()!=sha]
assert not changed_images,changed_images
full=json.loads((root/'kb/artifacts/design/ink-and-voice-reader-2026-10-19/preserved-before.json').read_text())
full_changed=[name for name,sha in full.items() if hashlib.sha256((root/name).read_bytes()).hexdigest()!=sha]
assert not full_changed,full_changed
result={'status':'pass','current_edition':current,'changed_page_associations':changed,'other_page_associations_preserved':len(new)-1,'other_sharing_images_unchanged':len(other),'protected_files':len(baseline),'historical_protected_files':len(full),'complete_cover_svg_matches_canonical':True,'new_image_cache_key':True,'image_bytes':asset.stat().st_size,'image_asset':home['asset'],'image_url':home['image_url'],'alt':home['alt'],'initial_html_og_and_twitter_match':True,'originals_and_runtime_unchanged':True,'publication':'Local only; no push/deployment or platform cache request.'}
(e/'export-verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
(e/'homepage-share.jpg').write_bytes(asset.read_bytes())
(e/'after-home-metadata.json').write_text(json.dumps(home,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False))
