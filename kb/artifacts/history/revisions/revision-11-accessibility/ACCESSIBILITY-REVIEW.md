# Accessibility review — Kabita Live

29 September 2026 · Revision 11 · Local design prototype

The main menu is now 17 px, language navigation and footer links are 16 px, and the main menu/language controls have 48 × 48 px minimum targets. These are minimum design defaults: do not shrink the navigation to make it fit. Collapse it to the Menu button below 900 px and let its links wrap when expanded. Retain the English Kabita Live masthead and the separate Odia signature.

## Changes made

- Increased navigation, language controls, reader tools and form-label sizes; preserved the uncluttered layout.
- Strengthened form boundaries and focus outlines. Ink on warm paper is 10.61:1, red earth is 6.08:1 and muted ink is 5.16:1, calculated from the specified sRGB colours.
- Made both reference documents’ scrolling tables keyboard focusable and visibly outlined.
- Corrected accessible roles for the language group and portrait placeholders.
- Made the skip link focus the main content. Added Escape handling for the mobile menu and focus handling for sharing.
- Allowed long headings, cover lettering and narrow archive/directory columns to adapt to enlarged or widely spaced text.

## Recorded checks

| Check | Scope | Result |
|---|---|---|
| axe-core 4.10.3, WCAG A/AA rule tags through WCAG 2.2 | All 40 HTML documents at 1280 CSS px | 0 automatic violations; 0 execution errors |
| Same automated rules, mobile menu expanded | All 40 documents at 320 CSS px | 0 automatic violations; 0 execution errors |
| Page reflow | Both widths above | No page-level horizontal overflow or broken images |
| Synthetic 200% text enlargement | All 40 documents at 1280 CSS px | No page-level horizontal overflow; text clipping candidates inspected and fixed |
| Increased line, letter, word and paragraph spacing | All 40 documents at 320 CSS px | No page-level horizontal overflow |
| Night reading with share dialog open | Odia reader at 320 CSS px | 0 automatic violations after the entrance animation completed |
| Keyboard walkthrough | Homepage and Odia reader | Skip link reaches main; reader controls reachable; Enter opens sharing; Escape closes it and returns focus to Share |
| Visual review | Desktop homepage and expanded 320 px mobile menu | Larger navigation remains readable and fits the layout |

The enlargement test doubles each element’s computed font size. It is a useful stress test, not a substitute for actual browser zoom or device font settings. The text-spacing test applies 1.5 line height, 0.12em letter spacing, 0.16em word spacing and 2em paragraph spacing. Reference tables deliberately retain horizontal scrolling within keyboard-accessible regions. A decorative image extends beyond the branding guide’s cover section; this is an intentional crop, not clipped text.

During the native dialog keyboard walkthrough, focus briefly entered browser chrome at the end of its sequence, then returned to the dialog. No underlying page link or control received focus while it was open. A supplemental first/last-control handler is included, but strict containment across browser/assistive-technology combinations remains a release check.

## What this does not certify

This is a prototype audit, not a WCAG conformance certification or an audit of the existing live website. Automated checking cannot resolve every accessibility question. The final desktop scan retains 62 contrast nodes marked **incomplete** across 11 documents, predominantly text over photographs, gradients, decorative layers, and a few obscured form/editorial elements. These are not counted as passes or automatic violations. Their exact locations are preserved in the JSON evidence and require manual contrast review at final image crops and interactive states.

Before launch, test the implemented site with VoiceOver/NVDA, actual browser zoom to 200% and 400%, physical touch devices, and readers of Odia/Hindi/English. Confirm pronunciation, language changes, reading order, complete poem line breaks, form errors, focus restoration, and sharing. The existing editor PDF was not included in the HTML audit; a tagged, accessible PDF requires a separate review.

## Editorial cheat card: readable navigation

- Main menu: **17 px / 1.0625 rem minimum**.
- Language links, footer links and form controls: **16 px / 1 rem minimum**.
- Main navigation and language targets: **48 px minimum height and width**.
- Use dark ink on warm paper; never place small navigation text directly on cover art.
- Keep visible keyboard focus. Do not remove outlines or reduce type to fit extra menu items.
- Test longer translated labels, narrow screens and enlarged text before adding navigation.

The 48 px target is our more generous design choice; WCAG 2.2 AA’s target-size criterion uses 24 CSS px with exceptions. Font size alone does not establish accessibility.

## Evidence and references

Raw results: desktop-1280.json, mobile-320-menu-open.json, text-enlargement-200.json, text-spacing-320.json, night-sharing-320.json. Each includes page names, measured navigation, errors, overflow and applicable automated findings. The local audit harness is in site/audit; axe-core is bundled with its license and is not loaded by normal magazine pages.

- [W3C: Contrast minimum](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html)
- [W3C: Target size minimum](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html)
- [W3C: Resize text](https://www.w3.org/WAI/WCAG22/Understanding/resize-text.html)
- [Deque: axe-core](https://github.com/dequelabs/axe-core)
