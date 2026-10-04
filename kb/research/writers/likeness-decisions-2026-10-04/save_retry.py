from apply_decisions import *
import sys
i=int(sys.argv[1]);generated=Path(sys.argv[2]);outcome=sys.argv[3];observation=sys.argv[4]
assert outcome in ['integrate','hold']
rp='kb/records/likeness-decisions-2026-10-04.json';record=read(rp);d=next(x for x in record['decisions'] if x['writer_id']==i);assert d['status']=='retry_pending'
master=f'artifacts/artwork/writer-portraits/{i}-review-retry-v1.png';target=ROOT/'kb'/master;assert not target.exists();shutil.copy2(generated,target)
source=next(x for x in read('kb/research/writers/portrait-sources.json') if x['writer_id']==i)
entry=dict(writer_id=i,source=source,source_sha256=sha(ROOT/'kb'/source['file']),master=master,master_sha256=sha(target),prompt=(B/f'{i}-retry-prompt.txt').read_text().strip(),style_reference='projects/site/assets/editors/pradeep-biswal-artistic-v1.webp',tool='built-in image_gen',review=observation,independent=False,publication_rights=source['rights'],status='integrated_pending_build' if outcome=='integrate' else 'rejected_candidate',verification_batch='likeness-decisions-2026-10-04',human_natural='Editorial Natural; preserve source blur, crop and occlusion rather than reconstruct missing details.',independent_likeness_review='pending',user_request='Try a targeted correction; Apply this')
if outcome=='integrate':
 mapping=read('projects/site/data/writer-portraits.json');assert mapping[str(i)]['kind']=='journal_photo';entry['previous_asset']=mapping[str(i)]
 stem=f'projects/site/assets/writers/{i}-review-retry-v1'
 script="const sharp=require('./projects/site/node_modules/sharp');(async()=>{const [input,stem]=process.argv.slice(1);for(const size of [600,128,64])await sharp(input).resize(size,size,{fit:'inside'}).webp({quality:90}).toFile(stem+(size===600?'':'-'+size)+'.webp')})().catch(e=>{console.error(e);process.exit(1)});"
 subprocess.run(['/Users/ahimanikya/.nvm/versions/node/v24.15.0/bin/node','-e',script,str(target),stem],cwd=ROOT,check=True)
 mapping[str(i)]={'src':stem.removeprefix('projects/site/')+'.webp','kind':'generated_portrait','credit':'AI-assisted artistic portrait from the journal-supplied photograph','width':600,'height':600};write('projects/site/data/writer-portraits.json',mapping);d['web_asset']=mapping[str(i)]['src']
edits=read('kb/research/writers/portrait-edits.json');edits.append(entry);write('kb/research/writers/portrait-edits.json',edits)
d.update(status='retry_integrated_pending_verification' if outcome=='integrate' else 'retry_hold',master='kb/'+master,master_sha256=entry['master_sha256'],review=observation);write(rp,record)
print(i,d['status'])
