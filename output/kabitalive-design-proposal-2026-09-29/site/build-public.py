"""Select only public reader pages/assets for Astro; never export the project KB."""
import argparse,json,re,shutil,os,html as html_lib
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote

root=Path(__file__).resolve().parent
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--release',action='store_true')
args=parser.parse_args()
status=json.loads((root/'data/content-status.json').read_text())
if args.release and not status['launch_ready']:
    raise SystemExit('Release blocked: '+ '; '.join(status['blockers']))
if args.release:
    translations=json.loads((root/'data/poem-translations.json').read_text())
    pending=[f'{ident}/{lang}' for ident,entry in translations.items() for lang,v in entry['variants'].items() if v.get('status')!='reviewed']
    if pending: raise SystemExit(f'Release blocked: {len(pending)} translation drafts await linguistic review.')
excluded={'credits-content.html'}
# Book reviews are retained locally for provenance, outside the reader publication.
excluded.update(p.name for p in root.glob('*.html') if re.fullmatch(r'reviews?(?:-\d+)?\.html', p.name))
pages=sorted(p.name for p in root.glob('*.html') if not p.is_symlink() and p.name not in excluded)
refs=set()
class Links(HTMLParser):
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        for k in ['src','href','poster']:
            if k in a:refs.add(a[k])
        if 'srcset' in a:
            for item in a['srcset'].split(','):refs.add(item.strip().split()[0])

for name in pages:
    html=(root/name).read_text()
    if re.search(r'https?://(?:www\.)?kabitalive\.com',html,re.I):
        raise SystemExit('Old-site dependency in '+name)
    Links().feed(html)

assets={'assets/app.js','assets/analytics.js','assets/private-feedback.js','assets/poem-marks.mjs','runtime-config.json'}
assets.update(str(p.relative_to(root)) for p in (root/'assets/fonts').glob('*-OFL.txt'))
assets.update(str(p.relative_to(root)) for p in (root/'assets/reading-editions').glob('issue-*.json'))
assets.add('assets/reading-library.json')
assets.add('assets/reading-all.json')
assets.add('assets/reader-pagination.mjs')
# Homepage views are loaded on demand, not all referenced by image markup.
for view in json.loads((root/'data/home-views.json').read_text()):
    assets.update([view['src'],view['small']])
assets.update(str(p.relative_to(root)) for p in (root/'assets/reading-authors').glob('poet-*.json'))
for value in refs:
    url=urlsplit(value)
    if url.scheme or value.startswith('#') or not url.path:continue
    relative=unquote(url.path)
    if relative.endswith('.html'):
        if relative not in pages:raise SystemExit('Public page links outside reader site: '+relative)
    elif relative.startswith('assets/'):
        assets.add(relative)
    else:raise SystemExit('Unexpected public resource: '+relative)
for relative in list(assets):
    if relative.endswith('.css'):
        css=(root/relative).read_text()
        for value in re.findall(r'url\([\s\'"]*([^\)\'"\s]+)',css):
            if not urlsplit(value).scheme:
                assets.add(str((Path(relative).parent/value)))
for relative in assets:
    p=root/relative
    if not p.is_file():raise SystemExit('Missing public asset: '+relative)
    if p.suffix in {'.js','.css','.json'} and 'kabitalive.com' in p.read_text():
        raise SystemExit('Old-site runtime dependency: '+relative)

# These are exclusively generated build directories, never source or historical evidence.
for directory in ['.generated','.public']:
    target=root/directory
    if target.exists():shutil.rmtree(target)
    target.mkdir()
(root/'.generated/pages').mkdir()
for name in pages:
    html=(root/name).read_text().replace('<main id="main"','<main data-pagefind-body id="main"',1)
    if args.release:
        html=html.replace('<meta name="robots" content="noindex,nofollow">','')
    (root/'.generated/pages'/name).write_text(html)
for relative in sorted(assets):
    target=root/'.public'/relative;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(root/relative,target)
# Use exact exported routes and build-time titles for consented measurements.
runtime=json.loads((root/'runtime-config.json').read_text())
base='/' + os.environ.get('SITE_BASE','').strip('/')
if not base.endswith('/'):base+='/'
runtime['analytics']['basePath']=base
runtime['analytics']['publicPages']={}
for name in pages:
    if name in {'404.html','search.html'}:continue
    title=re.search(r'<title>(.*?)</title>',(root/name).read_text(),re.S)
    if title:
        runtime['analytics']['publicPages'][base+name]=html_lib.unescape(title.group(1)).strip()
        if name=='index.html':runtime['analytics']['publicPages'][base]=html_lib.unescape(title.group(1)).strip()
(root/'.public/runtime-config.json').write_text(json.dumps(runtime,ensure_ascii=False,indent=2)+'\n')
(root/'.public/robots.txt').write_text('User-agent: *\nDisallow: /\n' if not args.release else 'User-agent: *\nAllow: /\n')
(root/'.generated/public-pages.json').write_text(json.dumps(pages,indent=2)+'\n')
(root/'.generated/release-manifest.json').write_text(json.dumps({'pages':pages,'assets':sorted(assets),'content_ready':status['launch_ready'],'release':args.release},indent=2)+'\n')
print(f'Public-only build inputs: {len(pages)} pages, {len(assets)} assets. Content ready: {status["launch_ready"]}.')
