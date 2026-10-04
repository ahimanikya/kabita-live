"""Apply the user's exact review selections; preserve source and candidate masters."""
from pathlib import Path
import hashlib,json,shutil,subprocess,datetime
ROOT=Path(__file__).resolve().parents[4]
B=Path(__file__).resolve().parent
def read(p): return json.loads((ROOT/p).read_text())
def write(p,d): (ROOT/p).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 src=Path('/Users/ahimanikya/Downloads/kabita-likeness-review-notes (1).json')
 saved=B/'user-review.json'
 if not saved.exists(): shutil.copy2(src,saved)
 assert sha(src)==sha(saved)
 notes=json.loads(saved.read_text())['notes']
 rows={str(r['writer_id']):r for r in read('kb/research/writers/likeness-holds-review-2026-10-04/manifest.json')['rows']}
 assert set(notes)==set(rows)
 baseline=B/'baseline.json'
 if not baseline.exists():
  paths=set()
  for pat in ['projects/site/content/**/*.json','projects/site/data/*.json','projects/site/assets/writers/*','kb/artifacts/artwork/portrait-sources/writers/*','kb/artifacts/artwork/writer-portraits/*']:
   paths.update(p for p in ROOT.glob(pat) if p.is_file())
  baseline.write_text(json.dumps({str(p.relative_to(ROOT)):sha(p) for p in sorted(paths)},indent=2)+'\n')
 plan=[]
 for ident,n in notes.items():
  r=rows[ident];assert n['name']==r['name']
  if n['decision'].startswith('Attempt '):
   attempt=int(n['decision'].split()[1]);a=r['assets'][attempt];assert a['label'].startswith(f'Attempt {attempt} ');assert sha(ROOT/a['path'])==a['hash']
   plan.append(dict(writer_id=int(ident),name=n['name'],decision=n['decision'],attempt=attempt,master=a['path'],master_sha256=a['hash'],prompt=a['prompt'],prior_hold=r['recorded_reason'],status='pending_application'))
  else:
   assert n['decision']=='Try a targeted correction'
   plan.append(dict(writer_id=int(ident),name=n['name'],decision=n['decision'],source=r['assets'][0]['path'],prior_hold=r['recorded_reason'],status='retry_pending'))
 recordpath='kb/records/likeness-decisions-2026-10-04.json'
 if (ROOT/recordpath).exists(): return
 record=dict(recorded_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),authorization='User supplied the review export and explicitly instructed Apply this.',import_sha256=sha(saved),review_export='research/writers/likeness-decisions-2026-10-04/user-review.json',status='applying',verification='pending',decisions=plan,independent_author_editor_review='Not claimed; human acceptance by Ahimanikya of specified saved attempts only.')
 write(recordpath,record)
 mapping=read('projects/site/data/writer-portraits.json');edits=read('kb/research/writers/portrait-edits.json');sources={x['writer_id']:x for x in read('kb/research/writers/portrait-sources.json')}
 script="const sharp=require('./projects/site/node_modules/sharp');(async()=>{const [input,stem]=process.argv.slice(1);for(const size of [600,128,64])await sharp(input).resize(size,size,{fit:'inside'}).webp({quality:90}).toFile(stem+(size===600?'':'-'+size)+'.webp')})().catch(e=>{console.error(e);process.exit(1)});"
 for d in record['decisions']:
  if d['status']!='pending_application':continue
  i=d['writer_id'];old=mapping[str(i)];assert old['kind']=='journal_photo'
  stem=f'projects/site/assets/writers/{i}-user-selected-20261004'
  subprocess.run(['/Users/ahimanikya/.nvm/versions/node/v24.15.0/bin/node','-e',script,str(ROOT/d['master']),stem],cwd=ROOT,check=True)
  mapping[str(i)]={'src':stem.removeprefix('projects/site/')+'.webp','kind':'generated_portrait','credit':'AI-assisted artistic portrait from the journal-supplied photograph','width':600,'height':600}
  s=sources[i]
  edits.append(dict(writer_id=i,source=s,source_sha256=sha(ROOT/'kb'/s['file']),master=d['master'].removeprefix('kb/'),master_sha256=d['master_sha256'],prompt=d['prompt'],tool='built-in image_gen; existing saved candidate selected by user',style_reference='projects/site/assets/editors/pradeep-biswal-artistic-v1.webp',review=f"User explicitly accepted attempt {d['attempt']} and requested application. Original self-review concern preserved: "+d['prior_hold'],independent=False,user_review={'reviewer':'Ahimanikya Satapathy','decision':d['decision'],'evidence':'research/writers/likeness-decisions-2026-10-04/user-review.json','authorization':'Apply this'},independent_likeness_review='user acceptance recorded; author/editor confirmation not claimed',previous_asset=old,publication_rights=s['rights'],status='user_approved_integrated_pending_build',verification_batch='likeness-decisions-2026-10-04'))
  d['status']='applied_pending_verification';d['web_asset']=mapping[str(i)]['src']
  write('projects/site/data/writer-portraits.json',mapping);write('kb/research/writers/portrait-edits.json',edits);write(recordpath,record)
 print('Applied',sum(x['status']=='applied_pending_verification' for x in record['decisions']),'saved selections; retries',sum(x['status']=='retry_pending' for x in record['decisions']))
if __name__=='__main__':main()
