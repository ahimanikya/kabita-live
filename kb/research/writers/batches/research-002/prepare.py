"""Source-grounded narrative drafts; no changes to source records or artwork."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
SITE = ROOT/'projects/site'
HOME = ROOT/'kb/research/writers'
DATE = '2026-10-01'

def source(label, url, supports, access='indexed_page_text'):
    return dict(label=label, url=url, supports=supports, access=access, accessed_on=DATE)

entries = {
  41: {
    'paragraphs': [
      'Pravakar Satapathy is an Odia poet and editor associated with Jajpur. His journal contributor note records his earlier editorship of the literary magazine Anisha. National Book Trust’s account of a 2013 programme in Jajpur names him among the speakers on encouraging reading in rural communities.',
      'His Kabita Live poem ମୋ କବିତା approaches poetry through images of a flower and an opening temple doorway, inviting the reader towards recognition rather than explanation. In ଟାଣ କଥା ପଦକ, a harmonium, a harsh word and the lingering mark of hurt bring the difficulty of tenderness into focus.'
    ],
    'sources': [source('National Book Trust · January 2014 newsletter, p.4', 'https://www.nbtindia.gov.in/writereaddata/attachment/monday-december-23-20132-56-45-pmnewsletter-jan-2014-for-web.pdf', ['Poet/editor role; 15 November 2013 reading-promotion discussion in Jajpur'], 'opened_pdf')],
    'identity_match': 'Name variant Satpathi, poet/editor role and Jajpur literary context match the supplied contributor identity and local poem22 signature. This does not establish every same-name book or award.',
    'local_basis': {'biography': 'Anisha editorship from preserved journal biography; not independently established.', 'poems_read': [22,494], 'interpretation': 'Second paragraph is close reading of these two poems, not a claim about the writer\u2019s whole oeuvre or personal experiences.'},
    'limitations': ['Singhasan (Lulu,2011), Gharatola (state bibliography,2007) and Antarman (library catalogue,2015) remain book leads, not confirmed reader bibliography.', 'Do not attribute the Folkfair award to Capt. Pravakar Satpathy, whose identity is not established.'],
    'next_action': 'Corroborate collection titles and Anisha history; retain existing user-supplied artistic portrait.'
  },
  377: {
    'paragraphs': [
      'Vikramaditya Singh writes in Hindi. His contributor biography records poetry collections and the publication of poems, short stories and essays in literary journals.',
      'His poems in Kabita Live range from the cultural landscape of Odisha to the intimate struggle to speak against suffering. मैं ओड़िशा हूं brings temples, rivers, weaving and food into a portrait of the state. इरादे बुलंद कर लेती तो अच्छा था addresses a woman burdened by silence and urges her towards a more assertive voice.'
    ],
    'sources': [],
    'status': 'source_limited_local_draft',
    'identity_match': 'Local writer377 and poem membership are verified; external poet/railway-official identity is still not tied to a matching journal work or biographical anchor.',
    'local_basis': {'biography': 'Literary forms and unnamed collections from preserved contributor record, explicitly attributed.', 'poems_read': [551,530], 'interpretation': 'The two named works directly support the discussion; no external appointment, award or named book is asserted.'},
    'limitations': ['Aadhe-Adhure Hum-Tum (2023) and Pukar Suno have a plausible same-name Bhubaneswar poet-author, but journal identity cannot yet be established.', 'No external sources are linked on the reader page because they remain unconfirmed identity leads.'],
    'leads': [source('Google Books · Aadhe-Adhure Hum-Tum author note','https://books.google.com/books?id=RM_qEAAAQBAJ',['Candidate author is a Hindi poet and East Coast Railway employee; needs identity confirmation'])],
    'next_action': 'Confirm whether the journal contributor wrote Aadhe-Adhure Hum-Tum and Pukar Suno. Keep external identity research open.'
  },
  233: {
    'paragraphs': [
      'Manju Chouhan is a poet, literary critic and English-literature academic whose contributor notes identify her with Chandigarh University. Her writing spans poetry, research and the close reading of other writers’ work.',
      'Her poem Moon and Me appears in Poetic Anthology WPC-5, where the changing moon becomes a companion and a mirror for the speaker. Literary Voice published her review of Rupa Rao’s A Poetic Odyssey: Life and Legacy of Dr. Jernail S. Anand in its 2026 volume, adding literary biography to the subjects of her critical writing.'
    ],
    'sources': [
      source('Poetic Anthology WPC-5 · Moon and Me, p.77','https://www.debracollege.ac.in/booksTeacher/123525Poetic%20Anthology%20WPC-5.pdf',['Poem, author name and Chandigarh University biography']),
      source('Literary Voice · A Poetic Odyssey review','https://literaryvoiceglobal.in/index.php/files/article/view/199',['Review authorship, English faculty affiliation and2026 volume'])
    ],
    'identity_match': 'Full name, English-literature academic role and Chandigarh University agree across the journal, anthology and scholarly review.',
    'local_basis': {'biography': 'University association corroborated externally; no current job rank asserted.', 'poems_read': [], 'interpretation': 'Moon comparison grounded in the anthology poem read in indexed source text; no external poem imported into Kabita Live.'},
    'limitations': ['Two supplied poetry-collection titles remain unknown; do not claim the unrelated same-name Marathi yoga book.', 'No Kabita Live poems are linked; do not add external poems to its contribution count.', 'Direct PDF retrieval failed and Literary Voice returned cache miss; indexed source text was available.'],
    'next_action': 'Identify collection titles, source portrait and missing journal contribution links; retain initials meanwhile.'
  },
  433: {
    'paragraphs': [
      'Annwesa Abhipsa Pani writes poetry alongside work in organisation and people development. Her contributor account in Borderless connects her literary practice with the study of English literature and records her association with Pune.',
      'Borderless published her poem Alive in December 2025. In Kabita Live, The Last Cartographer imagines memory as a way of mapping the lives of loved ones, while The Girl Who Walks in My Ink asks what writing can do in the face of a young girl’s death. Both poems give silence and absence a vivid physical presence.'
    ],
    'sources': [source('Borderless · Alive and contributor note, December 2025','https://borderlessjournal.com/tag/english/page/5/',['Named publication; organisation/people development; literary study and Pune context'])],
    'identity_match': 'Exact full name, Pune context, English-literature study and organisation/people-development profession match the journal contributor note.',
    'local_basis': {'poems_read': [677,768], 'interpretation': 'Second paragraph comments on the two actual local works; it does not imply autobiography.'},
    'limitations': ['No verified standalone collection in this pass; do not invent a selected-books section.', 'Source is an indexed journal archive page; a stable individual-poem permalink remains to verify.'],
    'next_action': 'Verify a stable Borderless permalink when accessible; author/editor factual review pending.'
  },
  415: {
    'paragraphs': [
      'Arun Sahu, also published as Arun Kumar Sahu, is a diplomat and bilingual writer in Odia and English. His work includes essays, fiction and poetry. His English publications include Iguana and Other Poems (2020) and Trinidad and Tobago: A Diplomat’s Cultural Expedition (2022).',
      'Light Green Eyes appeared in an English–Bulgarian edition from Academia Znanie in 2025, with Bulgarian translations by Zdravka Evtimova. His Kabita Live poem The Spring turns an ordinary act of hospitality—a fire and a cup of tea for a stranger—into an unexpected change of season.'
    ],
    'sources': [
      source('Embassy of India, Sofia · Arun Kumar Sahu biography','https://www.indembsofia.gov.in/page/ambassador-profile/',['Diplomat identity, two writing languages and named English publications']),
      source('National Library of Bulgaria · 2026 bibliography, entry82','https://nationallibrary.bg/BNB/s01/s01_2026_kn21.html',['Light Green Eyes,2025 publisher and translation from English by Zdravka Evtimova']),
      source('University of Economics–Varna · poetry meeting','https://www.ue-varna.bg/en/news/h-e-arun-kumar-sahu-the-ambassador-of-india-to-bulgaria-is-meeting-with-students/4100',['Bilingual English–Bulgarian edition'])
    ],
    'identity_match': 'Diplomat profession and Odia/English writing match the journal note and Embassy biography; excludes the same-name Odisha politician.',
    'local_basis': {'poems_read': [598], 'interpretation': 'Closing sentence describes the action and imagery of The Spring.'},
    'limitations': ['University announcement mistakenly says translation into English; National Library explicitly records translation from English into Bulgarian and takes precedence.', 'No verified book-specific public destination selected; titles remain in biography rather than linking unrelated pages.', 'Embassy direct fetch timed out; indexed official biography used.'],
    'next_action': 'Find stable book-specific publisher destinations; author/editor factual review pending.'
  }
}

if __name__ == '__main__':
    profiles = {p['id']: p for p in json.loads((SITE/'data/writer-profiles.json').read_text())}
    current = json.loads((SITE/'data/writer-enrichment.json').read_text())
    for ident, item in entries.items():
        reader = {'sections': [{'heading': 'Life and writing.', 'language': 'en', 'paragraphs': item['paragraphs']}], 'books': [], 'sources': [{k:s[k] for k in ['label','url']} for s in item['sources']], 'reviewed_on': DATE}
        record = {'writer_id': ident, 'name': profiles[ident]['name'], 'reviewed_on': DATE, 'batch': 'research-002', 'status': item.get('status','source_checked_local_draft'), 'independent': False, 'portrait_action': 'unchanged', 'reader_draft': reader, **{k:v for k,v in item.items() if k not in ['paragraphs','status']}}
        record['limitations'].append('Same-assistant research; author/editor factual review pending.')
        (HOME/'enrichment'/f'{ident}.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
        current[str(ident)] = reader
        (SITE/'data/writer-enrichment.json').write_text(json.dumps(current,ensure_ascii=False,indent=2)+'\n')
        print('Saved writer',ident)
