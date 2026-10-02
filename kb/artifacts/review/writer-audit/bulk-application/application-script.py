from pathlib import Path
import json,copy,hashlib,datetime
R=Path('/Users/ahimanikya/Projects/Kabita Live');S=R/'projects/site';K=R/'kb';O=K/'artifacts/review/writer-audit/bulk-application';now=datetime.datetime.now(datetime.timezone.utc).isoformat()
def read(p):return json.loads(p.read_text())
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
e=read(S/'data/writer-enrichment.json');before=copy.deepcopy(e);auditpath=K/'research/writers/audit-2026-10-01/findings.json';audit=read(auditpath);ids=sorted({i for f in audit['findings'] for i in f['writer_ids']});dossiers={i:read(K/f'research/writers/enrichment/{i}.json') for i in ids}
if (O/'before-dossiers.json').exists():dossiers={int(i):v for i,v in read(O/'before-dossiers.json').items()}
else:write(O/'before-enrichment.json',before);write(O/'before-findings.json',audit);write(O/'before-dossiers.json',dossiers)
protected=[S/'data/writer-profiles.json',S/'data/writer-quotes.json',*sorted((S/'content/editions').rglob('*.json'))]
write(O/'protected-hashes.json',{str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in protected})
def p(i,index,value):e[str(i)]['sections'][0]['paragraphs'][index]=value
p(255,0,'Tulika writes Hindi poetry and works across communication teaching and documentary film. An Amity University faculty profile records her co-direction of Khanabadosh and a January 2021 Pen In Books Young Author Award for the Hindi poetry manuscript Gulabi Canvas. Her poem here addresses the contradictions surrounding women’s education and independence.')
p(449,0,'Tulika Bibidh Rang writes Hindi poetry alongside work in communication education. Amity University’s faculty profile records her work in its School of Communication and interests in audiovisual storytelling and folk art. It dates a Pen In Books Young Author Award for her Hindi poetry manuscript Gulabi Canvas to January 2021.')
p(410,0,'Rima Sinha contributes Hindi poetry to Kabita Live. The poem gathered here is “रख लिया विक्षोभ बहुत”.');e['410']['sources']=[]
p(106,0,'Mandakini Bhattacharjee writes poetry, criticism and translation. Fakir Chand College’s faculty profile uses the spelling Mandakini Bhattacherya and records her work in English teaching. Her publications include the edited anthology The Mixed Fare and, with Jaydeep Sarangi, a translation of Jatin Bala’s A Life Uprooted: A Bengali Dalit Refugee Remembers, published by Sahitya Akademi in 2022.')
e['106']['sources'][0]['url']='https://fccollege.ac.in/UG/TeacherData?id=183'
p(408,0,'Padmashree R.P. contributes poetry to Kabita Live. The biography supplied with this profile describes a Bengaluru-based poet, teacher and teacher trainer.');e['408']['sources']=[]
p(404,0,'Pallabi Das writes poetry in Odia and English, as recorded in her contributor biography.');e['404']['sources']=[]
p(40,0,'Sujata Dash is a poet from Bhubaneswar and a retired banker. Her work appears in literary journals and anthologies. A 2025 contributor note in Our Poetry Archive lists four titles with Authorspress: More than Mere, Riot of Hues, Eternal Rhythm and Humming Serenades. Her Kabita Live biography records studies in English literature and writing in Odia, Hindi and English.');e['40']['books']=[]
p(236,0,'Divya Vats contributes Hindi poetry to Kabita Live. Her supplied contributor biography describes work in parenting, counselling and writing.');e['236']['sources']=[]
p(218,0,'Zakir Khan writes Odia poetry and fiction. The author note accompanying his poem “Swapna” in Samata describes work in journalism and translation; Sahitya Charcha has also published his fiction.');e['218']['books']=[]
e['218']['sources']=[s for s in e['218']['sources'] if 'culture.odisha' not in s['url']]
p(318,0,'Ranu Uniyal writes poetry in English and Hindi. Her university biography records her work in English at the University of Lucknow and a doctorate from the University of Hull. Her academic interests include women’s writing, disability studies and poetry. Her collections include Across the Divide, December Poems, The Day We Went Strawberry Picking in Scarborough and Saeeda Ke Ghar.')
p(318,1,'The opening passage of “Plums versus Pullum” recalls fruit from Ranikhet, the streets of Almora and a mother’s kitchen. “At Kedarnath” turns to the force of a flood, using the imagery of Shiva and a river’s voice to question human disregard for the natural world.')
p(429,1,'“Freedom Is Our Birthright” connects physical restraint with freedom of thought and spirit. “Glacier” uses images of ice and its surroundings to make an appeal for care of the earth. These readings concern the poems’ themes, rather than scientific claims or the writer’s personal history.')
p(382,1,'His collection A Land in the Sun is published by Penprints, whose description highlights “My Father’s Shirt” and “The Last Man in the Bar”. Kabita Live’s catalogue links this profile to “Krishna Again”, “The field is green” and “A Slow Fire”.')
p(389,0,'Gayatri Das writes in Odia and English, according to her Kabita Live contributor note. Her poem “Song of Stone” appears in the journal.')
p(438,0,'Fakir Chand College’s 2022–23 magazine includes Zahir Hossain Baidya’s poem “The Lone-Wolf” and identifies him at that time as an English Honours student.')
p(438,1,'His Kabita Live poem “Sinister Sense” contrasts a reported proposal about stray dogs with the threat of violence against women. Its disturbing questions lead to an appeal for protection; this is the poem’s rhetoric, not a biographical account of the writer.')
# Backfill evidence honestly: distinguish a freshly opened document from indexed access.
backfill={82:('Title, author spelling and Odia language match the captured contributor and local poems.',[('search_index_product_description; direct_open_failed',['Nija Nijara Premakhetra by Narmada Nilotpala; Paschima Publications; Odia poetry;2019'])]),257:('University CV explicitly bridges A.R. Malik and Majrooh Rashid; local contributor note and poem bylines match.',[('opened_pdf',['A.R. Malik/Majrooh Rashid identity; joined1991; teaching subjects; named books/monographs and English translations']),('prior_access_not_recorded',['Contributor note retained as prior research evidence; not freshly reopened in this pass'])]),337:('Captured Sabita Singh Meera biography and Hindi work title मन आकाशगंगा match the Savita Singh Meera author archive; Romanisation retained.',[('search_index_author_archive_and_poem; direct_open_failed',['Author byline सविता सिंह मीरा; मन आकाशगंगा and आवरण titles; indexed poem compared with local contribution'])])}
for i,(identity,sourceinfo) in backfill.items():
 d=dossiers[i];d['identity_match']=identity
 for source,(access,supports) in zip(d['sources'],sourceinfo):source.update(access=access,supports=supports,accessed_on='2026-10-02')
 d['evidence_backfilled_on']='2026-10-02'
 d.setdefault('limitations',[]).append('Evidence provenance backfilled; this is same-assistant review, not independent author/editor certification.')
