"""Losslessly package full licensed fonts as WOFF2. Requires fonttools[woff].
Only rerun when source fonts change; committed binaries keep CI dependency-free.
"""
from pathlib import Path
from fontTools.ttLib import TTFont
import json,hashlib
root=Path(__file__).resolve().parents[1]
report=[]
for source in sorted((root/'assets/fonts').glob('*.ttf')):
    target=source.with_suffix('.woff2')
    font=TTFont(source);font.flavor='woff2';font.save(target)
    original=TTFont(source);converted=TTFont(target)
    assert original.getBestCmap()==converted.getBestCmap()
    assert original.getGlyphOrder()==converted.getGlyphOrder()
    for tag in ('GSUB','GPOS','GDEF','fvar'):
        if tag in original:assert original[tag].compile(original)==converted[tag].compile(converted),tag
    report.append({'font':source.stem,'ttf_bytes':source.stat().st_size,'woff2_bytes':target.stat().st_size,'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'woff2_sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'glyphs':len(original.getGlyphOrder()),'shaping_and_variations_preserved':True})
print(json.dumps(report,indent=2))
