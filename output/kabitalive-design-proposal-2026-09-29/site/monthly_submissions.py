"""Year-round private journal intake; independent of the anthology."""
import re

def render_monthly_submission(root):
    path=root/'submit.html'
    text=path.read_text()
    body='''<main id="main" class="wrap monthly-form" tabindex="-1"><header class="monthly-opening"><span class="eyebrow">For poets · Open throughout the year</span><h1>Send a poem</h1><p>Share a poem in Odia, Hindi or English. The editors will choose the issue month if your work is selected.</p></header>
<p>Your entry and contact details are kept private for editorial review and retained indefinitely, whether or not the poem is selected. Nothing is published automatically. Keep your own copy.</p>
<p>Prefer email? Write to <a href="mailto:kabitaliveweb@gmail.com">kabitaliveweb@gmail.com</a>.</p>
<p id="monthly-status" role="status">Online form preview. You can prepare an entry here; nothing is sent.</p>
<noscript><p>Online submission needs JavaScript. Please email your poem, title, name and short biography to kabitaliveweb@gmail.com.</p></noscript>
<form id="monthly-form" action="submit.html" method="post" hidden>
<p>All fields are required unless marked optional. Unfinished text is saved in this browser tab when available; consent is never saved.</p><button type="button" class="btn" id="monthly-clear">Clear saved draft</button>
<fieldset id="monthly-fields"><legend>Your entry</legend>
<label for="monthly-name">Name to publish</label><input id="monthly-name" name="name" autocomplete="name" maxlength="120" required>
<label for="monthly-email">Email address</label><input id="monthly-email" name="email" type="email" autocomplete="email" autocapitalize="off" autocorrect="off" spellcheck="false" maxlength="254" required>
<label for="monthly-title">Poem title</label><input id="monthly-title" name="title" maxlength="200" required>
<fieldset class="monthly-options"><legend>Language</legend><label><input type="radio" name="language" value="or" required> Odia</label><label><input type="radio" name="language" value="hi"> Hindi</label><label><input type="radio" name="language" value="en"> English</label></fieldset>
<label for="monthly-poem">Your poem</label><p id="monthly-poem-help">Keep your original line and stanza breaks. Up to 30,000 characters.</p><textarea id="monthly-poem" name="poem" rows="12" maxlength="30000" aria-describedby="monthly-poem-help" required></textarea>
<fieldset class="monthly-options"><legend>About the work</legend><label><input type="radio" name="kind" value="original" required> Original poem</label><label><input type="radio" name="kind" value="translation"> Translation</label></fieldset>
<label for="monthly-credits">Original poet and translator (required for translations)</label><textarea id="monthly-credits" name="credits" rows="2" maxlength="1000"></textarea>
<label for="monthly-previous">Previous publication details (optional)</label><textarea id="monthly-previous" name="previous" rows="2" maxlength="2000"></textarea>
<label for="monthly-bio">Short biography</label><textarea id="monthly-bio" name="bio" rows="4" maxlength="5000" required></textarea>
<label class="monthly-consent"><input type="checkbox" name="consent" required> I have the right to submit this work, have identified any translation or previous publication, and agree to indefinite private storage for editorial review.</label>
</fieldset><button type="submit" class="btn solid" id="monthly-review-button">Review your entry</button></form>
<section id="monthly-summary" hidden aria-labelledby="monthly-summary-title"><h2 id="monthly-summary-title" tabindex="-1">Review your entry</h2><div id="monthly-summary-content"></div><p>Submitting is not a promise of selection or publication.</p><label id="monthly-reconsent-label" hidden><input type="checkbox" id="monthly-reconsent"> I confirm my submission rights and agree again to indefinite private storage of this saved entry for editorial review.</label><button class="btn" id="monthly-edit" type="button">Edit entry</button> <button class="btn solid" id="monthly-send" type="button">Submit privately</button></section>
<section id="monthly-result" hidden><h2 tabindex="-1" id="monthly-result-title">Entry received</h2><p id="monthly-reference"></p><p>Your poem is with the editors. Keep this reference and your own copy. Questions? Email kabitaliveweb@gmail.com.</p></section></main>'''
    text=re.sub(r'<main\b.*?</main>',lambda _:body,text,count=1,flags=re.S)
    text=text.replace('</head>','<link rel="stylesheet" href="assets/monthly-submissions.css?v=1"><script type="module" src="assets/monthly-form.mjs?v=1"></script></head>',1)
    text=text.replace('<script defer src="assets/analytics.js"></script>','')
    path.write_text(text)
