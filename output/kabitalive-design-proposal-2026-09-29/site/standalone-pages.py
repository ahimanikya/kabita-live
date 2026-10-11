"""Build local collection routes from available records, without inventing missing text."""
from urllib.parse import urlsplit, parse_qs

catalogue = {}
for p in current:
    catalogue[p['id']] = dict(p, issue=47, text_status='excerpt' if p['id'] in sample_routes else 'missing')
for featured in poems:
    wid = int(parse_qs(urlsplit(writers[featured['slug']]['source']).query)['id'][0])
    for ident, title, issue, month, year in writers[featured['slug']]['works']:
        catalogue.setdefault(ident, dict(id=ident,title=title,author=featured['author'],
            lang=featured['lang'],label=featured['label'],profile_id=wid,
            profile=profile_routes.get(wid,f'poet-{wid}.html'),issue=issue,text_status='missing'))
catalogue.setdefault(542,dict(id=542,title='A Poet Has No Land',author='Pradeep Biswal',
    lang='en',label='English',profile_id=1,profile='editor-pradeep.html',issue=None,text_status='missing'))

writer_profiles=load_writer_profiles(R)
profile_data={p['id']:p for p in writer_profiles}

def text_language(text):
    counts={lang:len(re.findall(pattern,text)) for lang,pattern in
            [('or',r'[\u0b00-\u0b7f]'),('hi',r'[\u0900-\u097f]'),('en',r'[A-Za-z]')]}
    return max(counts,key=counts.get)

for writer in writer_profiles:
    wid=writer['id']
    for work in writer['works']:
        lang=text_language(work['title'])
        old=catalogue.get(work['id'],{})
        catalogue[work['id']]=dict(old,**work,author=writer['name'],lang=old.get('lang',lang),
            label=old.get('label',{'or':'ଓଡ଼ିଆ','hi':'हिन्दी','en':'English'}[lang]),
            profile_id=wid,profile=profile_routes.get(wid,f'poet-{wid}.html'),
            text_status=old.get('text_status','missing'))

if publication_poems:
    publication_dates={x['number']:x for x in publication_issues}
    for full in publication_poems.values():
        ident=full['id'];wid=full['writer_id'];lang=full['language']
        catalogue[ident]=dict(id=ident,title=full['title'],author=full['author'] or 'Author not recorded',
            lang=lang,label={'or':'ଓଡ଼ିଆ','hi':'हिन्दी','en':'English'}[lang],profile_id=wid,
            profile=profile_routes.get(wid,f'poet-{wid}.html') if wid else 'poets.html',
            issue=full['edition'],text_status='complete')
        if wid and wid not in profile_data:
            writer=dict(id=wid,name=full['author'],biography='',works=[])
            profile_data[wid]=writer;writer_profiles.append(writer)
            directory.append(dict(name=full['author'],url=f'https://kabitalive.com/contri-view.php?id={wid}'))
    for writer in writer_profiles:
        works=[]
        for full in publication_poems.values():
            if full['writer_id']!=canonical_writer(writer['id']):continue
            date=publication_dates.get(full['edition'],{})
            works.append(dict(id=full['id'],title=full['title'],issue=full['edition'],month=date.get('month'),year=date.get('year')))
        writer['works']=sorted(works,key=lambda x:(x['issue'] or 0,x['id']),reverse=True)

for ident in publication_archived:
    catalogue.pop(ident,None)

for ident, p in catalogue.items():
    p['reader'] = sample_routes.get(ident,f'poem-{ident}.html')
    if ident in sample_routes:
        # Preserve the authored excerpts and established reader layout; disclose their extent.
        target=R/p['reader'];html=target.read_text()
        html=html.replace('<img class="end-mark"', '<p class="content-status">Opening excerpt. The complete poem is not yet available here.</p><img class="end-mark"',1)
        target.write_text(html)
        continue
    issue_route=f'issue-{p["issue"]}.html' if p['issue'] else 'poems.html'
    issue_crumb=f'<a href="{issue_route}">Issue {p["issue"]}</a> / Poetry' if p['issue'] else '<a href="poems.html">Poetry</a>'
    page(p['reader'],p['title'],crumb(issue_crumb)+
        head(p['label']+' · Poetry',e(p['title']))+
        '<article class="prose"><p class="byline">By <a href="'+p['profile']+'">'+e(p['author'])+'</a></p>'+
        '<p class="content-status">The complete poem is not yet available here.</p>'+
        btn('Explore the collection',issue_route,False)+'</article>',active='Poems')

