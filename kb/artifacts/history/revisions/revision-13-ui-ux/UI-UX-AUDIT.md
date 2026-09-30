# Kabita Live — UI and UX review

29 September 2026 · Revision 13 · 37 page designs and 3 companion documents

## Editorial approach

Poetic invitations frame the experience; navigation and actions tell readers exactly what happens. Existing strong headings remain. Original poem titles, writer names, book titles, dates and issue identities are preserved. No new poem text or unverified biographical detail was added.

The Odia signature remains the emotional centre. English editorial headings are used selectively for the shared interface; no automatic translations or decorative new Odia claims have been introduced.

## Changes made

- Selective copy: “The voices gathered here.”, “A voice across the pages.”, “Through the years.”, “Room for another voice.” and “Follow a word. Find a voice.”
- Local language filters have a visible label, selected-state underline, live result count and Clear filters action. Hidden results consistently leave the layout, including empty-state recovery.
- Search now has a visible current-section state in the main navigation.
- Archived issue previews show their verified month and link directly to original issue 45/46 contents, alongside a path to the current issue.
- Writer breadcrumbs return to the directory. Poem metadata that says “Original published poem” now links to the poem, while the writer’s name links to their profile.
- Reading size reset restores the mobile 22 px default instead of forcing desktop size.
- The branding guide, editable logo studies, proposal, HTML editor reference and printable PDF now agree on the English-only masthead and separate Odia signature. Language controls stay outside the masthead.
- Main menu remains 17 px; local filters 16 px with 48 px minimum targets. No new decoration or automatic motion was added.

## Verification

All 40 HTML documents received a heading/content review, local-link check and automated layout/accessibility scans at 1280 and 320 CSS px. Both scans completed with zero automatic WCAG A/AA rule violations, zero page-level horizontal overflow, and no broken images or execution errors. Every document has one H1; local files and fragment destinations resolve.

Interaction probes exercised actual rendered controls through the local QA harness: 5 Odia, 2 Hindi, 9 English and 16 total results on all three filtered pages; no-result search and reset; 427-entry directory recovery; archive year filtering; all three writer contribution searches; and all three poem reader size and share controls. Writer histories restored 4, 4 and 23 entries. Mobile reader size restored from 32 px to 22 px; sharing retained each original poem URL. These are application-level checks, not a replacement for testing with readers.

Visual spot checks covered desktop search, writer profile, branding guide and mobile contributor layout. The printable editor reference was regenerated, rendered and visually inspected. The review did not alter the live site.

## Remaining production work

The prototype still needs complete poem migration, approved portraits/biographies, verified original cover permissions, connected submission/moderation services and production search. Automated contrast checks still mark some image/gradient overlays as incomplete; manual final-image contrast and assistive-technology review remain before launch. Native Odia/Hindi readers should review wording and font shaping. This review is not a WCAG certification, usability study or tagged-PDF accessibility certification.

## Page-by-page decisions

