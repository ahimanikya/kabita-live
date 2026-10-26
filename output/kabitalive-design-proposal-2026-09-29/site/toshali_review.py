"""Public sign-in shell only: submission data is never included in a static build."""
def render_toshali_review(root,page):
    body='''<article class="toshali-invite" data-pagefind-ignore="all">
<p class="eyebrow">Toshali Anthology of Poetry 2027</p><h1>Private review desk</h1>
<p>For authorised anthology editors. Entries and photographs remain private and are retained indefinitely. Selection does not send an email. Rejection opens an editable email draft before you confirm sending. Decisions never publish a poem.</p>
<p id="review-status" role="status" aria-live="polite">Preparing sign-in…</p>
<button id="review-login" class="btn solid" type="button" disabled>Sign in with Google</button>
<button id="review-logout" class="btn" type="button" hidden>Sign out</button>
<noscript><p>Enable JavaScript to sign in and review entries.</p></noscript>
<section id="review-workspace" hidden>
<h2>Received entries</h2><p>Open an entry to read it and record a decision. Use Load more to see the next 25 entries.</p>
<ul id="review-entries"></ul><button id="review-more" class="btn" type="button">Load more</button>
<section id="review-entry" hidden aria-labelledby="review-title">
<h2 id="review-title" tabindex="-1" dir="auto"></h2><p id="review-author" dir="auto"></p><p id="review-reference"></p>
<img id="review-photo" width="160" height="160" alt="Contributor photograph" hidden>
<h3>Poem</h3><div id="review-poem" class="review-poem" dir="auto"></div>
<h3>Biodata</h3><p id="review-bio" dir="auto"></p>
<form id="review-decision" method="dialog"><fieldset><legend>Editorial decision</legend>
<label><input type="radio" name="decision" value="received" required> Received</label>
<label><input type="radio" name="decision" value="shortlisted"> Shortlisted</label>
<label><input type="radio" name="decision" value="selected"> Selected</label>
<label><input type="radio" name="decision" value="declined"> Reject · review email first</label>
</fieldset><button class="btn solid" type="submit">Save decision</button></form>
<h3>Recent decision history</h3><ul id="review-history"></ul>
<div hidden id="review-email"><input id="review-to"><input id="review-subject"><textarea id="review-body"></textarea></div>
</section></section></article>'''
    page('toshali-review.html','Toshali private review desk',body,desc='Sign in to the private Toshali anthology editorial desk.')
    path=root/'toshali-review.html'
    text=path.read_text().replace('<script defer src="assets/analytics.js"></script>','').replace('</head>','<meta name="robots" content="noindex,nofollow"><meta name="referrer" content="no-referrer"><link rel="stylesheet" href="assets/toshali-invitation.css?v=3"><script type="module" src="assets/toshali-review.mjs?v=1"></script></head>',1)
    path.write_text(text)
