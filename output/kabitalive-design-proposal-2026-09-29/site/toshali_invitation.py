"""Source-backed anthology invitation. Private Firebase intake; disabled until backend activation is verified."""
from html import escape
import json, hashlib
from writer_names import load_writer_profiles, writer_aliases

ROUTE = 'toshali-anthology-2027.html'
DESCRIPTION = 'Original poems on any theme, up to 30 lines. Send a bio of up to 75 words and a recent photograph by 31 October 2026.'


def invitation_profiles(root):
    profiles = load_writer_profiles(root)
    aliases = writer_aliases(root)
    portraits = json.loads((root/'data/writer-portraits.json').read_text())
    routes = {82:'poet-dokana.html',337:'poet-kshanika.html',257:'poet-drink.html',1:'editor-pradeep.html',43:'editor-paresh.html'}
    result = []
    for w in profiles:
        ident = w['id']
        if ident in aliases: continue
        name = {1:'Pradeep Biswal',43:'Paresh Kumar Pattnaik'}.get(ident,w['name'])
        names = [name,w.get('captured_name',''),*[a['name'] for a in profiles if aliases.get(a['id']) == ident]]
        art = portraits.get(str(ident),{})
        src = art.get('src') or {1:'assets/editors/pradeep-biswal-artistic-v2.webp',43:'assets/editors/paresh-kumar-pattnaik-artistic-v2.webp'}.get(ident,'')
        reusable = bool(src) and art.get('kind') != 'generic_artwork'
        if src: assert (root/src).is_file(), src
        result.append(dict(id=str(ident),name=name,names=list(dict.fromkeys(n for n in names if n)),profile=routes.get(ident,f'poet-{ident}.html'),image=src,reusable=reusable,kind=art.get('kind','generated_portrait' if src else 'missing'),photoHash=hashlib.sha256((root/src).read_bytes()).hexdigest() if reusable else '',photoSize=(root/src).stat().st_size if reusable else 0,photoType={'webp':'image/webp','jpg':'image/jpeg','jpeg':'image/jpeg','png':'image/png'}.get(src.rsplit('.',1)[-1],'') if reusable else ''))
    return sorted(result,key=lambda w:w['name'].casefold())


