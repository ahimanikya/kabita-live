#!/usr/bin/env python3
"""Generate a whole-project discovery catalogue from live KB concepts.
Created for Ahimanikya Satapathy with AI assistance. Archives are excluded.
"""
import json,re,argparse
from pathlib import Path
from check_bundle import ARCHIVES
root=Path(__file__).resolve().parents[1]/'kb'
def generate():
    rows=[]
    for p in sorted(root.rglob('*.md')):
        rel=p.relative_to(root).as_posix()
        if rel.startswith(ARCHIVES) or p.name in ['index.md','log.md']:continue
        text=p.read_text();head=text.split('\n---',1)[0]
        def field(key):
            m=re.search(r'^'+key+r':\s*(.+)$',head,re.M)
            if not m:return ''
            try:return json.loads(m[1])
            except ValueError:return m[1].strip('"\'')
        rows.append({'id':rel[:-3],'path':rel,'type':field('type'),'title':field('title') or p.stem})
    return json.dumps(rows,ensure_ascii=False,indent=2)+'\n'
if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--check',action='store_true');args=parser.parse_args();p=root/'catalog.json';text=generate()
    if args.check:
        if not p.exists() or p.read_text()!=text:raise SystemExit('Catalogue is stale; regenerate')
    else:p.write_text(text)
    print('Whole-project catalogue current: '+str(len(json.loads(text)))+' concepts')
