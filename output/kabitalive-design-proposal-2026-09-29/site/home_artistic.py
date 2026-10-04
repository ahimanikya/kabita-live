"""Apply the established artistic marks without changing homepage content."""
import re


def apply_home_artistic(site):
    path = site / 'index.html'
    text = path.read_text()

    def mark(name):
        svg = (site / f'assets/icons/earth-voice-v1/ink/{name}.svg').read_text()
        svg = re.sub(r' role="img"| aria-label="[^"]*"| aria-hidden="[^"]*"| focusable="[^"]*"', '', svg)
        return svg.replace('<svg ', '<svg class="home-artistic-mark" aria-hidden="true" focusable="false" ', 1)

    text = text.replace('<div class="home-invitation"><span class="eyebrow">',
                        '<div class="home-invitation"><span class="eyebrow home-artistic-label">' + mark('kendu'), 1)
    text, count = re.subn(r'(<a class="btn solid" href="issue-\d+\.html">)Read this edition',
                         lambda m: m[1] + mark('footer-story') + 'Read this edition', text, count=1)
    assert count == 1, 'Homepage edition action missing'
    for title, motif in [('A poem to begin with.', 'kendu'),
                         ('Recent editions', 'footer-story'),
                         ('The editors', 'footer-send-poem')]:
        text, count = re.subn(r'(<h2[^>]*>)' + re.escape(title) + '</h2>',
                             lambda m: m[1] + mark(motif) + '<span>' + title + '</span></h2>', text, count=1)
        assert count == 1, f'Homepage section missing: {title}'
    path.write_text(text.replace('</head>', '<link rel="stylesheet" href="assets/home-artistic.css?v=1"></head>'))
