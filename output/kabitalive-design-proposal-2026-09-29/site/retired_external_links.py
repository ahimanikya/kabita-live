"""Keep historical citation labels readable without confirmed dead click targets."""
import html,json,re

def remove_retired_links(markup, retired):
    def replace(match):
        href=re.search(r'\bhref\s*=\s*([\"\'])(.*?)\1',match['attrs'],re.I|re.S)
        if not href or html.unescape(href[2]) not in retired:return match[0]
        label=re.sub(r'\s*↗\s*$','',match['body'])
        return '<span class="unavailable-reference">'+label+'</span>'
    return re.sub(r'<a\b(?P<attrs>[^>]*)>(?P<body>.*?)</a>',replace,markup,flags=re.I|re.S)

def load_retired_links(root):
    path=root/'data/retired-external-links.json'
    return set(json.loads(path.read_text())['urls']) if path.exists() else set()
