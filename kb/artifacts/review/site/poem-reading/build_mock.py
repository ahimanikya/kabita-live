from pathlib import Path
import re,json
R=Path(__file__).resolve().parents[5]/'projects/site'
O=Path(__file__).resolve().parent.parent
s=(Path(__file__).parent/'source-poem-8.html').read_text()
s=s.replace('<title>', '<title>Review mock · ',1)
s=re.sub(r'<script[^>]*src="[^\"]*(?:analytics|feedback)[^\"]*"[^>]*></script>','',s)
s=s.replace('src="assets/appearance.js"','src="edition-polish-appearance.js"')
s=s.replace('src="assets/poem-reader.js?v=4"','src="poem-reading-base.js?v=19"')
s=s.replace('By Manorama Choudhury / ମନୋରମା ଚୌଧୁରୀ','By Manorama Choudhury')
s=s.replace(' · <span lang="or">ଓଡ଼ିଆ</span></p>','</p>')
# Keep the artwork and its accessible description; omit the competing visible caption.
s=re.sub(r'(<figure class="poem-art\b[^>]*>)(.*?)(</figure>)',lambda m:m[1]+re.sub(r'<figcaption\b[^>]*>.*?</figcaption>','',m[2],flags=re.S)+m[3],s,flags=re.S)
feedback=re.search(r'<a href="contact.html\?poem=8">.*?</a>',s,re.S).group(0)
s=s.replace(feedback,'<button type="button" id="open-focus"><svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M12 5C9 3 5 4 3 5v14c3-1 6-1 9 1 3-2 6-2 9-1V5c-2-1-6-2-9 0Zm0 0v15"/></svg><span>Read quietly</span></button>')
feedback=re.sub(r'<svg\b.*?</svg>','',feedback,flags=re.S)
more=re.search(r'<a class="poem-more".*?</a>',s,re.S).group(0)
s=s.replace(more,'')
s=s.replace('<div class="footer-line">','<nav id="poem-secondary-links" class="reader-feedback" aria-label="About this poem">'+more+feedback+'</nav><div class="footer-line">',1)
# Aa holds reading options; Share and Read quietly remain top-level actions.
controls=re.search(r'<div class="experience-bar">.*?(?=<div id="selection-tools")',s,re.S).group(0)
s=s.replace(controls,'',1)
mark_tools=re.search(r'<div class="mark-tools">.*?</div>',controls,re.S).group(0)
controls=controls.replace(mark_tools,'')
# Original is an alias for the actual source language, never a reconstructed text.
language_tabs='<div class="reading-tabs" role="tablist" aria-label="Poem language">'+''.join(f'<button type="button" role="tab" id="tab-{code}" data-reading-language="{code}" aria-selected="{str(code=="original").lower()}" aria-controls="reading-panel" tabindex="{0 if code=="original" else -1}">{label}</button>' for code,label in [('original','Original'),('or','Odia'),('hi','Hindi'),('en','English')])+'</div>'
controls=re.sub(r'<div class="reading-tabs".*?</div>',lambda _:language_tabs,controls,flags=re.S)
for old,new in [('>A</button>','>Standard</button>'),('>A+</button>','>Large</button>'),('>A++</button>','>Extra large</button>')]:controls=controls.replace(old,new)