def render_toshali_invitation(root, page):
    (root/'assets/toshali-poets.json').write_text(json.dumps(invitation_profiles(root),ensure_ascii=False,separators=(',',':'))+'\n')
    body = '''<article class="toshali-invite">
<div class="breadcrumb"><a href="index.html">Home</a> / A poetry invitation</div>
<header class="toshali-hero">
<div><p class="eyebrow">Toshali Literature Festival · Bhubaneswar</p>
<h1>Toshali Anthology<br>of Poetry <em>2027</em></h1>
<p class="toshali-deck">A place for your poem.<br>A gathering of voices.</p>
<p>Original poems on any theme are invited for an anthology to be released in January 2027 during the Toshali Literature Festival.</p>
<p class="toshali-deadline">Entries by <strong><time datetime="2026-10-31">31 October 2026</time>, 11:59 p.m. IST</strong></p>
<a class="btn solid" href="#prepare-entry">Prepare your entry <span aria-hidden="true">↓</span></a>
<p class="toshali-organiser">An invitation from Toshali Literature Trust, Bhubaneswar.</p></div>
<figure class="article-lead"><img src="assets/invitations/toshali/writing-desk-1536.webp" srcset="assets/invitations/toshali/writing-desk-640.webp 640w, assets/invitations/toshali/writing-desk-1200.webp 1200w, assets/invitations/toshali/writing-desk-1536.webp 1536w" sizes="(max-width:760px) 92vw, 46vw" width="1536" height="1024" fetchpriority="high" alt="An imagined writing desk with an open book and fountain pen, looking towards temple spires and trees in Bhubaneswar."></figure>
</header>
<section class="toshali-requirements" aria-label="What to send">
<div><span class="toshali-number">30</span><h2>Lines of poetry</h2><p>An original poem, on any theme.</p></div>
<div><span class="toshali-number">75</span><h2>Words about you</h2><p>A brief biodata to accompany your work.</p></div>
<div><span class="toshali-number">01</span><h2>Recent photograph</h2><p>Use your profile picture or upload a new one.</p></div>
</section>
<section class="toshali-intake" id="prepare-entry" aria-labelledby="entry-heading">
<aside><p class="eyebrow">Your contribution</p><h2 id="entry-heading">Let your words travel.</h2>
<p>Send your original poem, brief biodata and a recent photograph for consideration in the anthology.</p>
<p>Your entry and photograph are retained indefinitely, whether or not your poem is selected, and kept private for authorised anthology review. Nothing is published automatically. Keep your own copy of your poem.</p>
<p>Questions for the organisers?<br><a class="toshali-email" href="mailto:toshalianthology@gmail.com">toshalianthology@gmail.com</a></p>
<details><summary>About the anthology</summary><p>The announcement says copies will be available at a discount during the festival, and later on Amazon.</p><p>For language eligibility, selection details or other questions, please contact the organisers at the address above.</p></details>
</aside>
<div class="toshali-form-wrap">
<noscript><p>Email your original poem (up to 30 lines), bio (up to 75 words) and recent photograph to <a href="mailto:toshalianthology@gmail.com">toshalianthology@gmail.com</a>. Enable JavaScript to use the entry helper.</p></noscript>
<p id="intake-availability" class="toshali-help" role="status">Form preview — online submissions are not active here yet. You can review an entry without sending it.</p>
<form id="toshali-form" method="dialog" aria-labelledby="entry-heading">
<p class="toshali-form-note">Unfinished text is saved in this browser tab when available. Photographs and consent are not saved in the draft. Keep your own copy; browser recovery is not a backup.</p>
<p id="draft-recovery-status" class="toshali-help" role="status"></p><button id="clear-local-draft" class="btn" type="button">Clear saved draft</button>
<div class="toshali-fields"><div><label for="entry-name">Your name</label><input id="entry-name" name="poetName" autocomplete="name" maxlength="120" required aria-describedby="profile-help"><p class="toshali-help" id="profile-help">Start typing to find your Kabita Live profile.</p></div>
<div><label for="entry-email">Email address</label><input id="entry-email" name="email" type="email" autocomplete="email" maxlength="254" required></div></div>
<section id="profile-matches" aria-label="Matching poet profiles" hidden><p id="profile-match-status" class="toshali-help" role="status"></p><div id="profile-options"></div></section>
<div id="selected-profile" hidden></div>
<label for="entry-title">Poem title</label><input id="entry-title" name="poemTitle" maxlength="200" required dir="auto">
<label for="entry-poem">Your poem</label><p class="toshali-help" id="poem-help">Up to 30 verse lines. Blank lines between stanzas do not count. Paste your poem in its original language.</p>
<textarea id="entry-poem" name="poem" rows="12" required dir="auto" aria-describedby="poem-help poem-count" spellcheck="false"></textarea>
<p class="toshali-count" id="poem-count" role="status" aria-live="polite">0 / 30 lines</p>
<label for="entry-bio">Brief biodata</label><p class="toshali-help" id="bio-help">Up to 75 words. A few words about you and your writing.</p>
<textarea id="entry-bio" name="bio" rows="5" required dir="auto" aria-describedby="bio-help bio-count"></textarea>
<p class="toshali-count" id="bio-count" role="status" aria-live="polite">0 / 75 words</p>
<div id="photo-upload"><label for="entry-photo">Recent photograph</label><p class="toshali-help" id="photo-help">JPEG, PNG or WebP, up to 5 MB. Your original file is retained privately.</p><input id="entry-photo" name="photo" type="file" accept="image/jpeg,image/png,image/webp" required aria-describedby="photo-help photo-status"><p id="photo-status" class="toshali-help" role="status"></p><img id="photo-preview" width="120" height="120" alt="Your selected photograph" hidden></div><button class="btn" id="keep-profile-picture" type="button" hidden>Keep my profile picture</button><p class="toshali-help" id="photo-choice-status" role="status"></p>
<label class="toshali-check"><input type="checkbox" name="original" required> <span>I confirm this is my original poem and agree to indefinite private storage of my entry and photograph for anthology review.</span></label>
<button class="btn solid" id="prepare-button" type="submit" hidden>Review your entry</button>
<p class="toshali-help">Review your details before submitting. Nothing is sent at this step.</p>
</form>
<section class="toshali-draft" id="entry-draft" aria-labelledby="draft-heading" hidden>
<h3 id="draft-heading" tabindex="-1">Your entry is ready to review</h3>
<p><strong>Not submitted yet.</strong> Check your words and photograph before sending.</p>
<label for="entry-preview">Your entry</label><textarea id="entry-preview" readonly rows="12" dir="auto"></textarea>
<p id="entry-readiness" class="toshali-help" role="status">Checking submission availability…</p>
<div class="toshali-actions"><button class="btn solid" id="submit-entry" type="button" disabled>Submit privately</button><button class="btn" id="edit-entry" type="button">Edit entry</button></div>
<p id="entry-status" role="status" aria-live="polite"></p>
</section></div></section></article>'''
    page(ROUTE, 'Toshali Anthology of Poetry 2027', body, desc=DESCRIPTION)
    path = root / ROUTE
    text = path.read_text().replace('</head>', '<meta name="description" content="' + escape(DESCRIPTION, quote=True) + '"><link rel="stylesheet" href="assets/toshali-invitation.css?v=3"><script type="module" src="assets/toshali-invitation.mjs?v=3"></script></head>', 1)
    path.write_text(text)
