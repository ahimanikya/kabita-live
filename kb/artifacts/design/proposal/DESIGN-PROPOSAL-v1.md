# Kabita Live — a contemporary literary magazine

Design strategy, identity and implementation brief · 29 September 2026

**Recommendation:** Build a calm, art-led monthly journal around excellent reading in Odia, Hindi and English. Retain the name, domain, editorial standing and full archive. Give each issue an identifiable visual presence and each poem an uncluttered, carefully typeset page.

This is a proposal, not a change to the live website. Logo studies, colours and layouts are exploratory. Existing poem titles and one short attributed excerpt illustrate layout; cover compositions are new design studies, not actual commissioned issue artwork. Final Indic lettering and interface copy need the editors’ review.

## 1. What I studied

The public homepage; September 2026 Issue 47; the full issue listing; an Odia poem and its contributor profile; the contributors index; the About page; and the book-review listing. I inspected rendered desktop pages, a narrow homepage view, navigation, visible content and some computed typography. I also consulted primary font documentation, accessibility guidance and established literary publications.

The site initially challenged fresh browser visits and some direct detail links returned to the homepage. In-site navigation subsequently opened the audited sections. This is an observed access behaviour worth reproducing in staging, not proof that all deep links are permanently broken. The narrow view showed a crowded, wrapping brand header; the browser’s viewport override did not consistently apply across tabs, so this is a qualitative mobile finding, not a complete device audit. No analytics, administration, database, hosting configuration, accessibility certification or laboratory performance report was available.

Your clarification confirms the proposal must preserve **Odia, Hindi and English**. The About page also describes original work and translations, including an ambition to bring regional-language writing to wider audiences. That multilingual purpose should become clearer in the design.

## 2. Diagnosis: valuable magazine, weak presentation

| Observed element | Effect on the experience | Proposed response |
|---|---|---|
| Salmon header, cursive Latin name, feather emblem, mock book in a hand, circles and several decorative treatments | The site feels assembled from a general promotional template; visual elements compete for attention | A coherent masthead, restrained colour, editorial rules and one substantial artwork per issue |
| The opening viewport is largely a general quotation and promotional imagery | A new visitor takes too long to reach this month’s writing | Put issue date, identity, language choices and a reading action together near the top |
| Poem cards truncate author names and some titles; counters repeatedly show zero | Readers lose useful information while low-value metadata remains prominent | Show full titles and author names; remove counters from discovery surfaces |
| Odia, Hindi and English appear in successive sections with inconsistent labels | The publication’s language scope is easy to miss | Explicit, always visible language navigation and consistently named sections |
| The sampled Odia poem uses a computed 16px generic `ui-serif`, 28.8px line height and approximately 340px text block on the inspected 1280px desktop view | The work appears small relative to the surrounding page, and fallback fonts may differ between devices | Deliberate script-specific fonts, larger text, calibrated reading measure and size controls |
| An empty upcoming section and dated highlights occupy homepage space | The page communicates less editorial freshness than the current monthly issue deserves | Render modules only when populated; retire expired announcements automatically |
| Contributor discovery uses a Latin A–Z index | Useful for Roman names, incomplete for readers searching in native scripts | Native-script names, aliases and search; retain A–Z as an optional browse method |
| Issue listing has weak cover identity and an older issue appears out of date order | The archive feels administrative rather than collectible | Sort by actual publication date and offer a consistent cover-and-date library |
| Public feedback occupies substantial space; social icons inspected point to `#`; visitor counter and old footer year remain visible | These details weaken finish and distract from the reading journey | Real links only, private editorial contact, restrained footer, separate moderated reader responses |
| The sampled poem document declares `lang="zxx"` | Its language is not correctly identified for assistive technology | Correct document and passage language tags: `or`, `hi`, `en` |

The successful existing elements are important: a regular monthly rhythm, established poets, a substantial issue archive, individual poem URLs, contributor relationships, related works and an existing moderation policy. Preserve and improve them.

