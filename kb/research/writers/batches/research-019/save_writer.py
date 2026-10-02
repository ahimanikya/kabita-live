import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5];SITE=ROOT/'projects/site';HOME=ROOT/'kb/research/writers';DATE='2026-10-01'
def source(label,url,supports,access='opened_page'):
 return dict(label=label,url=url,supports=supports,access=access,accessed_on=DATE)
def save(ident,item):
 profiles={p['id']:p for p in json.loads((SITE/'data/writer-profiles.json').read_text())}
 current=json.loads((SITE/'data/writer-enrichment.json').read_text())
 if str(ident) in current:raise RuntimeError(f'Refuse overwrite {ident}')
 reader={'sections':[{'heading':'Life and writing.','language':'en','paragraphs':item['paragraphs']}],'books':item.get('books',[]),'sources':[{k:s[k] for k in ['label','url']} for s in item['sources']],'reviewed_on':DATE}
 record={'writer_id':ident,'name':profiles[ident]['name'],'reviewed_on':DATE,'batch':'research-019','status':item.get('status','source_checked_local_draft'),'independent':False,'portrait_action':'unchanged','reader_draft':reader,**{k:v for k,v in item.items() if k not in ['paragraphs','books','status']}}
 record['limitations'].append('Same-assistant research and close reading; independent author/editor factual review pending.')
 (HOME/'enrichment'/f'{ident}.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n');current[str(ident)]=reader;(SITE/'data/writer-enrichment.json').write_text(json.dumps(current,ensure_ascii=False,indent=2)+'\n');print('Saved',ident)
