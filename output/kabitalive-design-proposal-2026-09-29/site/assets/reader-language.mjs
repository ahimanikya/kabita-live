export const languageNames = {or: 'Odia', hi: 'Hindi', en: 'English'};

// Old language URLs/preferences resolve to the submitted language.
export function readingCode(poem) { return poem.source_language; }
export function poemChoice() { return 'original'; }
export function versionLabel(poem) { return 'Original · ' + languageNames[poem.source_language]; }
export function readingPosition(visible, poemIndex) {
  return visible.find(unit => unit.poemIndex === poemIndex) || visible[0];
}