Evidence: [homepage](https://kabitalive.com/), [sample poem](https://kabitalive.com/poemview.php?id=809), [archive](https://kabitalive.com/archive.php), [contributors](https://kabitalive.com/contri.php), [sample contributor](https://kabitalive.com/contri-view.php?id=82), [About](https://kabitalive.com/about.php), [book reviews](https://kabitalive.com/book_review.php). Captured views are in the accompanying evidence folder; see its index for limitations.

## 3. Positioning and creative direction

**Working positioning:** An independent monthly home for poetry across Odia, Hindi and English, rooted in a living literary community.

**Personality:** thoughtful, intimate, assured, contemporary and generous. Avoid institutional stiffness, luxury-brand affectation and social-feed bustle. Let the editor’s taste be visible in selection, sequencing, introductions and art choices.

**Suggested descriptor:** “A monthly journal of poetry.” A secondary line can state “Odia · Hindi · English.” This is proposed copy, not a claim about the magazine’s current tagline.

### Route A — The Literary Folio — recommended

Warm paper, deep ink, a restrained red-earth accent and generous margins. A substantial Odia masthead sits with a smaller Roman-script name. An asymmetrical first screen pairs the current issue with a flat, artist-designed cover. Fine rules, large poem titles and a composed table of contents create the impression of a cared-for publication.

This direction suits an established poet’s magazine and can remain recognisable while monthly artwork changes. Warmth comes from material colour and typography; no paper texture sits behind poem text.

### Route B — The Modern Review

Cool paper, midnight blue and a more assertive Roman masthead accompanied by Odia. A compact issue banner leads into a structured, three-language contents layout. Less cover-led, more immediately useful to frequent readers who want to scan titles.

This is a credible alternative if the editor prefers a cosmopolitan review with less of a printed-folio character. The core reader page remains quiet in both routes.

### Route C — The Artist’s Issue — occasional special edition

A larger commissioned artwork and more experimental cover composition, contained within the same navigation and reading system. Appropriate for an anniversary, thematic issue or artist collaboration. Do not make each monthly issue a bespoke web-design project.

References inform publishing patterns rather than visual imitation: [Poetry Foundation](https://www.poetryfoundation.org/) connects poems, poets and issues; [The Paris Review’s issue page](https://www.theparisreview.org/back-issues/256) makes cover art and a structured contents list part of one editorial object. Kabita Live should establish its own Indian, multilingual typographic voice.

## 4. Brand and logo system

Keep **Kabita Live** and `kabitalive.com`. Avoid introducing a new name that sacrifices recognition. Standardise spelling and spacing across the masthead, browser title, social profiles and email signature.

### Recommended master: an Odia-led wordmark

Set **କବିତା ଲାଇଭ** as the expressive primary line, with **Kabita Live** as the supporting line. Remove the trailing ellipsis. Use a compact vermilion point as punctuation, not a blinking live-status dot. The wordmark should feel grounded and clear, not ornamental or mechanically distorted.

The supplied study uses a real Odia typeface as its starting point. Final production should involve an Odia lettering specialist refining rhythm, joins, spacing and balance. Do not reshape characters to fit Latin lettering conventions. This is a refinement commission, not permission to alter spelling.

### Three coordinated assets

| Asset | Use | Proposed treatment |
|---|---|---|
| Primary bilingual wordmark | Homepage, issue covers, publication signature | Large Odia line, smaller Roman name, single accent point |
| Compact masthead | Mobile and poem reader | Short horizontal form with the same weight and spacing; omit descriptor first |
| Verse mark | Favicon, social avatar, spine, end mark | Three unequal horizontal strokes: the rhythm of a stanza; one accent point may be omitted at small sizes |

The verse mark is deliberately script-neutral so it can represent the whole publication. It is a secondary identifier; the wordmark carries the distinctive name. The alternative monogram is an Odia **କ** in a simple square field. Compare recognition at small sizes before choosing one favicon.

**Construction rules:** allow clear space at least equal to the height of the small Latin line; never place the mark on busy artwork without a solid quiet field; use a single colour for small reproduction; start testing the compact mark at 16, 24 and 32px. Full lockup minimum width is a testing question, initially 180px. Mobile headers must accommodate menu and search without squeezing the wordmark.

**Production deliverables:** outlined SVG and PDF masters; editable vector source; full-colour, ink-only and reversed versions; wordmark-only and symbol-only forms; 16/32/48px favicon exports; 180/192/512px app icons; social avatar; minimum-size sheet; usage rules; typeface licences and font inventory. The included SVGs are concept studies, not a trademark-cleared or fully outlined final identity.

## 5. Colour system

| Token | Hex | Role |
|---|---|---|
| Paper | `#F6F1E7` | Main reading surface |
| Ink | `#202923` | Body text and headings |
| Deep indigo | `#263D4B` | Masthead alternative, strong navigation and cover fields |
| Red earth | `#A54232` | Selected state, editorial accent and primary action |
| Muted ink | `#66675F` | Dates, labels and secondary information |
| Paper rule | `#D9D1C3` | Nonessential dividers |

Use approximately 80–90% quiet paper, with ink and restrained accents occupying the remaining visual area. These are compositional guidelines, not a literal pixel quota. Monthly artwork can introduce additional hues; interface colours remain stable. Do not permanently assign a colour to each language.

Calculated contrast against Paper: Ink **13.30:1**, Indigo **10.08:1**, Red earth **5.45:1**, Muted ink **5.08:1**. Paper rule is **1.35:1** and is appropriate only for decorative separators, not text, focus indication or the sole boundary of a control. Validate every hover, selected, disabled and dark appearance pairing separately. [W3C contrast guidance](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html).

Proposed dark reader: background `#19221F`, text `#EEE9DE`, muted text `#BCB8AD`, accent `#E6A38E`. Keep issue artwork in its intended colours and test all dark-reader states before release. Dark appearance is a reader option, not a second brand identity.

## 6. Typography for three languages

| Script / use | Recommended starting point | Initial desktop sizing |
|---|---|---|
| Odia poem and editorial prose | Noto Serif Oriya | 22px / 1.8 line height |
| Odia navigation and compact labels | Anek Odia | 16–18px / 1.5 |
| Hindi poem and editorial prose | Noto Serif Devanagari | 22px / 1.8 |
| Hindi compact labels | Anek Devanagari | 16–18px / 1.5 |
| English poem and prose | Source Serif 4 | 21px / 1.65 |
| English navigation and metadata | System sans-serif | 15–16px / 1.5 |

On phones, start poems at 20–22px, titles at 32–40px and metadata at 14–16px. On desktop, poem titles can be 44–60px. These values must be optically tuned with real content; scripts should feel equally prominent even when their numerical font sizes differ.

The official Noto project provides both serif and sans Odia families. Anek supports Odia, Devanagari and Latin within a coordinated family; it is a particularly useful headline and interface candidate. The font’s technical name contains “Oriya”; user-facing language labels should say “Odia” or “ଓଡ଼ିଆ”. [Noto Odia](https://notofonts.github.io/oriya/), [Anek by Ek Type](https://github.com/EkType/Anek), [Source Serif 4](https://fonts.google.com/specimen/Source+Serif+4), [Noto Serif Devanagari](https://fonts.google.com/noto/specimen/Noto+Serif+Devanagari).

**Poetry-specific rules:**

- Preserve authored line breaks, stanza gaps, indentation, punctuation and spelling. Typography must never silently rewrite a poem.
- Left-align the default reading text. Preserve intentionally centred or spatial poems as an explicit editorial exception.
- Never justify verse or use arbitrary letter-spacing on Odia or Devanagari. Do not manufacture italics for scripts whose selected font lacks them.
- Long lines should wrap with a modest hanging continuation indent. Never shrink the entire poem to force one long line to fit.
- Start with a maximum reading column of 640–720px and tune by script and poem; avoid treating Latin `ch` as a reliable measure of Odia character count.
- Offer normal, large and extra-large reading sizes. Browser zoom remains enabled. Test at 200% zoom and a 320 CSS-pixel viewport.
- Use actual Unicode text; do not render poems as images. Preserve original text alongside any search-normalised copy.
- Self-host licensed production font files, load only the scripts and weights required for the page, and check shaping after subsetting. Do not discard characters needed for conjuncts.

## 7. Information architecture and language behaviour

**Primary navigation:** Current issue · Poems · Poets · Archive · About. Place Reviews within the Poems/editorial area or expose it as a sixth item if readership warrants it. Search and Submit are clear utilities. Contact, editorial policy, corrections and privacy belong in the footer and relevant pages.

Provide persistent **ଓଡ଼ିଆ | हिन्दी | English** choices labelled as reading-language filters. The initial homepage shows all three languages, with Odia first and each section immediately discoverable. A reader can select one language and retain that preference. An explicit URL or shared poem always wins over a saved preference.

Distinguish **content language** from **interface language**. Choosing Hindi poems must not imply every work has been translated. Phase one can retain a concise shared English navigation with native-script language labels. If the editor can maintain reviewed interface translations, add localised navigation for all three languages. Never claim a translated edition exists merely because a language button exists.

**Translation relationships:** Record original language, translator, source work and publication rights. Offer “Read the translation” only when a linked, approved version exists. Side-by-side reading is a later enhancement; on phones, use clear version switching.

### Homepage, in reading order

1. Compact masthead and navigation, with language choices visible without opening a menu.
2. Current issue: month, year, issue number, artwork, brief editorial introduction and one “Read this issue” action. Avoid inventing themes for existing issues.
3. A clearly labelled selection from each language, with complete poem titles and bylines. Editors choose the order; popularity counters do not.
4. Short editor’s note with a link to the full note, only when supplied.
5. A small contributor selection and link to all poets.
6. Three previous issues with recognisable covers, dates and issue numbers.
7. One monthly issue-notification invitation and a clean footer.

On phones the masthead, current issue and a clear reading action should fit within roughly the first screen. Artwork follows rather than pushing every poem far down the page. Use no auto-advancing carousel.

### Current issue

A permanent issue URL, cover credit, publication date, editorial note and complete contents. All languages are visible as sections by default; filters can narrow them. Preserve the editor’s intended sequence. Include previous/next issue links. Offer a PDF only if the editorial team produces and proofreads a real accessible edition; an HTML issue is the primary reading experience.

### Poem page — the most important template

Start with a compact masthead, breadcrumb back to the issue, poem title, linked byline and issue metadata. Place text-size and appearance controls in one quiet row. Bring the opening verse into view early. Keep the text column free of sidebar advertising, social buttons and author portraits.

After the poem: a small end mark; copyright and translation credit; a concise author biography; previous/next poems in the same issue and language; related work by the author; a discreet share-link action. Reader responses may open below this material. No compulsory account to read.

Keep the existing moderation model but explain the pending state after submission. Separate literary responses from correction requests. A correction goes privately to the editor with the poem URL attached; it does not become a testimonial on the homepage.

### Poet page and directory

Use a consistent portrait crop, native-script name, optional Roman alias, short biography, languages and published work grouped by year or issue. Do not require a portrait. A calm name-based placeholder is preferable to an unrelated stock photo. Search should match approved name variants without silently altering the displayed name.

### Archive

Offer cover grid and compact list, year and language filters, plus search. Sort by publication date, not a text representation of issue numbers or internal database IDs. Every cover includes a legible date and issue number outside the image. Retain every issue’s original bibliographic identity.

### Reviews, submissions and About

Reviews need a distinct template: review title, reviewer, reviewed book, author/editor, publisher, year and cover credit. Avoid the ambiguous single “author” label for both reviewer and book author.

Create a findable submissions page with accepted languages, file format, originality/translation requirements, editorial response expectations and an email action. Preserve email submissions initially; the existing About page explicitly directs poets to email. Submission portals can wait until volume justifies them. The editor supplies the rules—do not invent deadlines or promised response times.

About should separate mission, masthead, submission guidance and comment policy into readable sections. Give the editor’s literary perspective a short, prominent statement and a proper portrait if desired, without turning the homepage into a personal biography.

## 8. Artwork and visual culture

Commission one distinctive cover image per issue or reuse a small, permission-cleared library with strong art direction. Suitable approaches include contemporary drawing, printmaking, cut-paper composition, restrained photography and typographic covers. Let themes range across city life, labour, memory, intimacy, landscape and abstraction; do not reduce Odia identity to a checklist of cultural motifs.

Odisha’s artistic traditions can be a source for commissioned collaboration, with the artist named and the work contextualised. Do not label a generic generated pattern as authentic Pattachitra or Jhoti. Motifs belong in cover art or section transitions, sparingly; never behind verses.

Use flat cover compositions in a consistent 3:4 frame. Maintain separate crops for issue cover, homepage landscape placement and social announcement rather than cutting off essential artwork automatically. Avoid faux 3D book mockups, glossy gradients, floating clip-art feathers and a different illustration on every poem card.

Portraits should share framing and scale, with mild exposure correction and original identity preserved. Do not invent author photographs. Credits and permission records live with each asset.

## 9. Components and interaction standards

Use a 12-column desktop grid inside a maximum 1200px content area, with 24–32px gutters. Mobile uses one column, 20–24px outer margins and consistent 8/16/24/32/48/64px spacing increments. These are starting tokens, adjusted in the prototype for real script dimensions.

Essential components: masthead; mobile menu; language filter; issue cover; issue header; poem list row; contributor byline; reading toolbar; stanza block; author biography; archive filter; search result; empty result; loading state; error page; moderation confirmation; submission guidance; newsletter form; footer.

Prefer rules and space to repeated elevated cards. Cards are appropriate for issue covers, not every sentence. Use modest or square corners. Buttons have clear labels and generous touch targets, ideally 44px. Essential information must not depend on hover or colour alone. Motion is brief and functional; respect reduced-motion preferences.

Search accepts titles, poet names and poem text in all three scripts. Begin with reliable Unicode matching and editorial aliases; evaluate transliterated matching against real names before promising it. Empty results retain the query and offer language reset and poet browsing.

Accessibility target is WCAG 2.2 AA: semantic heading order, real links/buttons, visible keyboard focus, skip-to-content, form labels and errors, correct language tags, decorative image handling and screen-reader checks. Logo exceptions do not excuse inaccessible navigation. [W3C reflow guidance](https://www.w3.org/WAI/WCAG22/Understanding/reflow.html).

## 10. Editorial system and maintenance

Choose the publishing platform after inspecting the current administration and export options. Public `.php` URLs do not identify the underlying CMS. A redesign may be possible on the existing backend if it safely supports structured content, revisions, reliable backups and maintainable templates.

If a replacement is needed, a carefully configured WordPress build is a practical shortlist candidate for a small editorial team. It supports distinct content types and revisions; its suitability depends on the actual editorial workflow and maintenance owner. Avoid selecting a complex headless stack solely for fashion. [WordPress content-type documentation](https://wordpress.org/documentation/article/what-is-post-type/).

**Core records:**

| Record | Required fields |
|---|---|
| Poem | Stable ID, title, language, exact stanza/line structure, poet relation, issue relation, sequence, publication status/date, credits and permissions |
| Poet | Stable ID, preferred name, native-script and approved Roman aliases, biography, optional portrait and credit |
| Issue | Number, month/year, actual publication date, editorial note, cover, artist credit, ordered contents |
| Translation | Original-work relation, target language, translator relation, source and permissions |
| Review | Reviewer, reviewed book metadata, body, language, issue where applicable |
| Media | Original file, derivatives, alternative text, creator, rights and usage scope |

Monthly workflow: receive submissions → edit → confirm exact text and credit → place in issue → preview desktop/mobile → approve → schedule or publish the complete issue → send one issue announcement. A draft issue must not appear in public navigation or search. Publication should not leave half an issue visible if one step fails.

Build content types independently from visual templates. Supply an editor guide, reusable cover/social templates, named maintenance ownership and a rehearsed backup/restore process. Keep optional homepage modules off when empty. New visual elegance must not create a monthly burden of manual layout work.

## 11. Migration and discoverability

Inventory the database, files and public URLs before estimating migration effort. Export and back up the original site. Count poems, poets, issues, reviews and media by language; do not infer counts from numeric IDs or the current issue number.

Preserve original text and author relationships. Review imported stanza breaks against source pages, including poems with unusual spacing. Do not auto-correct spelling or silently merge similarly named poets. Obtain editorial decisions for duplicate records and published contact information.

Create an explicit old-to-new URL map. Existing links such as `poemview.php?id=809` should continue to resolve to the exact work, either unchanged or through a permanent redirect. Do not redirect every old link to the homepage. Preserve inbound links from social media and search.

Use concise page titles, original-language descriptions, canonical URLs, a sitemap, social sharing images and appropriate structured metadata. Apply language alternates only to actual equivalent pages; unrelated poems in different languages are not translations. Keep the existing domain.

Performance goals for implementation: readable text available without animation delays; responsive image sizes; lazy loading below the first screen; limited font weights; no decorative hero video. Target Core Web Vitals in their “good” ranges and verify with real measurements after launch. No current performance score is claimed in this proposal.

## 12. Priorities, effort and acceptance

### First release — essential

Identity, typography and colour; homepage/current issue; three-language poem reader; contributor pages; archive and search; reviews; About/submissions/contact; reliable issue publishing; migration/redirects; mobile and accessibility checks; share previews; editor documentation.

### Second release — useful after the foundation works

Monthly opt-in email alerts, author recordings where rights and files exist, translation links, reader bookmarks without compulsory registration, selected archive collections and refined discovery. Add features only with an editorial owner.

### Defer

A native app, public follower counts, gamified reactions, AI-generated poem summaries, autoplay audio, elaborate animations, an always-on news feed and an online submission portal without demonstrated need.

**Planning estimate, not a vendor quote:** approximately 6–8 calendar weeks with one designer, one developer and a responsive editor, assuming exportable content and no major backend repair. Allow roughly 25–40 person-days across discovery/identity (4–6), template design/prototype (5–8), implementation (8–12), migration (4–7), and testing/handover (4–7). These activities overlap; archive cleanup and missing permissions can extend the schedule. Obtain a scoped fixed quote after the content inventory. Reserve part of the budget for recurring art, maintenance and editorial support, not only the initial launch.

| Acceptance area | Evidence required before launch |
|---|---|
| Reading | Editors approve sample poems in each script, long lines, stanza gaps and unusual formatting |
| Mobile | No header collision or page-wide horizontal overflow at 320, 390, 768 and 1280 CSS pixels; controls remain usable with zoom |
| Accessibility | Keyboard journey, visible focus, contrast states, language tags and screen-reader checks |
| Archive | Imported counts reconcile; every issue and author relation is checked; date ordering is correct |
| Existing links | Complete URL inventory tested against the migration map; no generic homepage fallbacks |
| Editorial operation | Editor independently prepares and publishes a test issue, then restores a revision |
| Sharing | Each language produces legible title, author and issue previews |
| Reliability | Backups and rollback rehearsed; draft content remains private; empty modules stay hidden |

Baseline reader behaviour before launch, then compare completed issue-to-poem journeys, next-poem use, archive discovery, search success and returning readers over subsequent issues. Avoid treating time-on-page alone as proof of reading quality. Success for the editor is equally concrete: fewer formatting corrections and no developer needed for a normal monthly issue.

## 13. What the editor needs to decide

The proposal is concrete enough to review without choosing technology first. Confirm the preferred visual route; the Odia/Roman masthead balance; whether all three interface languages can be maintained; the cover-art budget and permissions process; the future of public comments; and who owns publication and maintenance.

My recommendation is **The Literary Folio**, with an Odia-led bilingual wordmark, a script-neutral secondary mark, warm paper and red-earth colour, one credited artwork per issue, and identical care for the three reading languages. The first design to approve should be a real poem page and its mobile version; the homepage follows from that reading standard.
