"""Approved Send a poem layout, using existing artwork and editorial address.
Preserves the shared page shell, consent controls and footer.
"""
import re
from urllib.parse import urlencode

def apply_submission_polish(site):
    path=site/'submit.html'
    source=path.read_text()
    if 'assets/submission-refined.css' in source:
        return
    def icon(name):
     s=(site/f'assets/icons/earth-voice-v1/ink/{name}.svg').read_text();s=re.sub(r'role="img" aria-label="[^"]*"','aria-hidden="true" focusable="false"',s)
     return '<span class="submission-mark" aria-hidden="true">'+s+'</span>'
    pen=icon('footer-send-poem');book=icon('footer-story');leaf=icon('kendu');mail=icon('footer-contact')
    art=re.search(r'<figure class="opening-art".*?</figure>',source,re.S).group()
    email='kabitaliveweb@gmail.com'
    body='Dear editors,\n\nI would like to share a poem for your consideration.\n\nPoem title:\nName to publish under:\nLanguage:\nTranslation / original author and translator (if applicable):\nPrevious publication (if any):\n\nPoem (please preserve line and stanza breaks):\n\n\nShort biography:\nContact email:\n\nThank you.'
    mailto='mailto:'+email+'?'+urlencode({'subject':'Poetry submission · Kabita Live','body':body})
    main='''<main id="main" class="wrap submission-refined" tabindex="-1"><section class="submission-opening"><div><span class="eyebrow marked-label">'''+pen+'''A place for your words</span><h1>Send a poem</h1><p>Submit poetry in Odia, Hindi or English by email.</p></div>'''+art+'''</section><div class="submission-layout"><section class="submission-guide" aria-labelledby="before-send"><h2 id="before-send">Submission details</h2><p class="guide-intro">Include the following with your poem.</p><div class="submission-step">'''+book+'''<div><h3>Title and formatting</h3><p>Include its title and the name you’d like published. Keep your line breaks and the spaces between stanzas.</p></div></div><div class="submission-step">'''+pen+'''<div><h3>Language and publication</h3><p>Name the language. If it is a translation, credit the original poet and translator. Mention any previous publication.</p></div></div><div class="submission-step">'''+leaf+'''<div><h3>About the poet</h3><p>Add a short biography and the email address you’d like the editors to use.</p></div></div></section><aside class="submission-send" aria-labelledby="send-heading"><span class="eyebrow marked-label">'''+mail+'''To the editorial desk</span><h2 id="send-heading">Email your poem</h2><p>Open an email draft with space for your poem and a few words about yourself.</p><a class="btn solid draft-button" href="'''+mailto.replace('&','&amp;')+'">'+pen+'''Start your email</a><p class="send-help">Opens your email app. You can edit the draft before sending.</p><div class="webmail-option"><p>Using webmail? Write to</p><a class="submission-address" href="mailto:'''+email+'">'+email+'''</a><button type="button" class="copy-address" id="copy-editor-address">Copy email address</button><p id="copy-address-status" class="send-help" role="status" aria-live="polite"></p></div></aside></div></main>'''

    html=re.sub(r'<main\b.*?</main>',lambda m:main,source,count=1,flags=re.S)
    html=html.replace('</head>','<link rel="stylesheet" href="assets/submission-refined.css?v=1"><script defer src="assets/submission.js?v=1"></script></head>')
    path.write_text(html)
