"""Approved portrait-card directory; no biography generation or source edits."""
from html import escape
import json,re
from writer_names import writer_aliases

def render_poet_directory(SITE, writers, poems, profile_routes, routes):
    portraits=json.loads((SITE/'data/writer-portraits.json').read_text())
    quotes=json.loads((SITE/'data/writer-quotes.json').read_text())
    aliases=writer_aliases(SITE)
    alias_names={}
    for writer in writers:
     if writer['id'] in aliases:alias_names.setdefault(aliases[writer['id']],[]).append(writer['name'])
    rows=[{'data-directory-name':w['name'],'captured-name':' '.join([w.get('captured_name',''),*alias_names.get(w['id'],[])]),'href':profile_routes.get(w['id'],f"poet-{w['id']}.html")} for w in writers if w['id'] not in aliases]
    cards=[];evidence=[]
    for row in sorted(rows,key=lambda x:x['data-directory-name'].split('/')[0].strip().casefold()):
     raw=row['data-directory-name'];name=raw.split('/')[0].strip();wid={'poet-dokana.html':'82','poet-kshanika.html':'337','poet-drink.html':'257','editor-pradeep.html':'1','editor-paresh.html':'43'}.get(row['href']) or re.search(r'poet-(\d+)\.html',row['href']).group(1)
     if wid=='1':name='Pradeep Biswal'
     if wid=='43':name='Paresh Kumar Pattnaik'
     raw+=' '+row['captured-name']
     works=sorted([p for p in poems.values() if str(p.get('writer_id'))==wid],key=lambda p:p['id'])
     q=quotes.get(wid); selected=None;text=''
     if q:
      selected=poems.get(q['poem_id'])
      if selected:
       assert str(selected['writer_id'])==wid
       assert selected['text'][q['text_start']:q['text_end']]==q['text'],wid
       text='\n'.join(q['text'].strip().splitlines()[:2])
     elif works:
      selected=works[0]; text='\n'.join(selected['text'].strip().splitlines()[:2])
     portrait=portraits.get(wid,{}).get('src') or {'1':'assets/editors/pradeep-biswal-artistic-v2.webp','43':'assets/editors/paresh-kumar-pattnaik-artistic-v2.webp'}.get(wid); initials=''.join(x[0] for x in name.split()[:2]).upper()
     if portrait:assert (SITE/portrait).exists()
     generic=portraits.get(wid,{}).get('kind')=='generic_artwork'
     if generic:portrait=portraits[wid].get('thumbnail',portrait)
     pic=(f'<img src="{escape(portrait)}" alt="{"Generic writer artwork" if generic else ""}" width="64" height="64" loading="lazy" decoding="async">' if portrait else f'<span class="poet-initials" aria-hidden="true">{escape(initials)}</span>')
     body=f'<blockquote lang="{selected["language"]}">{escape(text)}</blockquote>' if text else '<p class="no-excerpt">Meet this writer in their profile.</p>'
     poem_route=routes.get(str(selected['id']),f"poem-{selected['id']}.html") if text else ''
     citation=f'<a class="poet-source" href="{escape(poem_route)}" title="{escape(selected["title"])}" aria-label="Read the quoted poem: {escape(selected["title"])}">From a poem ↗</a>' if text else ''
     count=f'{len(works)} poem'+('' if len(works)==1 else 's') if works else 'Writer profile'
     cards.append(f'<article class="poet-card" data-search="{escape(raw+" "+name)}" data-writer="{wid}"><div class="poet-card-identity">{pic}<h2><a class="poet-profile" href="{escape(row["href"])}">{escape(name)}</a></h2></div>{body}<div class="poet-card-meta"><span>{count}</span>{citation}</div></article>')
     evidence.append({'id':wid,'name':name,'profile':row['href'],'portrait':portrait,'poem_count':len(works),'quote_poem':selected['id'] if text else None,'excerpt':text})
    leaf=(SITE/'assets/icons/earth-voice-v1/ink/kendu.svg').read_text()
    leaf=re.sub(r'role="img" aria-label="[^"]*"','aria-hidden="true" focusable="false"',leaf)
    main='''<div class="poets-directory"><section class="poets-opening"><div><span class="eyebrow artistic-eyebrow">'''+leaf+''' The writers of Kabita Live</span><h1>Poets</h1><p>Find a poet by name and explore their poems.</p></div><img src="assets/section-art/voices-640.webp" alt="" width="640" height="427"><div class="poets-search"><label for="poet-find">Find a poet</label><div class="poets-search-field"><input type="search" id="poet-find" placeholder="Search a name in any script" autocomplete="off"><button type="button" id="poet-clear" hidden>Clear</button></div></div></section><p id="poet-results" class="poet-results" role="status" aria-live="polite"></p><div class="poet-cards" id="poet-cards">'''+''.join(cards)+'''</div><div id="poet-empty" hidden><h2>No poets found.</h2><p>Try another spelling, or clear your search to browse everyone.</p></div><div class="poets-more"><button type="button" class="btn" id="poet-more">Show more poets</button><p id="poet-progress"></p></div><noscript><p>All poets are shown when JavaScript is unavailable.</p></noscript></div>'''
    assert len(evidence)==len({x["id"] for x in evidence}), "Duplicate directory writer IDs"
    return main
