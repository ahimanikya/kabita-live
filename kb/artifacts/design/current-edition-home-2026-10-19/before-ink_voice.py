"""Apply the approved Ink & Voice website design after page assembly.

Magazine covers and source poetry are deliberately left intact.
"""
import re


def redesign_home(text):
    opening = re.search(r'<section class="home-opening\b.*?</section>', text, re.S)
    featured = re.search(r'<section id="featured-poems".*?</section>', text, re.S)
    assert opening and featured, 'Homepage source sections missing'
    artwork = opening.group().split('<figure class="home-art', 1)[1].removesuffix('</section>')
    artwork = '<figure class="home-art' + artwork
    action = re.search(r'<a class="btn solid".*?</a>', opening.group(), re.S).group()
    issue = re.search(r'<span class="eyebrow home-artistic-label">.*?</span>', opening.group(), re.S).group()
    issue = re.sub(r'<svg\b.*?</svg>', '', issue, flags=re.S)
    issue = issue.replace('eyebrow home-artistic-label', 'ink-issue-note')
    # Reuse the existing full, source-backed candidate pool and daily selection.
    candidates = featured.group().split('<div class="three"', 1)[1].removesuffix('</section>')
    candidates = '<div class="three"' + candidates
    new = (f'<section class="ink-opening" aria-labelledby="ink-home-title">'
           '<div class="ink-invitation"><span class="eyebrow">ODIA · HINDI · ENGLISH</span>'
           '<h1 id="ink-home-title">Poems to<br><em>keep close.</em></h1>'
           '<p class="ink-home-deck">A monthly journal of poetry.</p>' + action + issue + '</div>'
           '<section id="featured-poems" class="ink-feature" aria-labelledby="ink-feature-title">'
           '<h2 id="ink-feature-title">A poem to begin with</h2>'
           '<div class="ink-language" role="group" aria-label="Featured original language" hidden>'
           '<button type="button" data-feature-language="en" aria-pressed="false">English</button>'
           '<button type="button" data-feature-language="hi" lang="hi" aria-pressed="false">हिन्दी</button>'
           '<button type="button" data-feature-language="or" lang="or" aria-pressed="false">ଓଡ଼ିଆ</button>'
           '</div>' + candidates + '</section></section>'
           '<section class="ink-view" aria-label="A view from the journal">'
           '<div class="ink-view-copy"><span class="eyebrow">From the journal</span>'
           '<p class="epigraph">“Poetry is an echo,<br>asking a shadow to dance.”</p>'
           '<a class="text-link" href="poems.html">Find a poem</a></div>' + artwork + '</section>')
    return text.replace(opening.group(), new, 1).replace(featured.group(), '', 1)


def apply_ink_voice(site, filenames):
    count = 0
    for name in set(filenames):
        path = site / name
        if path.is_symlink():
            continue
        text = path.read_text()
        if not re.search(r'<body class="[^"]*\bsite-theme\b', text):
            continue
        if 'assets/ink-voice.css' in text:
            continue
        text = text.replace('</head>', '<link rel="preload" href="assets/fonts/Newsreader-Variable.woff2" as="font" type="font/woff2" crossorigin><link rel="stylesheet" href="assets/ink-voice.css?v=20261019-logo"></head>', 1)
        text = text.replace('<header class="wrap site-header">', '<header class="wrap site-header ink-header">', 1)
        signature = '<p class="ink-signature" lang="or">ମାଟିର ମହକ<br>ହୃଦୟର ସ୍ବର</p>'
        text = text.replace('<button type="button" class="menu menu-icon"', signature + '<button type="button" class="menu menu-icon"', 1)
        if name == 'index.html':
            text = redesign_home(text)
        path.write_text(text)
        count += 1
    print(f'Ink & Voice: {count} assembled reader pages styled; cover artwork unchanged.')
