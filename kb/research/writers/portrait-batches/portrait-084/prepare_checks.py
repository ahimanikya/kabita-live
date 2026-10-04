from pathlib import Path
import base64,os,json,hashlib,sys
num=sys.argv[1];b=Path('kb/research/writers/portrait-batches')/('portrait-'+num);q=json.loads(Path('kb/research/writers/portrait-batches.json').read_text());ids=next(x['writer_ids'] for x in q['batches'] if x['id']=='portrait-'+num);rows=[]
for i in [x for x in ids if x != 377]:
 row='<article><h2>#'+str(i)+'</h2>'
 for size in [64,128]:
  p=Path(f'projects/site/assets/writers/{i}-earth-voice-v1-{size}.webp');row+=f'<img style="width:{size}px;height:{size}px;border-radius:50%;object-fit:cover;margin:10px" src="data:image/webp;base64,{base64.b64encode(p.read_bytes()).decode()}" alt="Writer {i} {size}px circular thumbnail">'
 rows.append(row+'</article>')
page=b/'thumbnails.html';page.write_text('<!doctype html><html><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Portrait'+num+' thumbnails</title><body style="background:#f7f0e3;color:#274444;font:16px system-ui"><h1>Portrait'+num+' · circular crops</h1><main style="display:flex;flex-wrap:wrap;gap:30px">'+''.join(rows)+'</main></body></html>')
link=Path(f'projects/site/portrait-{num}-review.html')
if not link.exists():link.symlink_to(os.path.relpath(page.resolve(),link.parent.resolve()))
base=json.loads((b/'baseline.json').read_text());changed=[p for p,h in base.items() if hashlib.sha256(Path(p).read_bytes()).hexdigest()!=h];assert set(changed)<= {'projects/site/data/writer-portraits.json','projects/site/data/edition-art-direction.json'},changed
edits=json.loads(Path('kb/research/writers/portrait-edits.json').read_text());n=0
for e in edits:
 if e.get('source_sha256') and e.get('source',{}).get('file'):
  assert hashlib.sha256((Path('kb')/e['source']['file']).read_bytes()).hexdigest()==e['source_sha256'];n+=1
 if e.get('master_sha256') and e.get('master'):assert hashlib.sha256((Path('kb')/e['master']).read_bytes()).hexdigest()==e['master_sha256']
(b/'hash-check.json').write_text(json.dumps({'result':'PASS','baseline_files':len(base),'changed':changed,'source_records':n,'all_recorded_master_hashes':'PASS'},indent=2)+'\n');print(len(base),changed,n)
