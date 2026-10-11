/** Text identity is source-based; pages and columns are deliberately absent. */
export function textUnits(variant) {
  if (!variant || !Array.isArray(variant.blocks)) throw new TypeError('Reader blocks required');
  const blocks = new Set(), units = [];
  for (const block of variant.blocks) {
    if (!block || typeof block.id !== 'string' || !block.id || blocks.has(block.id)) throw new TypeError('Unique block identity required');
    blocks.add(block.id);
    const values = block.kind === 'verse' ? block.lines : block.kind === 'list' ? block.items : ['paragraph','heading','quote'].includes(block.kind) ? [block.unit] : ['image','rule'].includes(block.kind) ? [] : null;
    if (!Array.isArray(values)) throw new TypeError('Unknown or invalid reader block');
    const ids = new Set();
    for (const unit of values) {
      if (!unit || typeof unit.id !== 'string' || !unit.id || ids.has(unit.id) || typeof unit.text !== 'string') throw new TypeError('Unique text unit required');
      ids.add(unit.id); units.push({blockId:block.id,unitId:unit.id,text:unit.text});
    }
  }
  return units;
}
export function snapOffset(text,offset,language) {
  if (typeof text !== 'string' || !Number.isInteger(offset) || offset < 0 || offset > text.length) return null;
  const boundaries = [0,...Array.from(new Intl.Segmenter(language,{granularity:'grapheme'}).segment(text),x=>x.index+x.segment.length)];
  return boundaries.filter(x=>x<=offset).at(-1);
}
export function resolveAnchor(item,anchor) {
  if (!item || !anchor || anchor.contentId !== item.id) return {ok:false,reason:'content'};
  const variant = item.variants?.[anchor.language];
  if (!variant) return {ok:false,reason:'language'};
  if (typeof variant.revision !== 'string' || !variant.revision || variant.revision !== anchor.revision) return {ok:false,reason:'revision'};
  const unit = textUnits(variant).find(u=>u.blockId===anchor.blockId && u.unitId===anchor.unitId);
  if (!unit) return {ok:false,reason:'unit'};
  const offset = snapOffset(unit.text,anchor.offset,anchor.language);
  return offset === null ? {ok:false,reason:'offset'} : {ok:true,anchor:{contentId:item.id,language:anchor.language,revision:variant.revision,blockId:unit.blockId,unitId:unit.unitId,offset},text:unit.text};
}
export function startAnchor(item,requestedLanguage) {
  const language = item.variants?.[requestedLanguage] ? requestedLanguage : item.sourceLanguage;
  const variant = item.variants?.[language];
  if (!variant || typeof variant.revision !== 'string' || !variant.revision) throw new TypeError('Source variant/revision required');
  const unit = textUnits(variant)[0];
  return {language,fallback:language!==requestedLanguage,anchor:unit ? {contentId:item.id,language,revision:variant.revision,blockId:unit.blockId,unitId:unit.unitId,offset:0} : null};
}
