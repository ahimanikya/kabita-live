from pathlib import Path
import json,copy,hashlib
from datetime import datetime,timezone
R=Path.cwd();S=R/'projects/site';K=R/'kb';O=K/'artifacts/review/writer-audit/followup-2026-10-02';now=datetime.now(timezone.utc).isoformat()
read=lambda p:json.loads(p.read_text())
def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def digest(t):return hashlib.sha256(t.encode()).hexdigest()
names={'106':{'captured_name':'Mandakini Bhattacharjee','display_name':'Mandakini Bhattacherya'},'142':{'captured_name':'Nisith Raj','display_name':'Nitish Raj'},'177':{'captured_name':'Soumen Ray','display_name':'Soumen Roy'}}
for i,v in names.items():v.update(reviewed_on='2026-10-02',evidence=f'kb/research/writers/enrichment/{i}.json')
save(S/'data/writer-name-corrections.json',names)
e=read(S/'data/writer-enrichment.json')
e['142']['sections'][0]['paragraphs'][0]='Nitish Raj is a literary critic and author whose work spans editorial practice and support for fellow writers through Literia Insight and The Literary Mirror. NIT Jalandhar’s creative-writing course programme lists him as the author of Love in Modern Times and a resource person for its January 2024 course.'
e['177']['sections'][0]['paragraphs'][0]='Soumen Roy is the author of the novel Scar and the poetry collection Lyrical Musings. Both titles were reviewed by Literoma in January 2023. Penprints lists Scar in its 2022 catalogue; Lyrical Musings appeared with Notion Press in 2022.'
e['177']['sources'].append({'label':'Penprints — publisher catalogue for Scar','url':'https://penprints.in/shop/shop/'})
p=e['106']['sections'][0]['paragraphs'][0];print('OLD106',p)
p=p.replace('Mandakini Bhattacharjee','Mandakini Bhattacherya').replace('Publishing as Mandakini Bhattacherya, ','');e['106']['sections'][0]['paragraphs'][0]=p
# Correct the publication layer, preserving full captured input and the excluded text.
rules=read(S/'data/poem-reconciliation.json');translations=read(S/'data/poem-translations.json');corrections=[]
for i,iss,start,end in [(390,18,0,1),(699,39,18,35)]:
 path=S/f'content/editions/issue-{iss:02d}/poem-{i}.json';p=read(path);old=copy.deepcopy(p);oldhash=digest(p['text'])
 if i==699:
  first=copy.deepcopy(p['stanzas'][1:18]);first[-1]=first[-1][:-1];first[-1][-1]=first[-1][-1].removesuffix(' GLACIER')
  assert first==p['stanzas'][18:35], 'Glacier blocks differ; stop for review'
 else:
  raw=(K/'artifacts/content-import/editions/issue-18/poem-390.html').read_text()
  assert '<strong>When People stop listening</strong>' in raw
  extra=p['stanzas'][1];save(O/'poem-390-separated-work.json',dict(title=extra[0],author=p['author'],edition=18,captured_with_poem=390,status='preserved_separate_work',stanzas=[extra[1:]],text='\n'.join(extra[1:]),source_heading_markup='<strong>When People stop listening</strong>',note='Separately headed work preserved in KB; no invented poem ID or edition membership.'))
 p['stanzas']=p['stanzas'][start:end];p['text']='\n\n'.join('\n'.join(s) for s in p['stanzas']);p['status']='reconciled_full_text';save(path,p)
 rules['rules'][str(i)]={'captured_text_sha256':oldhash,'action':'keep_reviewed_stanzas','start_stanza':start,'end_stanza':end,'reason':'separately_headed_appended_work' if i==390 else 'identical_complete_block_duplicated_with_embedded_heading','evidence':'kb/artifacts/review/writer-audit/followup-2026-10-02'}
 t=translations[str(i)];assert t['source_sha256']==oldhash
 for lang,v in t['variants'].items():
  assert [len(x) for x in v['stanzas']]==[len(x) for x in old['stanzas']]
  v['stanzas']=v['stanzas'][start:end]
 t['source_sha256']=digest(p['text']);t['reconciliation']='2026-10-02: corresponding source-aligned stanza range retained; earlier draft preserved in KB; linguistic review still pending.'
 corrections.append(dict(poem_id=i,before_sha256=oldhash,after_sha256=digest(p['text']),kept_stanza_range=[start,end],source_preserved=True))
