from pathlib import Path
import json,hashlib,subprocess,datetime
R=Path('/Users/ahimanikya/Projects/Kabita Live');B=Path(__file__).resolve().parent
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
def read(p):return json.loads((R/p).read_text())
def write(p,d):(R/p).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
ids=[229,195,294,420,425,377];mapping=read('projects/site/data/writer-portraits.json');edits=read('kb/research/writers/portrait-edits.json');queue=read('kb/research/writers/portrait-batches.json');holds={x['writer_id']:x for x in queue['likeness_holds']}
base=B/'baseline.json'
if not base.exists():
 paths=set()
 for pat in ['projects/site/content/**/*.json','projects/site/data/*.json','projects/site/assets/writers/*','kb/artifacts/artwork/portrait-sources/writers/*','kb/artifacts/artwork/writer-portraits/*']:paths.update(p for p in R.glob(pat) if p.is_file())
 base.write_text(json.dumps({str(p.relative_to(R)):sha(p) for p in paths},indent=2)+'\n')
record={'recorded_at':now,'authorization':'Accept all candidate 2','scope':'Remaining likeness holds with an existing second generated candidate','status':'applied_pending_verification','decisions':[],'remaining_without_candidate_two':[150,227],'independent_author_editor_review':'User acceptance recorded; author/editor confirmation not claimed'}
script="const sharp=require('./projects/site/node_modules/sharp');(async()=>{const [input,stem]=process.argv.slice(1);for(const size of [600,128,64])await sharp(input).resize(size,size,{fit:'inside'}).webp({quality:90}).toFile(stem+(size===600?'':'-'+size)+'.webp')})().catch(e=>{console.error(e);process.exit(1)});"
for i in ids:
 rows=[e for e in edits if e['writer_id']==i and e.get('status')=='rejected_candidate'];assert len(rows)==2
 e=rows[1];p=R/'kb'/e['master'];assert 'v2' in p.name and sha(p)==e['master_sha256'];old=mapping[str(i)];assert old['kind']=='journal_photo'
 stem=f'projects/site/assets/writers/{i}-user-selected-candidate2-20261004';assert not (R/(stem+'.webp')).exists()
 subprocess.run(['/Users/ahimanikya/.nvm/versions/node/v24.15.0/bin/node','-e',script,str(p),stem],cwd=R,check=True)
 mapping[str(i)]={'src':stem.removeprefix('projects/site/')+'.webp','kind':'generated_portrait','credit':'AI-assisted artistic portrait from the journal-supplied photograph','width':600,'height':600}
 new=dict(e);new.update(status='user_approved_integrated_pending_build',previous_asset=old,user_review={'reviewer':'Ahimanikya Satapathy','decision':'Accept all candidate 2','candidate':2},review='User accepted saved Candidate2; original concern retained: '+holds[i]['reason'],verification_batch='accepted-candidate-two-2026-10-04',verification='pending',independent_likeness_review='User acceptance recorded; author/editor confirmation not claimed');edits.append(new)
 record['decisions'].append({'writer_id':i,'name':holds[i]['name'],'candidate':2,'master':'kb/'+e['master'],'master_sha256':e['master_sha256'],'prior_hold':holds[i],'web_asset':mapping[str(i)]['src'],'status':'integrated_pending_verification'})
 write('projects/site/data/writer-portraits.json',mapping);write('kb/research/writers/portrait-edits.json',edits);write('kb/records/accepted-candidate-two-2026-10-04.json',record)
print('Applied six saved Candidate2 portraits')
