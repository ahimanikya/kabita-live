"""Canonical reader action icons, reused by all reader entry points."""
from pathlib import Path
import re
ROOT=Path(__file__).resolve().parent
READ_QUIETLY_ICON='footer-story'

def quiet_reader_icon():
    svg=(ROOT/f'assets/icons/earth-voice-v1/ink/{READ_QUIETLY_ICON}.svg').read_text().strip()
    svg=re.sub(r' role="img"| aria-label="[^"]*"| aria-hidden="[^"]*"| focusable="[^"]*"','',svg)
    return svg.replace('<svg ','<svg aria-hidden="true" focusable="false" ',1)
