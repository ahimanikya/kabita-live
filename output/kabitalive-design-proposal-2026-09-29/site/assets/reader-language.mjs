export const languageNames = {or: 'Odia', hi: 'Hindi', en: 'English'};
export const languageGlyphs = {or: 'ଅ', hi: 'अ', en: 'A'};

// Keep the preference distinct from the language actually rendered. Original
// follows each poem; a named-language preference survives source changes.
export function readingCode(poem, preference = 'original') {
  return preference === 'original' || !poem.variants[preference] ? poem.source_language : preference;
}
export function poemChoice(poem, code) {
  return code === poem.source_language ? 'original' : code;
}
export function versionLabel(poem, code) {
  return code === poem.source_language ? 'Original · ' + languageNames[code] : languageNames[code] + ' translation · Original: ' + languageNames[poem.source_language];
}
export function readingPosition(visible, poemIndex) {
  return visible.find(unit => unit.poemIndex === poemIndex) || visible[0];
}
export function readerChoices(poem, preference = 'original') {
  const selected = poemChoice(poem, readingCode(poem, preference));
  return ['original', ...Object.keys(languageNames).filter(code => code !== poem.source_language)].map(choice => {
    const code = choice === 'original' ? poem.source_language : choice;
    return {choice, code, original: choice === 'original', selected: choice === selected, available: !!poem.variants[code]};
  });
}
