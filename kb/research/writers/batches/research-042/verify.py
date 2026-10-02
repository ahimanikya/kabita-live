import json,hashlib,html
from pathlib import Path
b=Path(__file__).resolve().parent;root=b.parents[4];site=root/'projects/site'
hashes=json.loads((b/'preserved-inputs.json').read_text())
for p,h in hashes.items():assert hashlib.sha256((site/p).read_bytes()).hexdigest()==h,p
old=json.loads((b/'enrichment-before.json').read_text());new=json.loads((site/'data/writer-enrichment.json').read_text())
for k,v in old.items():assert new[k]==v,k
for i in [139,138,116,115,110]:
 d=json.loads((root/f'kb/research/writers/enrichment/{i}.json').read_text());assert d['reader_draft']==new[str(i)]
 page=(site/f'poet-{i}.html').read_text()
 for s in new[str(i)]['sections']:
  for p in s['paragraphs']:assert html.escape(p) in page,(i,p)
r=dict(batch='research-042',status='verified',independent=False,writer_ids=[139,138,116,115,110],reader_drafts=5,externally_corroborated=3,source_limited=[116,115],checks=dict(public_build='passed',author_pages='PASS',editions='PASS',preserved_source_files=len(hashes),existing_narratives_preserved=len(old),rendered_narratives=5,browser_visual='Not repeated; prose/data only, approved renderer unchanged.'),limitations=['Independent author/editor review pending.','116 and 115 have no captured biography or secure external identity bridge; literary introductions only, candidate sources retained in KB.','138 external byline is Madhumita Dash; preferred reader name unchanged pending editor confirmation.','139 source text available through indexed excerpts; direct retrieval failed.','110 mortality poem treated as a speaker narrative, not author health evidence.'],resume='research-043',publication='No deployment or push.')
(b/'review.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
p=root/'kb/research/writers/enrichment-batches.json';d=json.loads(p.read_text())
for item in d['batches']:
 if item['id']==r['batch']:item['verification']='passed'
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n');print(r)
