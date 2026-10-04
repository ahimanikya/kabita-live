"""Verify closing-mark coverage against the pre-change reader and current sources."""
from pathlib import Path
import json,hashlib,re,sys
r=next(p for p in Path(__file__).resolve().parents if (p/'utkal.config.json').is_file());s=r/'projects/site';ev=Path(__file__).parent
sys.path.insert(0,str(s));old={'__file__':str(s/'poem_reader.py')};exec(compile((ev/'before/poem_reader.py').read_text(),'before-poem-reader','exec'),old)
base=json.loads((ev/'source-hashes-before.json').read_text())
assert all(hashlib.sha256((s/p).read_bytes()).hexdigest()==h for p,h in base.items())
source={p['id']:p for f in (s/'content/editions').glob('*/poem-*.json') for p in [json.loads(f.read_text())]}
poems=json.loads((s/'assets/reading-all.json').read_text())['poems'];counts={};variants=0
for p in poems:
 before=json.loads(re.search(r'id="reading-data">(.*?)</script>',old['render_reader'](source[p['id']]),re.S)[1])
 assert p['source_language']==before['source_language'] and p['variants'].keys()==before['variants'].keys()
 for code,v in p['variants'].items():
  for key in before['variants'][code]:assert v[key]==before['variants'][code][key],(p['id'],code,key)
  variants+=1
 for root in [s,s/'dist']:
  html=(root/p['route']).read_text();marks=re.findall(r'class="poem-closing-mark" data-end-mark="([a-z]+)" aria-hidden="true"',html)
  assert marks==([] if p['availability'] else [p['end_mark']]),(root,p['id'])
 counts[p['end_mark']]=counts.get(p['end_mark'],0)+1
for f in list((s/'assets/reading-editions').glob('*.json'))+list((s/'assets/reading-authors').glob('*.json')):
 for p in json.loads(f.read_text())['poems']:
  assert p['end_mark']==next(x['end_mark'] for x in poems if x['id']==p['id'])
for name in ['leaf','paired','sprig']:assert (s/f'dist/assets/poem-end-{name}.svg').read_bytes()==(s/f'assets/poem-end-{name}.svg').read_bytes()
result={'result':'PASS','poems':len(poems),'language_variants_unchanged':variants,'assignment_counts':counts,'protected_data_hashes_unchanged':len(base),'incomplete_poem_385':'No closing mark','coverage':'Standalone preview/public pages and all edition/poet/all-poem reader payloads','vector_export':'All three assets present and byte-identical in public build'}
(ev/'verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