def writer_work(writer):
    if not writer['works']:
        return '<section class="writer-work" id="contributions"><h2>Poems in Kabita Live</h2><p>No poems are currently linked to this profile.</p><a class="text-link" href="poems.html">Explore the poetry collection →</a></section>'
    rows=''
    for w in writer['works']:
        route=catalogue[w['id']]['reader'];lang=catalogue[w['id']]['lang']
        date=' '.join(str(x) for x in [w.get('month'),w.get('year')] if x) or 'Date not recorded'
        edition=(f'<a class="contribution-issue" href="issue-{w["issue"]}.html">Issue {w["issue"]}</a>'
                 if w['issue'] else '<span>Not recorded</span>')
        rows+=(f'<tr data-contribution="{e(w["title"])}"><td><a class="contribution-title" lang="{lang}" href="{route}">{e(w["title"])}</a>'
               f'<span class="contribution-mobile-date">{e(date)}</span></td><td data-label="Edition">{edition}</td><td data-label="Published">{e(date)}</td></tr>')
    count=len(writer['works'])
    heading='Poems in Kabita Live'
    return ('<section class="writer-work" id="contributions"><div class="section-head">'+
            f'<h2>{heading}</h2></div>'+
            f'<table class="contribution-table"><caption class="sr-only">Poems by {e(writer["name"])}</caption>'+
            '<thead><tr><th scope="col">Poem</th><th scope="col">Edition</th><th scope="col">Published</th></tr></thead>'+
            '<tbody>'+rows+'</tbody></table></section>')

exec(compile((R/'author-pages.py').read_text(),str(R/'author-pages.py'),'exec'),globals())

for p in directory:
    ident=int(parse_qs(urlsplit(p['url']).query)['id'][0])
    writer=profile_data.get(ident)
    if not writer:
        raise ValueError(f'Missing captured writer {ident}')
    route=profile_routes.get(ident,f'poet-{ident}.html')
    if ident in {1,43}:
        # Keep the approved editor narrative and portrait; add their complete captured contribution list.
        path=R/route;text=path.read_text()
        text=re.sub(r'<section class="editor-journal-note">.*?</section>','',text,flags=re.S)
        path.write_text(text.replace('<p class="profile-footnote">',writer_work(writer)+'<p class="profile-footnote">',1))
        continue
    render_author(writer)

for p in issues:
    n=p['number']
    if n==47:
        continue
    entries=[x for x in catalogue.values() if x['issue']==n]
    contents=''.join('<article class="poem-row"><span class="number">'+str(i+1)+'</span><h3><a href="'+x['reader']+'">'+e(x['title'])+
        '</a></h3><a href="'+x['profile']+'">'+e(x['author'])+'</a></article>' for i,x in enumerate(entries))
    page(f'issue-{n}.html',f'Issue {n}',crumb('<a href="archive.html">Archive</a> / '+str(n))+
        '<section class="issue-intro">'+cover(n)+'<div><span class="eyebrow">Issue '+str(n)+'</span><h1>'+e(p['month']+' '+p['year'])+
        '</h1><p class="signature" lang="or">ମାଟିର ମହକ · ହୃଦୟର ସ୍ବର</p></div></section>'+coverstory(n)+
        '<section class="section"><h2>Within these pages.</h2>'+contents+
        '<p class="content-status">The complete contents are not yet available here.</p></section>',active='Archive')

review_cards=''
for p in reviews:
    ident=int(parse_qs(urlsplit(p['url']).query)['id'][0]);route=f'review-{ident}.html'
    section_art[route]='book-reviews'
    body=(crumb('<a href="reviews.html">Book reviews</a>')+head('Book review',e(p['title']),'Review by '+e(p['author']))+
        '<article class="prose"><p class="content-status">The complete review is not yet available here.</p>'+btn('More book reviews','reviews.html',False)+'</article>')
    page(route,p['title'],body)
    if ident==11: page('review.html',p['title'],body)
    review_cards+='<article class="review-list-entry"><span class="eyebrow">Book review</span><h2><a href="'+route+'">'+e(p['title'])+'</a></h2><p>Review by '+e(p['author'])+'</p></article>'
page('reviews.html','Book reviews',head('Books in conversation','The reading continues.','A collection of reviews, with room for each reader’s voice.')+'<div class="two review-list">'+review_cards+'</div>')

