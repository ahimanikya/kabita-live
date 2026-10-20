"""Approved 3 October restraint pass; art masters and poem text stay intact."""
import re


def apply_human_natural(site):
    practical = {'poems.html', 'poets.html', 'contact.html', 'feedback.html', 'submit.html'}
    practical.update(p.name for p in site.glob('archive*.html') if not p.is_symlink())
    for path in site.glob('*.html'):
        if path.is_symlink():
            continue
        text = path.read_text()
        if path.name in practical:
            text, count = re.subn(r'(<main\b[^>]*class=")', r'\1utility-first ', text, count=1)
            assert count == 1, path.name
            # These decorative opening images remain in the art catalogue/KB.
            text = re.sub(r'<figure class="opening-art\b[^\"]*"[^>]*>.*?</figure>', '', text, flags=re.S)
            text = re.sub(r'<img src="assets/section-art/[^\"]+"[^>]*alt=""[^>]*>', '', text)
        text = text.replace('</head>', '<link rel="stylesheet" href="assets/human-natural.css?v=2"></head>')
        if '<details class="edition-story">' in text:
            text = text.replace('</head>', '<script defer src="assets/cover-story.js?v=1"></script></head>')
        path.write_text(text)
