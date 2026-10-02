"""Render the captured publication, using edition manifests as the content authority."""
publication_by_issue={x['number']:x for x in publication_issues}
language_labels={'or':'ଓଡ଼ିଆ','hi':'हिन्दी','en':'English'}

def poem_route(ident):
    return sample_routes.get(ident,f'poem-{ident}.html')

def author_link(p):
    if not p['writer_id']:
        return '<span>Author not recorded</span>'
    route=profile_routes.get(p['writer_id'],f'poet-{p["writer_id"]}.html')
    return f'<a href="{route}">{e(p["author"])}</a>'

def publication_rows(items,show_issue=False):
    result='<div class="poem-list">'
    for i,p in enumerate(items,1):
        lang=p['language'];route=poem_route(p['id'])
        metadata=language_labels[lang]
        if show_issue:
            metadata+=(f' · <a href="issue-{p["edition"]}.html">Issue {p["edition"]}</a>' if p['edition'] else ' · Edition unrecorded')
        result+=(f'<article class="poem-row" data-lang="{lang}" data-search="{e(p["title"]+" "+p["author"]+" "+p["text"])}">'
                 f'<span class="number">{i:02d}</span><h3 class="{lang}" lang="{lang}"><a href="{route}">{e(p["title"])}</a></h3>'
                 f'<div class="byline row-author">{author_link(p)}<br><small>{metadata}</small></div>'
                 f'<a class="arrow" href="{route}" aria-label="Read {e(p["title"])}">↗</a></article>')
    return result+'</div><p class="empty" id="empty-results" hidden>No poems match. Try another word or language.</p>'

def edition_rows(items):
    result='<div class="poem-list edition-poem-list">'
    for i,p in enumerate(items,1):
        lang=p['language'];route=poem_route(p['id'])
        result+=(f'<article class="poem-row edition-poem-row" data-lang="{lang}" data-search="{e(p["title"]+" "+p["author"])}">'
            f'<span class="number">{i:02d}</span><h3 class="{lang}" lang="{lang}"><a href="{route}">{e(p["title"])}</a></h3>'
            f'<div class="byline row-author">{author_link(p)}</div>'
            f'<span class="edition-language" lang="{lang}">{language_labels[lang]}</span>'
            f'<a class="edition-read" href="{route}" aria-label="Read {e(p["title"])}"><svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true" focusable="false" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M12 5.5C9 3.8 6 3.8 3 4.5v14c3-.7 6-.7 9 1 3-1.7 6-1.7 9-1v-14c-3-.7-6-.7-9 1Z"/><path d="M12 5.5v14M6 8h3m6 0h3M6 11h3m6 0h3"/></svg><span class="read-tooltip" aria-hidden="true">Read poem</span></a></article>')
    return result+'</div><p class="empty" id="empty-results" hidden>No poems in this language in this edition. Choose another language or All languages.</p>'

def edition_filters():
    return '<div class="filter edition-filter" role="group" aria-label="Filter poems by language">'+''.join(f'<button data-language="{v}" aria-pressed="{str(v=="all").lower()}" lang="{v if v!="all" else "en"}">{n}</button>' for v,n in [('all','All languages'),('or','ଓଡ଼ିଆ'),('hi','हिन्दी'),('en','English')])+'</div><p class="sr-only" id="filter-status" role="status" aria-live="polite" aria-atomic="true"></p>'

