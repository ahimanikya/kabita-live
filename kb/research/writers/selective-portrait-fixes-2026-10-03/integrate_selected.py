"""Integrate explicitly reviewed selective revisions; preserve original and prior files."""
from pathlib import Path
import json,hashlib,subprocess
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[4]
record_path=ROOT/'kb/records/selective-portrait-fixes-2026-10-03.json'
q=json.loads(record_path.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
map_path=ROOT/'projects/site/data/writer-portraits.json';edit_path=ROOT/'kb/research/writers/portrait-edits.json'
mapping=json.loads(map_path.read_text());edits=json.loads(edit_path.read_text());sources=json.loads((ROOT/'kb/research/writers/portrait-sources.json').read_text())
selected=[r for r in q['items'] if r['status']=='selected_after_visual_review']
assert len(selected)+sum(r['status']=='retain_existing_after_review' for r in q['items'])==13,'Finish every review before integration'
prior={str(r['writer_id']):mapping[str(r['writer_id'])] for r in selected}
script="""const sharp=require('./projects/site/node_modules/sharp');(async()=>{const [input,out]=process.argv.slice(1);let meta;for(const size of [600,128,64]){const target=out+(size===600?'':'-'+size)+'.webp';const r=await sharp(input).resize(size,size,{fit:'inside'}).webp({quality:90}).toFile(target);if(size===600)meta=r;}console.log(JSON.stringify({width:meta.width,height:meta.height}));})().catch(e=>{console.error(e);process.exit(1)});"""
for r in selected:
 wid=r['writer_id'];key=str(wid);candidate=ROOT/r['candidate'];assert sha(candidate)==r['candidate_sha256'];assert sha(ROOT/r['source'])==r['source_sha256']
 source=next(s for s in sources if s['writer_id']==wid);v=r['version'];stem=f'{wid}-earth-voice-v{v}'
 dest=ROOT/f'projects/site/assets/writers/{stem}'
 assert not dest.with_suffix('.webp').exists(),'Do not overwrite an existing revision'
 meta=json.loads(subprocess.check_output(['/Users/ahimanikya/.nvm/versions/node/v24.15.0/bin/node','-e',script,str(candidate),str(dest)],cwd=ROOT,text=True))
 mapping[key]={'src':f'assets/writers/{stem}.webp','kind':'generated_portrait','credit':prior[key]['credit'],**meta}
 edits.append({'writer_id':wid,'source':source,'source_sha256':sha(ROOT/r['source']),'master':str(Path(r['candidate']).relative_to('kb')),'master_sha256':sha(candidate),'prompt':(ROOT/r['prompt_path']).read_text().strip(),'tool':'built-in image_gen','review':r['review'],'independent':False,'status':'integrated_pending_build','previous_asset':prior[key],'publication_rights':source['rights'],'verification_batch':'selective-portrait-fixes-2026-10-03','human_natural':'Source-led Editorial Natural watercolor; targeted reduction of etched detail','independent_likeness_review':'pending'})
 r.update(status='integrated_pending_build',selected_asset=mapping[key]['src'],derivative_hashes={str(size):sha(ROOT/f'projects/site/assets/writers/{stem}{"" if size==600 else "-"+str(size)}.webp') for size in [600,128,64]})
map_path.write_text(json.dumps(mapping,ensure_ascii=False,indent=2)+'\n');edit_path.write_text(json.dumps(edits,ensure_ascii=False,indent=2)+'\n')
q['status']='integrated_pending_verification';q['integrated_at']=datetime.now(timezone.utc).isoformat();q['previous_mapping']=prior;record_path.write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n')
print('Integrated',len(selected),'reviewed revisions; prior assets preserved.')
