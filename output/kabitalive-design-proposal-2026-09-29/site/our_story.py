"""Apply the approved Our Story narrative, consolidated credits and artistic marks."""
import re


def apply_our_story(site):
    path = site / 'about.html'
    s = path.read_text()
    if 'class="wrap inner-artistic our-story"' in s:
        return
    old=re.search(r'<div class="side-layout"><div class="prose">(.*?)</div><aside',s,re.S).group(1)
    new='''<h2 class="or" lang="or">ମାଟିର ମହକ · ମନର ସ୍ୱର</h2>
    <p class="story-signature">The fragrance of earth. The voice of the heart.</p>
    <p>Rooted in Odia, Kabita Live brings poetry in Odia, Hindi and English into a shared literary home. Each language has its own music; each poem offers another way of seeing.</p>
    <h2>Room for another voice.</h2>
    <p>We welcome original poems and translations, established writers and younger voices, and readers across places and generations. A poem begins with its writer and continues with everyone who reads it.</p>
    <p>Read an edition, share a poem with its poet’s name, or write to the editorial desk. Your responses are private, and always welcome.</p>
    <div class="story-invitations"><a class="text-link" href="submit.html">Send a poem</a><a class="text-link" href="feedback.html">Write to the editors</a></div>'''
    s=s.replace(old,new,1)
    start=s.index('<section class="colophon" id="credits-writers">');end=s.index('<section class="colophon" id="privacy">',start)
    writers=s[start:end]
    s=s[:start]+s[end:]
    inside=writers.removeprefix('<section class="colophon" id="credits-writers">').removesuffix('</section>')
    inside=inside.replace('<h2>The voices in these pages.</h2>','',1)
    credit_details='<details id="credits-writers"><summary>Poets, portraits and biography references</summary><div class="colophon-details">'+inside+'</div></details>'
    marker='</section>\n<section class="journal-paths">'
    assert marker in s
    s=s.replace(marker,credit_details+'</section>\n<section class="journal-paths">',1)
    # Keep privacy alongside credits; journal navigation follows both.
    a=s.index('<section class="journal-paths">');b=s.index('<section class="colophon" id="privacy">',a)
    paths=s[a:b];s=s[:a]+s[b:];s=s.replace('</main>',paths+'</main>',1)

    def mark(name):
        svg = (site / f'assets/icons/earth-voice-v1/ink/{name}.svg').read_text()
        svg = re.sub(r' role="img"| aria-label="[^"]*"| aria-hidden="[^"]*"| focusable="[^"]*"', '', svg)
        return svg.replace('<svg ', '<svg class="story-mark" aria-hidden="true" focusable="false" ', 1)

    s = s.replace('<h2>Room for another voice.</h2>', '<h2 class="story-artistic-heading">'+mark('kendu')+'<span>Room for another voice.</span></h2>', 1)
    for label, motif in [('The editorial desk', 'footer-send-poem'), ('Credits &amp; colophon', 'footer-story')]:
        s = s.replace('<span class="eyebrow">'+label+'</span>', '<span class="eyebrow story-artistic-label">'+mark(motif)+label+'</span>', 1)
    for href, label, motif in [('submit.html', 'Send a poem', 'footer-send-poem'), ('feedback.html', 'Write to the editors', 'footer-contact')]:
        s = s.replace(f'<a class="text-link" href="{href}">{label}</a>', f'<a class="text-link story-action" href="{href}">'+mark(motif)+label+'</a>', 1)
    s = s.replace('class="wrap inner-artistic"', 'class="wrap inner-artistic our-story"', 1)
    s = s.replace('<title>About · Kabita Live</title>', '<title>Our Story · Kabita Live</title>', 1)
    s = s.replace('</head>', '<link rel="stylesheet" href="assets/our-story.css?v=1"><script defer src="assets/our-story.js?v=1"></script></head>', 1)
    path.write_text(s)
