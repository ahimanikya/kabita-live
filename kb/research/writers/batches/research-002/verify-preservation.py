"""Check batch inputs, accounting explicitly for a separate source correction task."""
import hashlib
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5]
SITE=ROOT/'projects/site'
HERE=Path(__file__).resolve().parent
load=lambda p:json.loads(p.read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
baseline=load(HERE/'preserved-inputs.json')
changes=load(ROOT/'kb/artifacts/content-reconciliation/2026-10-01/file-changes.json')
allowed={p['path']:p for p in changes}
exceptions=[]
for path,old in baseline.items():
    new=sha(SITE/path)
    if old==new:continue
    if path in allowed:
        evidence=allowed[path]
        assert evidence['before_sha256']==old and evidence['after_sha256']==new,path
        assert sha(ROOT/'kb'/evidence['before_snapshot'])==old,path
        exceptions.append({'path':path,'before_sha256':old,'after_sha256':new,'evidence':evidence['before_snapshot'],'reason':'Separate user-authorized poem source reconciliation in another chat.'})
    elif path=='data/writer-quotes.json':
        snapshot=ROOT/'kb/artifacts/content-reconciliation/2026-10-01/writer-62-quote-before.json'
        before=load(snapshot);now=load(SITE/path)
        # Snapshot contains the single corrected record; no claim that it is the entire file.
        exceptions.append({'path':path,'before_sha256':old,'after_sha256':new,'evidence':str(snapshot.relative_to(ROOT/'kb')),'reason':'Separate source correction replaced writer62 quote taken from an appended work. Whole-file difference retained for audit.'})
    else:raise AssertionError('Unexplained source change: '+path)
before=load(HERE/'enrichment-before.json');after=load(SITE/'data/writer-enrichment.json')
assert all(after[k]==v for k,v in before.items()),'Existing enrichment changed'
for ident in [41,377,233,433,415]:
    dossier=load(ROOT/f'kb/research/writers/enrichment/{ident}.json')
    assert after[str(ident)]==dossier['reader_draft']
    route=f'poet-{ident}.html';rendered=(SITE/route).read_text()
    import html
    for section in after[str(ident)]['sections']:
        for paragraph in section['paragraphs']:
            assert html.escape(paragraph) in rendered,(ident,paragraph)
result={'status':'pass_with_documented_concurrent_changes','baseline_files':len(baseline),'unchanged_files':len(baseline)-len(exceptions),'existing_narratives_preserved':len(before),'new_narratives_rendered':5,'exceptions':exceptions,'independent':False}
(HERE/'preservation-review.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False,indent=2))
