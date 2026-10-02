"""Match existing non-cover illustrations to textual motifs, with review evidence."""
from pathlib import Path
import json,re,hashlib,unicodedata,collections
ROOT=Path(__file__).resolve().parents[1];R=ROOT/'projects/site'
library=json.loads((R/'data/poem-art-library.json').read_text())['artworks']
assert all(a['src'].startswith(('assets/poem-art/','assets/section-art/')) for a in library)
issues=json.loads((R/'content/editions/index.json').read_text());poems={}
for issue in issues:
 for ident in issue['poem_ids']:poems[str(ident)]=json.loads((R/f'content/editions/issue-{issue["number"]:02d}/poem-{ident}.json').read_text())
for ident in json.loads((R/'content/editions/unassigned/index.json').read_text()):poems[str(ident)]=json.loads((R/f'content/editions/unassigned/poem-{ident}.json').read_text())
def norm(s):return unicodedata.normalize('NFC',s).casefold()
def matches(term,text):
 # Avoid English substrings such as 'sea' inside 'season'; Indic roots support inflection.
 return bool(re.search(r'\b'+re.escape(term)+r'(?:s|es|ed|ing)?\b',text)) if term.isascii() else any(token.startswith(term) for token in re.split(r'[\s।,!?;:()\[\]\"…]+',text))
# Read and reviewed in context: rain dominates the title and repeated imagery in 815.
overrides={
 '815':('courtyard-petals','Repeated rain and soaking imagery: ବର୍ଷା / ଭିଜ; wet courtyard replaces an unrelated sea scene.'),
 '818':('writer-profile','The absent poet and collective forgetting suggest a vacant chair and closed notebook.'),
 '820':('reading-room','The poet grows quiet; water, garden and poetry remain present. An open notebook beside still water connects those images.'),
 '823':('sea-breeze-cloth','ପବନ is wind, moving freely and becoming music; lifted cloth gives the invisible air a visible gesture.'),
 '808':('our-story','Ancestral soil, parents and successive homes anchor the poem. The earthen home evokes belonging without claiming its depicted house is in Bengal.'),
 '811':('pond-at-dawn','Devotional poem opens with blue ocean and sky and later evokes the Yamuna. Quiet water supports that imagery without inventing a deity portrait.'),
 '816':('koraput-morning','The grounding farm, soil and wild landscape are central to renewal in this poem. The earthen path and open hillside echo that setting without identifying the actual farm.'),
 '817':('archive','School, books and enduring memory recur throughout. Aged books hold the years without inventing a portrait of the remembered person.'),
 '819':('search','The closing free flight, wings and return to a nest favour an open window and horizon over a generic writing desk.'),
 '821':('send-a-poem','Writing to preserve ordinary lives is the explicit subject; blank notebook and pen are the direct visual connection.'),
 '822':('courtyard-petals','Flowers, light and a walkway structure the poem; flower petals on a sunlit path are an atmospheric association, not a botanical depiction of oleander.')
}
assigned={};evidence={};counts=collections.Counter()
for ident,p in sorted(poems.items(),key=lambda x:int(x[0])):
 if ident in ('809','810','814'):continue
 title=norm(p['title']);body=norm(p['text']);candidates=[]
 for a in library:
  found=[];score=0
  for theme,terms in a['themes'].items():
   hits=[t for t in terms if matches(norm(t),body) or matches(norm(t),title)]
   title_hits=[t for t in hits if matches(norm(t),title)]
   if hits:
    points=12*len(title_hits)+min(8,len(hits)*2)
    score+=points;found.append({'theme':theme,'terms':hits,'title_terms':title_hits})
  candidates.append((score,a['id'],found))
 best_score=max(x[0] for x in candidates)
 if ident in overrides:
  art,reason=overrides[ident];match=next(x for x in candidates if x[1]==art);kind='context_reviewed';score=match[0];hits=match[2]
 elif best_score:
  tied=[x for x in candidates if x[0]==best_score]
  score,art,hits=min(tied,key=lambda x:hashlib.sha256(f'{ident}:{x[1]}'.encode()).hexdigest());kind='textual_motif';reason='Matched original-language title/body motifs; heuristic association, not a full literary interpretation.'
 else:
  art=['reading-room','editorial-desk','send-a-poem'][int(hashlib.sha256(ident.encode()).hexdigest(),16)%3];kind='neutral_reading_context';score=0;hits=[];reason='No strong motif found. Neutral book/page artwork supports reading without claiming a literal scene; editorial review needed.'
 assigned[ident]=art;counts[kind]+=1
 words=[w for f in hits for w in f['terms']]
 excerpt=next((line for line in p['text'].splitlines() if any(matches(norm(w),norm(line)) for w in words)),'')
 evidence[ident]={'title':p['title'],'language':p['language'],'art':art,'basis':kind,'score':score,'matches':hits,'source_excerpt':excerpt,'reason':reason,'editorial_review':kind!='context_reviewed'}
doc={'version':3,'policy':'Content motifs take priority over variety. Stable tie-breaking; neutral reading-context fallback; edition covers excluded. Preserve three bespoke illustrations.','assignments':assigned}
(R/'data/poem-art-assignments.json').write_text(json.dumps(doc,ensure_ascii=False,indent=2)+'\n')
(ROOT/'kb/records/poem-art-match-evidence.json').write_text(json.dumps({'method':'Multilingual motif matching with original-text evidence; current assistant self-review, not native editorial certification','counts':dict(counts),'dedicated_preserved':[809,810,814],'poems':evidence},ensure_ascii=False,indent=2)+'\n')
print(dict(counts))
