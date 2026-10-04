// Choose the initial disclosure state once; afterwards the reader owns it.
// Native details keeps the entire cultural story available without JavaScript.
if (matchMedia('(min-width:761px)').matches) {
  document.querySelectorAll('details.edition-story').forEach(story => { story.open = true; });
}
