from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[4];O=Path(__file__).parent
A=json.loads((R/'kb/research/writers/audit-2026-10-01/findings.json').read_text());E=json.loads((R/'projects/site/data/writer-enrichment.json').read_text());C={str(p['id']):p for p in json.loads((R/'projects/site/data/writer-profiles.json').read_text())}
rows=[]
decision_path=R/'kb/research/writers/audit-2026-10-01/applied-decisions.json'
applied=json.loads(decision_path.read_text()) if decision_path.exists() else {}
for p in A['profiles']:
 i=str(p['writer_id']);d=json.loads((R/p['dossier']).read_text());e=E[i]
 route={82:'poet-dokana.html',257:'poet-drink.html',337:'poet-kshanika.html'}.get(int(i),f'poet-{i}.html')
 assert (R/'projects/site'/route).exists(),route
 rows.append(dict(id=i,name=d.get('display_name',p['name']),route=route,enrichment=e,original=C.get(i,{}).get('biography',''),flags=p['screening_flags'],findings=[f for f in A['findings'] if int(i) in f['writer_ids']],sources=d.get('sources',[]),limitations=d.get('limitations',[]),hash=hashlib.sha256(json.dumps(e,sort_keys=True,ensure_ascii=False).encode()).hexdigest()))
data=json.dumps({'schema':1,'audit':'writer-audit-2026-10-01','counts':A['counts'],'profiles':rows,'applied_decisions':applied},ensure_ascii=False).replace('<','\\u003c').replace('\u2028','\\u2028').replace('\u2029','\\u2029')
html=(O/'template.html').read_text().replace('/*REVIEW_SCRIPT*/',(O/'review.js').read_text()).replace('<!--REVIEW_DATA-->',data)
(O/'writer-audit-review.html').write_text(html)
p=R/'projects/site/writer-audit-review.html'
import os
if not p.exists():p.symlink_to(os.path.relpath(O/'writer-audit-review.html',p.parent.resolve()))
assert p.is_symlink()
print(f'Review generated: {len(rows)} profiles; {len(A["findings"])} findings; public export excludes review symlink.')
