"""Compact reader response controls; service and moderation contracts stay unchanged."""
from html import escape
from reader_icons import reader_action_icon
HEART='<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M12 20.5 3.8 12.4C-1.6 6.8 6.4 0 12 6.8 17.6 0 25.6 6.8 20.2 12.4Z"/></svg>'
COMMENT='<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M20 4H4v13h4v4l5-4h7Z"/><path d="M7 8h10M7 12h7"/></svg>'
def action(label,icon,attrs='',tag='button'):
 return f'<{tag} class="response-icon" '+('type="button" ' if tag=='button' else '')+f'aria-label="{escape(label)}" title="{escape(label)}" {attrs}>{icon}<span class="response-tip" aria-hidden="true">{escape(label)}</span></{tag}>'
def share_action(attrs='data-share-page'):
 return action('Share',reader_action_icon('share'),attrs)
def feedback_link(poem_id):
 return action('Private feedback',reader_action_icon('footer-contact'),f'href="contact.html?poem={poem_id}"','a')
def article_actions():
 return (action('Like',HEART,'data-response-like aria-pressed="false" disabled')+
 action('Comments',COMMENT,'data-response-comments data-response-toggle="comments" aria-expanded="false" aria-controls="response-comments" disabled')+
 action('Private feedback',reader_action_icon('footer-contact'),'data-response-toggle="feedback" aria-expanded="false" aria-controls="response-feedback"')+
 '<span class="response-divider" aria-hidden="true"></span>'+share_action())
def poem_actions(poem_id):
 return (action('Like this poem',HEART,'data-like-proxy aria-pressed="false" disabled')+
 action('Comments',COMMENT,'data-response-toggle="comments" aria-expanded="false" aria-controls="response-comments" disabled')+
 feedback_link(poem_id)+'<span class="response-divider" aria-hidden="true"></span>'+share_action(f'data-share="{poem_id}"'))
def sharing_fields():
 return '<p data-share-status role="status" aria-live="polite"></p><label data-share-manual hidden>Page link<input data-share-field readonly aria-label="Page link"></label>'
