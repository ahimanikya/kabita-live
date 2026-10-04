from poem_reader import render_reader, TRANSLATIONS
"""Render the captured publication, using edition manifests as the content authority."""
publication_by_issue={x['number']:x for x in publication_issues}
language_labels={'or':'ଓଡ଼ିଆ','hi':'हिन्दी','en':'English'}

def discovery_mark(name):
    import re
    svg=(R/f'assets/icons/earth-voice-v1/ink/{name}.svg').read_text()
    svg=re.sub(r' role="img"| aria-label="[^"]*"| aria-hidden="[^"]*"| focusable="[^"]*"','',svg)
    return svg.replace('<svg ','<svg aria-hidden="true" focusable="false" ',1)

discovery_styles='<link rel="stylesheet" href="assets/reading-discovery.css?v=12">'

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
        titles={lang:p['title'],**{code:v['title'] for code,v in TRANSLATIONS.get(str(p['id']),{}).get('variants',{}).items()}}
        reading_attrs=f' data-reading-titles="{e(json.dumps(titles,ensure_ascii=False))}"' if show_issue else ''
        searchable=p['title']+' '+p['author']+' '+p['text']+(' '+' '.join(titles.values()) if show_issue else '')
        result+=(f'<article class="poem-row" data-lang="{lang}"{reading_attrs} data-search="{e(searchable)}">'
                 f'<span class="number">{i:02d}</span><h3 class="{lang}" lang="{lang}"><a href="{route}">{e(p["title"])}</a></h3>'
                 f'<div class="byline row-author">{author_link(p)}<br><small>{metadata}</small></div>'
                 f'<a class="arrow" href="{route}" aria-label="Read {e(p["title"])}">↗</a></article>')
    return result+'</div><p class="empty" id="empty-results" hidden>No poem found along this path. Try another title, poet or line.</p>'

edition_writer_names={x['id']:x['name'].split('/')[0].strip() for x in load_writer_profiles(R)}

def edition_poet(p,show_issue=False):
    ident=p['writer_id']
    name=edition_writer_names.get(ident,p['author'].split('/')[0].strip()) or 'Author not recorded'
    route=profile_routes.get(ident,f'poet-{ident}.html') if ident else None
    asset=writer_portraits.get(str(ident),{}).get('src')
    if ident in (1,43):
        slug='pradeep' if ident==1 else 'paresh'
        asset=next(x['portrait'] for x in json.loads((R/'editor-profiles.json').read_text()) if x['slug']==slug)
    if asset:
        if not (R/asset).is_file():raise ValueError(f'Missing edition portrait: {asset}')
        small=(R/asset).with_name(Path(asset).stem+'-64.webp')
        retina=(R/asset).with_name(Path(asset).stem+'-128.webp')
        srcset=''
        if small.is_file() and retina.is_file():
            asset=str(small.relative_to(R));srcset=f' srcset="{e(str(retina.relative_to(R)))} 2x"'
        picture=f'<img src="{e(asset)}"{srcset} width="56" height="56" alt="" loading="lazy" decoding="async">'
    else:
        initials=''.join(word[0] for word in name.split()[:2]) if ident else '—'
        picture=f'<span class="edition-poet-initials" aria-hidden="true">{e(initials)}</span>'
    portrait=(f'<a class="edition-poet-portrait" href="{route}" aria-label="About {e(name)}">{picture}</a>' if route else f'<span class="edition-poet-portrait">{picture}</span>')
    byline=f'<a href="{route}">{e(name)}</a>' if route else e(name)
    if show_issue and p['edition']:
        byline+=f'<small class="collection-issue"><a href="issue-{p["edition"]}.html">Issue {p["edition"]}</a></small>'
    language={'or':'Odia','hi':'Hindi','en':'English'}[p['language']]
    return (f'<div class="edition-poet-context">{portrait}<div class="byline row-author">{byline}</div>'
        f'<span class="edition-language original-language" lang="en"><span class="mobile-original-label">Original: </span>{language}</span></div>')

