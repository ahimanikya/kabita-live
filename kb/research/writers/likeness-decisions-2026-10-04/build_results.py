from apply_decisions import *
import base64,html
record=read('kb/records/likeness-decisions-2026-10-04.json');sources={x['writer_id']:x for x in read('kb/research/writers/portrait-sources.json')};mapping=read('projects/site/data/writer-portraits.json')
def uri(p):
 p=ROOT/p;return 'data:image/'+('png' if p.suffix=='.png' else 'webp')+';base64,'+base64.b64encode(p.read_bytes()).decode()
def esc(s):return html.escape(str(s))
cards=[];thumbs=[]
for d in record['decisions']:
 i=d['writer_id'];held=d['status']=='retry_hold';selected='attempt' in d
 if held:
  preview=B/f'{i}-held-preview.webp'
  if not preview.exists():subprocess.run(['/Users/ahimanikya/.nvm/versions/node/v24.15.0/bin/node','-e',"require('./projects/site/node_modules/sharp')(process.argv[1]).resize(600,600,{fit:'inside'}).webp({quality:88}).toFile(process.argv[2])",str(ROOT/d['master']),str(preview)],cwd=ROOT,check=True)
  result=uri(preview.relative_to(ROOT))
 else:result=uri('projects/site/'+d['web_asset'])
 source=uri('kb/'+sources[i]['file'])
 label='Photo retained — retry still on hold' if held else (f"Your selection applied · attempt {d['attempt']}" if selected else 'New retry applied · independent review pending')
 observation=d.get('review', 'Your acceptance resolves the earlier self-review hold for this selected attempt. The original concern remains recorded below; author confirmation is not claimed.')
 cards.append(f'<article id="writer-{i}"><h2>{esc(d["name"])} <small>#{i}</small></h2><strong class="status">{esc(label)}</strong><div class="comparison"><figure><img src="{source}" alt="Original photograph of {esc(d["name"])}"><figcaption>Original photograph</figcaption></figure><figure><img src="{result}" alt="Selected or retried artwork for {esc(d["name"])}"><figcaption>{"New candidate — not applied" if held else "Artwork now used locally"}</figcaption></figure></div><p>{esc(observation)}</p><details><summary>Why it was originally held</summary><p>{esc(d["prior_hold"])}</p></details></article>')
 if not held:
  thumb=uri('projects/site/'+d['web_asset'].replace('.webp','-128.webp'))
  thumbs.append(f'<a class="thumb" href="#writer-{i}"><img src="{thumb}" alt="{esc(d["name"])} circular thumbnail"><span>#{i} {esc(d["name"])}</span></a>')
page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>Your portrait review — applied results</title><style>body{margin:0;background:#f6f0e5;color:#273330;font:17px/1.5 system-ui}main{max-width:1120px;margin:auto;padding:28px}h1,h2{font-family:Georgia,serif}h1{font-size:38px}small{font:15px system-ui;color:#68736e}a{color:#175d5b}header{border-bottom:1px solid #c9c5b8;padding-bottom:24px}nav{display:flex;gap:22px;flex-wrap:wrap}.gallery{display:grid;grid-template-columns:repeat(7,1fr);gap:20px 12px;padding:20px 0}.thumb{text-align:center;font-size:12px;text-decoration:none}.thumb img{display:block;width:96px;height:96px;object-fit:cover;border-radius:50%;margin:0 auto 8px}.thumb span{display:block}article{background:#fffcf6;padding:24px;margin:24px 0;border:1px solid #d9d3c5;border-radius:10px;scroll-margin-top:20px}.comparison{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin:22px 0}figure{margin:0}figure img{display:block;width:100%;max-height:440px;object-fit:contain;background:#e8e3d9}figcaption{font-size:14px;margin-top:8px}.status{color:#175d5b;font-size:15px}details{padding:12px;background:#f4eee2}summary{cursor:pointer} @media(max-width:600px){main{padding:16px}h1{font-size:30px}.gallery{grid-template-columns:repeat(3,1fr)}.thumb img{width:80px;height:80px}article{padding:16px}.comparison{gap:10px}h2{font-size:23px}figcaption{font-size:12px}}</style><main><header><h1>Your portrait review — applied results</h1><p><b>23 selections applied. 12 targeted retries completed: 10 applied, 2 remain on hold.</b></p><p>The original photos and all earlier artwork are preserved. Sutanuka Ghosh Roy and Sweety Sony Lall retain their photos; their new candidates appear below with the remaining concerns. The other five newer holds were outside this review export.</p><p>These are local changes. Independent likeness confirmation for new retries remains pending. Your acceptance is recorded for the 23 selected attempts.</p><nav><a href="#thumbnails">33 applied thumbnails</a><a href="#writer-150">Sutanuka’s remaining hold</a><a href="#writer-227">Sweety’s remaining hold</a></nav></header><section id="thumbnails"><h2>Applied circular thumbnails</h2><div class="gallery">'''+''.join(thumbs)+'</div></section>'+''.join(cards)+'</main></html>'
out=ROOT/'kb/artifacts/review/likeness-decisions-2026-10-04/index.html';out.parent.mkdir(parents=True,exist_ok=True);out.write_text(page)
link=ROOT/'projects/site/portrait-review-results.html'
if not link.exists():link.symlink_to(__import__('os').path.relpath(out,link.parent.resolve()))
print('Wrote35 comparisons and33 thumbnails',out)
