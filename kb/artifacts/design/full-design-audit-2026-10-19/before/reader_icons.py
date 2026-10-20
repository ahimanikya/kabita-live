"""Canonical reader action icons, reused by all reader entry points."""
from pathlib import Path
import re
ROOT=Path(__file__).resolve().parent
READ_QUIETLY_ICON='footer-story'

def reader_action_icon(name):
    svg=(ROOT/f'assets/icons/earth-voice-v1/ink/{name}.svg').read_text().strip()
    svg=re.sub(r' role="img"| aria-label="[^"]*"| aria-hidden="[^"]*"| focusable="[^"]*"','',svg)
    return svg.replace('<svg ','<svg aria-hidden="true" focusable="false" ',1)

def quiet_reader_icon():
    return reader_action_icon(READ_QUIETLY_ICON)
