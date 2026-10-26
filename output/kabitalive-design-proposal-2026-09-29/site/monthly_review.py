"""Public sign-in shell only: submission data is never included in a static build."""
def render_monthly_review(root,page):
    body='''<article class="toshali-invite monthly-form" data-pagefind-ignore="all">
<p class="eyebrow">Kabita Live · Monthly journal</p><h1>Private review desk</h1>
<p>For authorised journal editors. Entries remain private and are retained indefinitely. Selection does not send an email. Rejection opens an editable email draft before you confirm sending. Decisions never publish a poem.</p>
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
<label><input type="radio" name="decision" value="next_issue"> Keep for next issue</label><label><input type="radio" name="decision" value="declined"> Reject · review email first</label><label for="review-month">Issue month (selected or next-issue poems; optional until assigned)</label><input id="review-month" name="issueMonth" type="month" min="2000-01" max="2099-12" pattern="20[0-9]{2}-(0[1-9]|1[0-2])" aria-describedby="review-month-help"><p id="review-month-help">Use YYYY-MM if your browser shows a text field. Leave blank until a month is assigned. This does not publish the poem.</p>
</fieldset><button class="btn solid" type="submit">Save decision</button></form>
<h3>Submission details</h3><p id="review-details" class="monthly-verse"></p><h3>Recent decision history</h3><ul id="review-history"></ul>
<div hidden id="review-email"><input id="review-to"><input id="review-subject"><textarea id="review-body"></textarea></div>
</section></section></article>'''
    page('monthly-review.html','Kabita monthly private review desk',body,desc='Sign in to the private Kabita monthly journal editorial desk.')
    path=root/'monthly-review.html'
    text=path.read_text().replace('<script defer src="assets/analytics.js"></script>','').replace('</head>','<meta name="robots" content="noindex,nofollow"><meta name="referrer" content="no-referrer"><link rel="stylesheet" href="assets/toshali-invitation.css?v=3"><link rel="stylesheet" href="assets/monthly-submissions.css?v=1"><script type="module" src="assets/monthly-review.mjs?v=1"></script></head>',1)
    path.write_text(text)
