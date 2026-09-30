# Kabita Live — public-site coverage and project handoff

29 September 2026 · Revision 06

The prototype covers every public page type found through the journal’s navigation. It has 36 linked designs, plus the branding guide, proposal and editors’ HTML cheat sheet. This is template and browsing coverage, not a completed migration of every poem, biography or review. No live site changes were made.

## Evidence and scope

| Source | Observed public records | Treatment |
|---|---:|---|
| [Homepage](https://kabitalive.com/) | 16 poems in Issue 47: 5 Odia, 2 Hindi, 9 English | All titles and credits verified by opening their individual poem pages; three reader previews, remaining original links |
| [Contributor directory](https://kabitalive.com/contri.php) | 427 distinct profile URLs with visible name labels | Full A–Z/name-search index; preserve source IDs and native-script labels |
| [Archive](https://kabitalive.com/archive.php) | 47 issues, November 2022–September 2026 | Complete date/issue index, year filter and five year collections; three proposed-cover layouts |
| [Book reviews](https://kabitalive.com/book_review.php) | 8 listed articles | Complete listing and a sourced example reading layout |
| [Highlights](https://kabitalive.com/adv.php) | 4 announcements dated 2023–2024 | All remain explicitly historical; one optional detail-page design |
| [About](https://kabitalive.com/about.php) | Mission, email-only submissions/queries, moderated comments | Preserve the guidance in About, submissions, private contact and reader-response journeys |
| [Editor profile](https://kabitalive.com/contri-view.php?id=1) | Biography and one poem contribution | Concise stable biography, editorial role and contribution link |
| [Managing-editor link](https://kabitalive.com/contri-view.php?id=43) | Returned homepage twice when followed from the homepage | Profile design uses the verified role only; fuller biography/history pending verification |

The indexes are metadata snapshots observed through the rendered public pages. Private administration, unpublished work, database completeness and unlinked routes were not audited. A record’s presence in an index does not prove every external destination is healthy. No administrative access was attempted.

The directory includes repeated hidden biography fragments; only visible name labels and their profile URLs were used. Equal name strings with different IDs are retained as separate records. The archive lists Issue 2 out of chronological order; the new index sorts by verified issue number, without changing its date or legacy ID. Source ID is not the same as issue number.

## Complete route mapping

| Existing route or section | Proposed destination | Retained behavior |
|---|---|---|
| `/`, `index.php` | `index.html` | Homepage, current issue, three languages, writers, archive and signatures |
| `index.php?#chapters` | `poems.html` | Full current contents, title/name search, reading-language filters |
| `poemview.php?id=…` | Three `poem-*.html` samples | Script-specific reading, stanza/line shape, share, text size, night reading, response and correction |
| Current contributor carousel | `current-contributors.html` | All 16 names and profile paths in a stable list |
| `contri.php` and A–Z anchors | `poets.html` | 427 names with A–Z filtering, native-script search, empty state |
| `contri-view.php?id=…` | Three `poet-*.html` samples | Approved portrait slot, native/Roman names, biography and dated contribution library |
| `archive.php` | `archive.html`, `archive-2022.html` through `archive-2026.html` | All 47 records, year filters and cover/list choice |
| `archive-view.php?id=…` | `issue-47.html`, `issue-46.html`, `issue-45.html` | Issue identity, cover, contents, adjacent reading and archive return |
| `about.php` | `about.html` | Editorial mission, email submission path, comment moderation guidance |
| Editorial links | `editorial-team.html`, `editor-pradeep.html`, `editor-paresh.html` | Verified roles, bios where available and contribution path |
| Email-only poem submissions | `submit.html` | Existing email address, manuscript preparation, draft action |
| `index.php?#contact` | `contact.html` | Editorial/private queries, correction context and contact form preview |
| Homepage Feedback / Reviews | `feedback.html` | Public reader letters separate from book reviews and private correspondence |
| Poem comments | Reader response disclosure on each poem | Validation and moderation preview; no network submission |
| `book_review.php` | `reviews.html` | All eight listed review titles and credits |
| `bookview.php?id=…` | `review.html` | Reviewer separated from book creators; actual publisher-cover slot and verified metadata |
| `adv.php` | `highlights.html` | Four historical notices with original dates |
| Proposed announcement permalink | `highlight.html` | Optional detail layout; the public source currently groups notices on one page |
| Homepage Upcoming, currently empty | `upcoming.html` | No unverified date or poet list; suppress empty homepage block |
| Proposed utilities | `search.html`, `not-found.html` | Search, empty results and recovery routes |
| Review-only tools | `cover-studies.html`, `site-coverage.html`, `all-pages.html` | Artwork directions, audit map and navigable design inventory |

## What the new project should own

The separate Kabita Live project should contain only the magazine design, content model, verified source metadata and production implementation. The current poetry/music/video project does not belong in that repository. A self-contained source package is supplied, ready to move into a dedicated project; no app project, new chat, repository or deployment has been created automatically.

Decisions carried forward: retain **କବିତା ଲାଇଭ. / Kabita Live**, English-only Kabita Live masthead with a separate Odia signature, **ମାଟିର ମହକ। ମନର ସ୍ୱର।** throughout, existing English epigraph, equal care for three reading languages, photographic issue art, quiet poem interiors, dedicated writer profiles, smooth sharing and editor cheat sheet. Jhara is a superseded exploration.

## Production work in order

1. Inspect the actual publishing administration and export formats. Choose the implementation only after that inspection; public PHP URLs are not evidence of the CMS.
2. Create a stable content model: Work, Person, Issue, Contribution/Role, Review, Book, Announcement, Media/Credit and moderated Response. Keep native names, aliases, translation relationships and legacy IDs separately.
3. Export and reconcile all published records. Preserve poem text, stanza breaks, deliberate spacing, titles, credits, publication dates, issue order and historical covers. Import approved biographies and portraits. Reconcile native/Roman spelling variants with the editor.
4. Build these responsive templates over real content, with complete search and issue publishing. Keep original URLs working, or issue one-to-one permanent redirects after verification. Do not redirect missing content indiscriminately to the homepage.
5. Connect email/contact and moderated feedback. Preserve the source guidance that submissions and private queries go to email. Keep public book reviews distinct from reader feedback.
6. Add canonical metadata and per-work social preview images. The working share dialog does not itself create crawler-visible social cards. Test native sharing, clipboard failure, cancellation and legacy links on real phones.
7. Proofread all three scripts with editors. Test long/spatial poems, keyboard and screen-reader use, image descriptions, reduced motion, 200% zoom, empty states and failed submissions. Confirm rights and source credits for final covers.
8. Rehearse one complete monthly issue with the editor, including revision, scheduling, preview and recovery. Publish only after the production content and release are approved.

## Completion boundary

Finished now: visual identity and guide; editor cheat sheet; 36 linked page designs; public metadata indexes; three sourced writer histories; two editorial-profile layouts; realistic proposed covers; working local browsing, reading and sharing controls; mobile/desktop layout checks.

Still production work: full-text and portrait migration, final editorial copy/artwork approval, CMS integration, full-site search, durable preferences, actual forms/moderation, social-image generation at publish time, redirect testing, deployment and real-device/accessibility verification. No future publication date, content acceptance, public message delivery or complete migration is implied by this preview.


## Current UI and UX review — Revision 13
All 40 HTML pages were reviewed. Selective poetic headings, local filter counts/reset, archive reading paths and shared branding are updated. Navigation remains 17 px and language selection stays beside poem lists. See `revision-13-ui-ux/UI-UX-AUDIT.md` for individual page decisions and verification. Earlier revision notes document history.


## Revision 15 — Homepage artwork and arrival

The homepage now pairs its Odia signature with a large realistic Odisha-inspired scene: a rain-washed courtyard, indigo doorway, brass vessel and luminous fields. The caption is “Life, after rain.” This newly generated artwork replaces the faint decorative watercolor in the homepage opening. Text remains on warm paper beside the image; on mobile, the image follows the signature. The existing epigraph and Read this issue action remain. Inner-page headers retain their established artwork. Original and optimized files are in site/assets/home/; the prompt and verification are in revision-15-homepage/.


## Revision 16 — Section banners

Inner-page banners now use 60% text left and 40% artwork right, stacking on narrow phones. Fourteen new soft illustrations give the main sections their own imagery. Related pages share section art; poems and issues keep individual artwork. The homepage caption is LIFE AS IT IS, with a subtle Generated artwork credit. The editor guide and cheat sheet include the new layout rule. See revision-16-section-banners for prompts, provenance, page mapping and verification.


## Revision 17 — Shared header and quieter footer

All journal pages now use the homepage masthead without an extra inner-page tagline row. The footer has the Odia signature, three links and one author-credit line. Secondary journal links live on Our story; design-review links live on All page designs. See revision-17-header-footer/ for verification.


Revision 18: all 47 editions now have distinct generated cover artwork, responsive web versions and editable SVG covers. The attached Colours of home palette guides the interface and updated branding materials. A small shared leaf-and-water header separator appears on all 37 journal designs. Cover prompts and provenance are in revision-18-covers/manifest.json. Archive filtering and year galleries retain all verified issue dates and source links.