page('feedback.html','Write to the editors',head('The journal and its readers','Write to the editors',
    'Send a reading response, correction or suggestion.')+
    '<article class="prose"><p>Your note goes privately to the editorial desk. Include the poem’s title and poet when writing about a particular work.</p>'+
    btn('Write a private note','contact.html')+'<p>To share a poem with friends, use Share on its reading page.</p></article>')

page('highlights.html','Literary life',head('Around the journal','Literary life,<br>carefully gathered.',
    'Books, readings and gatherings from the editorial desk.')+
    '<article class="prose"><p>New announcements will appear here.</p>'+btn('Read the current issue','issue-47.html',False)+'</article>')
page('highlight.html','Literary life',head('Around the journal','More words to gather.')+
    '<p>Find the journal’s announcements and literary gatherings.</p>'+btn('Explore literary life','highlights.html'))

# Contact always has an honest working fallback. Firebase enables private intake only after configuration.
contact=R/'contact.html';text=contact.read_text().replace('data-demo="contact"','data-feedback="private"')
text=text.replace('All fields are required except the poem link. This preview sends and stores nothing.',
    'Your message is private. Use the email draft to send it through your email app.')
text=text.replace('Preview message','Open email draft')
text=text.replace('name="name" autocomplete="name" required','name="name" autocomplete="name" maxlength="120" required')
text=text.replace('name="message" required','name="message" maxlength="5000" required')
contact.write_text(text)
submit=R/'submit.html';text=submit.read_text();text=re.sub(r'<div class="notice">These are proposed submission prompts.*?</div>','',text,flags=re.S);submit.write_text(text)
upcoming=R/'upcoming.html';text=upcoming.read_text();upcoming.write_text(text)

about=R/'about.html';text=about.read_text().replace('Reading responses are reviewed before appearing; they do not publish immediately.',
    'Reading responses go privately to the editorial desk. Poems can be shared with their title and poet intact.')
text=text.replace('</main>',author_colophon()+'</main>')
text=text.replace('</main>', '<section class="colophon" id="privacy"><h2>A little care for your privacy.</h2>'+
    ('<p>Private feedback is stored for the editorial team. Public comments show your chosen name and words only after editorial approval. Likes and comments use an anonymous browser identifier; they do not create a reader account. Clearing browser data can reset that identifier.</p>' if json.loads((R/'runtime-config.json').read_text()).get('engagement',{}).get('publicComments') else '<p>Feedback is sent privately to the editorial desk. Public comments are not enabled.</p>')+
    '<p>Reader response features use Google reCAPTCHA Enterprise and Firebase App Check to limit automated abuse. Google processes browser and network signals for this security check, separately from optional Analytics. Google’s <a href="https://policies.google.com/privacy">Privacy Policy</a> and <a href="https://policies.google.com/terms">Terms of Service</a> apply.</p>'+
    '<div id="analytics-settings" hidden><p>Optional Google Analytics helps us understand which pages readers visit. It is off until you choose to allow it. Messages and search terms are not sent to analytics.</p>'+
    '<button class="btn" id="allow-analytics">Allow analytics</button> <button class="btn" id="decline-analytics">Keep analytics off</button>'+
    '<p id="analytics-status" role="status"></p></div></section></main>')
text=text.replace('<details><summary>Typefaces and their makers</summary>', '<details id="credits-translations"><summary>Translations</summary><div class="colophon-details"><p>The additional Odia, Hindi and English reading versions follow each poem’s original language. Original and translated versions are labelled in the reader. The original poems remain unchanged and belong to their respective authors.</p></div></details>'+'<details><summary>Typefaces and their makers</summary>')
about.write_text(text)

status={'schema_version':1,'complete_poem_texts':0,'excerpt_poems':len(sample_routes),'known_poem_records':len(catalogue),
    'issue_records':len(issues),'writer_records':len(directory),'review_records':len(reviews),
    'captured_writer_profiles':len(writer_profiles),'writer_biographies':sum(bool(p['biography']) for p in writer_profiles),
    'complete_review_texts':0,'launch_ready':False,
    'blockers':['Full poem texts and complete issue membership must be imported.','Complete reviews, missing writer biographies and biography fact-checks need editorial content.']}
(R/'data/content-status.json').write_text(json.dumps(status,ensure_ascii=False,indent=2)+'\n')
(R/'data/local-routes.json').write_text(json.dumps({str(k):v['reader'] for k,v in catalogue.items()},indent=2)+'\n')
