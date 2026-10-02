"""Create stable five-writer batches and refresh research progress from dossiers."""
import json
from collections import Counter
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'projects/site'
HOME = ROOT / 'kb/research/writers'

def read(path):
    return json.loads(path.read_text())

def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')

profiles = {p['id']: p for p in read(SITE/'data/writer-profiles.json')}
works = {}
for file in sorted((SITE/'content/editions').glob('*/poem-*.json')):
    poem = read(file)
    ident = poem.get('writer_id')
    if ident is None:
        continue
    profiles.setdefault(ident, {'id': ident, 'name': poem['author']})
    if poem.get('status') != 'archived':
        works.setdefault(ident, set()).add(poem['id'])
writers = [i for i in profiles if i not in {1, 43}]
enrichment = read(SITE/'data/writer-enrichment.json')
portraits = read(SITE/'data/writer-portraits.json')
manifest = HOME/'enrichment-batches.json'
if manifest.exists():
    plan = read(manifest)
else:
    existing = [i for i in writers if str(i) in enrichment]
    remaining = [i for i in [41, 377, 233] if i not in existing]
    remaining += [i for i in writers if i not in existing and i not in remaining]
    plan = {
        'created_on': '2026-10-01', 'batch_size': 5,
        'authorization': 'create batch and then do one batch at a time - let\u2019s enrich each one of them',
        'scope': 'All 427 non-editor writers; editor profiles remain separate.',
        'previously_enriched': existing,
        'order': 'Resume three partial investigations, then captured directory order; archive-discovered writers follow. Membership is stable after creation.',
        'workflow': [
            'One batch at a time; no parallel writers or agents. Save each writer dossier before proceeding.',
            'Read captured biography and relevant original poems. Research author, publisher, university and literary sources; verify identity beyond the name.',
            'Preserve captured biography, poem texts, translations, portraits, selected quotes and approved design. No new portrait or layout changes in narrative batches.',
            'Write concise supported narrative; record claim basis, source access, contradictions and rejected namesakes. Never invent books, awards or appointments.',
            'Record source-limited enrichment separately from external corroboration. Unresolved cases stay open in follow-up tracking; finish other writers.',
            'Integrate sourced drafts with credits in the central colophon. Build and run author, edition and source-preservation checks before closing batch verification.',
            'Refresh this register, activity ledger, catalogue and handoff. Proceed to next batch without a new batch approval. Never publish or push.',
            'All drafts need author/editor factual review. A researched batch is not proof that every source question is resolved.'
        ],
        'batches': [{'id': f'research-{n+2:03d}', 'writer_ids': remaining[n*5:n*5+5], 'verification': 'pending'} for n in range((len(remaining)+4)//5)]
    }

rows = []
for ident in writers:
    path = HOME/'enrichment'/f'{ident}.json'
    dossier = read(path) if path.exists() else {}
    rows.append({
        'writer_id': ident, 'name': profiles[ident]['name'],
        'research_status': dossier.get('status', 'pending'),
        'enriched_reader_draft': str(ident) in enrichment,
        'portrait_kind': portraits.get(str(ident), {}).get('kind', 'initials'),
        'linked_poems': len(works.get(ident, [])),
        'dossier': f'research/writers/enrichment/{ident}.json' if path.exists() else None,
        'next_action': dossier.get('next_action', 'Author/editor factual review pending.' if str(ident) in enrichment else 'Identity-check and research sources; enrich supported details.')
    })
by_id = {r['writer_id']: r for r in rows}
finished = {'source_checked_local_draft', 'source_limited_local_draft', 'research_hold'}
for batch in plan['batches']:
    states = [by_id[i]['research_status'] for i in batch['writer_ids']]
    batch['writers'] = [{'id': i, 'name': profiles[i]['name'], 'status': by_id[i]['research_status']} for i in batch['writer_ids']]
    batch['status'] = ('verified' if batch['verification'] == 'passed' else 'awaiting_verification') if all(s in finished for s in states) else ('in_progress' if any(s != 'pending' for s in states) else 'pending')
    batch['unresolved_writer_ids'] = [i for i in batch['writer_ids'] if by_id[i]['research_status'] in {'source_limited_local_draft', 'research_hold', 'research_partial_identity'}]
assigned = plan['previously_enriched'] + [i for b in plan['batches'] for i in b['writer_ids']]
assert len(assigned) == len(set(assigned)) == 427
assert set(assigned) == set(writers)
plan['counts'] = {'writers': len(writers), 'previously_enriched': len(plan['previously_enriched']), 'batches': len(plan['batches']), 'enriched_reader_drafts': len(enrichment), **dict(Counter(b['status'] for b in plan['batches']))}
plan['next_batch'] = next((b['id'] for b in plan['batches'] if b['status'] != 'verified'), None)
save(manifest, plan)
save(HOME/'enrichment-progress.json', {
    'updated_on': date.today().isoformat(), 'scope': plan['scope'],
    'batch_register': 'research/writers/enrichment-batches.json',
    'capture_history': 'research-queue.json is historical capture evidence, not enrichment progress.',
    'counts': {'writers': len(writers), 'reader_drafts': len(enrichment), **dict(Counter(r['research_status'] for r in rows))},
    'writers': sorted(rows, key=lambda r: r['name'].casefold())
})
print(json.dumps({'counts': plan['counts'], 'next_batch': plan['next_batch']}, indent=2))
loop_path = ROOT/'kb/records/writer-enrichment-loop.json'
loop_status = read(loop_path).get('setup_status', 'UNKNOWN') if loop_path.exists() else 'UNKNOWN'
execution_note = ('The writer-enrichment heartbeat is paused after the draft pass; independent author/editor review and source-limited follow-up remain open.'
                  if loop_status == 'PAUSED' and plan['next_batch'] is None else
                  f'Writer-enrichment heartbeat status: {loop_status}. Resume only within its recorded authorization.')
lines = [
    '---', 'type: "Research workflow register"', 'title: "Writer enrichment batches"', '---', '',
    '# Writer enrichment batches', '',
    'One batch at a time. Research records and sourced narrative drafts are saved per writer; each batch closes only after its checks pass. Layout approval and portrait generation remain separate.', '',
    f"**{len(enrichment)} of 427** writers have enriched reader drafts. {427-len(enrichment)} remain. These drafts still need author/editor factual review.", '',
    'The 15 previously enriched profiles are preserved. The remaining 412 are assigned to 83 stable batches of up to five. Source-limited cases stay visible for follow-up; completion of a batch does not certify every biographical claim independently.', '',
    f'**Execution:** {execution_note} One batch at a time; no overlapping workers or subagents. Authorization: `kb/records/writer-enrichment-loop.json`. Do not resume the historical research-001 preparation script over newer dossiers.', '',
    f"**Resume:** {plan['next_batch'] or 'All batches verified'}. Finish its verification before selecting another batch.", '',
    '| Batch | Writers | Status | Follow-up |',
    '| --- | --- | --- | --- |'
]
for batch in plan['batches']:
    names = '; '.join(profiles[i]['name'].split('/')[0].strip() for i in batch['writer_ids'])
    follow = ', '.join(str(i) for i in batch['unresolved_writer_ids']) or '—'
    lines.append(f"| {batch['id']} | {names} | {batch['status'].replace('_',' ')} | {follow} |")
lines += ['', 'Status is generated from the canonical dossiers and verification records. Source notes, unresolved identity leads and attribution remain in the KB; public references are consolidated in Our Story.']
(HOME/'ENRICHMENT-BATCHES.md').write_text('\n'.join(lines)+'\n')
