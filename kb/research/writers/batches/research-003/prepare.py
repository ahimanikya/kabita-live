"""Research batch003. Run only to integrate the reviewed five-writer draft set."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5]
SITE=ROOT/'projects/site'
HOME=ROOT/'kb/research/writers'
DATE='2026-10-01'
def source(label,url,supports,access='opened_page'):
 return dict(label=label,url=url,supports=supports,access=access,accessed_on=DATE)
entries={
398:{'paragraphs':[
'Aishwariya Laxmi is an author, poet, editor and book blogger based in Chennai. Her debut collection, Birds of Paradise: Poems on Life, Liberty, and the Pursuit of Happiness, was published by Alien Buddha Press in 2024. Her website, Aishwariya’s LittLog, brings together her poetry, book reviews and reflections on writing.',
'In her Kabita Live poem I’m a writer, the work of writing includes the thinking that remains invisible to others. Its conversational lines turn questions of showing and telling into a gentler reminder: a writer’s worth cannot be measured by how much of that effort is seen.'
], 'books':[{'title':'Birds of Paradise: Poems on Life, Liberty, and the Pursuit of Happiness','detail':'Poetry · Alien Buddha Press, 2024','url':'https://aishwariyalaxmi.com/birds-of-paradise/'}],
'sources':[source('Aishwariya’s LittLog · Birds of Paradise','https://aishwariyalaxmi.com/birds-of-paradise/',['Author, Chennai, writing/editing/blogging and publisher']),source('Aishwariya’s LittLog · collection review, December2024','https://aishwariyalaxmi.com/2024/12/10/review-of-my-debut-book-by-candice-louisa-daquin/',['Full book title and2024 publication'],'indexed_page_text')],
'identity_match':'Exact name, Chennai, exact debut title and author website agree with the preserved contributor note.','poems_read':[565],
'limitations':['No aggregate anthology counts or promotional review praise repeated. The poem discussion is close reading, not personal-history inference.']},
394:{'paragraphs':[
'Abeera Mirza is a poet from Gujrat, Pakistan, whose work has appeared in Raven Cage Zine and Orfeu. In a 2023 interview with The Mount Kenya Times, she described finding inspiration in everyday experience, nature and small moments that can pass unnoticed. She also spoke about the challenge of finding words for complex feelings.',
'Her Kabita Live poem The Waterfall gives a personal ambition the persistence of flowing water. Rocky paths, repeated falls and the effort of climbing carry its movement towards achievement; the speaker’s determination holds the poem together.'
], 'sources':[source('Raven Cage Zine94 · contributor biography, p.94','https://www.ral-m.com/revue/IMG/pdf/ravencagezine94.pdf',['Gujrat poet identity and actual publication'],'opened_pdf'),source('The Mount Kenya Times · interview,2 October2023, p.24','https://www.mountkenyatimes.co.ke/wp-content/uploads/2023/10/Oct-2-2023-Mt-Kenya-Times-ePAPER.pdf',['First-person account of inspiration and writing challenges'],'opened_pdf'),source('Orfeu · Abeera Mirza, September2024','https://orfeu.al/abeera-mirza-1646',['Publication of poems and Gujrat identity'])],
'identity_match':'Exact name, Gujrat/Pakistan and named journal affiliations match the captured biography; interview and Orfeu share abeera_quotes author handle.','poems_read':[545],
'limitations':['Do not repeat uncorroborated Mughal descent, gold medal, degree, precise employment rank, awards or anthology totals.','Jar of Emotions appears only in supplied contributor copy at Orfeu; await a publisher/bibliographic record before selected-book inclusion.','Contributor biographies are corroboration of identity/publication, not independent verification of every promotional claim.']},
388:{'paragraphs':[
'Aiswarya Pradhan writes poetry in Odia and is associated with Bhawanipatna in Kalahandi. Her collection ତୁମେ ଗଲାପରେ is named in her contributor note in Satyabadi’s August 2026 issue and in a regional report on the Devagiri literary honours.',
'Her Kabita Live poems find large emotional questions in ordinary things. ସାବୁନ୍ turns a bar of soap into a meditation on possession, touch and the wish to wash away the past. ପସରା ବିକୁଥିବା ଝିଅ follows a young seller whose load carries the weight of hunger, hope and a future still to be secured.'
], 'sources':[source('Satyabadi · August2026, p.46','https://fliphtml5.com/aukd/pwnf/46/',['Poetry contributor, Bhawanipatna/Kalahandi and collection ତୁମେ ଗଲାପରେ'],'indexed_page_text_direct_fetch_failed'),source('Kranti Kshetra · Devagiri honours report','https://www.krantikshetra.in/?p=9315',['Bhawanipatna poet and first collection title'],'opened_page')],
'identity_match':'Exact Odia name, Bhawanipatna/Kalahandi and matching location signature in local poem721 corroborate the Satyabadi identity. No identity link to the similarly named civil servant is asserted.','poems_read':[721,533],
'limitations':['Satyabadi page46 supplied indexed text but direct fetch returned an internal error.','No publisher/year or book destination established for the collection; title remains in narrative only.','Honour announcement is prospective; no awarded-status assertion. Proposed second book ଶେଷଭୋଗ remains unconfirmed.']},
381:{'paragraphs':[
'Amanita Sen is a Kolkata-based poet, translator and literary critic. Her collections include Candle in My Dream, published by Writers Workshop, and What I Don’t Tell You, published by Authorspress. Her work with The Antonym includes poetry editing, interviews and translations from Bengali.',
'With Amitava Sen, she edited Chime of Time: Yearbook of Bengali Poetry in Translation, published by The Antonym Collections in 2025. Her Kabita Live poem To my son moves from a mother’s tear to memories of infancy, then towards autumn and the passing years. Its final gesture finds in the child a poem beyond writing.'
], 'books':[{'title':'Chime of Time: Yearbook of Bengali Poetry in Translation','detail':'Co-edited with Amitava Sen · The Antonym Collections,2025','url':'https://books.google.com/books/about/Chime_of_Time.html?id=MuiSEQAAQBAJ'}],
'sources':[source('The Antonym · Amanita Sen','https://www.theantonymmag.com/amanita-sen/',['Kolkata literary identity, collections, poetry editing and Bengali translations']),source('Chime of Time · bibliographic record','https://books.google.com/books/about/Chime_of_Time.html?id=MuiSEQAAQBAJ',['Co-editors, publisher,2025 and ISBN9789349203709'],'opened_book_record')],
'identity_match':'Exact name, Kolkata, poetry and editorial work agree with journal note and publisher record.','poems_read':[505],
'limitations':['Collection totals differ across dated biographies; no fixed total asserted.','IPPL award and academic degree require organizer/university corroboration; omitted from new draft.','Motherhood poem read as lyric speaker, not confirmation of private family biography.']},
380:{'paragraphs':[
'Anita Panda is a Mumbai-based poet writing in English and Hindi. Her collection Songs of My Soul appeared in 2023. She also brought together Genesis (2021), a volume of poems by her late brother, Colonel Surya Panda, preserving his writing as a literary tribute.',
'Her poem Broken but undaunted appeared in Setu in June 2025. In Kabita Live’s तू कशि़श और नज़्म है, an insistent address urges its listener to break restrictions and claim the freedom to write her own story. Images of flight, rivers and an open sky give that encouragement a physical energy.'
], 'sources':[source('Setu · Special Edition: Anita Panda, June2025','https://www.setumag.com/2025/06/special-edition-anita-panda.html',['Bilingual identity,2023 collection and publication']),source('Anita Panda · author publication record','https://in.linkedin.com/in/anita-panda-87010013',['Mumbai and explicit attribution of Genesis poems to Colonel Surya Panda'],'indexed_profile_text'),source('Odisha News Times · Songs of My Soul launch, February2023','https://www.odishanewstimes.com/2023/02/15/anita-pandas-songs-of-my-soul-released/',['Mumbai author, collection launch and publisher'],'indexed_page_text')],
'identity_match':'Exact name, Mumbai, Songs of My Soul and Genesis dedicated to soldier brother agree across the captured journal note and source records.','poems_read':[499],
'limitations':['Genesis retailer metadata lists Anita as author, while description and her own publication record explicitly credit her brother’s poems. New wording preserves this distinction.','Hindi book Bhavnaon ki Dastak listed on author profile, but publisher destination not yet verified; omit rather than making the biography a catalogue of unverified leads.','No inferred personal beliefs, health details or literary accolades included.']}
}
if __name__=='__main__':
 profiles={p['id']:p for p in json.loads((SITE/'data/writer-profiles.json').read_text())}
 current=json.loads((SITE/'data/writer-enrichment.json').read_text())
 for ident,item in entries.items():
  if str(ident) in current:raise RuntimeError(f'Refuse overwriting existing enrichment {ident}')
  reader={'sections':[{'heading':'Life and writing.','language':'en','paragraphs':item['paragraphs']}],'books':item.get('books',[]),'sources':[{k:s[k] for k in ['label','url']} for s in item['sources']],'reviewed_on':DATE}
  dossier={'writer_id':ident,'name':profiles[ident]['name'],'reviewed_on':DATE,'batch':'research-003','status':'source_checked_local_draft','independent':False,'portrait_action':'unchanged','reader_draft':reader,**{k:v for k,v in item.items() if k not in ['paragraphs','books']},'next_action':'Author/editor factual review pending; follow up only on explicitly recorded bibliographic gaps.'}
  dossier['limitations'].append('Same-assistant research and close reading; independent factual and linguistic review pending.')
  (HOME/'enrichment'/f'{ident}.json').write_text(json.dumps(dossier,ensure_ascii=False,indent=2)+'\n')
  current[str(ident)]=reader
  (SITE/'data/writer-enrichment.json').write_text(json.dumps(current,ensure_ascii=False,indent=2)+'\n')
  print('Saved writer',ident)
