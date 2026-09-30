---
type: "Design reference"
title: "Approved design system"
---

Derived from [the canonical KB design source](../artifacts/design/brand-guide/DESIGN-SYSTEM.md); edit that source and regenerate.

# Kabita Live — design system

The journal should feel like cotton paper, a quiet room and a voice close enough to hear. Art creates atmosphere; poems, names and navigation stay clear. This document separates approved decisions from the component work still to review.

## Approved foundations

| Element | Standard |
|---|---|
| Identity | English-only Kabita Live masthead; the same mark on the site and magazine. |
| Signature | ମାଟିର ମହକ / ମନର ସ୍ୱର in dark ink, with a shared left edge. No repeat in the footer. |
| Colour | Paper #F5EFDF; ink #263C3C; sea #125465; laterite #963F28; hearth #78643A; muted ink #655F51; pale paper #EAE1CD; rules #D2C6AC. Use colour by role, not by page. |
| English | Cormorant Garamond 500 for display; genuine italic for large quotations. Source Serif 4 for sustained reading. |
| Odia | Noto Serif Oriya throughout. Natural spacing and upright shaping. |
| Hindi | Tiro Devanagari Hindi 400 upright. Natural spacing; no synthetic bold or slant. |
| Reading | Poems 24px desktop / 22px mobile, with 1.8–2 line height. Preserve verse and stanza breaks. Reader enlargement offers 28px and 32px. |
| Interface | Clear sans serif with approved script fallbacks. Main navigation 17px; primary navigation targets 48px. |
| Page openings | Shared masthead. Most inner-page banners use 60% text on the left, 40% unique art on the right; stack without clipping on phones. |
| Surface | Cotton paper at 16%. Poem pages vary deterministically between monsoon and earth wash at 18%, softened to 12.6% on phones. Night reading has no texture. |
| Footer | One desktop row: ownership left, links right. Two clean left-aligned rows on small screens. No repeated design credit. |
| Ornament | One small artistic header separator. Use restrained section rules, quiet external-link marks and no duplicate decorative dividers. |
| Art | A distinct cultural narrative per cover; protect the focal point and keep typography separate from artwork. Preserve historical originals. |

## Attribution and disclosure

Our Story → Credits & colophon is the common home for redesign credit, font credits, generated-art disclosure, portrait sources and editor biography references. The existing Our story footer link makes this available everywhere without another footer item.

Remove repeated generic “Artwork study” and “Generated illustration” captions from reader pages. Keep meaningful artwork titles such as LIFE AS IT IS. Keep alt text descriptive; it does not replace the visible colophon. Each editor profile links directly to its specific source record in the colophon.

Poet bylines, translators, reviewer names and the identity of quoted work remain beside their content. Cover narratives keep their cultural references. Record any asset-specific credit placement requirement with that asset and honour it; a common colophon does not override an agreed credit placement. Exported covers and social images need accompanying provenance because they travel separately from the website.

## Component review queue

| Priority | Component | What to inspect | Completion evidence |
|---|---|---|---|
| 1 | Poem reader | Title/byline hierarchy, stanza rhythm, long lines, 28/32px enlargement, night mode, reading toolbar on phones. | All three scripts at 360px and desktop, keyboard operation and enlarged text without clipping. |
| 2 | Links, buttons and forms | One primary action, quiet text links, external marks, hover, focus, pressed, disabled, error and success states. | A shared component specimen with all states; status is never colour-only. |
| 3 | Search and navigation | Filter location, clear/reset action, no results, loading, recoverable errors, menu focus and return path. | Realistic populated and empty states; keyboard and touch checks. |
| 4 | Cards and metadata | Issue/date, language, author and translator placement; long names and titles; cover/list views. | Same content hierarchy across poem, writer and archive cards. |
| 5 | Artwork and cropping | Portrait identity, focal point, 40% banners, cover aspect ratio, missing artwork and descriptive alt text. | Desktop and phone crop examples; no stretching or text baked into artwork. |
| 6 | Spacing and responsive rhythm | Shared gutters, section gaps, reading measure, heading gaps and dense footnotes. | Adopt one spacing scale after visual review and migrate component exceptions deliberately. |

## Spacing: candidate scale for the next review

Proposed shared steps: 4, 8, 12, 16, 24, 32, 48 and 64px. Use 8–12px within small groups, 16–24px between related elements, 32px between content groups and 48–64px between major sections. These are candidate tokens, not a claim that every current page has been normalized. Existing optical adjustments, including the compact Odia signature, must survive the migration.

## Interaction and accessibility review gates

The prototype includes keyboard focus, labelled filters, reader sizing, night reading and sharing controls. Still review these as one coherent component family. Prefer brief functional transitions; avoid looping decorative motion and honour reduced-motion preferences. Keep at least 44px effective touch targets, visible keyboard focus and sufficient text contrast. Check 200% text enlargement as well as phone layouts; the earlier enlarged-header breakpoint concern remains open until retested and resolved.

Automated axe and overflow checks are useful evidence, not a complete accessibility certification. A fluent editor should inspect all three scripts, names and punctuation before publication.

## Ownership of the system

The visual branding guide is the editor-facing reference. This document records component decisions and pending reviews. Brand tokens describe implemented foundations; candidate values stay explicitly marked until adopted. Keep font licenses and artwork provenance with the handoff files. Update the guide, tokens and component examples together when a decision changes.

## Interactive review desk

Open `site/design-system-review.html` for 18 groups, including five locked foundations and 13 decisions to review. Each undecided group has two directions, live samples, a phone preview and a review checklist. Approve a direction, request changes, leave notes or reopen a decision. Previewing a different option does not erase the previously approved option.

Choices are saved only in the browser under the review version. Download decisions as JSON for a durable handoff. Browser decisions do not automatically edit source files or publish the website. The exported record distinguishes the currently previewed option from the approved option. Use the exported decisions to implement the selected components in a subsequent pass.

The sample library covers reading controls, navigation, buttons, metadata cards, form validation, feedback states, live Unicode search, sharing dialogs, artwork, missing imagery, separators and reduced-motion behaviour. Public journal copy and existing layouts remain separate until an option is applied.

## Literary benchmark and icon candidates — Revision 40

The source-linked study is `site/literary-study.html`. The visual review is `site/icon-atelier.html`: 14 editorial motifs and 12 familiar action symbols, with ink and restrained earth-accent treatments. These are candidates, not approved replacements for the logo, separator or existing reader controls. Each asset has a cultural/use record in `site/assets/icons/earth-voice-v1/manifest.json`; 24-unit utility and 48-unit editorial masters remain separate. The dedicated package is `Kabita-Live-Earth-and-Voice-Icons-v0.1.zip`. Existing delivery ZIPs remain revision-39 snapshots.

Utkal Blueprint was initially studied as a reference, then adopted locally under the user’s explicit instruction. The root KB records the project-specific charter, authorization and pinned source. Utkal Project small-size/colour/reverse master discipline informed the study; its book-and-boat geometry was not copied. The user clarified that the project should first adopt Blueprint and build its own reusable icon catalogue. No external icon repository integration is claimed.

## Approved icon treatment — Revision 41

Ahimanikya selected **Option A: single-colour Quiet ink**: “I like the icon with the single-color option A”. Use one ink colour per icon; no laterite accent wash. Option B is preserved only as a historical comparison. This approves the treatment, while specific motif placement remains the next review. The logo and approved header separator are separate existing identity assets.

The homepage now introduces Pradeep Biswal (Editor) and Paresh Kumar Pattnaik (Managing Editor), with links to their profiles. These titles were reconfirmed on the original magazine site; no unsupported duties or reporting structure were added.
