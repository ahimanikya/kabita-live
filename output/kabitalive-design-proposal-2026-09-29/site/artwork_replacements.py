"""Apply approved versioned artwork after page generation; preserve source assets."""
import json,re
from pathlib import Path

def apply_artwork_replacements(root):
    mapping=json.loads((root/'artwork-replacements.json').read_text())
    pattern=re.compile('|'.join(re.escape(k) for k in sorted(mapping,key=len,reverse=True)))
    paths=list(root.glob('*.html'))+list((root/'assets').glob('reading*.json'))+list((root/'assets/reading-editions').glob('*.json'))+list((root/'assets/reading-authors').glob('*.json'))
    for path in paths:
        if path.is_symlink(): continue
        old=path.read_text(); new=pattern.sub(lambda m:mapping[m.group()],old)
        if new!=old:path.write_text(new)
