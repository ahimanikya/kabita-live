"""Validate explicit target-language lineation without reusing source tail offsets."""
import hashlib
import json

def stanza_hash(stanzas):
    return hashlib.sha256(json.dumps(stanzas, ensure_ascii=False, separators=(',', ':')).encode()).hexdigest()

def validate_layout(source, variant):
    stanzas = variant['stanzas']
    assert stanzas and all(s and all(isinstance(line, str) and line.strip() for line in s) for s in stanzas), 'Empty translation verse'
    layout = variant.get('reader_layout')
    if layout is None:
        assert list(map(len, stanzas)) == list(map(len, source['stanzas'])), 'Changed target lineation needs explicit reader_layout'
        return None
    assert layout['source_sha256'] == hashlib.sha256(source['text'].encode()).hexdigest(), 'Stale layout source'
    assert layout['stanzas_sha256'] == stanza_hash(stanzas), 'Stale target layout'
    count = layout['verse_line_count']
    assert type(count) is int and 0 < count <= sum(map(len, stanzas)), 'Invalid target verse boundary'
    breaks = layout['before_lines']
    assert isinstance(breaks, list) and all(type(i) is int and 0 < i < count for i in breaks), 'Invalid target stanza boundaries'
    assert breaks == sorted(set(breaks)), 'Duplicate or unordered stanza boundaries'
    # Revisions with embedded-line offsets need a separately verified mapping.
    assert layout.get('inline_breaks') == [], 'Explicit target layout requires reviewed verse lines, not inherited inline offsets'
    return layout