dossiers[106]['sources'][0].update(url='https://fccollege.ac.in/UG/TeacherData?id=183',access='opened_page',accessed_on='2026-10-02',supports=['Institutional spelling Mandakini Bhattacherya; English teaching; The Mixed Fare; A Life Uprooted co-translation and2022 publication.'])
# Preserve uncertainty as explicit follow-up rather than treating cautious wording as identity confirmation.
resolutions={
1:('reviewed_followup','Compared identical captured biographies and mapped all four poems across192/224. Retained stable IDs and poem ownership.','Editor/author confirmation of canonical profile and any merge.'),
2:('reviewed_followup','Compared distinctive captured biographies and mapped Anger(244) and Worthy Meeting(482) across256/366. Separate IDs retained.','Editor/author confirmation before combining contributor records.'),
3:('mitigated_followup','Both profiles now consistently attribute January2021 manuscript recognition to the university; neither presents the manuscript as a published book.','Confirm whether255/449 are one identity before a merge; source2020 date remains historical.'),
4:('mitigated_followup','Removed the unconfirmed external Hindi-byline attribution from410 and retained only local contribution facts.','Confirm342/410 identity and preferred spelling before combining profiles.'),
5:('reviewed_followup','Retained captured heading and explicit Nitish Raj spelling in the source-attributed biography; recorded institutional evidence and original spelling.','Confirm preferred display byline with author/editor before changing the journal heading.'),
6:('reviewed_followup','Catalogue supports Soumen Roy for Lyrical Musings; retained explicit Ray/Roy bridge and original journal spelling.','Confirm preferred journal byline; no silent rename.'),
7:('mitigated_followup','Freshly opened college profile confirms Bhattacherya, teaching and bibliography; biography now explicitly attributes institutional spelling and role.','Confirm preferred journal display spelling before changing the captured heading.'),
8:('mitigated_followup','Removed independent-sounding profession statement and unconfirmed LinkedIn linkage; role is explicitly attributed to the supplied profile biography.','Confirm R.P./Niranjan name bridge; no credentials or surname inferred.'),
9:('reviewed_followup','Kept modest supplied-note attribution, existing poem and spelling; no outside Ma Yongbo biography or books imported. Exact-title search did not establish provenance.','Chinese/Roman preferred name, original poem and translator still need confirmation.'),
10:('closed_corrected','Removed the uncertain Junagarh event attribution and its public source link; local language facts retained.',''),
12:('closed_corrected','Retained a clearly attributed dated list of titles; removed the two biography-linked book cards and the unsupported solo-collection classification.','Publisher/ISBN/role evidence is still needed before restoring independent book cards.'),
13:('closed_retained','Retained explicitly attributed Literary Vibes wording and no book card, as the recommendation permits when a publisher record is unavailable.','Publisher/title-page verification remains optional follow-up before adding a book card.'),
14:('closed_corrected','Roles now refer explicitly to the supplied contributor biography; removed the inferred professional-profile link and no qualifications added.',''),
15:('closed_corrected','Removed Nandan Kaanan from the narrative and shelf because catalogue authorship does not yet bridge to this contributor; evidence retained in KB.','Confirm title-page/publisher identity before restoring that book.'),
16:('mitigated_followup','Attributed academic affiliation to university biography and restricted Plums commentary to its opening passage.','Editor must reconcile the boundary of poem390; original text retained.'),
17:('mitigated_followup','Restricted commentary to named poems’ themes without treating duplicate Glacier blocks as intentional structure or science as fact.','Editor/source reconciliation for duplicate block in poem699; original preserved.'),
18:('closed_corrected','Current authoritative catalogue already links382 to three poems and389 to one. Removed the stale no-poem sentence and made publisher description distinct from local work.',''),
19:('closed_corrected','Backfilled identity evidence, claim support, actual access modes and reader_draft for82/257/337; uncertainty and source failures recorded honestly.','Independent factual review remains separate.'),
20:('closed_corrected','Removed broad claims about the poet’s overall practice; kept dated college attribution and shorter commentary on the actual poem.','')}
changes=[]
for i in ids:
 d=dossiers[i];related=[f for f in audit['findings'] if i in f['writer_ids']]
 if i==49:continue
 (O/f'original-{i}.json').write_text(json.dumps(before[str(i)],ensure_ascii=False,indent=2)+'\n')
 d['reader_draft']=copy.deepcopy(e[str(i)]);d['editorial_resolution']={'recorded_at':now,'user_direction':'Can we apply them all','findings':[f['id'] for f in related],'changes':[resolutions[int(f['id'].rsplit('-',1)[1])][1] for f in related],'independent_factual_review':'not_certified'}
 if before[str(i)]!=e[str(i)]:changes.append(i);e[str(i)]['reviewed_on']='2026-10-02';d['reader_draft']=copy.deepcopy(e[str(i)])
 write(K/f'research/writers/enrichment/{i}.json',d)
