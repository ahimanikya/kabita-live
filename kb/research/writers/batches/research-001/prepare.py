"""Apply this reviewed research batch; preserve captured biographies and art."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
SITE = ROOT / 'projects/site'
DEST = ROOT / 'kb/research/writers/enrichment'
DATE = '2026-10-01'

def source(label, url, supports, access='indexed_page_text'):
    return dict(label=label, url=url, supports=supports, access=access, accessed_on=DATE)

entries = {}
def add(ident, paragraphs, sources, identity, books=None, limitations=None):
    entries[str(ident)] = dict(
        sections=[dict(heading='Life and writing.', language='en', paragraphs=paragraphs)],
        books=books or [], sources=sources, identity=identity, limitations=limitations or [])

add(21, [
    'Manorama Choudhury is a poet, songwriter and mixed-media artist originally from Berhampur, Odisha. She writes in Odia, Hindi and English, and has presented her poetry through South Asian Poets of New England and other literary gatherings.',
    'Her Odia book Ashtanayika: Tatwa O Kabita explores the eight heroines of classical Indian aesthetics. With Jayakrushna Choudhury, she co-authored Astanayika: The Romantic Heroines from Natyasastra to Modernity, published in 2025. The book brings classical scholarship and poetry into a discussion of love, longing and their expression in the arts.'
], [source('Manorama Choudhury · author biography', 'https://www.manoramachoudhury.com/about', ['Berhampur origin; three writing languages; visual arts and SAPNE readings']), source('Motilal Banarsidass · Astanayika, Google Play Books listing', 'https://play.google.com/store/books/details/Manorama_Choudhury_Astanayika?id=qfyAEQAAQBAJ', ['Co-authorship, publisher, 2025 edition and subject'])],
    'Matched three writing languages, Odisha origin, US literary activity and author site linked from the book biography to the supplied journal identity.',
    [dict(title='Astanayika: The Romantic Heroines from Natyasastra to Modernity',detail='With Jayakrushna Choudhury · Motilal Banarsidass Publishing House, 2025',url='https://play.google.com/store/books/details/Manorama_Choudhury_Astanayika?id=qfyAEQAAQBAJ')],
    ['Personal website manorama.me returned403 on direct retrieval; no claims about present residence or awards added.'])

add(56, [
    'Debarati Sen is a poet from Kolkata whose collections include Blurred Musings and Saudade. She studied English at Presidency College, Kolkata; the author note accompanying Blurred Musings also records her work in the English Department of Presidency University.',
    'She describes writing as a source of personal release and draws on experiences from everyday life. Blurred Musings appeared in 2022, and Saudade was published by Penprints. Her poems have also appeared in literary journals, including The Chakkar.'
], [source('Blurred Musings · author note and book listing', 'https://play.google.com/store/books/details/DEBARATI_SEN_BLURRED_MUSINGS?id=z_hbEAAAQBAJ',['English education; Presidency role; author account of writing']),source('Penprints · Saudade', 'https://penprints.in/shop/product/saudade-by-debarati-sen/', ['Saudade and January2022 debut']),source('The Chakkar · two poems by Debarati Sen','https://www.thechakkar.com/home/debaratisenpoems',['Poetry publication'])],
    'Matched Blurred Musings and Presidency English-department background. Excluded the University of Houston anthropologist of the same name.',
    [dict(title='Blurred Musings',detail='Poetry · Book-O-Pedia',url='https://play.google.com/store/books/details/DEBARATI_SEN_BLURRED_MUSINGS?id=z_hbEAAAQBAJ'),dict(title='Saudade',detail='Poetry · Penprints',url='https://penprints.in/shop/product/saudade-by-debarati-sen/')],
    ['Penprints direct retrieval returned cache miss; indexed publisher text was available. Award claims and current employment not independently established.'])

add(62, [
    'Paramita Mukherjee Mullick is a poet, editor and literary curator with a background in science and education. Her literary work includes promoting multilingual poetry and bringing readers and writers together through poetry events.',
    'Her English collection Cloud Nine arranges its poems in sections named after cloud formations. Published by Inking Innovations, it gathers writing about places, people and feelings. Her poetry also appears in Piker Press, whose author archive includes My Shadow and Light Cannot Be Stopped.'
], [source('Piker Press · Paramita Mukherjee Mullick','https://www.pikerpress.com/author/547/paramita-mukherjee-mullick',['Scientist, editor, curator; multilingual poetry; named poem publications'],'opened_page'),source('Inking Innovations · Cloud Nine','https://inkinginnovations.com/book/cloud-nine/',['English collection; cloud-named sections and subject matter'])],
    'Full name, scientific background, multilingual poetry activity and Cloud Nine agree with journal biography.',
    [dict(title='Cloud Nine',detail='English poetry · Inking Innovations',url='https://inkinginnovations.com/book/cloud-nine/')],
    ['Book and translation totals vary across dated biographies; omitted totals, current appointments and unverified awards. Publisher direct fetch unavailable.'])

add(28, [
    'Tejaswini Patil is a poet, teacher and editor who writes in Marathi, Hindi and English. She founded INNSÆI Journal and MatruAkshar, publications concerned with creative writing, translation and literary exchange.',
    'Her poetry collections include Talons and Nets, Verses of Silence, A Glass of Time and the Hindi collection Kaainat. Talons and Nets also appeared in a bilingual English–Romanian edition from Eikon in 2017, translated by Ligia Tomoiagă.'
], [source('INNSÆI Journal · contributor biography, January–March2025','https://www.innsaeijournal.com/wp-content/uploads/2025/05/INNSAEI-Vol-VI-Issue-1-Jan-Mar-25.pdf',['Founding role and writing in three languages']),source('INNSÆI Journal · October–December2023 author note','https://www.innsaeijournal.com/wp-content/uploads/2024/01/A-Oct-Dec-23-Issue-IV-Draft.pdf',['Named English and Hindi books']),source('Eikon · Talons and Nets','https://www.librariaeikon.ro/poezie/364-odgoane-i-navoade-talons-and-nets.html',['Author and2017 edition'],'opened_page'),source('Technical University of Cluj-Napoca · Ligia Tomoiagă bibliography','https://www.iosud.utcluj.ro/files/Dosare%20abilitare/TOMOIAGA%20Ligia%20Mara/e.2_Lista%20de%20lucrari.pdf',['English–Romanian translation credit and2017 edition'])],
    'Matched founding journals, academic background and Talons and Nets. Tejaswini Deepak Patil/Dange is a documented name variant.',
    [dict(title='Talons and Nets / Odgoane și năvoade',detail='English–Romanian edition · Eikon, 2017',url='https://www.librariaeikon.ro/poezie/364-odgoane-i-navoade-talons-and-nets.html')],
    ['Some biographies incorrectly attach the Romanian translation to A Glass of Time. The translator bibliography and Eikon listing support Talons and Nets. No current college post or awards asserted.'])

add(327, [
    'Prabhanjan K. Mishra writes poetry in Odia and English and works as a translator, critic and editor. He is a former president of Poetry Circle, Mumbai, and formerly edited its journal Poiesis.',
    'His poetry collections include Vigil, Lips of a Canyon and Litmus. He edited A Holi of Poetry, published by Black Eagle Books in 2023, bringing the work of seven Odia poets to English-language readers through translation. His editorial work also includes From the Master’s Loom, a collection of Fakirmohan Senapati’s stories in English.'
], [source('Black Eagle Books · A Holi of Poetry','https://www.blackeaglebooks.org/product/a-holi-of-poetry/',['Bilingual work; former Poetry Circle roles; anthology scope, editor and2023 publication']),source('Spillwords · Prabhanjan K. Mishra','https://spillwords.com/author/prabhanjankmishra/',['Three named collections; Fakirmohan Senapati editorial work'])],
    'Matched two writing languages and former Poetry Circle/Poiesis roles from the supplied biography.',
    [dict(title='A Holi of Poetry',detail='Editor and translator · Black Eagle Books, 2023',url='https://www.blackeaglebooks.org/product/a-holi-of-poetry/')],
    ['Publisher direct retrieval returned cache miss; indexed publisher text available. Personal contact details excluded.'])

add(76, [
    'Rashmi Mohapatra writes poetry in Odia and English. Her background includes a master’s degree in economics from Jawaharlal Nehru University and a career in banking, from which she took voluntary retirement.',
    'The 2021 ISWAL literary handbook names three of her Odia collections: Aparahnar Geeta, Abarna Pruthibi and Aparichita Pratibimba. It also publishes her English poem The Born Dead. Her contributions to Kabita Live span both languages.'
], [source('Literoma · ISWAL2021 handbook, p.63','https://authoralak.com/img/Handbook_ISWAL2021.pdf',['JNU economics; banking; languages; three named collections'],'opened_pdf')],
    'Matched JNU degree, banking retirement, Mumbai context and two languages. Did not merge singer, politician or devotional-book namesakes.', [],
    ['Handbook lists three books, later journal note says four. Named historically documented works rather than claiming an up-to-date total. No book-specific destination yet.'])

add(184, [
    'Varsha Saran writes poetry in Hindi and English. Her 2017 contributor note records her connection with Meerut and postgraduate study at Chaudhary Charan Singh University.',
    'Her English poems have appeared in Our Poetry Archive, including O’Love, Peaceful Thoughts and On the Ashes of Time. Alongside writing for journals and anthologies, she has shared recitations through her Varsha Saran ekSrijan channel.'
], [source('Our Poetry Archive · Varsha Saran, May2017','https://ourpoetryarchive.blogspot.com/2017/05/varsha-saran.html',['Meerut, postgraduate education, Hindi and English; named poems']),source('Our Poetry Archive · January2018 contributor note','https://ourpoetryarchive.blogspot.com/2018/01/?m=0',['On the Ashes of Time and named recitation channel'])],
    'Matched Meerut, postgraduate institution and Hindi/English writing to journal biography.', [],
    ['Historical contributor accounts support literary activity, not current location. No verified standalone book titles or award-organizer records yet.'])

add(49, [
    'Sujit Kumar Satapathy writes poetry in Odia and Koshli–Sambalpuri. His publications include Ichchhavati, published by Sahitya Akademi in 2015, and Nuraa, a Koshli–Sambalpuri poetry collection listed in the Akademi’s 2022–23 annual report.',
    'He took part in Sahitya Akademi’s Yubasahiti poetry-reading programme in Bhubaneswar in April 2017. The journal’s contributor account also records his background in science teaching in Odisha.'
], [source('Sahitya Akademi · Annual Report2022–23, p.204','https://www.sahitya-akademi.gov.in/aboutus/pdf/AR-2022-23.pdf',['Nuraa language, authorship and publication']),source('Sahitya Akademi · Yubasahiti,7April2017','https://sahitya-akademi.gov.in/pdf/yuvasahiti_7-4-17.pdf',['Poetry-reading participation']),source('Exotic India · Ichchhavati','https://www.exoticindia.com/book/details/ichchhavati-oriya-mzq005/',['2015 Sahitya Akademi edition; ISBN9788126049660'])],
    'Matched exact book title, Odia/Koshli languages and2015 debut; official award digest also matches1991 birth year.',
    [dict(title='Ichchhavati',detail='Odia poetry · Sahitya Akademi, 2015',url='https://www.exoticindia.com/book/details/ichchhavati-oriya-mzq005/')],
    ['Appearance in2024 award recommendations is not an award win. Nuraa has no verified book-specific link; retained in narrative.'])

add(455, [
    'Alok Kumar Ray is a bilingual poet from Odisha who writes in Odia and English. His teaching background is in political science, alongside a literary practice that includes poetry and anthology editing.',
    'His English collection Sillage was published by Sankalp Publication. His Odia poetry includes Meghapanata, and he has edited the bilingual anthology Trouvaille. His poetry has also appeared in World Inkers.'
], [source('Sankalp Publication · Sillage, Google Books listing','https://books.google.com/books/about/Sillage.html?id=9NwSEAAAQBAJ',['Publisher, poetry authorship, political-science teaching']),source('VerbalArt · Alok Kumar Ray contributor note','https://vscorpiozine.wordpress.com/tag/dr-alok-kumar-ray-2/',['Meghapanata; Trouvaille editorship']),source('World Inkers · Daughter','https://worldinkers.com/2026/07/29/daughter-by-dr-alok-kumar-ray/',['Named poem and bilingual author note'])],
    'Matched bilingual Odisha identity and academic context across publisher and contributor biographies. Same-titled Daughter poems have different texts and are not treated as matching works.',
    [dict(title='Sillage',detail='English poetry · Sankalp Publication',url='https://books.google.com/books/about/Sillage.html?id=9NwSEAAAQBAJ')],
    ['No current faculty rank asserted; award claims omitted. Bibliographic provider categorizes book as fiction despite publisher description identifying poetry.', 'World Inkers Daughter starts With patience repaired; local poem767 starts After the aroma of a rapport. Preserve both as separate observations; do not replace local text or claim identical publication.'])

add(460, [
    'Anamika Nath is a poet and writer with a professional background in forensic medicine. Her literary work appears alongside her medical and research practice; her contributor biography in The Hemlock Journal identifies her as a forensic medicine specialist.',
    'My Wardrobe Has Mitochondrial DNA was longlisted for the Wingword Poetry Prize in 2023. In 2026, The Certificates was shortlisted in The Hemlock Journal’s Still I Rise poetry contest.'
], [source('Wingword Poetry Prize · My Wardrobe Has Mitochondrial DNA','https://www.wingword.in/blog/anamika-nath',['2023 longlist, poem and author'],'opened_page'),source('The Hemlock Journal · Still I Rise shortlist,16August2026','https://thehemlockjournal.com/2026/08/16/shortlist-announced-still-i-rise-voices-of-women-from-around-the-world-poetry-contest/',['2026 shortlist and forensic-medicine biography'])],
    'Matched doctor/forensic-medicine identity to journal biography; organizer sources identify the poems and selection levels.', [],
    ['Other supplied awards, current job title and editorial role not verified in this pass. Hemlock direct request rate-limited; indexed organizer announcement was available.'])

add(27, [
    'Prahallad Satapathy is a bilingual poet from Balangir who writes in Odia and English. A retired associate professor of economics, he has contributed poetry to literary magazines and anthologies.',
    'Srujan published his poem Staircase of Bones in its inaugural 2021 issue. His work also appears in Sahitya Akademi’s Indian Literature: Life Spent with Shadows was published in the January–February 2020 issue.'
], [source('Srujan · Volume1 Issue1,2021, p.38','https://instituteofinsight.org/wp-content/uploads/2021/08/Srujan-2021-v1-i1.pdf',['Balangir; retired economics teacher; languages; poem']),source('Indian Literature · January–February2020 contents','https://www.jstor.org/stable/e27266610',['Life Spent with Shadows and two credited names'])],
    'Matched Balangir, economics career and bilingual writing; journal index corroborates publication.', [],
    ['Did not infer translator role from two-name index alone; no current book total or Academy office asserted.'])

add(456, [
    'Antara Mukherjee is a poet, short-story writer and English-literature teacher whose work also encompasses cultural-heritage research. Her academic activity includes research on Abanindranath Tagore’s garden house at Konnagar and women’s cotton craft in West Bengal.',
    'Her poem Expression appears in The Wise Owl. Alongside creative writing, she has presented research on Bengal’s shared cultural histories, including food, craft and the relationship between place and memory.'
], [source('Durgapur Government College · English research record','https://durgapurgovtcollege.ac.in/research-english/',['Named garden-house and cotton-craft projects; cultural-history presentations'],'opened_page'),source('The Wise Owl · Expression and author biography','https://editor2733.wixsite.com/website-4/antara-mukherjee',['Poet, short-story writer and English teacher; poem'])],
    'Matched Dr Antara Mukherjee, West Bengal Educational Service and heritage research. Excluded Mumbai/Bangalore novelist name match without corroboration.', [],
    ['Source biographies differ between Durgapur and Taki appointments. No current institution or rank asserted; journal-supplied Taki information preserved separately.'])

if __name__ == '__main__':
    current = json.loads((SITE/'data/writer-enrichment.json').read_text())
    profiles = {str(x['id']):x for x in json.loads((SITE/'data/writer-profiles.json').read_text())}
    for ident, entry in entries.items():
        dossier = dict(writer_id=int(ident), name=profiles[ident]['name'], reviewed_on=DATE,
                       status='source_checked_local_draft', independent=False,
                       identity_match=entry['identity'], sources=entry['sources'],
                       journal_record='research/writers/captured-profiles.json',
                       limitations=entry['limitations']+['Same-assistant research; author/editor factual review pending.'],
                       portrait_action='unchanged', batch='research-001')
        public = {k:entry[k] for k in ['sections','books']}
        public['sources']=[{k:s[k] for k in ['label','url']} for s in entry['sources']]
        public['reviewed_on']=DATE
        dossier['reader_draft']=public
        (DEST/f'{ident}.json').write_text(json.dumps(dossier,ensure_ascii=False,indent=2)+'\n')
        current[ident]=public
    (SITE/'data/writer-enrichment.json').write_text(json.dumps(current,ensure_ascii=False,indent=2)+'\n')
    print(f'Integrated {len(entries)} researched writer drafts; {len(current)} total.')