for issue in publication_issues:
    n=issue['number'];entries=[publication_poems[pid] for pid in issue['poem_ids']]
    date=f'{issue["month"]} {issue["year"]}';art=cover_by_number[n]
    refs=' '.join(f'<a class="text-link" href="{e(ref["url"])}" target="_blank" rel="noopener noreferrer">{e(ref["label"])} ↗</a>' for ref in art.get('sources',[]))
    cover_figure='<figure class="edition-cover">'+cover(n)+f'<figcaption>{e(art["cultural_connection"])}'+(f'<span class="edition-cover-sources">{refs}</span>' if refs else '')+'</figcaption></figure>'
    page(f'issue-{n}.html',f'Issue {n} · {date}',crumb('<a href="archive.html">Archive</a> / '+str(n))+
        '<section class="issue-intro edition-opening">'+cover_figure+f'<div><span class="eyebrow">Issue {n}</span><h1>{e(date)}</h1>'+
        f'<div class="edition-story"><h2>{e(art["title"])}</h2><p>{e(art["story"])}</p></div></div></section>'+
        '<section class="section edition-contents"><div class="section-head"><h2>Within these pages.</h2><a class="text-link" href="archive.html">All editions</a></div>'+edition_filters()+edition_rows(entries)+'</section>',
        active='Current issue' if n==47 else 'Archive')

import re

def reader_icon(name):
    svg=(R/f'assets/icons/earth-voice-v1/ink/{name}.svg').read_text()
    svg=re.sub(r' role="img"| aria-label="[^"]*"','',svg)
    return svg.replace('<svg ','<svg aria-hidden="true" focusable="false" ',1)

poem_art_captions=json.loads((R/'data/poem-art-captions.json').read_text())
for p in publication_poems.values():
    ident=p['id'];lang=p['language'];label=language_labels[lang];n=p['edition'];route=poem_route(ident)
    issue=publication_by_issue.get(n);date=f'{issue["month"]} {issue["year"]}' if issue else 'Poetry collection'
    if ident in sample_routes:
        slug=sample_routes[ident].removeprefix('poem-').removesuffix('.html')
        art=f'<figure class="poem-art"><img src="assets/poem-art/{slug}.webp" alt="{art_alts[slug]}" width="1536" height="1024"><figcaption>{e(poem_art_captions[str(ident)])}</figcaption></figure>'
    elif n:
        art_record=cover_by_number[n]
        art=f'<figure class="poem-art"><img src="{art_record["artwork"]}" alt="{e(art_record["alt"])}" width="1024" height="1536" decoding="async"><figcaption>{e(art_record["cultural_connection"])}</figcaption></figure>'
    else:
        art=site_art('poems.html').replace('class="opening-art"','class="poem-art"').replace(' aria-hidden="true"','').replace('</figure>','<figcaption>A quiet place for words.</figcaption></figure>')
    issue_route=f'issue-{n}.html' if n else 'poems.html'
    issue_label=f'{date} · Issue {n}' if n else date
    actions=(f'<div class="poem-actions" role="group" aria-label="Poem actions"><button type="button" data-share="{ident}">'+reader_icon('share')+'<span>Share</span></button>'+
        f'<a href="contact.html?poem={ident}">'+reader_icon('write')+'<span>Write to the editor</span></a></div>')
    body=(f'<section class="poem-opening"><div class="poem-heading"><p class="reader-meta"><a href="{issue_route}">{e(issue_label)}</a> · <span lang="{lang}">{label}</span></p>'+
        f'<h1 class="{lang}" lang="{lang}">{e(p["title"])}</h1><p class="byline">'+('By ' if p['writer_id'] else '')+author_link(p)+'</p>'+actions+'</div>'+art+'</section>')
    body+=('<div class="reading-layout"><article class="reader"><div class="reader-tools"><div class="size-group" role="group" aria-label="Poem text size">'+
        '<button data-size="24" aria-pressed="true" aria-label="Standard text size">A</button><button data-size="28" aria-pressed="false" aria-label="Large text">A+</button><button data-size="32" aria-pressed="false" aria-label="Extra large text">A++</button></div></div>')
    body+=f'<div class="verse {lang}" lang="{lang}">'+''.join('<p class="stanza">'+'<br>'.join(e(line) for line in stanza)+'</p>' for stanza in p['stanzas'])+'</div>'
    body+='</article></div><div class="poem-reading-end"><div class="poem-end-ornament" aria-hidden="true"><span></span>'+reader_icon('paddy')+'<span></span></div>'
    steps=[]
    previous=None;next_poem=None
    if issue:
        ordered=issue['poem_ids'];pos=ordered.index(ident)
        if pos>0:
            previous=publication_poems[ordered[pos-1]]
            steps.append(f'<a class="poem-step previous" href="{poem_route(previous["id"])}" aria-label="Previous poem: {e(previous["title"])}" title="{e(previous["title"])}">'+reader_icon('next')+'<span>Previous</span></a>')
    if previous is None:
        steps.append('<button type="button" class="poem-step previous" disabled aria-label="Previous poem unavailable">'+reader_icon('next')+'<span>Previous</span></button>')
    if p['writer_id']:
        writer_route=profile_routes.get(p['writer_id'],f'poet-{p["writer_id"]}.html')
        steps.append(f'<a class="poem-more" href="{writer_route}">More by this poet</a>')
    if issue and pos+1<len(ordered):
        next_poem=publication_poems[ordered[pos+1]]
        steps.append(f'<a class="poem-step next" href="{poem_route(next_poem["id"])}" aria-label="Next poem: {e(next_poem["title"])}" title="{e(next_poem["title"])}"><span>Next</span>'+reader_icon('next')+'</a>')
    if next_poem is None:
        steps.append('<button type="button" class="poem-step next" disabled aria-label="Next poem unavailable"><span>Next</span>'+reader_icon('next')+'</button>')
    if steps:body+='<nav class="poem-after" aria-label="Continue reading">'+''.join(steps)+'</nav>'
    body+='</div>'
    page(route,p['title'],body,active='Poems')