def edition_rows(items,show_issue=False):
    result='<div class="poem-list edition-poem-list">'
    for i,p in enumerate(items,1):
        lang=p['language'];route=poem_route(p['id'])
        titles={lang:p['title'],**{code:v['title'] for code,v in TRANSLATIONS.get(str(p['id']),{}).get('variants',{}).items()}}
        translated_lines=[line for variant in TRANSLATIONS.get(str(p['id']),{}).get('variants',{}).values() for stanza in variant['stanzas'] for line in stanza]
        issue=publication_by_issue.get(p['edition'])
        edition_search=f'Issue {issue["number"]} Edition {issue["number"]} {issue["month"]} {issue["year"]}' if issue else 'Edition not recorded'
        searchable=' '.join([p['title'],p['author'],edition_writer_names.get(p['writer_id'],''),p['text'],*titles.values(),*translated_lines,edition_search])
        reading_attrs=f' data-reading-titles="{e(json.dumps(titles,ensure_ascii=False))}" data-search="{e(searchable)}" data-edition="{p["edition"] or "unassigned"}" data-poet="{p["writer_id"] or "unknown"}"'
        result+=(f'<article class="poem-row edition-poem-row" data-lang="{lang}"{reading_attrs}>' 
            f'<span class="number">{i:02d}</span><h3 class="{lang}" lang="{lang}"><a href="{route}">{e(p["title"])}</a></h3>'
            +edition_poet(p,show_issue)+
            f'<a class="edition-read" href="{route}" aria-label="Read {e(p["title"])}"><svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true" focusable="false" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M12 5.5C9 3.8 6 3.8 3 4.5v14c3-.7 6-.7 9 1 3-1.7 6-1.7 9-1v-14c-3-.7-6-.7-9 1Z"/><path d="M12 5.5v14M6 8h3m6 0h3M6 11h3m6 0h3"/></svg><span class="read-tooltip" aria-hidden="true">Read poem</span></a></article>')
    return result+'</div>'

def collection_tools_markup():
    return '<script defer src="assets/collection-reader.js?v=4"></script><div class="collection-tools-row"><div class="collection-reader-tools" id="collection-reader-tools"><button type="button" id="collection-tools-button" aria-expanded="false" aria-controls="collection-reader-panel" aria-label="Reader tools"><span class="reader-aa" aria-hidden="true">Aa</span></button><section class="collection-reader-panel" id="collection-reader-panel" aria-label="Reader tools" hidden><div class="collection-tools-head"><strong>Reader tools</strong><button type="button" id="collection-tools-close" aria-label="Close reader tools">×</button></div><p class="collection-tools-label">Language</p><div class="collection-choices" role="group" aria-label="Reading language">'+''.join(f'<button type="button" data-collection-language="{code}" aria-pressed="{str(code=="original").lower()}">{label}</button>' for code,label in [('original','Original'),('or','Odia'),('hi','Hindi'),('en','English')])+'</div><p class="collection-tools-label">Text size</p><div class="collection-choices collection-sizes" role="group" aria-label="Text size">'+''.join(f'<button type="button" data-collection-size="{code}" aria-pressed="{str(code=="standard").lower()}">{label}</button>' for code,label in [('standard','Standard'),('large','Large'),('extra-large','Extra large')])+'</div><p>Choose a language for the titles and the poems you open.</p><button class="text-link" type="button" id="collection-tools-reset">Reset reading tools</button></section></div></div>'

def collection_actions(route,title,kind):
    metadata=e(json.dumps({'id':route.removesuffix('.html'),'reader':route,'title':title,'author':'Kabita Live','lang':'en','kind':kind},ensure_ascii=False))
    return '<div class="collection-actions" role="group" aria-label="Reading actions">'+collection_tools_markup()+f'<button type="button" data-share-collection="{metadata}">'+discovery_mark('share')+'<span>Share</span></button><button type="button" id="open-focus">'+discovery_mark('footer-story')+'<span>Read quietly</span></button>'+('<a class="text-link collection-archive" href="archive.html">All editions</a>' if kind=='edition' else '')+'</div>'

from poem_experience import prepare_readers, enhance_poem, encoded
import re
reader_portraits={}
for p in publication_poems.values():
    portrait=re.search(r'<img src="([^"]+)"',edition_poet(p))
    if portrait:reader_portraits[p['writer_id']]=portrait[1]
experience_readers=prepare_readers(publication_poems,publication_issues,poem_route,edition_writer_names,reader_portraits)

