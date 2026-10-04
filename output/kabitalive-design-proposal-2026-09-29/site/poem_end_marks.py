"""Approved stable closing marks, shared through the reader payload."""
import json
from pathlib import Path
OVERRIDES=json.loads((Path(__file__).resolve().parent/'data/poem-end-mark-overrides.json').read_text())
KINDS=('leaf','leaf','leaf','paired','sprig')
def end_mark_kind(ident):
    kind=OVERRIDES.get(str(ident),KINDS[int(ident)%len(KINDS)])
    if kind not in {'leaf','paired','sprig'}:raise ValueError('Unknown poem end mark: '+kind)
    return kind
def end_mark_html(ident):
    if str(ident)=='385':return '' # Incomplete text must not imply a confirmed ending.
    return '<span class="poem-closing-mark" data-end-mark="'+end_mark_kind(ident)+'" aria-hidden="true"></span>'
