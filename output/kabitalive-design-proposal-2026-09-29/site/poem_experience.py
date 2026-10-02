"""Approved poem-page composition and per-edition quiet-reader data."""
from pathlib import Path
from html import escape
import json,re
from poem_reader import render_reader
from writer_names import writer_aliases
ROOT=Path(__file__).resolve().parent
READING_RE=re.compile(r'(<script type="application/json" id="reading-data">)(.*?)(</script>)',re.S)
DECORATION=re.compile(r'(?:[\s*＊_—–=\-]{3,}|\s*∎\s*)')
EDITION_NEIGHBORS={}

def encoded(data):
    return json.dumps(data,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')

def prepare_readers(poems,issues,routes,names,portraits):
    EDITION_NEIGHBORS.clear()
    readers={}
    for ident,p in poems.items():
        data=json.loads(READING_RE.search(render_reader(p))[2])
        data['author']=names.get(p['writer_id'],p['author'].split('/')[0].strip()) or 'Author not recorded'
        data['route']=routes(ident)
        data['portrait']=portraits.get(p['writer_id'],'')
        data['availability']='The complete poem text is awaiting confirmation.' if ident==385 else ''
        for v in data['variants'].values():
            v['hidden_lines']=[i for i,line in enumerate(l for st in v['stanzas'] for l in st) if DECORATION.fullmatch(line)]
        readers[ident]=data
    target=ROOT/'assets/reading-editions';target.mkdir(exist_ok=True)
    for issue in issues:
        payload={'edition':issue['number'],'label':f'{issue["month"]} {issue["year"]} · Issue {issue["number"]}', 'poems':[readers[i] for i in issue['poem_ids']]}
        (target/f'issue-{issue["number"]}.json').write_text(encoded(payload)+'\n')
        for position,ident in enumerate(issue['poem_ids']):
            start=max(0,min(position-2,len(issue['poem_ids'])-5))
            EDITION_NEIGHBORS[ident]=[(n+1,readers[item]) for n,item in enumerate(issue['poem_ids']) if start<=n<start+5]
    library={'editions':[], 'poets':[]}
    for issue in sorted(issues,key=lambda i:i['number'],reverse=True):
        library['editions'].append({'id':issue['number'],'label':f'{issue["month"]} {issue["year"]} · Issue {issue["number"]}', 'count':len(issue['poem_ids']), 'url':f'assets/reading-editions/issue-{issue["number"]}.json'})
    ordered=list(dict.fromkeys(i for issue in sorted(issues,key=lambda i:i['number'],reverse=True) for i in issue['poem_ids']))
    ordered.extend(i for i in poems if i not in ordered)
    (ROOT/'assets/reading-all.json').write_text(encoded({'label':'All poems','poems':[readers[i] for i in ordered]})+'\n')
    library['editions'].insert(0,{'id':'all','label':'All editions','count':len(ordered),'url':'assets/reading-all.json'})
    authors={}
    for ident in ordered:
        writer=poems[ident]['writer_id']
        if writer is not None: authors.setdefault(writer,[]).append(readers[ident])
    author_target=ROOT/'assets/reading-authors';author_target.mkdir(exist_ok=True)
    for writer,items in sorted(authors.items(),key=lambda pair:pair[1][0]['author'].casefold()):
        label=items[0]['author'];url=f'assets/reading-authors/poet-{writer}.json'
        (ROOT/url).write_text(encoded({'author':writer,'label':label,'poems':items})+'\n')
        library['poets'].append({'id':writer,'label':label,'count':len(items),'url':url})
    for alias,canonical in writer_aliases(ROOT).items():
        # Old saved reader URLs retain access to the complete grouped collection.
        (author_target/f'poet-{alias}.json').write_text((author_target/f'poet-{canonical}.json').read_text())
    (ROOT/'assets/reading-library.json').write_text(encoded(library)+'\n')
    return readers

def edition_panel(p,menu):
    rows=[]
    for number,item in EDITION_NEIGHBORS.get(p['id'],[]):
        code=item['source_language'];title=item['variants'][code]['title']
        current=' aria-current="page"' if item['id']==p['id'] else ''
        rows.append(f'<li><a href="{escape(item["route"],quote=True)}"{current}><span class="toc-number">{number:02}</span><span><span class="toc-title" lang="{code}">{escape(title)}</span><span class="toc-author">{escape(item["author"])}</span></span></a></li>')
    if not rows:
        return '<section class="edition-glance related-only" aria-label="About this poem">'+menu+'</section>'
    contents='<nav aria-labelledby="edition-glance-heading"><h2 id="edition-glance-heading">In this edition</h2><ol>'+''.join(rows)+f'</ol><a class="toc-all" href="issue-{p["edition"]}.html#edition-poems">All poems in this edition</a></nav>'
    return '<section class="edition-glance">'+contents+menu+'</section>'

def enhance_poem(body,p,data):
    if len(data['variants'][data['source_language']]['title'])>42:
        body=re.sub(r'(<h1 class=")([^"]*)',r'\1\2 long-title',body,count=1)
    # Keep actual text arrays and line offsets; omit only visual ornament lines.
    body=READING_RE.sub(lambda m:m[1]+encoded(data)+m[3],body)
    body=re.sub(r'<figcaption\b[^>]*>.*?</figcaption>','',body,flags=re.S)
    body=re.sub(r' · <span lang="(?:or|hi|en)">.*?</span></p>','</p>',body,count=1)
    body=body.replace('By '+escape(p['author']), 'By '+escape(data['author']))
    feedback=re.search(r'<a href="contact.html\?poem=\d+">.*?</a>',body,re.S).group(0)
    quiet='<button type="button" id="open-focus"><svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M12 5C9 3 5 4 3 5v14c3-1 6-1 9 1 3-2 6-2 9-1V5c-2-1-6-2-9 0Zm0 0v15"/></svg><span>Read quietly</span></button>'
    body=body.replace(feedback,quiet,1)
    feedback=re.sub(r'<svg\b.*?</svg>','',feedback,flags=re.S)
    more=re.search(r'<a class="poem-more".*?</a>',body,re.S)
    def contextual_link(link,title,hint):
        return link[:link.index('>')+1]+'<span class="context-link-title">'+escape(title)+'</span><span class="context-link-help">'+escape(hint)+'</span></a>'
    links=(contextual_link(more[0],'More by this poet',f'Explore {data["author"]}’s poems.') if more else '')
    links+=contextual_link(feedback,'Write to the editor','Send a private note about this poem.')
    if more:body=body.replace(more[0],'',1)
    menu='<nav id="poem-secondary-links" class="reader-feedback context-hints" aria-label="About this poem">'+links+'</nav>'
    body=body.replace('</figure>',edition_panel(p,menu)+'</figure>',1)
    # Readers without a translation retain four choices; unavailable choices are disabled.
    choices=[]
    for code,label in [('original','Original'),('or','Odia'),('hi','Hindi'),('en','English')]:
        enabled=code=='original' or code in data['variants']
        attrs='' if enabled else ' disabled title="Translation unavailable"'
        choices.append(f'<button type="button" role="tab" id="tab-{code}" data-reading-language="{code}" aria-selected="{str(code=="original").lower()}" aria-controls="reading-panel" tabindex="{0 if code=="original" else -1}"{attrs}>{label}</button>')
    old=re.search(r'(?:<div class="experience-bar">.*?)?<div class="reader-tools">.*?(?=<div id="selection-tools")',body,re.S)
    if not old:raise ValueError(f'Missing reader controls for {p["id"]}')
    body=body[:old.start()]+body[old.end():]
    controls='<div class="experience-bar"><div class="reading-tabs" role="tablist" aria-label="Poem language">'+''.join(choices)+'</div></div>'
    controls+='<div class="reader-tools"><div class="size-group" role="group" aria-label="Poem text size">'+''.join(f'<button data-size="{size}" aria-pressed="{str(size==24).lower()}" aria-label="{label} text size">{label}</button>' for size,label in [(24,'Standard'),(28,'Large'),(32,'Extra large')])+'</div></div>'
    panel='<section id="page-bookmarks" aria-label="Reader tools" hidden><div class="page-tools-head"><strong>Reader tools</strong><button id="page-bookmarks-close" type="button" aria-label="Close reader tools">×</button></div>'+controls+'<button id="page-save-place" type="button">Bookmark this poem</button><details id="page-saved-details"><summary>Saved places &amp; passages</summary><div id="page-saved-list"></div><div class="mark-tools"><button type="button" class="clear-marks" id="clear-marks" hidden>Clear marks</button></div></details><p class="page-tools-tip">Select words in the poem to underline them. Saved on this device.</p><span id="page-saved-status" class="sr-only" role="status"></span></section>'
    body=body.replace('<div class="poem-actions" role="group" aria-label="Poem actions">','<div class="poem-actions" role="group" aria-label="Poem actions"><button id="page-bookmarks-button" type="button" aria-label="Reader tools" title="Language, text size, bookmarks and more" aria-expanded="false" aria-controls="page-bookmarks"><span class="reader-aa" aria-hidden="true">Aa</span></button>',1)
    body=body.replace('</div></div><figure class="poem-art','</div>'+panel+'</div><figure class="poem-art',1)
    body=re.sub(r'<div id="reading-panel"[^>]*>', '<div id="reading-panel" role="tabpanel" aria-labelledby="tab-original" tabindex="0">',body,count=1)
    # No-JavaScript verse also suppresses decoration, retaining source text in hidden spans.
    body=re.sub(r'(?P<prefix><p class="stanza">|<br>)(?P<text>[*＊_—–=\-\s]{3,})(?=<br>|</p>)',lambda m:m['prefix']+'<span class="source-end-marker" hidden>'+m['text']+'</span>',body)
    dataset={'url':f'assets/reading-editions/issue-{p["edition"]}.json'} if p['edition'] else {}
    body+='<script type="application/json" id="focus-edition-data">'+encoded(dataset)+'</script>'+(ROOT/'templates/quiet-reader.html').read_text()
    engagement=(ROOT/'templates/poem-engagement.html').read_text().replace('{{POEM_ID}}',str(p['id']))
    body=body.replace('<div class="poem-reading-end">',engagement+'<div class="poem-reading-end">',1)
    return body
