"""Apply the approved Our Story narrative, consolidated credits and artistic marks."""
import re


def apply_our_story(site):
    path = site / 'about.html'
    s = path.read_text()
    if 'class="wrap inner-artistic our-story"' in s:
        return
    old=re.search(r'<div class="side-layout"><div class="prose">(.*?)</div><aside',s,re.S).group(1)
    new='''<h2 class="or" lang="or">ମାଟିର ମହକ · ହୃଦୟର ସ୍ବର</h2>
    <p class="story-signature">The fragrance of earth. The voice of the heart.</p>
    <p>Rooted in Odia, Kabita Live welcomes original poems and translations in Odia, Hindi and English, from established and younger writers. Each language has its own music. Read an edition, share a poem with its poet’s name, or write privately to the editorial desk—wherever you call home.</p>
    <div class="story-invitations"><a class="text-link" href="submit.html">Send a poem</a><a class="text-link" href="feedback.html">Write to the editors</a></div>'''
    s=s.replace(old,new,1)
    s=s.replace('<h1>A familiar name.<br>A living literary home.</h1>', '<h1>Our story</h1>', 1)
    s=s.replace('<h2 style="margin-top:28px">', '<h2 style="margin-top:20px">')
    # Equal portrait treatment for the three human editors; reuse approved artwork.
    editors = [
        ('Pradeep Biswal', 'Editor', 'editor-pradeep.html', 'assets/editors/pradeep-biswal-artistic-v2.webp'),
        ('Paresh Kumar Pattnaik', 'Managing Editor', 'editor-paresh.html', 'assets/editors/paresh-kumar-pattnaik-artistic-v2.webp'),
        ('Ahimanikya Satapathy', 'Creative Editor', 'ahimanikya-satapathy.html', 'assets/writers/ahimanikya-satapathy-earth-voice-v1.webp'),
    ]
    for name, role, profile, portrait in editors:
        pattern = r'<h2(?: style="[^"]*")?>' + re.escape(name) + r'</h2><p>' + re.escape(role) + r'</p><a class="text-link" href="' + re.escape(profile) + r'">Profile(?: ↗)?</a>'
        card = (f'<a class="story-editor" href="{profile}"><img src="{portrait}" alt="" '
                f'width="80" height="80" loading="lazy" decoding="async">'
                f'<div><h2>{name}</h2><p>{role}</p></div></a>')
        s, count = re.subn(pattern, lambda _: card, s, count=1)
        assert count == 1, f'Missing About editor: {name}'
    # Explain the editorial process before the design story and consolidated credits.
    design = (site / 'templates/our-story-design.html').read_text()
    symbol = (site / 'assets/kabita-live-symbol-ink-voice.svg').read_text()
    logo = ('<svg class="story-design-logo" viewBox="0 0 256 256" width="72" height="72" '
            'aria-hidden="true" focusable="false">' +
            ''.join(re.findall(r'<path\b[^>]+/>', symbol)) + '</svg>')
    design = design.replace('<!-- design-logo -->', logo)
    credit_marker = '<section class="colophon" id="credits"'
    assert credit_marker in s
    process = (site / 'templates/our-story-ai.html').read_text()
    s = s.replace(credit_marker, process + design + credit_marker, 1)
    s = s.replace('<div class="story-invitations">', '<div class="story-invitations"><a class="text-link" href="#design">The design story</a>', 1)
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

    for label, motif in [('The editorial desk', 'footer-send-poem'), ('Credits &amp; colophon', 'footer-story')]:
        s = s.replace('<span class="eyebrow">'+label+'</span>', '<span class="eyebrow story-artistic-label">'+mark(motif)+label+'</span>', 1)
    for href, label, motif in [('submit.html', 'Send a poem', 'footer-send-poem'), ('feedback.html', 'Write to the editors', 'footer-contact')]:
        s = s.replace(f'<a class="text-link" href="{href}">{label}</a>', f'<a class="text-link story-action" href="{href}">'+mark(motif)+label+'</a>', 1)
    s = s.replace('class="wrap inner-artistic"', 'class="wrap inner-artistic our-story"', 1)
    s = s.replace('<title>About · Kabita Live</title>', '<title>Our Story · Kabita Live</title>', 1)
    s = s.replace('</head>', '<link rel="stylesheet" href="assets/our-story.css?v=editor-portraits-20261102"><script defer src="assets/our-story.js?v=1"></script></head>', 1)
    # Keep artwork credits concise; historical production detail stays in the KB.
    s = re.sub(r'<p>The homepage artwork <em>LIFE AS IT IS</em>.*?</p>', '<p>Covers and illustrations are artistic interpretations created for Kabita Live.</p>', s, count=1, flags=re.S)
    s = s.replace('Sources reviewed 29 September 2026; book titles retain their source spellings.', '')
    # Native disclosure: collapsed on About, expanded by existing hash navigation.
    privacy_start = s.index('<section class="colophon" id="privacy">')
    privacy_end = s.index('</section>', privacy_start) + len('</section>')
    privacy = s[privacy_start:privacy_end]
    privacy = privacy.replace('<section class="colophon" id="privacy"><h2>A little care for your privacy.</h2>', '<details class="colophon" id="privacy"><summary>A little care for your privacy.</summary>', 1)
    privacy = privacy.removesuffix('</section>') + '</details>'
    s = s[:privacy_start] + privacy + s[privacy_end:]
    path.write_text(s)
