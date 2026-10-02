import hashlib,html,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5]; SITE=ROOT/'projects/site'; HERE=Path(__file__).parent
read=lambda p:json.loads(p.read_text())
originals=read(HERE/'preserved-inputs.json');before=read(HERE/'enrichment-before.json');current=read(SITE/'data/writer-enrichment.json')
for rel,digest in originals.items():assert hashlib.sha256((SITE/rel).read_bytes()).hexdigest()==digest,rel
for ident,record in before.items():assert current[ident]==record,ident
ids=[194,178,174,171,170]
for ident in ids:
 entry=current[str(ident)];page=(SITE/f'poet-{ident}.html').read_text()
 for section in entry['sections']:
  for para in section['paragraphs']:assert html.escape(para) in page,(ident,para)
 assert read(ROOT/f'kb/research/writers/enrichment/{ident}.json')['reader_draft']==entry
report={'batch':'research-007','status':'verified','independent':False,'writer_ids':ids,'reader_drafts':5,'externally_corroborated':4,'source_limited':[194],'checks':{'public_build':'passed','author_pages':'PASS','editions':'PASS','preserved_source_files':len(originals),'existing_narratives_preserved':len(before),'rendered_narratives':len(ids)},'limitations':['Ananya Goswami remains source-limited: no confidently matched external identity.','Library, news and government sources with direct-access failures recorded as indexed evidence.','No independent factual review; author/editor review pending. No design, portrait or original-poem changes.'],'resume':'research-008','publication':'No deployment or push.'}
(HERE/'review.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,indent=2))
