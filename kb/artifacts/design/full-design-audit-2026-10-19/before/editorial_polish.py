"""Apply the approved editorial layouts after authoritative contributions are joined.

Source decisions: kb/records/editorial-polish-applied.json.
No dependency on historical mock files or copied profile data at build time.
"""
import re

def apply_editorial_polish(site):
    def icon(name):
        s=(site/f'assets/icons/earth-voice-v1/ink/{name}.svg').read_text()
        s=re.sub(r'role="img" aria-label="[^"]*"','aria-hidden="true" focusable="false"',s)
        return '<span class="editorial-mark" aria-hidden="true">'+s+'</span>'
    pen=icon('footer-send-poem'); book=icon('footer-story'); leaf=icon('kendu')
    for source in ('editorial-team.html','editor-pradeep.html','editor-paresh.html'):
        path=site/source
        s=path.read_text()
        if 'assets/editorial-refined.css' in s:
            continue
        s=s.replace('<main id="main" class="wrap"','<main id="main" class="wrap editorial-refined"')
        if source=='editorial-team.html':
         s=s.replace('<span class="eyebrow">The people tending the journal</span>','<span class="eyebrow artistic-label">'+pen+'The people tending the journal</span>')
         s=s.replace('Meet the writers whose literary lives come together in Kabita Live.','Every issue begins with listening.<br>Meet the two writers behind these pages.')
         s=s.replace('Poetry, translation and the conversation between languages.','Poetry and translation.<br>A conversation between languages.').replace('Stories, social observation and an invitation to younger readers.','Stories of the world around us.<br>A welcome for younger readers.')
         invitation='<section class="editorial-strip editorial-invitation" id="share-poem" aria-label="Contribute to the journal"><div><h2>An idea worth sharing.</h2><p>An essay, a reflection on a book, or a thought on poetry. Send your article to the editorial desk.</p><a class="btn solid marked-link" href="mailto:kabitaliveweb@gmail.com?subject=Article%20submission%20%C2%B7%20Kabita%20Live">'+book+'Submit an article</a></div><div><h2>A poem begins with you.</h2><p>Some words ask to be shared. Send your poem in Odia, Hindi or English to the editorial desk.</p><a class="btn solid marked-link" href="submit.html">'+pen+'Submit a poem</a></div></section>'
         s=re.sub(r'<section class="editorial-strip">.*?</section>',lambda m:invitation,s,flags=re.S)
        else:
         s=re.sub(r'<section class="editor-journal-role">.*?</section>','',s,flags=re.S)
         s=s.replace('<span class="eyebrow">Editor · Kabita Live</span>','<span class="eyebrow artistic-label">'+leaf+'Editor</span>').replace('<span class="eyebrow">Managing Editor · Kabita Live</span>','<span class="eyebrow artistic-label">'+leaf+'Managing Editor</span>')
         if source=='editor-pradeep.html':
          s=s.replace('A poet in Odia and English, a translator and an editor, Pradeep Biswal brings a life in literature and public service to Kabita Live.','Poetry in Odia and English.<br>Translation opening another door.')
          s=s.replace('At Kabita Live, where he is listed as Editor, that bilingual practice sits naturally within a journal that welcomes Odia, Hindi and English together.','That bilingual practice sits naturally within a journal that welcomes Odia, Hindi and English together.')
          s=s.replace('Poems by Pradip Biswal, Editor','Poems by Pradeep Biswal')
         else:
          s=s.replace('An Odia fiction writer whose work includes short stories, novels and books for younger readers, Paresh Kumar Pattnaik is Kabita Live’s Managing Editor.','Odia stories and novels.<br>New worlds for younger readers.')
          s=s.replace('Paresh Kumar Pattnaik writes fiction in Odia and is listed by Kabita Live as its Managing Editor.','Paresh Kumar Pattnaik writes fiction in Odia.')
          s=re.sub(r'<section class="writer-work" id="contributions">.*?</section>', lambda m: m[0] if 'data-contribution=' in m[0] else '', s, flags=re.S)
         s=s.replace('<h2>A few places to begin.</h2>','<h2 class="artistic-heading">'+book+'A few places to begin.</h2>')
         s=s.replace('<a class="text-link" href="contact.html">Write to the editorial desk</a>','<a class="text-link marked-link" href="contact.html">'+pen+'Write to the editorial desk</a>')
        s=s.replace('</head>','<link rel="stylesheet" href="assets/editorial-refined.css?v=3"></head>')
        path.write_text(s)