def collection_reader(entries,url):
    return '<script type="application/json" id="focus-entry-data">'+encoded(experience_readers[entries[0]['id']])+'</script><script type="application/json" id="focus-edition-data">'+encoded({'url':url,'collection':True})+'</script>'+(R/'templates/quiet-reader.html').read_text()

for issue in publication_issues:
    n=issue['number'];entries=[publication_poems[pid] for pid in issue['poem_ids']]
    date=f'{issue["month"]} {issue["year"]}';art=cover_by_number[n]
    refs=' '.join(f'<a class="text-link" href="{e(ref["url"])}" target="_blank" rel="noopener noreferrer">{e(ref["label"])} ↗</a>' for ref in art.get('sources',[]))
    culture=f'<div class="edition-cultural"><h3>Cultural connection</h3><p>{e(art["cultural_connection"])}</p>'+(f'<div class="edition-cover-sources">{refs}</div>' if refs else '')+'</div>'
    cover_figure='<figure class="edition-cover">'+cover(n)+'</figure>'
    current=n==current_home_issue['number']
    issue_label=(f'<span class="eyebrow discovery-label">{discovery_mark("footer-story")}Current issue · {n}</span>' if current else f'<span class="eyebrow discovery-label">{discovery_mark("footer-story")}Issue {n}</span>')
    jump='<a class="edition-jump" href="#edition-poems">'+discovery_mark('footer-story')+'Browse poems</a>'
    page(f'issue-{n}.html',f'Issue {n} · {date}',discovery_styles+crumb('<a href="archive.html">Archive</a> / '+str(n))+
        '<section class="issue-intro edition-opening'+(' current-edition' if current else ' artistic-edition')+'">'+cover_figure+f'<div>{issue_label}<h1>{e(date)}</h1>'+jump+
        f'<details class="edition-story"><summary>About this cover</summary><h2>{e(art["title"])}</h2><p>{e(art["story"])}</p>{culture}</details></div></section>'+
        '<section class="section edition-contents" data-collection-reader id="edition-poems" tabindex="-1" aria-label="Poems in this edition">'+collection_actions(f'issue-{n}.html',f'{date} · Issue {n}','edition')+'<div class="edition-contents-separator" aria-hidden="true"></div>'+edition_rows(entries)+'</section>'+collection_reader(entries,f'assets/reading-editions/issue-{n}.json'),
        active='Current issue' if current else 'Archive')

import re

def reader_icon(name):
    svg=(R/f'assets/icons/earth-voice-v1/ink/{name}.svg').read_text()
    svg=re.sub(r' role="img"| aria-label="[^"]*"','',svg)
    return svg.replace('<svg ','<svg aria-hidden="true" focusable="false" ',1)

def poem_byline(p):
    if not p['writer_id']:
        return '<p class="byline">Author not recorded</p>'
    ident=p['writer_id'];route=profile_routes.get(ident,f'poet-{ident}.html')
    asset=writer_portraits.get(str(ident),{}).get('src')
    if ident in (1,43):
        slug='pradeep' if ident==1 else 'paresh'
        asset=next(x['portrait'] for x in json.loads((R/'editor-profiles.json').read_text()) if x['slug']==slug)
    small=(R/asset).with_name(Path(asset).stem+'-64.webp') if asset else None
    retina=(R/asset).with_name(Path(asset).stem+'-128.webp') if asset else None
    if small and small.exists() and retina.exists():
        portrait=f'<img class="poem-poet-portrait" src="{e(str(small.relative_to(R)))}" srcset="{e(str(retina.relative_to(R)))} 2x" width="56" height="56" alt="" decoding="async">'
    elif asset:
        if not (R/asset).is_file():raise ValueError(f'Missing poet portrait: {asset}')
        portrait=f'<img class="poem-poet-portrait" src="{e(asset)}" width="56" height="56" alt="" decoding="async">'
    else:portrait=''
    return f'<p class="byline poem-byline"><a href="{route}">{portrait}<span>By {e(p["author"])}</span></a></p>'

poem_art_library={a['id']:a for a in json.loads((R/'data/poem-art-library.json').read_text())['artworks']}
for artwork in poem_art_library.values():
    if not artwork['src'].startswith(('assets/poem-art/','assets/section-art/')) or not (R/artwork['src']).is_file():
        raise ValueError(f"Poem artwork must be a present non-cover asset: {artwork['src']}")