all_publication_poems=[publication_poems[pid] for issue in publication_issues for pid in issue['poem_ids']]+[p for p in publication_poems.values() if not p['edition']]
for route,title,kicker,heading in [('poems.html','Poems','The reading room','Find a poem.<br>Stay a little longer.'),('search.html','Search','A word can lead you somewhere','Follow a word.<br>Find a voice.')]:
    page(route,title,head(kicker,heading,f'{len(publication_poems)} poems, with a path through {len(publication_issues)} editions.')+
        '<div class="search-field"><label><span class="label">Search all poems</span><input id="list-search" type="search" placeholder="Title, poet or words from a poem"></label></div>'+filters().replace('Poems in this issue','Poems in the collection')+publication_rows(all_publication_poems,True),active='Poems')

# Include source-linked contributors found in editions but absent from the directory capture.
extra_writers=[w for w in writer_profiles if w['id'] not in {x['id'] for x in json.loads((R/'data/writer-profiles.json').read_text())}]
if extra_writers:
    path=R/'poets.html';html=path.read_text()
    for w in extra_writers:
        entry=f'<a class="directory-entry" data-directory-name="{e(w["name"])}" href="poet-{w["id"]}.html"><span>{e(w["name"])}</span><small>View profile</small></a>'
        marker=f'<section class="directory-section" data-letter="{w["name"][0].upper()}"'
        start=html.index(marker);end=html.index('</div></section>',start)
        html=html[:end]+entry+html[end:]
    path.write_text(html.replace('427 entries',f'{len(writer_profiles)} entries'))

status=json.loads((R/'data/content-status.json').read_text())
status.update(complete_poem_texts=len(publication_poems),excerpt_poems=0,known_poem_records=len(publication_poems),
    complete_edition_contents=len(publication_issues),edition_assigned_poems=sum(bool(p['edition']) for p in publication_poems.values()),
    unassigned_poems=[p['id'] for p in publication_poems.values() if not p['edition']],
    missing_author_names=[p['id'] for p in publication_poems.values() if not p['author']],
    writer_records=len(writer_profiles),captured_writer_profiles=len(json.loads((R/'data/writer-profiles.json').read_text())),launch_ready=False,
    blockers=['One poem has no recorded edition and one has no recorded author.',
              'Complete reviews, missing writer biographies and editorial content review remain outstanding.'])
(R/'data/content-status.json').write_text(json.dumps(status,ensure_ascii=False,indent=2)+'\n')
(R/'data/local-routes.json').write_text(json.dumps({str(pid):poem_route(pid) for pid in publication_poems},indent=2)+'\n')