save(S/'data/poem-reconciliation.json',rules);save(S/'data/poem-translations.json',translations)
# Quote wording remains identical; only source offsets move after de-duplication.
quotes=read(S/'data/writer-quotes.json');q=quotes['429'];p=read(S/'content/editions/issue-39/poem-699.json');q['text_start']=p['text'].index(q['text']);q['text_end']=q['text_start']+len(q['text']);save(S/'data/writer-quotes.json',quotes)
qr=read(K/'records/writer-quote-selections.json');qr0=next(x for x in qr['selections'] if x.get('writer_id')==429);qr0['source_offsets']={'start':q['text_start'],'end':q['text_end']};qr0['reconciliation']='2026-10-02: unchanged quotation re-anchored in single retained Glacier block.';save(K/'records/writer-quote-selections.json',qr)
# Replace preliminary wording now that the poem boundary is established.
p=e['318']['sections'][0]['paragraphs'];p[:]=[x.replace('The opening passage of ', '').replace('the opening passage of ', '') for x in p]
for i in ['106','142','177','318','429']:e[i]['reviewed_on']='2026-10-02'
save(S/'data/writer-enrichment.json',e)
changes={5:'Applied Nitish Raj from the supplied biography, paired editorial affiliations and NIT Jalandhar programme. Original capture retained; profile route unchanged.',6:'Applied Soumen Roy from the supplied biography and exact Scar/Lyrical Musings pair, corroborated by Literoma, publisher Penprints and the book catalogue. Original capture retained; profile route unchanged.',7:'Applied Mandakini Bhattacherya from the supplied biography, college faculty record and exact anthology/editorial bibliography. Original capture retained; profile route unchanged.',16:'Compared original HTML and separated the explicitly bold-titled When People stop listening from Plums versus Pullum. Preserved the entire appended work and prior translations in the KB; retained the source-attributed academic role.',17:'Verified that the two complete Glacier blocks are identical apart from embedded title/byline. Retained one complete block and matching draft translations; original capture and prior data preserved.'}
a=read(K/'research/writers/audit-2026-10-01/findings.json')
for f in a['findings']:
 n=int(f['id'].rsplit('-',1)[1])
 if n in changes:
  f['status']='closed_corrected';f.setdefault('resolution_history',[]).append(f['resolution']);f['resolution']={'recorded_at':now,'user_direction':'Can we apply them all; continue','change':changes[n],'followup':'','independent':False};f.setdefault('fresh_checks',[]).append(changes[n])
for i,n in [('106',7),('142',5),('177',6),('318',16),('429',17)]:
 p=K/f'research/writers/enrichment/{i}.json';d=read(p);d.setdefault('review_history',[]).append({'recorded_at':now,'previous_limitations':d.get('limitations',[]),'previous_next_action':d.get('next_action')});d['reviewed_on']='2026-10-02';d['reader_draft']=copy.deepcopy(e[i]);d['editorial_resolution']={'recorded_at':now,'user_direction':'Can we apply them all; continue','changes':[changes[n]],'evidence':'kb/artifacts/review/writer-audit/followup-2026-10-02','independent_factual_review':'not_certified'}
 d['limitations']=[x for x in d.get('limitations',[]) if not any(t in x.lower() for t in ['preferred','ray/roy','direct retrieval','direct page retrieval','second','duplicat','boundary','spelling requires'])]
 d['limitations'].append('Applied as evidence-backed editorial correction under user authorization; no direct author attestation or independent reviewer is claimed.')
 if i in names:d['display_name']=names[i]['display_name'];d['identity_match']=changes[n]
 d['next_action']='Independent editorial review remains welcome; this audit finding is resolved locally.'
 if i=='106':d['sources'][0].update(url='https://fccollege.ac.in/UG/TeacherData?id=183',access='opened_page',accessed_on='2026-10-02')
 if i=='142':d['sources'][0].update(access='opened_pdf',accessed_on='2026-10-02')
 if i=='177':d['sources'].append({'label':'Penprints — publisher catalogue for Scar','url':'https://penprints.in/shop/shop/','access':'opened_page','accessed_on':'2026-10-02','supports':['Scar; Soumen Roy; 2022; ISBN 978-81-956197-8-8']})
 save(p,d)
closed=[f['id'] for f in a['findings'] if f['status'].startswith('closed')];remaining=[f['id'] for f in a['findings'] if not f['status'].startswith('closed')];a['counts'].update(closed_findings=len(closed),followup_findings=len(remaining));save(K/'research/writers/audit-2026-10-01/findings.json',a)
ad=read(K/'research/writers/audit-2026-10-01/applied-decisions.json')
for i,n in [('106',7),('142',5),('177',6),('318',16),('429',17)]:ad[i].update(hash=digest(json.dumps(e[i],sort_keys=True,ensure_ascii=False)),notes=changes[n],updated_at=now,authorization='Can we apply them all; continue',scope='Evidence-backed editorial correction; no independent certification claimed.')
save(K/'research/writers/audit-2026-10-01/applied-decisions.json',ad)
save(O/'summary.json',dict(recorded_at=now,authorization='Can we apply them all; continue',name_corrections=names,poem_corrections=corrections,closed_findings=closed,remaining_findings=remaining,publication='local only',verification='pending'))
print('Updated three display names and two poems; remaining findings:',len(remaining))
