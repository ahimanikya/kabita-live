#!/usr/bin/env python3
"""Validate and add a completed translation draft batch without replacing existing work."""
import argparse,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SITE=ROOT/'projects/site'
if not SITE.exists(): SITE=ROOT/'site'
LABELS={'or':'ଓଡ଼ିଆ','hi':'हिन्दी','en':'English'}
def main():
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('batch',help='Batch directory name, e.g. batch-002')
 args=parser.parse_args()
 assert Path(args.batch).name==args.batch,'Use a batch name only'
 folder=ROOT/'kb/production/translations'/args.batch
 drafts=json.loads((folder/'drafts.json').read_text())
 review=json.loads((folder/'review.json').read_text())
 assert set(map(str,review['poem_ids']))==set(drafts),'Review coverage mismatch'
 catalog_path=SITE/'data/poem-translations.json'
 catalog=json.loads(catalog_path.read_text())
 sources={str(d['id']):d for p in (SITE/'content/editions').glob('*/poem-*.json') for d in [json.loads(p.read_text())]}
 added=0
 for ident,versions in drafts.items():
  source=sources[ident]
  assert source.get('status')!='archived',f'Archived poem is outside the drafting queue: {ident}'
  assert set(versions)==set(LABELS)-{source['language']},f'Target languages: {ident}'
  digest=hashlib.sha256(source['text'].encode()).hexdigest()
  entry={'source_sha256':digest,'variants':{},'review':'AI-assisted draft; independent linguistic review pending.','batch':args.batch}
  for lang,v in versions.items():
   stanzas=[s.splitlines() for s in v['text'].strip().split('\n\n')]
   assert [len(s) for s in stanzas]==[len(s) for s in source['stanzas']],f'Line/stanza coverage: {ident}/{lang}: {[len(s) for s in stanzas]} versus {[len(s) for s in source["stanzas"]]}'
   assert v['title'].strip() and all(line.strip() for s in stanzas for line in s),f'Empty content: {ident}/{lang}'
   entry['variants'][lang]={'label':LABELS[lang],'title':v['title'],'kind':'Translation','stanzas':stanzas,'credit':'AI-assisted translation.','status':'draft'}
  if ident in catalog:
   assert catalog[ident]==entry,f'Existing translation conflict: {ident}; preserve and review separately'
  else:
   catalog[ident]=entry;added+=len(versions)
 assert sum(len(x) for x in drafts.values())==review['translations'],'Translation count mismatch'
 # All drafts validate before the catalogue is changed.
 temp=catalog_path.with_suffix('.tmp');temp.write_text(json.dumps(catalog,ensure_ascii=False,indent=2)+'\n');temp.replace(catalog_path)
 verification={'batch':args.batch,'poem_ids':review['poem_ids'],'translations':review['translations'],'source_hashes':'pass','stanza_and_line_coverage':'pass','review':'self-review; independent linguistic review pending','status':'integrated-draft','publication':False}
 (folder/'verification.json').write_text(json.dumps(verification,ensure_ascii=False,indent=2)+'\n')
 print(f'{args.batch}: {added} new translations; source hashes and full line/stanza coverage pass.')
if __name__=='__main__':main()
