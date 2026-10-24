"""Public sign-in shell only: submission data is never included in a static build."""
def render_toshali_review(root,page):
    body='''<article class="toshali-invite" data-pagefind-ignore="all">
<p class="eyebrow">Toshali Anthology of Poetry 2027</p><h1>Private review desk</h1>
<p>For authorised anthology editors. Entries and photographs remain private and are retained indefinitely. Decisions here do not publish a poem or send an email.</p>
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
<label><input type="radio" name="decision" value="declined"> Declined</label>
</fieldset><button class="btn solid" type="submit">Save decision</button></form>
<h3>Recent decision history</h3><ul id="review-history"></ul>
<h3>Email draft</h3><p>Check and edit this draft, then copy it into the Toshali mailbox to send manually. Saving a decision sends no email.</p>
<button id="review-draft" class="btn" type="button">Prepare draft from saved decision</button>
<div id="review-email" hidden><label for="review-to">Recipient</label><input id="review-to" type="email" readonly>
<label for="review-subject">Subject</label><input id="review-subject" readonly>
<label for="review-body">Message — edit before sending</label><textarea id="review-body" rows="12"></textarea>
<button id="review-copy" class="btn" type="button">Copy recipient, subject and message</button></div>
</section></section></article>'''
    page('toshali-review.html','Toshali private review desk',body,desc='Sign in to the private Toshali anthology editorial desk.')
    path=root/'toshali-review.html'
    text=path.read_text().replace('<script defer src="assets/analytics.js"></script>','').replace('</head>','<meta name="robots" content="noindex,nofollow"><meta name="referrer" content="no-referrer"><link rel="stylesheet" href="assets/toshali-invitation.css?v=3"><script type="module" src="assets/toshali-review.mjs?v=1"></script></head>',1)
    path.write_text(text)