actions=re.search(r'<div class="poem-actions"[^>]*>(.*?)</div>',s,re.S)
menu_actions=actions.group(1)
launcher='<div class="poem-actions" role="group" aria-label="Poem actions"><button id="page-bookmarks-button" type="button" aria-label="Reader tools" title="Language, text size, bookmarks and more" aria-expanded="false" aria-controls="page-bookmarks"><span class="reader-aa" aria-hidden="true">Aa</span></button>'+menu_actions+'</div>'
s=s[:actions.start()]+launcher+s[actions.end():]
panel='<section id="page-bookmarks" aria-label="Reader tools" hidden><div class="page-tools-head"><strong>Reader tools</strong><button id="page-bookmarks-close" type="button" aria-label="Close reader tools">×</button></div>'+controls+'<button id="page-save-place" type="button">Bookmark this poem</button><details id="page-saved-details"><summary>Saved places &amp; passages</summary><div id="page-saved-list"></div>'+mark_tools+'</details><p class="page-tools-tip">Select words in the poem to underline them. Saved on this device.</p><span id="page-saved-status" class="sr-only" role="status"></span></section>'
s=s.replace('</div></div><figure class="poem-art', '</div>'+panel+'</div><figure class="poem-art',1)
s=s.replace('</head>','<link rel="stylesheet" href="poem-reading-mock.css?v=22"><script type="module" src="poem-reading-mock.js?v=22"></script></head>')
issues=json.loads((R/'content/editions/index.json').read_text());issue=next(x for x in issues if x['number']==1)
routes=json.loads((R/'data/local-routes.json').read_text());names={x['id']:x['name'].split('/')[0].strip() for x in json.loads((R/'data/writer-profiles.json').read_text())}
source={x['id']:x for p in (R/'content/editions').glob('*/poem-*.json') for x in [json.loads(p.read_text())]}
poems=[]
for ident in issue['poem_ids']:
 html=(R/routes[str(ident)]).read_text();data=json.loads(re.search(r'<script type="application/json" id="reading-data">(.*?)</script>',html,re.S).group(1));data['author']=names.get(source[ident]['writer_id'],source[ident]['author'].split('/')[0].strip());data['route']=routes[str(ident)]
 for variant in data['variants'].values():
  # Display-only exclusions: preserved source strings and offsets stay intact.
  variant['hidden_lines']=[i for i,text in enumerate(line for stanza in variant['stanzas'] for line in stanza) if re.fullmatch(r'(?:[\s*＊_—–=\-]{3,}|\s*∎\s*)',text)]
 poems.append(data)
s=s.replace('</body>','<script type="application/json" id="focus-edition-data">'+json.dumps({'edition':1,'label':'November 2022 · Issue 1','poems':poems},ensure_ascii=False).replace('<','\\u003c')+'</script>\n'+(Path(__file__).parent/'reader.html').read_text()+'</body>')
(O/'poem-reading-mock.html').write_text(s)
base=(Path(__file__).parent/'source-poem-reader.js').read_text().replace('"./poem-marks.mjs?v=2"','"./assets/poem-marks.mjs?v=2"').replace('return poemMarkKey(data.id,language);',"return 'kbl-quiet-review-marks-v1:'+data.id+':'+language;")
base=base.replace("if(saved===null&&data.id===810)","if(false)")
base=base.replace("if(text.trim()==='∎')return;", "if(text.trim()==='∎'||(v.hidden_lines||[]).includes(lineIndex))return;")
base=base.replace('});verse.append(p);',"});if(p.querySelector('.poem-line'))verse.append(p);")
# Preserve both earlier review stores once, then share underlines between modes.
base=base.replace('let saved=read(markKey(),null);',"""let saved=read(markKey(),null);
 const migration=markKey()+':regular-migrated';
 if(!read(migration,false)){
  const earlier=read('kbl-review-only:'+poemMarkKey(data.id,language),[]);
  saved=normalized([...(Array.isArray(saved)?saved:[]),...(Array.isArray(earlier)?earlier:[])]);
  save(markKey(),saved);save(migration,true);
 }""")
base=base.replace('save(markKey(),marks);',"save(markKey(),marks);document.dispatchEvent(new CustomEvent('review-marks-changed'));")
base=base.replace('render(data.source_language);',"document.addEventListener('review-marks-changed',()=>{marks=normalized(read(markKey(),[]));drawMarks()});\nrender(data.source_language);")
base=base.replace('function render(code){', "function render(choice){\n const code=choice==='original'?data.source_language:choice;")
base=base.replace('t.dataset.readingLanguage===code','t.dataset.readingLanguage===choice').replace("'tab-'+code","'tab-'+choice")
base=base.replace('render(data.source_language);',"render('original');")
(O/'poem-reading-base.js').write_text(base)
print('Mock source and19-poem edition dataset generated.')
