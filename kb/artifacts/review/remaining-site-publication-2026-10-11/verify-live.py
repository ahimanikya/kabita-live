from pathlib import Path
import hashlib,json,re,posixpath,urllib.request,xml.etree.ElementTree as ET
root=Path('/Users/ahimanikya/.codex/worktrees/remaining-site-publication/Kabita Live/output/kabitalive-design-proposal-2026-09-29/site')
def fetch(name):
 with urllib.request.urlopen('https://kabitalive.com/'+name,timeout=45) as r:
  assert r.status==200
  return r.read()
checks={}
sitemap=fetch('sitemap.xml');assert b'translation-review' not in sitemap;checks['sitemap_urls']=len(ET.fromstring(sitemap));assert checks['sitemap_urls']==1306
review=fetch('translation-review.html').decode();assert 'noindex,follow' in review and 'data-pagefind-body' not in review and '1,312 variants' in review;checks['review_noindex']=True
about=fetch('about.html').decode();assert 'draft interpretations' not in about and 'independent linguistic review is pending' not in about;checks['reader_draft_notice_removed']=True
assert b'translation-review' not in fetch('llms.txt');checks['llm_guide_excluded']=True
runtime=json.loads(fetch('runtime-config.json'));assert runtime['firebase']['appCheck']['enabled'];assert all(runtime['engagement'][k]=='1' for k in ['feedbackReceiptVersion','commentReceiptVersion','articleResponseVersion']);assert 'translation-review' not in json.dumps(runtime);checks['protected_services_enabled']=True
checks['asset_hashes']={}
manifest=json.loads((root/'.service-build.json').read_text())
# esbuild dependency names differ with CI/local module resolution; compare content
# after normalizing only its eight-character generated filename hashes.
def normalized(raw):return re.sub(rb'-[A-Z0-9]{8}\.js',b'-BUILDHASH.js',raw)
expected={hashlib.sha256(normalized((root/n).read_bytes())).hexdigest() for n in manifest['files']}
seen=set();pending=['assets/engagement.js','assets/private-feedback.js'];actual=set()
while pending:
 name=pending.pop()
 if name in seen:continue
 seen.add(name);raw=fetch(name);checks['asset_hashes'][name]=hashlib.sha256(raw).hexdigest();actual.add(hashlib.sha256(normalized(raw)).hexdigest())
 for dep in re.findall(r'["\'](\./services/[^"\']+\.js|\./[^"\']+\.js)["\']',raw.decode()):pending.append(posixpath.normpath(posixpath.join(posixpath.dirname(name),dep)))
assert actual==expected, {'missing':len(expected-actual),'unexpected':len(actual-expected)}
checks['service_graph_matches']='Exact content after generated filename-hash normalization'
for name in ['assets/analytics.js','assets/reading-all.json','assets/poem-art/editions/36/begin-again-at-the-bench-v1.webp']:
 digest=hashlib.sha256(fetch(name)).hexdigest();assert digest==hashlib.sha256((root/'dist'/name).read_bytes()).hexdigest(),name;checks['asset_hashes'][name]=digest
for name in ['index.html','issue-48.html','poem-dokana.html','poem-644.html','thirty-languages-and-the-journey-of-a-poem.html']:
 page=fetch(name).decode();assert 'draft interpretations' not in page;assert 'translation-review.html' not in page;assert 'index,follow,max-image-preview:large' in page
checks['representative_pages']=5
Path(__file__).with_name('live-verification.json').write_text(json.dumps(checks,indent=2)+'\n');print(json.dumps(checks,indent=2))
