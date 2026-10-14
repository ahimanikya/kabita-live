"""Explicit prose engagement context; numeric poem controls remain unchanged."""
from engagement_footer import article_actions, sharing_fields
CONTEXTS={
 'issue-48.html':('kabita:article:edition-48-editorial','or'),
 'thirty-languages-and-the-journey-of-a-poem.html':('kabita:article:language-journey','en')
}
def append_article_responses(root,file,body):
 if file not in CONTEXTS:return body
 ident,language=CONTEXTS[file]
 template=(root/'templates/article-engagement.html').read_text()
 return body+template.replace('{{RESPONSE_ACTIONS}}',article_actions()).replace('{{SHARING_FIELDS}}',sharing_fields()).replace('{{CONTENT_ID}}',ident).replace('{{LANGUAGE}}',language)
