# Kabita Live — header and footer close review

29 September 2026 · Review of revision 23 · No journal design changes made

The direction is sound: the header establishes the name and helps readers find their way; the footer ends with the Odia signature and a quiet image. Keep this structure. Prioritise the enlarged-text navigation problem, then refine the ornament and the signature’s wrapping.

## Header

### Keep

- English-only **Kabita Live** with the sea-blue symbol and serif wordmark. It is legible, distinctive and calm. Retain the Odia voice in the page content and closing signature.
- The six plain navigation labels: **Current issue, Poems, Poets, Editors, Archive, Search**. Their job is orientation; poetic labels would make these harder to scan. Keep reading-language filters within the reading experience.
- Current-section colour plus an underline. The underline gives a second cue beyond colour.
- 17 px navigation and 48 px navigation/menu targets. These are comfortably sized. The desktop header is approximately 106 px high; the phone header is about 90 px while closed.
- A normal scrolling header. A persistent header would take reading space; the present design feels appropriate for poetry.

### Fix first: navigation at enlarged text sizes

At 200% text size, the header cannot fit its wordmark and desktop links into one row at 901 px and 1024 px. At 901 px, Editors, Archive and Search extend beyond the viewport; at 1024 px, Archive and Search extend beyond it. The fixed 900 px menu breakpoint does not respond to the space the enlarged content requires.

Recommended behaviour: allow the masthead to wrap cleanly, put desktop navigation onto a full-width second row when needed, and allow navigation items to wrap. Preserve the compact menu for narrow screens. Do not reduce type or conceal the overflow. Test just above the breakpoint and with text enlarged independently of the viewport.

This is a real issue missed by the preceding automated desktop/phone audit. That audit remains evidence for its tested conditions, not a guarantee for all widths or text settings.

### Refine the decorative separator

The two long page rules stop before the short rules already drawn inside the ornament. The visible gaps make a delicate separator look assembled from separate pieces. The leaf-and-water shape is attractive; it needs cleaner integration.

Use one pair of continuous outer rules and a single, smaller central motif. Give the motif a deliberate amount of breathing room; remove its redundant internal horizontal rules. Keep the current low-contrast rule colour. This is decorative artwork and should remain ignored by screen readers.

In night reading, the wordmark and links adapt well, but the motif’s dark, fixed sea-blue/rust colours nearly disappear. Give the decorative motif a subdued night palette, without making it brighter than navigation.

### Phone menu

The menu opens into two readable rows at 320 and 390 px. Opening state is announced through aria-expanded; Escape closes it and returns focus to Menu. Keep this behaviour. A visible “Close” label in the open state would make dismissal more explicit, but is a refinement rather than a defect.

The home-logo link is only about 32–39 px tall, depending on width. This is not a measured minimum-target compliance failure, but increasing its invisible hit area to 44–48 px would improve touch comfort without enlarging the wordmark.

## Footer

### Keep

- Exactly three links: **Our story · Send a poem · Contact**. All have 48 px targets and 16 px text.
- The small boat at the right edge. It closes the page with a sense of place. It is subtle at normal size and remains visually coherent on the dark reading background.
- The Odia signature on the left and the ownership note below. At 1280 px, the footer is approximately 132 px high, excluding the approach space. At 390 px it is approximately 178 px.
- The ownership note at 13 px, muted but readable. Keep biography and portrait sources with their relevant pages, and keep the redesign credit on Our Story.

### Refine the Odia signature

The current desktop signature is 19 px and the phone version 18 px. A modest increase to 20 px desktop / 19 px phone would give the closing line more presence while keeping the links secondary. This is an aesthetic recommendation, not an accessibility requirement.

The more important change is phrase-aware wrapping. At 901 px with doubled text, “ମନର” appears at the end of one line and “ସ୍ୱର” alone on the next. Group the two phrases, letting the entire second phrase move to a new line when possible:

ମାଟିର ମହକ
ମନର ସ୍ୱର

Use the centred dot only when both phrases sit on one line. At extreme enlargement, permit further wrapping instead of forcing horizontal overflow. Do not use a hard no-wrap rule that fails on narrow screens.

### Orientation and spacing

The three footer links are identical on every page and currently have no current-page indicator. On Our Story, Send a poem and Contact, add aria-current and a quiet underline to the corresponding footer link. This extends the header’s orientation pattern without adding content.

The desktop footer’s empty centre is useful breathing room. Keep it. The phone footer has a clear three-step rhythm: signature, links, ownership note. If making it slightly tighter, reduce vertical gaps by only 4–6 px and retain the large link targets.

## Evidence and limitations

- All **37 journal pages** share one header structure and an identical footer. The four proposal/branding documents are companion documents, not journal templates.
- Checked seven widths: 320, 390, 768, 900, 901, 1024 and 1280 px; normal and 200% text, 14 combinations total.
- Normal-size header/footer controls fit at all seven widths.
- Header overflow is confirmed at 901/1024 px with doubled text. The full homepage also shows a separate 28 px overflow at 768 px with doubled text, but its header/footer controls stay within the viewport; investigate page content separately.
- Verified menu open/close state and Escape focus return through the actual page event handlers.
- Reviewed actual day and night rendering, mobile open menu, desktop close-ups and enlarged-text failure.
- These are browser measurements, source inspection and visual review. The 200% exercise doubles rendered text sizes; it is not a complete screen-reader or native-browser-zoom certification.

## Suggested refinement order

1. Repair enlarged-text navigation and verify the breakpoint boundary.
2. Make the separator continuous and give it a restrained night palette.
3. Group the Odia signature phrases and add footer current-page cues.
4. Enlarge the logo’s touch area and optionally clarify the open menu label.
5. Recheck all journal templates with the shared changes.

The interactive close-up board is at `site/audit/header-footer-review.html`. Screenshots and responsive measurements are saved alongside this review.