poem_art_assignments=json.loads((R/'data/poem-art-assignments.json').read_text())['assignments']
poem_art_captions=json.loads((R/'data/poem-art-captions.json').read_text())
edition_art_path=R/'data/edition-art-direction.json'
edition_art_direction=json.loads(edition_art_path.read_text()) if edition_art_path.exists() else {'poems':{}}
for p in publication_poems.values():
    ident=p['id'];lang=p['language'];label=language_labels[lang];n=p['edition'];route=poem_route(ident)
    issue=publication_by_issue.get(n);date=f'{issue["month"]} {issue["year"]}' if issue else 'Poetry collection'
    directed_art=edition_art_direction['poems'].get(str(ident))
    if directed_art and directed_art['edition']!=n:
        raise ValueError(f'Edition artwork scope mismatch for poem {ident}')
    if directed_art and directed_art['mode']=='text':
        art='<aside class="poem-art poem-text-context" aria-label="Edition and poet context"><!--poem-context--></aside>'
    elif directed_art and directed_art['mode']=='illustrated':
        if not directed_art['src'].startswith('assets/poem-art/editions/') or not (R/directed_art['src']).is_file():
            raise ValueError(f'Missing edition-specific artwork for poem {ident}')
        art=f'<figure class="poem-art framed"><img src="{directed_art["src"]}" alt="{e(directed_art["alt"])}" width="{directed_art["width"]}" height="{directed_art["height"]}" decoding="async"><figcaption>{e(directed_art["caption"])}</figcaption></figure>'
    elif ident in sample_routes:
        slug=sample_routes[ident].removeprefix('poem-').removesuffix('.html')
        art=f'<figure class="poem-art"><img src="assets/poem-art/{slug}.webp" alt="{art_alts[slug]}" width="1536" height="1024"><figcaption>{e(image_caption(f"assets/poem-art/{slug}.webp"))}</figcaption></figure>'
    else:
        art_record=poem_art_library[poem_art_assignments[str(ident)]]
        art=f'<figure class="poem-art {art_record.get("visual_treatment", "framed")}"><img src="{art_record["src"]}" alt="{e(art_record["alt"])}" width="{art_record["width"]}" height="{art_record["height"]}" decoding="async"><figcaption>{e(image_caption(art_record["src"]))}</figcaption></figure>'
    issue_route=f'issue-{n}.html' if n else 'poems.html'
    issue_label=f'{date} · Issue {n}' if n else date
    actions=(f'<div class="poem-actions" role="group" aria-label="Poem actions"><button type="button" data-share="{ident}">'+reader_icon('share')+'<span>Share</span></button>'+
        f'<a href="contact.html?poem={ident}">'+reader_icon('write')+'<span>Write to the editor</span></a></div>')
    body=(f'<section class="poem-opening"><div class="poem-heading"><p class="reader-meta"><a href="{issue_route}">{e(issue_label)}</a> · <span lang="{lang}">{label}</span></p>'+
        f'<h1 class="{lang}" lang="{lang}">{e(p["title"])}</h1>'+poem_byline(p)+actions+'</div>'+art+'</section>')
    body+=render_reader(p)
    # The edition panel already provides nearby poems; finish the verse with
    # its existing closing mark and keep reader responses in their own slot.
    if p['writer_id']:
        writer_route=profile_routes.get(p['writer_id'],f'poet-{p["writer_id"]}.html')
        body+=f'<a class="poem-more" href="{writer_route}">More by this poet</a>'
    body+='<!--poem-responses-->'
    body=enhance_poem(body,p,experience_readers[ident])
    page(route,p['title'],body,active='Poems')