for f in audit['findings']:
 num=int(f['id'].rsplit('-',1)[1])
 if num==11:continue
 status,change,followup=resolutions[num];f['status']=status;f['resolution']={'recorded_at':now,'user_direction':'Can we apply them all','change':change,'followup':followup,'independent':False}
# Fresh checks changed these records' source-access flags.
for profile in audit['profiles']:
 if profile['writer_id'] in [82,257,337]:profile['screening_flags']=[x for x in profile['screening_flags'] if x!='source_access_not_recorded']
 if profile['writer_id'] in [82,337] and 'all_recorded_sources_indexed_only' not in profile['screening_flags']:profile['screening_flags'].append('all_recorded_sources_indexed_only')
write(S/'data/writer-enrichment.json',e);write(auditpath,audit)
# Record application, not fabricated independent clearance; retain any unresolved finding state.
ap=K/'research/writers/audit-2026-10-01/applied-decisions.json';dec=read(ap)
for i in ids:
 if i==49:continue
 related=[f for f in audit['findings'] if i in f['writer_ids']]
 dec[str(i)]={'hash':hashlib.sha256(json.dumps(e[str(i)],sort_keys=True,ensure_ascii=False).encode()).hexdigest(),'decision':'approved','notes':'User authorized recommended handling. '+' '.join(f['resolution']['change'] for f in related)+' Follow-up: '+' '.join(f['resolution']['followup'] for f in related if f['resolution']['followup']),'updated_at':now,'authorization':'Can we apply them all','finding_ids':[f['id'] for f in related],'scope':'Current cautious text accepted; unresolved identity/content evidence remains in findings.'}
write(ap,dec)
poems=[read(p) for p in (S/'content/editions').glob('*/poem-*.json')];maps={str(i):[{'poem_id':p['id'],'title':p['title'],'edition':p['edition']} for p in poems if p.get('writer_id')==i] for i in [192,224,256,366,255,449,342,410,382,389]};write(O/'contribution-mapping.json',maps)
summary={'recorded_at':now,'authorization':'Can we apply them all','changed_reader_profiles':changes,'reviewed_profile_ids':[i for i in ids if i!=49],'total_findings':20,'closed_findings':[f['id'] for f in audit['findings'] if f['status'].startswith('closed')],'followup_findings':[f['id'] for f in audit['findings'] if not f['status'].startswith('closed')],'original_poems_and_captured_records':'unchanged; hashes recorded','publication':'local only','verification':'pending'}
write(O/'summary.json',summary);print(json.dumps(summary,indent=2))
