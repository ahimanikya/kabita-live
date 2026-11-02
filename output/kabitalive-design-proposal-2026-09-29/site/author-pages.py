"""Author profiles share the approved editor layout; evidence stays in the KB."""
writer_portraits=json.loads((R/'data/writer-portraits.json').read_text())
writer_enrichment=json.loads((R/'data/writer-enrichment.json').read_text())
writer_quotes=json.loads((R/'data/writer-quotes.json').read_text())

def author_quote(writer):
    selection=writer_quotes.get(str(writer['id']))
    if not selection:return ''
    poem=publication_poems[selection['poem_id']]
    text=selection['text']
    if poem['writer_id']!=canonical_writer(writer['id']) or poem['text'][selection['text_start']:selection['text_end']]!=text:
        raise ValueError(f'Quote source mismatch for writer {writer["id"]}')
    lang=poem['language'];route=catalogue[poem['id']]['reader']
    return f'<figure class="author-quote" data-quote-poem="{poem["id"]}"><blockquote lang="{lang}">{e(text)}</blockquote><figcaption>— <a href="{e(route)}" lang="{lang}"><cite>{e(poem["title"])}</cite></a></figcaption></figure>'

def author_artistic_mark(name):
    svg=(R/f'assets/icons/earth-voice-v1/ink/{name}.svg').read_text()
    svg=re.sub(r' role="img"| aria-label="[^"]*"| aria-hidden="[^"]*"| focusable="[^"]*"','',svg)
    return svg.replace('<svg ','<svg class="author-artistic-mark" aria-hidden="true" focusable="false" ',1)

def author_identity(name):
    roman,separator,native=name.partition('/')
    if separator and re.search(r'[\u0900-\u097f\u0b00-\u0b7f]',native):
        lang=text_language(native)
        return f'<h1 lang="{text_language(roman)}">{e(roman.strip())}</h1><p class="author-native {lang}" lang="{lang}">{e(native.strip())}</p>'
    lang=text_language(name)
    return f'<h1 class="{lang}" lang="{lang}">{e(name)}</h1>'

def author_portrait(writer):
    asset=writer_portraits.get(str(writer['id']))
    if asset:
        if not (R/asset['src']).is_file():raise ValueError(f'Missing portrait for writer {writer["id"]}')
        if asset['kind']=='generic_artwork':
            return f'<figure class="editor-portrait author-portrait generic_artwork"><img src="{e(asset["src"])}" alt="Generic feminine watercolor illustration; not a likeness of {e(writer["name"])}" width="600" height="600" decoding="async"><figcaption class="small muted">Generic artwork · photograph unavailable</figcaption></figure>'
        kind=asset['kind'];shape=' portrait-tall' if asset.get('aspect')=='3:4' else '';width=asset.get('width',600);height=asset.get('height',600);label='Artistic portrait of ' if kind=='generated_portrait' else 'Portrait of '
        return f'<figure class="editor-portrait author-portrait {kind}{shape}"><img src="{e(asset["src"])}" alt="{label}{e(writer["name"])}" width="{width}" height="{height}" decoding="async"></figure>'
    roman=writer['name'].split('/')[0].strip()
    initials=''.join(word[0] for word in roman.split()[:2]).upper()
    return f'<div class="editor-portrait author-initials" aria-hidden="true"><span>{e(initials)}</span></div>'

def author_sidebar(writer,enriched):
    books=enriched.get('books',[])
    if books:
        return '<aside class="editor-book-shelf" id="selected-books"><h2>A few places to begin.</h2><p class="small muted">Selected books</p><ul>'+''.join(f'<li><a href="{e(b["url"])}" target="_blank" rel="noopener noreferrer">{e(b["title"])} ↗</a><span>{e(b["detail"])}</span></li>' for b in books)+'</ul></aside>'
    return ''

def author_biography_sections(sections):
    """Keep source paragraphs whole; only long, multi-paragraph lives may fold."""
    paragraphs=[p for section in sections for p in section['paragraphs']]
    fold=len(paragraphs)>1 and sum(len(p.split()) for p in paragraphs)>110
    def paragraph(text,lang):
        return f'<p lang="{lang}">{e(text)}</p>'
    opening=[];remaining=[];first_paragraph=True
    for section in sections:
        heading=f'<h2>{e(section["heading"])}</h2>'
        lang=section.get('language','en')
        languages=section.get('paragraph_languages',[lang]*len(section['paragraphs']))
        parts=[paragraph(p,language) for p,language in zip(section['paragraphs'],languages)]
        if fold and first_paragraph and parts:
            continuation=' class="profile-intro-continued"' if parts[1:] else ''
            opening.append('<section'+continuation+'>'+heading+parts[0]+'</section>')
            if parts[1:]:remaining.append('<section>'+''.join(parts[1:])+'</section>')
            first_paragraph=False
        elif fold and not first_paragraph:
            remaining.append('<section>'+heading+''.join(parts)+'</section>')
        else:
            opening.append('<section>'+heading+''.join(parts)+'</section>')
    if fold:
        opening.append('<details class="profile-more" open><summary><span class="more-closed">Read more about the poet</span><span class="more-open">Show less</span></summary><div class="profile-more-content">'+''.join(remaining)+'</div></details>')
    return ''.join(opening)

