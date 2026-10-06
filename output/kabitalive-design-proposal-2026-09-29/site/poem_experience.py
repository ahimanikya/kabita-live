"""Approved poem-page composition and per-edition quiet-reader data."""
from pathlib import Path
from html import escape
import json,re
from poem_reader import render_reader
from reader_icons import quiet_reader_icon
from writer_names import writer_aliases
ROOT=Path(__file__).resolve().parent
READING_RE=re.compile(r'(<script type="application/json" id="reading-data">)(.*?)(</script>)',re.S)
DECORATION=re.compile(r'(?:[\s*＊_—–=\-]{3,}|\s*∎\s*)')
EDITION_NEIGHBORS={}

def encoded(data):
    return json.dumps(data,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')

def prepare_readers(poems,issues,routes,names,portraits,artworks=None):
    EDITION_NEIGHBORS.clear()
    readers={}
    for ident,p in poems.items():
        data=json.loads(READING_RE.search(render_reader(p))[2])
        data['author']=names.get(p['writer_id'],p['author'].split('/')[0].strip()) or 'Author not recorded'
        data['route']=routes(ident)
        data['portrait']=portraits.get(p['writer_id'],'')
        data['illustration']=(artworks or {}).get(ident)
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
    quiet='<button type="button" id="open-focus" aria-label="Read quietly">'+quiet_reader_icon()+'<span>Read quietly</span></button>'
    body=body.replace(feedback,quiet,1)
    feedback=re.sub(r'<svg\b.*?</svg>','',feedback,flags=re.S)
    more=re.search(r'<a class="poem-more".*?</a>',body,re.S)
    def contextual_link(link,title,hint):
        return link[:link.index('>')+1]+'<span class="context-link-title">'+escape(title)+'</span><span class="context-link-help">'+escape(hint)+'</span></a>'
    links=(contextual_link(more[0],'More by this poet',f'Explore {data["author"]}’s poems.') if more else '')
    links+=contextual_link(feedback,'Write to the editor','Send a private note about this poem.')
    if more:body=body.replace(more[0],'',1)
    menu='<nav id="poem-secondary-links" class="reader-feedback context-hints" aria-label="About this poem">'+links+'</nav>'
    if '<!--poem-context-->' in body:
        body=body.replace('<!--poem-context-->',edition_panel(p,menu),1)
    else:
        body=body.replace('</figure>',edition_panel(p,menu)+'</figure>',1)
    # Three script shortcuts; the source-language tab is the original reading.
    choices=[]
    for code,glyph,native,name in [('or','ଅ','ଓଡ଼ିଆ','Odia'),('hi','अ','हिन्दी','Hindi'),('en','A','English','English')]:
        enabled=code in data['variants'];selected=code==data['source_language']
        hint=native+' · '+name if native!=name else name
        if selected:hint+=' · Original'
        if not enabled:hint+=' · Translation unavailable'
        attrs='' if enabled else ' disabled'
        choices.append(f'<button type="button" role="tab" id="tab-{code}" data-reading-language="{code}" lang="{code}" aria-label="Read in {name}" title="{hint}" aria-selected="{str(selected).lower()}" aria-controls="reading-panel" tabindex="{0 if selected else -1}"{attrs}>{glyph}<span class="poem-language-tip" aria-hidden="true">{hint}</span></button>')
    old=re.search(r'(?:<div class="experience-bar">.*?)?<div class="reader-tools">.*?(?=<div id="selection-tools")',body,re.S)
    if not old:raise ValueError(f'Missing reader controls for {p["id"]}')
    body=body[:old.start()]+body[old.end():]
    language_controls='<div class="language-front poem-language-front"><div class="reading-tabs" role="tablist" aria-label="Poem language">'+''.join(choices)+'</div></div>'
    body=body.replace('<div class="poem-actions" role="group" aria-label="Poem actions">',language_controls+'<div class="poem-actions" role="group" aria-label="Poem actions">',1)
    panel='<section id="page-bookmarks" aria-label="Reader tools" hidden><div class="page-tools-head"><strong>Reader tools</strong><button id="page-bookmarks-close" type="button" aria-label="Close reader tools">×</button></div><button id="page-save-place" type="button">Bookmark this poem</button><details id="page-saved-details"><summary>Saved places &amp; passages</summary><div id="page-saved-list"></div><div class="mark-tools"><button type="button" class="clear-marks" id="clear-marks" hidden>Clear marks</button></div></details><p class="page-tools-tip">Select words in the poem to underline them. Saved on this device.</p><span id="page-saved-status" class="sr-only" role="status"></span></section>'
    body=body.replace('<div class="poem-actions" role="group" aria-label="Poem actions">','<div class="poem-actions" role="group" aria-label="Poem actions"><button id="page-bookmarks-button" type="button" aria-label="Bookmarks and saved passages" title="Bookmarks and saved passages" aria-expanded="false" aria-controls="page-bookmarks"><svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="1.4" aria-hidden="true"><path d="M6 3.5h12v17l-6-4-6 4z"/></svg><span>Bookmarks</span></button>',1)
    body,count=re.subn(r'</div></div>(<(?:figure|aside) class="poem-art)',lambda m:'</div>'+panel+'</div>'+m[1],body,count=1)
    if count!=1:raise ValueError(f'Missing reader-tools insertion point for {p["id"]}')
    body=re.sub(r'<div id="reading-panel"[^>]*>', f'<div id="reading-panel" role="tabpanel" aria-labelledby="tab-{data["source_language"]}" tabindex="0">',body,count=1)
    # No-JavaScript verse also suppresses decoration, retaining source text in hidden spans.
    body=re.sub(r'(?P<prefix><p class="stanza">|<br>)(?P<text>[*＊_—–=\-\s]{3,})(?=<br>|</p>)',lambda m:m['prefix']+'<span class="source-end-marker" hidden>'+m['text']+'</span>',body)
    dataset={'url':f'assets/reading-editions/issue-{p["edition"]}.json'} if p['edition'] else {}
    body+='<script type="application/json" id="focus-edition-data">'+encoded(dataset)+'</script>'+(ROOT/'templates/quiet-reader.html').read_text()
    engagement=(ROOT/'templates/poem-engagement.html').read_text().replace('{{POEM_ID}}',str(p['id']))
    # One genuine Like control, moved into the toolbar; comments remain below.
    like_row=re.search(r'<div class="like-row">.*?</div>',engagement,re.S)[0]
    like_row=like_row.replace('data-like aria-pressed', 'data-like disabled aria-pressed').replace('aria-label="Like this poem"', 'aria-label="Like this poem" title="Like this poem"')
    like_row=like_row.replace('<span data-like-label>', '<span data-like-label class="poem-action-tip" aria-hidden="true">').replace('<span data-like-count aria-hidden="true">', '<span data-like-count class="sr-only" aria-hidden="true">').replace('<span data-like-status role="status">','<span data-like-status class="sr-only" role="status">')
    like_row=like_row.removeprefix('<div class="like-row">').removesuffix('</div>')
    engagement=re.sub(r'<div class="like-row">.*?</div>','',engagement,flags=re.S)
    actions=re.search(r'<div class="poem-actions"[^>]*>.*?</div>',body,re.S)
    compact=actions[0].replace('</div>',like_row+'</div>')
    compact=compact.replace('<span>Bookmarks</span>','<span class="poem-action-tip" aria-hidden="true">Bookmarks</span>').replace('<span>Share</span>','<span class="poem-action-tip" aria-hidden="true">Share</span>').replace('<span>Read quietly</span>','<span class="poem-action-tip" aria-hidden="true">Read quietly</span>')
    compact=compact.replace('data-share="', 'aria-label="Share poem" title="Share poem" data-share="').replace('aria-label="Read quietly"','aria-label="Read quietly" title="Read quietly"')
    body=body[:actions.start()]+compact+body[actions.end():]
    body=body.replace(language_controls+compact,'<div class="poem-toolbar" aria-label="Poem reading tools">'+language_controls+compact+'</div>',1)
    body=body.replace('<!--poem-responses-->',engagement,1)
    return body
