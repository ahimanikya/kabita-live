"""Assign only dedicated poem artwork, retaining stable choices between builds."""
from pathlib import Path
import json, hashlib
R=Path(__file__).resolve().parents[1]/'projects/site'
path=R/'data/poem-art-assignments.json'
library=json.loads((R/'data/poem-art-library.json').read_text())['artworks']
pool=[x['id'] for x in library]
assert pool and all(x['src'].startswith('assets/poem-art/') for x in library)
doc=json.loads(path.read_text()) if path.exists() else {}
# Earlier cover reuse was rejected by the user and preserved in KB history.
assigned=doc.get('assignments',{}) if doc.get('version')==2 else {}
issues=json.loads((R/'content/editions/index.json').read_text())
issues.append({'number':'unassigned','poem_ids':json.loads((R/'content/editions/unassigned/index.json').read_text())})
for issue in issues:
    ids=[str(i) for i in issue['poem_ids'] if i not in (809,810,814)]
    used=set();previous=None
    for ident in ids:
        if assigned.get(ident) not in pool:
            available=[n for n in pool if n not in used and n!=previous]
            if not available:
                used=set();available=[n for n in pool if n!=previous]
            assigned[ident]=min(available,key=lambda n:hashlib.sha256(f'poem-only:{ident}:{n}'.encode()).hexdigest())
        used.add(assigned[ident]);previous=assigned[ident]
        if len(used)==len(pool):used=set()
doc={'version':2,'policy':'Poem-only artwork, stable per poem; vary before repeating and never repeat adjacent artwork. Three dedicated illustrations remain pinned. Covers are excluded.','assignments':assigned}
path.write_text(json.dumps(doc,ensure_ascii=False,indent=2)+'\n')
print(f'{len(assigned)} stable assignments from {len(pool)} dedicated poem artworks; three bespoke illustrations retained.')
