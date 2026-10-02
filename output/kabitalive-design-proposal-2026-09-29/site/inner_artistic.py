"""Carry the approved artistic opening treatment into remaining reader templates."""
import re

def apply_inner_artistic(site):
    motifs={
        'about.html':'earth-voice','contact.html':'footer-contact',
        'feedback.html':'footer-contact','current-contributors.html':'kendu',
        'reviews.html':'footer-story','review.html':'footer-story',
        'highlights.html':'kendu','highlight.html':'kendu',
        'upcoming.html':'paddy','not-found.html':'next-poetic',
        'poem-385.html':'footer-story','poem-727.html':'footer-story',
    }
    motifs.update({p.name:'footer-story' for p in site.glob('review-*.html') if p.stem.removeprefix('review-').isdigit()})
    for name,motif in motifs.items():
        path=site/name
        text=path.read_text()
        svg=(site/f'assets/icons/earth-voice-v1/ink/{motif}.svg').read_text()
        svg=re.sub(r' role="img"| aria-label="[^"]*"| aria-hidden="[^"]*"| focusable="[^"]*"','',svg)
        svg=svg.replace('<svg ','<svg aria-hidden="true" focusable="false" ',1)
        text=text.replace('<main id="main" class="wrap"','<main id="main" class="wrap inner-artistic"',1)
        pattern=r'(<section class="page-head"><div class="page-head-copy">)<span class="eyebrow">'
        text,count=re.subn(pattern,lambda m:m[1]+'<span class="eyebrow inner-artistic-label">'+svg,text,count=1)
        assert count==1,f'Artistic opening missing: {name}'
        path.write_text(text.replace('</head>','<link rel="stylesheet" href="assets/inner-artistic.css?v=2"></head>'))

    # Directory openings already have their artistic mark; add just the waterline.
    for path in [site/'poets.html',*site.glob('archive*.html')]:
        if path.is_symlink():continue
        text=path.read_text()
        if 'class="archive-directory"' not in text and 'class="poets-directory"' not in text:continue
        path.write_text(text.replace('</head>','<link rel="stylesheet" href="assets/inner-artistic.css?v=2"></head>'))
