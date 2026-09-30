"""Local routing and reader copy. Source evidence remains in the project KB."""
import re
from urllib.parse import urlsplit, parse_qs

REVIEW_FILES = {
    'all-pages.html', 'branding-guide.html', 'cover-studies.html', 'design-system-review.html',
    'design-system-sample.html', 'editor-cover-card.html', 'editors-cheat-sheet.html',
    'icon-atelier.html', 'literary-study.html', 'magazine-branding.html', 'proposal.html',
    'responsive-check.html', 'site-coverage.html',
}
sample_routes = {809: 'poem-dokana.html', 810: 'poem-kshanika.html', 814: 'poem-drink.html'}
profile_routes = {82:'poet-dokana.html',337:'poet-kshanika.html',257:'poet-drink.html',
                  1:'editor-pradeep.html',43:'editor-paresh.html'}
issue_ids = {int(parse_qs(urlsplit(x['url']).query)['id'][0]):int(re.search(r'\d+',x['title']).group())
             for x in json.loads((R/'data/issues.json').read_text())}


def local_route(url):
    parts = urlsplit(url)
    if parts.hostname not in {'kabitalive.com', 'www.kabitalive.com'}:
        return url
    pid = parse_qs(parts.query).get('id', [''])[0]
    if pid.isdigit():
        ident = int(pid)
        if parts.path.endswith('poemview.php'):
            return sample_routes.get(ident, f'poem-{ident}.html')
        if parts.path.endswith('contri-view.php'):
            return profile_routes.get(ident, f'poet-{ident}.html')
        if parts.path.endswith('archive-view.php') and ident in issue_ids:
            return f'issue-{issue_ids[ident]}.html'
        if parts.path.endswith('bookview.php'):
            return f'review-{ident}.html'
    if parts.path in {'', '/', '/index.php'}:
        return 'index.html'
    return {'/about.php':'about.html','/adv.php':'highlights.html'}.get(parts.path, '')


def reader_copy(body):
    # These are review notes from the former prototype, not journal content.
    body = re.sub(r'<p class="reader-note">(?:(?!</p>).)*</p>', '', body, flags=re.S)
    body = re.sub(r'<a\b[^>]*>Original writer profile.*?</a>', '', body, flags=re.S)
    body = re.sub(r'<a\b[^>]*>Read the full published poem.*?</a>', '', body, flags=re.S)
    body = re.sub(r'<details><summary class="text-link">Leave a reading response</summary>.*?</details>',
                  '<p><a class="text-link" href="contact.html">Write to the editors</a></p>', body, flags=re.S)
    def anchor(m):
        before, url, after, label = m.groups()
        target = local_route(url)
        if not target:
            return label
        if target != url:
            after = re.sub(r'\s+(?:target|rel)="[^"]*"', '', after)
        return '<a' + before + 'href="' + target + '"' + after + '>' + label + '</a>'
    body = re.sub(r'<a([^>]*?)href="(https?://(?:www\.)?kabitalive\.com[^" ]*)"([^>]*)>(.*?)</a>',
                  anchor, body, flags=re.S)
    body = body.replace('Use the journal’s existing editorial address.', 'Write to the editorial desk.')
    body = body.replace('Corrections go to the editorial desk. Reading responses remain with their poem.',
                        'Notes, reading responses and corrections go to the editorial desk.')
    return body
