"""Pin the aggregate backend allowlist to the verified public build. Never deploy."""
import argparse,json,sys
from pathlib import Path
root=Path(__file__).resolve().parents[3]
p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');p.add_argument('--runtime',type=Path,default=root/'projects/site/.public/runtime-config.json');args=p.parse_args()
sys.path.insert(0,str(root/'tools'))
from check_audience_release import public_pages
runtime=json.loads(args.runtime.read_text())
pages=public_pages(runtime['audience']['publicPages'])
assert pages and all(not any(token in path for token in ('proof','review','submit','editor-workspace','editor-management','search')) for path in pages)
target=root/'kb/production/editorial-service/backend/audience-pages.json'
content=json.dumps(dict(sorted(pages.items())),ensure_ascii=False,indent=2)+'\n'
if args.check:
 if target.read_text()!=content:raise SystemExit('Aggregate route manifest drift; run prepare.py after the verified public build')
else:target.write_text(content)
print(f'Aggregate public-route manifest: {len(pages)} paths; no deployment')
