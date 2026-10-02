"""Approved cover-only archive, shared by archive and saved year routes."""
from html import escape

def render_archive(site, issues, cover, year='all'):
    issues=sorted(issues,key=lambda issue:issue['number'],reverse=True)
    years=sorted({str(issue['year']) for issue in issues},reverse=True)
    icon=(site/'assets/icons/earth-voice-v1/ink/footer-story.svg').read_text()
    controls=''.join(f'<button type="button" data-archive-year="{value}" aria-pressed="{str(value==year).lower()}">{label}</button>' for value,label in [('all','All years')]+[(y,y) for y in years])
    cards=[]
    for issue in issues:
        n=issue['number'];date=escape(f"{issue['month']} {issue['year']}")
        cards.append(f'<article class="issue-card" data-issue-year="{issue["year"]}"><a href="issue-{n}.html" aria-label="Open issue {n}">{cover(n)}</a><div class="edition-identity"><h2><a href="issue-{n}.html">{date}</a></h2><p>Issue {n} · {len(issue["poem_ids"])} poems</p></div></article>')
    return ('<link rel="stylesheet" href="assets/archive-directory.css?v=1"><script defer src="assets/archive-directory.js?v=1"></script>'
        f'<div class="archive-directory" data-initial-year="{year}"><section class="archive-opening"><div><span class="eyebrow artistic-eyebrow">'+icon+
        ' The archive</span><h1>Every issue,<br>another beginning.</h1><p>Forty-seven gatherings of words.<br>Open a cover; let a poem find you.</p></div><img src="assets/section-art/archive-640.webp" width="640" height="427" alt=""></section>'
        '<div class="archive-years" role="group" aria-label="Choose a year">'+controls+'</div><p id="archive-results" role="status" aria-live="polite"></p><div class="cover-grid archive-gallery">'+''.join(cards)+
        '</div><div class="archive-more"><button type="button" class="btn" id="archive-more">Show more editions</button><p id="archive-progress"></p></div></div>')