def render_author(writer):
    ident=writer['id'];extra=writer_enrichment.get(str(ident),{});works=writer['works']
    # Preserve every historical URL while canonical links use the grouped identity.
    route=f'poet-{ident}.html' if ident in writer_identity_aliases else profile_routes.get(ident,f'poet-{ident}.html')
    bio=writer['biography'];sections=extra.get('sections',[])
    body='<link rel="stylesheet" href="assets/author-artistic.css?v=20261102"><script defer src="assets/author-profile.js?v=20261102"></script><div class="author-clear profile-polish">'+crumb('<a href="poets.html">Poets</a> / '+e(writer['name'].split('/')[0].strip()))
    body+='<section class="editor-profile-opening author-profile-opening"><div>'+author_identity(writer['name'])+author_quote(writer)+'</div>'+author_portrait(writer)+'</section>'
    biography='<article id="biography" class="prose editor-biography">'
    if sections:
        biography+=author_biography_sections(sections)
    elif bio:
        # Preserve paragraph-specific script labels in unenriched biographies.
        paragraphs=[p for p in bio.split('\n') if p.strip()]
        source_sections=[{'heading':'Life and writing.','paragraphs':[p.strip() for p in paragraphs],
                          'paragraph_languages':[text_language(p) for p in paragraphs]}]
        biography+=author_biography_sections(source_sections)
    else:
        biography+='<section><h2>A voice in these pages.</h2>'
        if works:
            langs=sorted({catalogue[w['id']]['lang'] for w in works})
            languages=', '.join({'or':'Odia','hi':'Hindi','en':'English'}[x] for x in langs)
            biography+=f'<p>This collection brings together {e(writer["name"].split("/")[0].strip())}’s contributions to Kabita Live, with work in {languages}. Follow each poem to its edition, or read through the collection below.</p>'
        else:biography+='<p>A contributor to the journal’s gathering of voices. Explore Kabita Live’s poetry collection below.</p>'
        biography+='</section>'
    books=author_sidebar(writer,extra)
    biography=biography.replace('<h2>','<h2>'+author_artistic_mark('footer-send-poem'),1)
    contributions=writer_work(writer,compact_profile=True).replace('<h2>','<h2>'+author_artistic_mark('footer-story'),1)
    body+='<div class="author-reading-layout author-clear-reading'+(' has-books' if books else '')+'">'+biography+'</article>'+books+'</div>'+contributions+'</div>'
    page(route,writer['name'],body,active='Poets')
    if ident in writer_identity_aliases:
        target=profile_routes[ident]
        path=R/route
        path.write_text(path.read_text().replace('</head>',f'<link rel="canonical" href="{target}"></head>',1).replace('<main id="main"','<main data-pagefind-ignore="all" id="main"',1))

def author_colophon():
    credit='<section class="colophon" id="credits-writers"><h2>The voices in these pages.</h2><p class="profile-footnote">Biographies and photographs are drawn from the journal’s contributor records. Supplied biographies may describe roles held at the time they were written. Where an artistic portrait is shown, it is based on the writer’s supplied photograph. Pravakar Satapathy’s artistic portrait uses a photograph supplied for this redesign; the other artistic portraits use journal-supplied photographs. Portraits awaiting artistic treatment retain their original photographs. Where photographs are unavailable, shared generic watercolor figures are used and labelled; these do not depict the writers. Research references for expanded profiles appear below. Corrections are welcome through the <a href="contact.html">editorial desk</a>.</p>'
    credit+='<details class="colophon-details"><summary>Author biography references</summary>'
    for ident,extra in writer_enrichment.items():
        name=profile_data[int(ident)]['name']
        portrait=writer_portraits.get(str(ident))
        portrait_credit=portrait.get('credit','Journal-supplied photograph') if portrait else 'Initials; no portrait photograph available'
        portrait_credit=portrait_credit.replace('AI-assisted ', '')
        portrait_credit=portrait_credit[:1].upper()+portrait_credit[1:]
        from datetime import date
        reviewed=date.fromisoformat(extra.get('reviewed_on','2026-09-29')).strftime('%d %B %Y').lstrip('0')
        references='; '.join(f'<a href="{e(s["url"])}" target="_blank" rel="noopener noreferrer">{e(s["label"])} ↗</a>' for s in extra.get('sources',[])) or 'Biography based on the journal’s contributor record and published poems'
        credit+=f'<section class="credit-source" id="credits-writer-{ident}"><h3>{e(name)}</h3><p class="profile-footnote">'+references+f'. Portrait: {e(portrait_credit)}. References reviewed {reviewed}.</p></section>'
    return credit+'</details></section>'
