"""Apply the approved Ink & Voice website design after page assembly.

Magazine covers and source poetry are deliberately left intact.
"""
import re
from html import escape
from hashlib import sha256


def favicon_link(site):
    """Use the current logo and refresh the browser cache when its artwork changes."""
    asset = 'assets/kabita-live-symbol-ink-voice.svg'
    revision = sha256((site / asset).read_bytes()).hexdigest()[:12]
    return f'<link rel="icon" type="image/svg+xml" sizes="any" href="{asset}?v={revision}">'


def redesign_home(text, edition, cover_markup):
    opening = re.search(r'<section class="home-opening\b.*?</section>', text, re.S)
    featured = re.search(r'<section id="featured-poems".*?</section>', text, re.S)
    assert opening and featured, 'Homepage source sections missing'
    action = re.search(r'<a class="btn solid".*?</a>', opening.group(), re.S).group()
    issue = re.search(r'<span class="eyebrow home-artistic-label">.*?</span>', opening.group(), re.S).group()
    issue = re.sub(r'<svg\b.*?</svg>', '', issue, flags=re.S)
    issue = issue.replace('eyebrow home-artistic-label', 'ink-issue-note')
    # Reuse the existing full, source-backed candidate pool and visit selection.
    candidates = featured.group().split('<div class="three"', 1)[1].removesuffix('</section>')
    candidates = '<div class="three"' + candidates
    number = edition['number']
    # Reuse the reviewed front cover and its explicit edition-page link.
    cover_markup = cover_markup.replace(f'cover-b cover-{number}"', f'cover-b cover-{number} magazine-object"')
    current = (f'<section class="ink-current-edition" aria-labelledby="ink-edition-title">'
               '<div class="ink-edition-copy"><span class="eyebrow">Current edition</span>'
               f'<h2 id="ink-edition-title">Issue {number}</h2>'
               f'<p class="ink-edition-meta">{escape(edition["date"])} · {edition["poem_count"]} poems</p>'
               f'<h3>{escape(edition["title"])}</h3><p class="ink-edition-story">{escape(edition["story"])}</p>'
               f'<a class="btn solid" href="issue-{number}.html">Read this edition <span aria-hidden="true">↗</span></a>'
               '</div><div class="ink-edition-cover">' + cover_markup + '</div></section>')
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
           '</div>' + candidates + '</section></section>' + current)
    return text.replace(opening.group(), new, 1).replace(featured.group(), '', 1)


def apply_ink_voice(site, filenames, *, current_edition, current_cover):
    # Keep the original leaf/stream geometry; the website mark inherits its theme.
    symbol = (site / 'assets/kabita-live-symbol-ink-voice.svg').read_text()
    paths = ''.join(re.findall(r'<path\b[^>]+/>', symbol))
    mark = ('<svg class="brand-symbol" viewBox="0 0 256 256" '
            'width="41" height="41" aria-hidden="true" focusable="false">' + paths + '</svg>')
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
        text = text.replace('</head>', '<link rel="preload" href="assets/fonts/Newsreader-Variable.woff2" as="font" type="font/woff2" crossorigin><link rel="stylesheet" href="assets/ink-voice.css?v=20261019-complete-audit"></head>', 1)
        text = text.replace('<img src="assets/kabita-live-symbol.svg" alt=""><span><span class="brand-title">', mark + '<span><span class="brand-title">', 1)
        text = text.replace('<link rel="icon" href="assets/kabita-live-symbol.svg">', favicon_link(site), 1)
        # Keep the established compact masthead/menu markup. The signature belongs on covers.
        if name == 'index.html':
            text = redesign_home(text, current_edition, current_cover)
        path.write_text(text)
        count += 1
    print(f'Ink & Voice: {count} assembled reader pages styled; cover artwork unchanged.')
