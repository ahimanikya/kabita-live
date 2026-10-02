"""Current-edition homepage candidates; source excerpts stay in publication records."""
from datetime import datetime
from html import escape, unescape
import json


def render_home_features(root, issue, source_poems, profile_routes, sample_routes, format_excerpt):
    portraits=json.loads((root/'data/writer-portraits.json').read_text())
    from writer_names import load_writer_profiles
    names={p['id']:p['name'] for p in load_writer_profiles(root)}
    approved=json.loads((root/'data/home-featured.json').read_text())
    labels={'or':'ଓଡ଼ିଆ','hi':'हिन्दी','en':'English'}
    groups={lang:[] for lang in labels}
    for ident in issue['poem_ids']:
        p=source_poems[ident];lang=p['language']
        if lang not in groups or p.get('status')!='captured_full_text' or not p['text'].strip():continue
        author=names.get(p['writer_id'],p['author']).split('/')[0].strip()
        # Keep the approved display names and small portraits for the original three cards.
        f=approved.get(str(ident),{})
        if f and (f['writer_id']!=p['writer_id'] or f['excerpt'] not in p['text']):
            raise ValueError(f'Homepage excerpt identity/source mismatch: {ident}')
        profile=profile_routes.get(p['writer_id'],f'poet-{p["writer_id"]}.html')
        route=sample_routes.get(ident,f'poem-{ident}.html')
        portrait=f.get('portrait') or portraits.get(str(p['writer_id']),{}).get('src')
        picture=''
        if portrait:
            if not (root/portrait).is_file():raise ValueError(f'Missing homepage portrait: {portrait}')
            retina=f.get('portrait_2x')
            srcset=f' srcset="{escape(portrait)} 1x, {escape(retina)} 2x"' if retina else ''
            picture=f'<a class="card-portrait" href="{profile}" aria-label="Meet {escape(author)}"><img src="{escape(portrait)}"{srcset} alt="" width="64" height="64" loading="lazy" decoding="async"></a>'
        excerpt=format_excerpt(unescape(f.get('excerpt',p['text'])),lang)
        card=(f'<article class="language-card" data-featured-poem="{ident}" data-lang="{lang}"><div class="language-label"><span lang="{lang}">{labels[lang]}</span></div>'
              f'<div class="card-identity">{picture}<div class="card-identity-copy"><h3 class="{lang}" lang="{lang}"><a href="{route}">{escape(unescape(p["title"]))}</a></h3><a class="byline" href="{profile}">{escape(author)}</a></div></div>'
              f'<p class="excerpt {lang}" lang="{lang}">{escape(excerpt)}</p><a class="text-link" href="{route}">Read the poem</a></article>')
        groups[lang].append((ident,card))
    anchor=datetime.strptime(f'{issue["year"]} {issue["month"]}', '%Y %B').strftime('%Y-%m-01')
    fallback=''.join(items[0][1] for items in groups.values() if items)
    templates=''.join(f'<template data-featured-language="{lang}" data-poem-id="{ident}" data-pagefind-ignore>{card}</template>' for lang,items in groups.items() for ident,card in items)
    return (f'<div class="three" id="daily-featured-poems" data-rotation-start="{anchor}" data-edition="{issue["number"]}">{fallback}</div>'
            f'<div hidden id="featured-poem-pool" data-pagefind-ignore>{templates}</div><script type="module" src="assets/home-featured.js?v=1"></script>')