| Page | Current main heading | Decision |
|---|---|---|
| about.html | A familiar name. / A living literary home. | Kept the main invitation. Replaced the mission-section heading with “Room for another voice.” |
| all-pages.html | One identity. / A whole journal. | Kept: existing editorial tone or factual identity already suits the page. Reviewed shared header, reading hierarchy, next action and narrow-screen layout. |
| archive-2022.html | 2022 | Kept the year as the clear heading. Refined supporting line to “Month by month, the pages gather.” |
| archive-2023.html | 2023 | Kept the year as the clear heading. Refined supporting line to “Month by month, the pages gather.” |
| archive-2024.html | 2024 | Kept the year as the clear heading. Refined supporting line to “Month by month, the pages gather.” |
| archive-2025.html | 2025 | Kept the year as the clear heading. Refined supporting line to “Month by month, the pages gather.” |
| archive-2026.html | 2026 | Kept the year as the clear heading. Refined supporting line to “Month by month, the pages gather.” |
| archive.html | Every issue, / another beginning. | Kept the main heading. Refined sections to “An issue, an opening.” and “Through the years.” Verified year filtering. |
| branding-guide.html | A familiar name. / A more poetic presence. | Kept strong poetic chapter headings. Reconciled English masthead, Odia signature, local filters, logo assets and navigation sizing. |
| contact.html | Keep the conversation going. | Kept the conversational heading. Clarified required fields and preview-only submission. |
| cover-studies.html | A different world / on every cover. | Kept: existing editorial tone or factual identity already suits the page. Reviewed shared header, reading hierarchy, next action and narrow-screen layout. |
| current-contributors.html | The voices gathered here. | Changed heading to “The voices gathered here.” Names remain exact; corrected the section-heading level. |
| editor-paresh.html | Paresh Kumar Pattnaik | Kept: existing editorial tone or factual identity already suits the page. Reviewed shared header, reading hierarchy, next action and narrow-screen layout. |
| editor-pradeep.html | Pradeep Biswal | Kept the writer’s exact name. Contribution heading becomes “A voice across the pages.” Writer breadcrumbs link back to Poets where applicable. |
| editorial-team.html | At the editorial desk. | Kept the poetic framing and names. Corrected profile-card heading level. |
| editors-cheat-sheet.html | Kabita Live | Kept functional checklist headings. Updated English masthead, signature placement, filter placement, sizing and printable PDF. |
| feedback.html | Words that find / their way back. | Kept: existing editorial tone or factual identity already suits the page. Reviewed shared header, reading hierarchy, next action and narrow-screen layout. |
| highlight.html | Shalandi Books | Kept: existing editorial tone or factual identity already suits the page. Reviewed shared header, reading hierarchy, next action and narrow-screen layout. |
| highlights.html | Literary life, / carefully gathered. | Kept: existing editorial tone or factual identity already suits the page. Reviewed shared header, reading hierarchy, next action and narrow-screen layout. |
| index.html | ମାଟିର ମହକ। / ମନର ସ୍ୱର। | Kept: existing editorial tone or factual identity already suits the page. Reviewed shared header, reading hierarchy, next action and narrow-screen layout. |
| issue-45.html | Issue 45 | Kept issue identity; added verified month and a direct original-issue action. Secondary heading: “Open these pages.” |
| issue-46.html | Issue 46 | Kept issue identity; added verified month and a direct original-issue action. Secondary heading: “Open these pages.” |
| issue-47.html | Sixteen poems. / A shared horizon. | Kept “Sixteen poems. A shared horizon.” Added live count and local filter reset. |
| magazine-branding.html | A familiar name. / Room for the poetry. | Kept: existing editorial tone or factual identity already suits the page. Reviewed shared header, reading hierarchy, next action and narrow-screen layout. |
| not-found.html | This path has grown quiet. | Kept: existing editorial tone or factual identity already suits the page. Reviewed shared header, reading hierarchy, next action and narrow-screen layout. |
| poem-dokana.html | ଦୋକାନ | Preserved original poem title and author. Checked reading sizes, canonical sharing link and close behavior; standard size now restores the mobile default. |
| poem-drink.html | Drink | Preserved original poem title and author. Checked reading sizes, canonical sharing link and close behavior; standard size now restores the mobile default. |
| poem-kshanika.html | क्षणिका | Preserved original poem title and author. Checked reading sizes, canonical sharing link and close behavior; standard size now restores the mobile default. |
| poems.html | Find a poem. / Stay a little longer. | Kept the existing poetic invitation. Added local language label, live count, clear/reset and list hierarchy. |
| poet-dokana.html | Narmada Nilotpala | Kept the writer’s exact name. Contribution heading becomes “A voice across the pages.” Writer breadcrumbs link back to Poets where applicable. |
| poet-drink.html | Majrooh Rashid | Kept the writer’s exact name. Contribution heading becomes “A voice across the pages.” Writer breadcrumbs link back to Poets where applicable. |
| poet-kshanika.html | Sabita Singh Meera | Kept the writer’s exact name. Contribution heading becomes “A voice across the pages.” Writer breadcrumbs link back to Poets where applicable. |
| poets.html | A gathering of voices. | Kept “A gathering of voices.” Replaced database-style eyebrow with “The writers of Kabita Live.” Verified empty-state recovery. |
| proposal.html | କବିତା ଲାଇଭ. — brand and design proposal | Kept practical section titles for scanning. Removed superseded Odia-led masthead and persistent-language navigation guidance. |
| review.html | Toshali Anthology of / Love Poems 2026 | Kept: existing editorial tone or factual identity already suits the page. Reviewed shared header, reading hierarchy, next action and narrow-screen layout. |
| reviews.html | The reading continues. | Kept: existing editorial tone or factual identity already suits the page. Reviewed shared header, reading hierarchy, next action and narrow-screen layout. |
| search.html | Follow a word. / Find a voice. | Changed the invitation to “Follow a word. Find a voice.” Added current-section indicator, result feedback and reset. |
| site-coverage.html | Every kind of page. / One coherent journal. | Kept: existing editorial tone or factual identity already suits the page. Reviewed shared header, reading hierarchy, next action and narrow-screen layout. |
| submit.html | Send us your words. | Kept: existing editorial tone or factual identity already suits the page. Reviewed shared header, reading hierarchy, next action and narrow-screen layout. |
| upcoming.html | A new issue / is taking shape. | Kept: existing editorial tone or factual identity already suits the page. Reviewed shared header, reading hierarchy, next action and narrow-screen layout. |

Evidence: desktop-1280.json, mobile-320.json, journeys-320.json and page-decisions.json. Earlier accessibility evidence remains in revision-11-accessibility.
