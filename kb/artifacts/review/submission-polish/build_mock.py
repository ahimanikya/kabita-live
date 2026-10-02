from pathlib import Path
import re,os,json,hashlib
from urllib.parse import urlencode
OUT=Path(__file__).parent;ROOT=OUT.resolve().parents[3];SITE=ROOT/'projects/site'
source=(SITE/'submit.html').read_text();(OUT/'source-submit.html').write_text(source)
def icon(name):
 s=(SITE/f'assets/icons/earth-voice-v1/ink/{name}.svg').read_text();s=re.sub(r'role="img" aria-label="[^"]*"','aria-hidden="true" focusable="false"',s)
 return '<span class="submission-mark" aria-hidden="true">'+s+'</span>'
pen=icon('footer-send-poem');book=icon('footer-story');leaf=icon('kendu');mail=icon('footer-contact')
art=re.search(r'<figure class="opening-art".*?</figure>',source,re.S).group()
email='kabitaliveweb@gmail.com'
body='Dear editors,\n\nI would like to share a poem for your consideration.\n\nPoem title:\nName to publish under:\nLanguage:\nTranslation / original author and translator (if applicable):\nPrevious publication (if any):\n\nPoem (please preserve line and stanza breaks):\n\n\nShort biography:\nContact email:\n\nThank you.'
mailto='mailto:'+email+'?'+urlencode({'subject':'Poetry submission · Kabita Live','body':body})
main='''<main id="main" class="wrap submission-mock" tabindex="-1"><nav class="submission-review" aria-label="Preview navigation"><span>Submission · Design preview</span><a href="submit.html">Compare current page</a></nav><section class="submission-opening"><div><span class="eyebrow marked-label">'''+pen+'''A place for your words</span><h1>Send us your words.</h1><p>A poem written in quiet can begin a conversation.<br>Share yours in Odia, Hindi or English.</p></div>'''+art+'''</section><div class="submission-layout"><section class="submission-guide" aria-labelledby="before-send"><h2 id="before-send">Before your poem travels.</h2><p class="guide-intro">A few details help the editors meet the poem—and the person behind it.</p><div class="submission-step">'''+book+'''<div><h3>Let the poem keep its shape.</h3><p>Include its title and the name you’d like published. Keep your line breaks and the spaces between stanzas.</p></div></div><div class="submission-step">'''+pen+'''<div><h3>Tell us its journey.</h3><p>Name the language. If it is a translation, credit the original poet and translator. Mention any previous publication.</p></div></div><div class="submission-step">'''+leaf+'''<div><h3>A little about you.</h3><p>Add a short biography and the email address you’d like the editors to use.</p></div></div></section><aside class="submission-send" aria-labelledby="send-heading"><span class="eyebrow marked-label">'''+mail+'''To the editorial desk</span><h2 id="send-heading">Your next step.</h2><p>Open an email draft with space for your poem and a few words about yourself.</p><a class="btn solid draft-button" href="'''+mailto.replace('&','&amp;')+'">'+pen+'''Start your email</a><p class="send-help">Opens your email app. You can edit the draft before sending.</p><div class="webmail-option"><p>Using webmail? Write to</p><a class="submission-address" href="mailto:'''+email+'">'+email+'''</a><button type="button" class="copy-address" id="copy-editor-address">Copy email address</button><p id="copy-address-status" class="send-help" role="status" aria-live="polite"></p></div></aside></div></main>'''
html=re.sub(r'<main\b.*?</main>',lambda m:main,source,count=1,flags=re.S).replace('<title>','<title>Preview · ',1)
html=html.replace('</head>','<style>'+(OUT/'mock.css').read_text()+'</style></head>').replace('<script defer src="assets/analytics.js"></script>','')
html=html.replace('</body>','''<script>document.querySelector('#copy-editor-address').addEventListener('click',async()=>{const status=document.querySelector('#copy-address-status');try{await navigator.clipboard.writeText('kabitaliveweb@gmail.com');status.textContent='Email address copied.'}catch{status.textContent='Please select and copy the email address above.'}});</script></body>''')
(OUT/'submit-polish-mock.html').write_text(html)
p=SITE/'submit-polish-mock.html'
if not p.exists():p.symlink_to(os.path.relpath(OUT/'submit-polish-mock.html',p.parent.resolve()))
(OUT/'source-integrity.json').write_text(json.dumps({'source':'submit.html','sha256':hashlib.sha256(source.encode()).hexdigest(),'email':email},indent=2)+'\n')
print('Submission preview created; reader page unchanged.')
