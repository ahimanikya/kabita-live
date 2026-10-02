import json
from pathlib import Path
from save_writer import source
root=Path(__file__).resolve().parents[5]
p=root/'kb/research/writers/enrichment/150.json';d=json.loads(p.read_text())
u='https://www.hawakal.com/books/english-books/poetry-english-books/opera-poems/'
d['reader_draft']['books'].append(dict(title='Opera: poems',detail='Poetry; Hawakal Publishers, 2024.',url=u))
s=source('Hawakal Publishers — Opera: poems',u,'Author Sutanuka Ghosh Roy; English poetry;62pages;release5January2024;ISBN9788119858941.')
d['sources'].append(s);d['reader_draft']['sources'].append({k:s[k] for k in ['label','url']})
d['limitations']=[v for v in d['limitations'] if not v.startswith('Opera publication')]
d['limitations'].append('Setu author-page URL has2018 date but includes later book; do not infer original publication date from URL. Opera date from publisher metadata.')
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
p=root/'projects/site/data/writer-enrichment.json';r=json.loads(p.read_text());r['150']=d['reader_draft'];p.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
