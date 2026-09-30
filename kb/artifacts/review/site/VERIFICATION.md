# Design verification — 29 September 2026

- Checked all 23 linked pages at 320 and 1280 CSS-pixel widths in the browser: 46 layout checks, zero horizontal overflow and zero broken images.
- Visually inspected the desktop homepage and a 390-pixel Odia reader. Refined the mobile homepage to reduce repeated branding and reach the issue sooner.
- Verified internal page/asset destinations and exactly one main heading per page.
- Exercised homepage → issue → Hindi filter → Hindi reader navigation.
- Exercised large reading text, night appearance and share dialog. Confirmed that share destinations retain the original poem ID and credit. Social posting and the operating-system share sheet were not invoked; clipboard behavior depends on browser permission, with a selectable-text fallback provided.
- Exercised mobile menu expansion, Unicode title search, no-result feedback and matching result restoration.
- Exercised correction links: contact reason and original poem URL are prefilled.
- Exercised the contact form with local sample values and confirmed its explicit unsent preview state.
- Exercised archive cover/list switch.
- Reduced-motion styling, focus indicators, semantic labels and native dialog behavior are present. Full screen-reader, device-sharing, 200%-zoom and long/spatial-poem testing remain production checks.

This is a static design prototype. The current issue shows three short excerpts; historical issues, biography and review material use explicit placeholders. No forms submit or persist information. No live site content was changed.

## Revision 04

Verified the exact retained name and final dot across all 23 page files, and rechecked their internal page/asset links. Visually checked the longer wordmark on the 320-pixel homepage: no horizontal overflow or broken images. Both poetic signatures remain.

## Revision 05

- Checked 27 HTML documents (24 page designs plus branding guide, proposal and editor reference) at 320 and 1280 CSS pixels: 54 checks, zero horizontal overflow or broken images.
- Visually inspected the realistic cover gallery with separately typeset mastheads and signatures.
- Confirmed all internal page, image and stylesheet destinations resolve.
- Checked Sabita Singh Meera’s title search returns the requested contribution; the 2025 filter shows exactly 11 source-listed entries and no other year.
- Writer data contains 4, 23 and 4 sourced contributions, respectively. These are not invented placeholder totals.
- Rendered and visually inspected the one-page A4 editor cheat-sheet PDF; no text clipping or overflow. Native CoreText was used for Odia shaping.
- Real posting, social metadata crawling, production publishing and historical full-text migration remain outside this prototype.


## Revision 06 — complete public coverage

- 36 generated linked designs plus three companion HTML documents.
- 39 documents at 320px and 1280px = 78 checked layouts; zero horizontal overflow and zero broken local images. Results saved in `revision-06/responsive-results.json`.
- Full writer index: 427 visible-name/profile records, preserved by source ID. Roman search “Sabita” and Odia search “ନର୍ମଦା” each returned the expected single record. A–Z selection updated visible entries.
- Archive: all 47 source records; selecting 2022 returned November and December only.
- Current issue: 16 detail-page-verified title/byline pairs; Hindi route returned two poems. Unmatched query showed helpful no-results state.
- Reader feedback: required fields and preview response confirmed that nothing was sent. No live form submissions were made.
- New coverage page visually inspected on desktop; responsive layout verified at mobile width. Existing reader/share behaviors retained from prior verification.
- These checks do not constitute a real-device or screen-reader accessibility certification. Full source content migration and external-link health remain production tasks.


## Revision 07 — Odisha and poetic atmosphere

Shared decorative divider and softer edge treatment applied; cover direction and guide updated. Existing cover image files were not edited. All 39 documents checked at 320px and 1280px: 78 layouts, zero horizontal overflow or broken images. Cover page visually inspected. Portable source build passed. See `revision-07/responsive-results.json`.


## Revision 08 — simplified visitor experience

All 39 preview documents checked at 320px and 1280px: 78 layouts, zero overflow or broken images. Homepage visually inspected. Main reading action opens the 16-poem issue. Odia reader share dialog retains the original canonical URL and opens/closes correctly. Portable source rebuild and local-link check passed.


## Revision 11 — readable navigation and accessibility
Main menu 17 px; language links 16 px; primary navigation targets 48 px. All 40 HTML documents scanned at 1280 and 320 CSS px: zero automatic WCAG A/AA violations after fixes. Synthetic text enlargement and spacing checks completed. Manual contrast and assistive-technology review remain; see revision-11-accessibility/ACCESSIBILITY-REVIEW.md in the project package.