all_publication_poems=[publication_poems[pid] for issue in publication_issues for pid in issue['poem_ids']]+[p for p in publication_poems.values() if not p['edition']]
finder_poets={str(p['writer_id'] or 'unknown'):edition_writer_names.get(p['writer_id'],p['author'].split('/')[0].strip()) or 'Author not recorded' for p in all_publication_poems}
poet_options='<option value="">All poets</option>'+''.join(f'<option value="{e(ident)}">{e(name)}</option>' for ident,name in sorted(finder_poets.items(),key=lambda item:item[1].casefold()))
edition_options='<option value="">All editions</option>'+''.join(f'<option value="{issue["number"]}">Issue {issue["number"]} · {issue["month"]} {issue["year"]}</option>' for issue in publication_issues)
if any(not p['edition'] for p in all_publication_poems):edition_options+='<option value="unassigned">Edition not recorded</option>'
poem_finder='<div class="poem-finder poem-finder-options"><div class="search-field"><label><span class="label finder-label">Find a poem</span><input id="list-search" type="search" placeholder="A title, a poet, a remembered line" aria-controls="poem-results"></label></div><label class="finder-choice"><span class="finder-label">Poet</span><select id="poem-poet-filter" aria-controls="poem-results">'+poet_options+'</select></label><label class="finder-choice"><span class="finder-label">Edition</span><select id="poem-edition-filter" aria-controls="poem-results">'+edition_options+'</select></label></div>'
for route,title,kicker,heading in [('poems.html','Poems','The reading room','Find a poem')]:
    opening=head(discovery_mark('kendu')+kicker,heading,f'Search {len(publication_poems)} poems by title, poet or a remembered line.').replace('class="eyebrow"','class="eyebrow discovery-label"',1)

    page(route,title,discovery_styles+'<div class="poems-artistic" data-collection-reader>'+opening+
        '<section class="section edition-contents collection-contents" aria-label="Find and read poems">'+collection_actions('poems.html','Poems · Kabita Live','collection')+poem_finder+'<div class="finder-summary"><p class="filter-status" id="filter-status" role="status" aria-live="polite" aria-atomic="true"></p><button type="button" id="filter-reset" class="text-link" hidden>Clear search</button></div>'+edition_rows(all_publication_poems,True).replace('<div class="poem-list edition-poem-list">','<div class="poem-list edition-poem-list" id="poem-results">',1)+'<p class="empty" id="empty-results" hidden>No poem found. Try another word, poet or edition, or clear your search.</p>' +'<nav id="poem-pagination" class="poem-pagination" aria-label="Poem results pages" hidden><button type="button" class="btn" id="poems-previous">Previous</button><span id="poems-page" aria-live="polite"></span><button type="button" class="btn" id="poems-next">Next</button></nav><noscript><p>All poems are available below without JavaScript. You can also <a href="archive.html">browse by edition</a>.</p></noscript></section></div>'+collection_reader(all_publication_poems,'assets/reading-all.json'),active='Poems')

# Retain old bookmarks without maintaining a second poem catalogue.
(R/'search.html').write_text('''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>Find a poem · Kabita Live</title><link rel="canonical" href="poems.html"><script src="assets/search-redirect.js"></script><noscript><meta http-equiv="refresh" content="0;url=poems.html"></noscript></head><body data-pagefind-ignore><p>Browse and search in <a href="poems.html">Poems</a>.</p></body></html>''')

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

if publication_archived:
    for p in publication_archived.values():
        route=poem_route(p['id'])
        page(route,p['title'],crumb('<a href="archive.html">Archive</a> / Poem')+
            head('Poem',e(p['title']))+
            '<article class="prose"><p class="byline">'+author_link(p)+'</p>'+
            '<p>The poem text is currently unavailable.</p>'+
            f'<p>Originally listed in Issue {p["edition"]}.</p>'+
            '<a class="text-link" href="archive.html">Back to the archive</a></article>',active='Archive')

status=json.loads((R/'data/content-status.json').read_text())
status.update(complete_poem_texts=len(publication_poems),excerpt_poems=0,known_poem_records=len(publication_poems)+len(publication_archived),
    archived_poem_records=sorted(publication_archived),
    complete_edition_contents=len(publication_issues),edition_assigned_poems=sum(bool(p['edition']) for p in publication_poems.values()),
    unassigned_poems=[p['id'] for p in publication_poems.values() if not p['edition']],
    missing_author_names=[p['id'] for p in publication_poems.values() if not p['author']],
    writer_records=len(writer_profiles),captured_writer_profiles=len(json.loads((R/'data/writer-profiles.json').read_text())),launch_ready=False,
    blockers=['One poem has no recorded edition and one has no recorded author.',
              'Complete reviews, missing writer biographies and editorial content review remain outstanding.'])
(R/'data/content-status.json').write_text(json.dumps(status,ensure_ascii=False,indent=2)+'\n')
(R/'data/local-routes.json').write_text(json.dumps({str(pid):poem_route(pid) for pid in publication_poems},indent=2)+'\n')
