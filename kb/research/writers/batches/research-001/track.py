"""Maintain a distinct enrichment register without rewriting capture history."""
import json
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parents[5]
SITE = ROOT / 'projects/site'
KB = ROOT / 'kb/research/writers'

def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')

partials = {
    41: {
        'reason': 'Possible book and literary-event matches need stronger corroboration before adding them to the reader biography.',
        'leads': [
            {'url': 'https://www.lulu.com/shop/pravakar-satpathy/singhasan/ebook/product-1rgq8zwk.html', 'observation': 'Singhasan, Odia poetry by Pravakar Satpathy, EPUB dated 10 July 2011. Name and language alone do not establish identity.'},
            {'url': 'https://www.nbtindia.gov.in/writereaddata/attachment/monday-december-23-20132-56-45-pmnewsletter-jan-2014-for-web.pdf', 'observation': 'January 2014 newsletter page 4 reports editor and poet Pravakar Satpathi speaking at a November 2013 Jajpur reading event. Regional/editorial context is promising but not yet conclusive.'}
        ],
        'excluded_claims': [{'url': 'https://folkfair.in/awardees/', 'reason': 'Awardee is Capt. Pravakar Satpathy, former principal of SCS College, Puri. Identity not established; do not attribute the award.'}],
        'next_action': 'Corroborate Singhasan or Anisha editorship against the journal identity; existing user-supplied artistic portrait remains unchanged.'
    },
    377: {
        'reason': 'Hindi-language and regional matches are insufficient to distinguish this writer from namesakes.',
        'leads': [
            {'url': 'https://www.prabhatkhabar.com/state/bihar/gaya/vikramaditya-became-the-president-of-vishva-hindi-parishad/amp', 'observation': '2025 report names a railway official from Amas, Gaya, as Odisha Vishva Hindi Parishad president; no verified match to journal poems.'},
            {'url': 'https://pankhuris.com/author/vikramaditya-singh-pathik/', 'observation': 'Writer uses Pathik; relationship to Kabita Live contributor unconfirmed.'}
        ],
        'excluded_claims': ['Do not merge the Himachal politician of the same name.'],
        'next_action': 'Find a matching poem, collection title or author-controlled identity before enriching.'
    },
    233: {
        'reason': 'Chandigarh University affiliation has a plausible external match; book titles, portrait and journal contributions remain unresolved.',
        'leads': [
            {'url': 'https://elsaindia.blogspot.com/', 'observation': 'Literary-society author note describes Manju Chouhan as a professor at UILAH, Chandigarh University. Find stable article permalink before using as reader source.'},
            {'url': 'https://www.literaryvoiceglobal.in/index.php/files/issue/view/5', 'observation': 'January 2026 contents list a review by Dr Manju Chouhan, pp.48–49; full affiliation confirmation still needed.'}
        ],
        'excluded_claims': [],
        'next_action': 'Verify stable author note and book titles. Zero linked journal poems is an import/linking gap, not evidence of no literary output.'
    }
}
profiles = {p['id']: p for p in json.loads((SITE/'data/writer-profiles.json').read_text())}
works = {}
for file in (SITE/'content/editions').glob('*/poem-*.json'):
    poem = json.loads(file.read_text())
    ident = poem.get('writer_id')
    if ident is None:
        continue
    profiles.setdefault(ident, {'id': ident, 'name': poem['author']})
    works.setdefault(ident, []).append(poem['id'])
for ident, details in partials.items():
    save(KB/'enrichment'/f'{ident}.json', {
        'writer_id': ident, 'name': profiles[ident]['name'],
        'reviewed_on': '2026-10-01', 'status': 'research_partial_identity',
        'independent': False, 'batch': 'research-001', 'reader_changes': False,
        **details
    })

enrichment = json.loads((SITE/'data/writer-enrichment.json').read_text())
portraits = json.loads((SITE/'data/writer-portraits.json').read_text())
rows = []
for ident, p in sorted(profiles.items(), key=lambda x: x[1]['name'].casefold()):
    if ident in {1, 43}:
        continue
    path = KB/'enrichment'/f'{ident}.json'
    record = json.loads(path.read_text()) if path.exists() else {}
    rows.append({
        'writer_id': ident, 'name': p['name'],
        'research_status': record.get('status', 'pending'),
        'enriched_reader_draft': str(ident) in enrichment,
        'portrait_kind': portraits.get(str(ident), {}).get('kind', 'initials'),
        'linked_poems': len(set(works.get(ident, []))),
        'dossier': f'research/writers/enrichment/{ident}.json' if path.exists() else None,
        'next_action': record.get('next_action', 'Author/editor factual review pending.' if str(ident) in enrichment else 'Read supplied biography; identity-check external sources; enrich only supported details.')
    })
save(KB/'enrichment-progress.json', {
    'updated_on': '2026-10-01',
    'scope': '427 non-editor writer profiles; two editor profiles tracked separately.',
    'workflow': 'Research in small saved groups. Start with the review examples and recent contributors, then remaining contributors in directory order. No automatic workers. Mockups are review-only; author/editor factual review remains pending.',
    'capture_history': 'research-queue.json remains the historical capture queue, not the enrichment status register.',
    'counts': {'writers': len(rows), 'reader_drafts': len(enrichment), **dict(Counter(r['research_status'] for r in rows))},
    'writers': rows
})
print(f'Tracked {len(rows)} writers; {len(enrichment)} enriched drafts; {len(partials)} partial identity investigations.')
