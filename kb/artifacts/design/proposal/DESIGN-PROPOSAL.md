# କବିତା ଲାଇଭ. — brand and design proposal

Design strategy, identity and implementation brief · Retained-name edition · 29 September 2026

**Branding recommendation:** Retain **Kabita Live**, with the exact Odia wordmark **କବିତା ଲାଇଭ.** and its final dot. Pair it with **ମାଟିର ମହକ · ମନର ସ୍ୱର** as the brand signature, and keep **“Poetry is an echo, asking a shadow to dance.”** as the literary epigraph. Renew the presentation while preserving recognition, the domain, existing links, all three languages and the complete archive. No live changes have been published.

The selected direction retains the established name and applies the Literary Folio theme across 36 linked page designs. The companion [visual branding guide](brand-guide/BRANDING-GUIDE.html) shows the current logo family, both signatures, colour tokens, typography, imagery and social applications. The name and signature hierarchy reflect the agreed direction; final lettering, production artwork and interface copy still need editorial refinement. Short attributed excerpts and clearly marked placeholders illustrate layouts. No live website changes have been published.

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

**Brand signature:** “ମାଟିର ମହକ · ମନର ସ୍ୱର” **Retained literary epigraph:** “Poetry is an echo, asking a shadow to dance.” **Supporting descriptor:** “A monthly journal of poetry.” A separate utility line states “Odia · Hindi · English.”

### The theme on every page

**ମାଟିର ମହକ · ମନର ସ୍ୱର** is an operating principle for the whole magazine: grounded materials, human presence, warmth and room for the writer’s voice. The exact line leads the homepage hero and appears in every footer. A red-earth rule, warm paper, deliberate typography and a restrained watercolor edge carry it through inner pages. Full imagery stays outside the verse column. The theme is recognisable without repeating the same large illustration behind every page.

### Which language leads the identity?

**Use Kabita Live alone in the masthead.** The English name connects the three reading languages. The Odia signature **ମାଟିର ମହକ · ମନର ସ୍ୱର** carries the journal’s roots separately, leading the homepage hero, with its feeling carried by artwork and paper elsewhere. The footer does not repeat the signature. Preserve original scripts in poems and author names. The English epigraph has its own quiet placement.

Language selection belongs beside poem lists on Current issue, Poems and Search. Keep the main navigation at 17 px and local filter controls at 16 px, with 48 px targets. Do not add language controls back to the masthead.

### Selected direction — The Literary Folio

Warm paper, deep ink, restrained red earth and generous margins. The English masthead sits above a separate Odia signature; soft Odisha-inspired imagery frames an unpainted centre. The existing English epigraph has a separate quiet placement. A clear current-issue action follows the homepage masthead.

Use the illustrated treatment on the homepage and issue openers. Reader pages use compact branding and uninterrupted verse columns. Archive covers, full bylines, quiet rules and deliberate typography give the magazine a consistent editorial character. On mobile, the masthead compresses to bring the reading action closer.

The earlier Modern Review and Artist’s Issue routes remain exploratory references. They are not competing recommendations in this edition. A future special issue may commission distinctive art within the same identity and reading system.

References inform publishing patterns rather than visual imitation: [Poetry Foundation](https://www.poetryfoundation.org/) connects poems, poets and issues; [The Paris Review’s issue page](https://www.theparisreview.org/back-issues/256) makes cover art and a structured contents list part of one editorial object. Kabita Live should establish its own Indian, multilingual typographic voice.

## 4. Brand and logo system

Retain **Kabita Live**, which carries years of reader recognition. Use the English name alone in the masthead; retain **କବିତା ଲାଇଭ.** for Odia editorial references. Keep `kabitalive.com`, social account names and existing poem URLs. Introduce the refreshed logo, typography, artwork and page templates together, with no rename or “formerly” label.

### Recommended master: Kabita Live in English

Pair the typeset **Kabita Live** name with the leaf-and-stream symbol. Set the Odia signature separately, with enough space to read naturally. The existing English epigraph remains independent. Use Source Serif 4 for the wordmark; verify the signature’s Odia shaping with a fluent editor. Earlier Odia-led wordmark studies are archived explorations.

### Three coordinated assets

| Asset | Use | Proposed treatment |
|---|---|---|
| Primary English wordmark | Homepage, issue covers, publication signature | Kabita Live with the symbol; separate Odia signature |
| Compact masthead | Mobile and poem reader | Short horizontal form with the same weight and spacing; omit descriptor first |
| Leaf-and-stream mark | Favicon, social avatar, spine, end mark | Organic page/leaf forms, flowing negative space and one red-earth drop; simplify for small sizes |

The leaf-and-stream symbol suggests the movement of poetry and remains script-neutral across the three languages. The English wordmark carries the established name. Test a simplified one-colour version for small favicons; keep the full tagline for larger masthead placements.

**Construction rules:** let x equal one quarter of the symbol’s height and preserve at least x of clear space around the complete lockup. Start with a minimum full-lockup width of 360 CSS px / 75 mm, compact-lockup width of 180 CSS px / 40 mm, and symbol width of 24 CSS px / 6 mm. These are proposed review limits, pending actual-size proofing. Below 32 px, use the simplified one-colour mark without its small drop; a 16 px favicon still needs optical refinement. Never sacrifice the name or signature legibility to squeeze a logo into a header.

**Production deliverables:** outlined SVG and PDF masters; editable vector source; full-colour, ink-only and reversed versions; wordmark-only and symbol-only forms; 16/32/48px favicon exports; 180/192/512px app icons; social avatar; minimum-size sheet; usage rules; typeface licences and font inventory. The included SVGs are concept studies, not a trademark-cleared or fully outlined final identity.

## 5. Colour system

| Token | Hex | Role |
|---|---|---|
| Paper | `#F5EFDF` | Main reading surface |
| Ink | `#263C3C` | Body text and headings |
| Deep sea blue | `#125465` | Masthead alternative, strong navigation and cover fields |
| Laterite | `#963F28` | Selected state, editorial accent and primary action |
| Muted ink | `#655F51` | Dates, labels and secondary information |
| Pale paper | `#EAE1CD` | Inset panels and social cards |
| Paper rule | `#D2C6AC` | Nonessential dividers |

Use approximately 80–90% quiet paper, with ink and restrained accents occupying the remaining visual area. These are compositional guidelines, not a literal pixel quota. Monthly artwork can introduce additional hues; interface colours remain stable. Do not permanently assign a colour to each language.

Calculated contrast against Paper: Ink **10.61:1**, Sea blue **10.08:1**, Laterite **6.08:1**, Muted ink **5.16:1**. Paper rule is **1.43:1** and is appropriate only for decorative separators, not text, focus indication or the sole boundary of a control. Validate every hover, selected, disabled and dark appearance pairing separately. [W3C contrast guidance](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html).

Proposed dark reader: background `#1C292B`, text `#F3EADB`, muted text `#C0BCAE`, accent `#EEAA8B`. Keep issue artwork in its intended colours and test all dark-reader states before release. Dark appearance is a reader option, not a second brand identity.

## 6. Typography for three languages

| Script / use | Recommended starting point | Initial desktop sizing |
|---|---|---|
| Odia poem and editorial prose | Noto Serif Oriya | 24px / 1.8–2 line height |
| Odia navigation and compact labels | Anek Odia | 16–18px / 1.5 |
| Hindi poem and editorial prose | Tiro Devanagari Hindi | 24px / 1.8–2 |
| Hindi compact labels | Tiro Devanagari Hindi | 16–18px / 1.5 |
| English poem and prose | Source Serif 4 | 24px / 1.8–2 |
| English navigation and metadata | System sans-serif | 15–16px / 1.5 |

On phones, start poems at 20–22px, titles at 32–40px and metadata at 14–16px. On desktop, poem titles can be 44–60px. These values must be optically tuned with real content; scripts should feel equally prominent even when their numerical font sizes differ.

The official Noto project provides both serif and sans Odia families. Anek supports Odia, Devanagari and Latin within a coordinated family; it is a particularly useful headline and interface candidate. The font’s technical name contains “Oriya”; user-facing language labels should say “Odia” or “ଓଡ଼ିଆ”. [Noto Odia](https://notofonts.github.io/oriya/), [Anek by Ek Type](https://github.com/EkType/Anek), [Source Serif 4](https://fonts.google.com/specimen/Source+Serif+4), [Tiro Devanagari Hindi](https://www.tiro.com/fonts/tiro-devanagari-hindi).

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

**Primary navigation:** Current issue · Poems · Poets · Archive · Search. About, submissions and contact remain in the footer.

Keep **ଓଡ଼ିଆ | हिन्दी | English** filters beside the poem lists, outside the masthead. The homepage welcomes all three languages. Choosing a filter selects original work in that language; it does not translate a poem.

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

Give every writer a dedicated stable profile page, linked from every byline. Use a consistent approved portrait crop, native-script name, approved Roman alias, biography, writing languages and a complete contribution library grouped by year and issue. Include poems, reviews, translations and essays where verified, keeping each role and credit distinct. Add title search and year/type filters against real records. Publication counts must be calculated from verified relationships, not supplied as decorative numbers.

The updated examples import the contribution metadata visible on the three existing profiles: 4 works for Narmada Nilotpala, 23 for Sabita Singh Meera and 4 for Majrooh Rashid. Current sample poems open the new reader designs; earlier entries link to their original published pages. Full biography and portrait use remains subject to editorial approval. Do not require a portrait. A calm name-based placeholder is preferable to an unrelated stock photo. Search should match approved name variants without silently altering the displayed name.

### Archive

Offer cover grid and compact list, year and language filters, plus search. Sort by publication date, not a text representation of issue numbers or internal database IDs. Every cover includes a legible date and issue number outside the image. Retain every issue’s original bibliographic identity.

### Reviews, submissions and About

Reviews need a distinct template: review title, reviewer, reviewed book, author/editor, publisher, year and cover credit. Avoid the ambiguous single “author” label for both reviewer and book author.

Create a findable submissions page with accepted languages, file format, originality/translation requirements, editorial response expectations and an email action. Preserve email submissions initially; the existing About page explicitly directs poets to email. Submission portals can wait until volume justifies them. The editor supplies the rules—do not invent deadlines or promised response times.

About should separate mission, masthead, submission guidance and comment policy into readable sections. Give the editor’s literary perspective a short, prominent statement and a proper portrait if desired, without turning the homepage into a personal biography.

## 8. Artwork and visual culture

Commission one distinctive cover image per issue or reuse a small, permission-cleared library with strong art direction. Suitable approaches include contemporary drawing, printmaking, cut-paper composition, restrained photography and typographic covers. Let themes range across city life, labour, memory, intimacy, landscape and abstraction; do not reduce Odia identity to a checklist of cultural motifs.

Odisha’s artistic traditions can be a source for commissioned collaboration, with the artist named and the work contextualised. Do not label a generic generated pattern as authentic Pattachitra or Jhoti. Motifs belong in cover art or section transitions, sparingly; never behind verses.

Use distinctive realistic artistic cover images in a consistent 3:4 frame. Give each issue its own photographic or painterly-realistic composition: earth after rain, intimate human spaces, work, city life, landscape or another editorially chosen subject. Use commissioned or licensed photographs where available; generated concepts must be labelled and reviewed. Keep the exact bilingual masthead, signature, issue and date as real typeset layers, separate from the image. The cover should be visibly richer and more image-led than the quiet content inside. Do not repeat the soft header watercolor as every issue’s cover. Preserve historical original covers; new studies are proposals, not retrospective replacements.

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

The proposal is concrete enough to review without choosing technology first. The retained name and Literary Folio direction are now the basis of the design. Confirm final English lettering and Odia signature spacing; whether all three interface languages can be maintained; the cover-art budget and permissions process; the future of public comments; and who owns publication and maintenance.

My recommendation is **The Literary Folio**, with the established **Kabita Live** name, the Odia brand signature and existing English epigraph, the leaf-and-stream logo, warm paper and red-earth colour, one credited artwork per issue, and identical care for the three reading languages. The first design to approve should be a real poem page and its mobile version; the homepage follows from that reading standard.


## 14. Identity, poetic atmosphere and sharing

**Retain Kabita Live and use it alone in the English masthead.** Keep the Odia signature separate; preserve the exact Odia name କବିତା ଲାଇଭ. when used in editorial copy.

### Why retain the name?

Years of publishing give an established name familiarity and emotional value. The refresh should strengthen that recognition through typography, illustration and a more thoughtful reading experience. Jhara was an explored direction; it is no longer the recommended publication name.

### Two complementary poetic signatures

**Brand signature: ମାଟିର ମହକ · ମନର ସ୍ୱର** (“The fragrance of earth. The voice of the heart.”)

Use this Odia line in the homepage invitation and on branded social cards; omit it from the shared website footer. The user selected it as an essential part of the identity.

**Retained literary epigraph: “Poetry is an echo, asking a shadow to dance.”**

Keep this exact existing wording as the journal’s literary epigraph on the homepage, About page and spacious issue openers. It supplies continuity and an invitation across the three languages. It is not newly written brand copy.

Brand hierarchy: **କବିତା ଲାଇଭ.** as the principal name; **Kabita Live** as the Roman companion; the Odia brand signature paired with the identity. Give the English epigraph a separate, quiet placement. The compact logo may omit the signature inside the lockup, but the shared header retains the Odia signature on a separate line. The earlier alternative “ଅକ୍ଷରେ ଅକ୍ଷରେ ଜୀବନ।” is no longer an active recommendation.

### Refresh without a rename

Keep the domain, publication name, social account names and all existing poem links. No “formerly” label or domain migration is needed. Coordinate the refreshed masthead, colours, typography and sharing artwork at launch. This is a local design proposal; nothing has been published to the live site.

### Logo: a leaf carrying a stream

`kabita-live-symbol.svg` replaces the earlier three-line secondary mark with an original vector concept. Two ink-coloured organic forms suggest a leaf or opened page. The negative space bends like a stream, and a restrained red-earth drop completes the movement. It suggests writing, water and growth without pretending to reproduce an Odia letter or a traditional sacred symbol.

The symbol is paired with real typeset **Kabita Live**, never generated lettering. The wordmark remains readable when the artwork disappears. The small standalone symbol omits the tagline; create a simplified one-colour version for favicon testing before production. The supplied mark is a review concept; final spacing, optical adjustments and uniqueness review remain part of identity production.

### A poetic atmosphere with an Odisha connection

Use an airy watercolor edge composition: wetland reeds, a lotus bud, two birds and a small wooden boat. These connect to Odisha through a Chilika-inspired wetland setting, not through a collage of monuments. The illustration is interpretive, not a documentary depiction or claimed example of a named traditional craft.

Place the imagery at the outer edges of the homepage masthead and lightly in issue-opening or closing areas. Keep the name and signature in generous clear space. The poem column stays opaque and plain. Retain Odia, Hindi and English as equal reading choices.

“Floating” should first describe composition: detached, soft forms with abundant empty space. The current design stays still. Any future optional motion must honour reduced-motion preferences and avoid scroll hijacking or continuous movement beside a poem. If continuous ambient motion is later requested, provide a persistent pause control and pause when the masthead is off-screen.

The preview uses the generated transparent illustration without changing its content; a compressed WebP copy is supplied for web presentation. No source photography or approved character assets from the separate poetry-film project are used.

Cultural reference: [Odisha Tourism on Chilika and its birds](https://odishatourism.gov.in/content/tourism/en/experience/event/chilika-bird-festival-2026.html). Odisha's [palm-leaf art tradition](https://www.works.odisha.gov.in/en/odisha-tourism/palm-leaf-painting) could inform a future commissioned manuscript drawing; the current image does not claim to reproduce it.

### Sharing is a primary reader action

Keep a labelled Share action beside the reading controls and repeat it after the poem. It should be easy to find without covering the text. On narrow screens, controls wrap; a floating rail is unnecessary.

#### Mobile

One tap opens the device's native share sheet when supported. Provide the exact canonical poem link, full title and author. The reader chooses the app and recipient and completes the send. The website cannot guarantee which apps a device offers. If native sharing is unavailable, open the compact fallback panel immediately.

#### Desktop and fallback

Show WhatsApp, Facebook, email and Copy link with visible labels. Support the publication's other existing channels where their current share mechanisms are verified. LinkedIn or X can sit under More if the editors want them; avoid five repeated icon bars. Preserve the intended sharing capability, while replacing the current `#` placeholders with working actions. Social-profile links in the footer remain separate from sharing the current poem.

Copy link should copy the canonical URL and report success only when clipboard access succeeds. On failure, show a selectable URL. Cancelling a native share is a normal dismissal, not an error. Never display “Posted” or “Sent” merely because a share window opened.

#### What travels with the poem

- The complete title and exact author name, in the original script.
- Issue number and date, plus the canonical link to that poem.
- A well-typeset social preview image with the new identity and a quiet edge motif.
- A short excerpt only when the editor has approved its wording and use; do not automatically publish the whole poem in a graphic.

Production social card starting sizes: 1200×630 for link previews, 1080×1080 for square cards and 1080×1920 for optional story exports. The latter two are separately composed artwork, not automatic crops. Use server-generated or pre-rendered images with the selected script's real fonts; preserve title and author when they wrap. Always attach alt text where the destination supports it.

Instagram is not a generic webpage-link-share endpoint. Offer an approved card download or device file sharing where supported, with a caption and link the reader can use. Do not claim an Instagram post was made or guarantee image previews in every destination; platforms may cache or ignore supplied metadata.

#### Technical handoff and acceptance

Use HTTPS, feature detection for `navigator.share`, and `navigator.canShare` before file sharing. Invoke the native share only from the user's click. Provide fallbacks for unavailable APIs, restrictive browser policies, clipboard rejection and offline state. Serve title/description/image metadata in the initial response, use a public image URL, and avoid duplicating URL fields in the share payload. [MDN Web Share API documentation](https://developer.mozilla.org/en-US/docs/Web/API/Navigator/share).

Test on iOS Safari, Android Chrome and desktop browsers with and without native sharing. Verify every language, a long title, a multi-author credit, cancellation, successful copy, copy failure, back/close behaviour and actual link-preview rendering. Test the existing canonical URLs after migration. Record a share intent rather than claiming a completed external post in analytics.

The current page prototype opens a branded share panel. Copy link and Copy caption attempt a real clipboard copy only when the reader selects them, with a selectable-text fallback. Native sharing and external share destinations also require a reader action; opening them never means a post was sent. Production must add verified metadata and generated social-preview images.

## 15. Designs and branding handoff

The [visual branding guide](brand-guide/BRANDING-GUIDE.html) is the identity reference for this proposal. Its asset folder supplies full-colour, ink and reversed wordmark studies; a compact lockup; symbol variants; and machine-readable colour/type tokens. Wordmark SVGs retain editable text and require the named fonts; they are not outlined production masters.

The [page design index](site/all-pages.html) links all 36 responsive examples. See `site/PAGE-DESIGNS.md` for every page and `site/VERIFICATION.md` for completed checks and remaining implementation work. The guide includes title-only social-card compositions; final share-image exports and publishing metadata are production deliverables.

Retain the existing name, domain and original poem links. Introduce the refreshed identity as a visual renewal of Kabita Live, without a renaming campaign.

## 16. Editors’ daily reference

Use the one-page editor cheat sheet in `brand-guide/EDITORS-CHEAT-SHEET.html` and its companion PDF. It covers exact naming, both signatures, language hierarchy, the theme across every page, realistic cover art, writer profiles, typography, colour and sharing. The final checklist is designed for the monthly publishing routine. The updated cover gallery is `site/cover-studies.html`.


## 18. Complete public-page coverage — Revision 06

The expanded prototype now has **36 linked designs**, plus the visual branding guide, proposal and editors’ HTML cheat sheet. The [coverage map](site/site-coverage.html) connects the existing routes and sections to each design. Every public page type found through navigation has a corresponding treatment; unpublished/admin pages and database completeness were outside this audit.

The [writer directory](site/poets.html) includes all 427 visible source name/profile entries, with native-script search and A–Z filtering. The [archive](site/archive.html) includes all 47 issue records and five year collections. The [current issue](site/issue-47.html) lists all 16 verified titles and credits, and the [book reviews](site/reviews.html) list all eight public articles. These are complete public indexes, not a claim that every full poem, biography or article has been migrated.

New journeys include the [current contributors](site/current-contributors.html), [editorial team](site/editorial-team.html), individual editor profiles, [reader letters](site/feedback.html), forthcoming-issue empty state and historical announcement treatment. Public feedback stays distinct from book reviews and private correction requests.

The source About page confirms email-only submissions/private queries and delayed moderation of comments. The managing editor’s original profile link returned to the homepage in two in-site attempts; his role is retained, with biography and contributions pending verification. The editor’s Roman name varies between source locations, so the profile uses the homepage spelling pending editorial confirmation.

The prototype preserves original destinations where content has not been imported. The standalone project package contains editable source, local assets, evidence metadata, branding guide, cheat sheet and the complete production handoff. It can be moved into a dedicated Kabita Live project without the poetry/video project’s assets. No new app project or deployment has been created.

Sources: [archive](https://kabitalive.com/archive.php), [contributors](https://kabitalive.com/contri.php), [current issue](https://kabitalive.com/), [book reviews](https://kabitalive.com/book_review.php), [About](https://kabitalive.com/about.php), [highlights](https://kabitalive.com/adv.php).


## 19. Odisha as a felt presence — Revision 07

**ମାଟିର ମହକ · ମନର ସ୍ୱର** is the emotional brief for the whole journal. Let “earth” shape material, colour, light and sense of place; let “voice” shape typography, breathing room, humane language and the quiet around a poem. Repeating the line is only one part of the system.

Keep the three existing realistic cover studies. Where a meaningful connection is possible, commission or license images made in Odisha: the wetland edges of Chilika and Mangalajodi, a rain-dark courtyard or path, a lived-in threshold, cloth and its maker, an evening shore, or contemporary life in a town. The image should speak to the issue’s emotional world; avoid forcing a location onto an unrelated subject. A single intimate scene is preferable to a collage of regional symbols.

The [cover direction](site/cover-studies.html) now pairs the existing images with these future commissioning directions. Their present labels remain generated studies, not photographs of named places. A verified photograph receives its real location and photographer credit; commissioned art receives artist/inspiration credit; generated art is labelled Odisha-inspired. Odisha also includes contemporary and urban experience; do not confine its identity to picturesque rural nostalgia.

Across the shared pages, a leaf-and-water divider introduces a soft pause after headings, while warm paper, earth accents and the existing watercolor edge supply continuity. These marks are original abstract decoration, not a claimed traditional motif. Full imagery is reserved for covers and roomy openers; verse remains still and clear. No new automatic motion has been added.

References for future commissions: [Chilika and Mangalajodi](https://odishatourism.gov.in/content/tourism/en/discover/attractions/lakes-waterfalls/chilika-nature-camps.html), [Odisha arts and crafts](https://odishatourism.gov.in/content/tourism/en/discover/attractions/arts-crafts.html). These inform the art direction; no source photographs were copied.


## 20. Simple, poetic and connected — Revision 08

Every page should invite a person in, give them one clear next step and leave room for the words. The homepage now opens with the Odia signature and one Read this issue action; repeated oversized name blocks, the extra signature panel, motion button and redundant issue banner have been removed. Navigation is reduced to reading and discovery, with secondary journal links in the footer. The three language choices remain visible.

A compact shared header replaces the stacked English translation and utility rows. Design-review tools sit in a footer disclosure, keeping the reading experience clear. Reader sharing stays beside the reading controls; the repeated second share button has been removed. One understated divider and a quiet watercolor edge carry the poetic atmosphere. Covers retain their realistic imagery and Odisha art direction.

Connection comes from the poem, the named writer, a welcoming invitation and an easy way to respond or share. Avoid extra slogans, decorative counters, repeated calls to action, unnecessary panels, automatic movement and interruptions. Preserve exact credits, useful dates, honest preview notices and accessible controls.


## 21. UI and UX refinement — Revision 13

Preserve good poetic headings and all original poem titles, writer names, issue dates and book titles. Add warmth to the editorial framing: “The voices gathered here.”, “A voice across the pages.” and “Through the years.” Navigation, forms and filter labels stay direct. Local filters show a live result count and a Clear filters action; archived previews link directly to the original issue. The English masthead and separate Odia signature now match throughout the review documents. See revision-13-ui-ux/UI-UX-AUDIT.md for the page-by-page decisions and verification.


## 22. Illustrated openings — Revision 14

The visual signature now reads **ମାଟିର ମହକ · ମନର ସ୍ୱର** on one line, or the two phrases on separate lines without punctuation. This is a brand styling choice, not a change to the punctuation of published poetry.

Use one consistent site illustration to the right of inner-page introductions and as a quiet right-aligned footer echo. The existing Odisha-inspired wetland illustration supplies that site identity. Monthly covers remain distinct editorial works. Writer profiles retain their identity/portrait area, with the site illustration to the right. Issue openers place their own cover on the right.

The three sample poem pages now have individual generated editorial illustrations: a closed shop after rain, a rain-washed railway platform and an evening window. They mix contemporary painting with everyday regional materials, avoiding unverified claims about traditional art forms. They are proposed interpretations based on the available excerpts; editorial review should consider the complete poem. Place one artwork beside the title, not behind the words. Mobile layouts keep it small and above the full-width title; the verse remains an uninterrupted reading column.


## Revision 15 — Homepage artwork and arrival

The homepage now pairs its Odia signature with a large realistic Odisha-inspired scene: a rain-washed courtyard, sea blue doorway, brass vessel and luminous fields. The caption is “LIFE AS IT IS”. This newly generated artwork replaces the faint decorative watercolor in the homepage opening. Text remains on warm paper beside the image; on mobile, the image follows the signature. The existing epigraph and Read this issue action remain. Inner-page headers retain their established artwork. Original and optimized files are in site/assets/home/; the prompt and verification are in revision-15-homepage/.


## Revision 16 — A banner for each section

Inner-page openings use a 60/40 split: clear text on the left, a soft watercolor illustration on the right. Fourteen distinct section illustrations cover reading, writers, archives, correspondence and the other main journeys. Related pages share their section artwork. Each poem and magazine issue keeps its own art. On narrow phones the banner stacks, preserving readable headings. The shared footer watercolor remains.

The homepage caption is LIFE AS IT IS, followed by Generated artwork in a subtle warm grey. The brand guide and editor cheat sheet include the banner rule. Prompt records, the route map and verification accompany revision-16-section-banners.


## Revision 17 — Consistent masthead and quieter footer

All 37 journal designs now share the homepage masthead exactly, except the active navigation link. The extra inner-page Odia tagline row has been removed. The unique 60/40 section banners remain underneath.

The footer contains the Odia signature, three links (Our story, Send a poem, Contact), a small water-and-reeds accent and the existing author-credit statement. The repeated logo, English descriptor, publication descriptor, extra rules and disclosures are removed. Secondary journal links are grouped on Our story; design-review materials are grouped on All page designs.

The Odia theme remains in the homepage invitation, section artwork and footer. Navigation stays 17 px, and footer links retain 48 px targets.


## Revision 18 — Colours of home

The supplied reference guides ivory #F5EFDF, laterite #963F28, sea blue #125465 and hearth #78643A. These are interpreted digital palette values, not official Utkal Project specifications. Forty-seven distinct generated portrait artworks are paired with the verified November 2022–September 2026 editions. They are proposed new covers; original historical artwork and poems remain at their source. A small native SVG leaf-and-water ornament separates the shared masthead from every journal page. Full-size cover masters, optimized web copies, prompts and a numbered manifest accompany the project.


## Cover narratives and cultural range — revision 19

All 47 proposed covers now have original poetic stories and separate cultural notes. Ten artworks introduce Sambalpuri bandha, Puri gamucha, kendu woodland, Similipal, Deomali, Fakir Mohan Senapati, Pipili appliqué, Raghurajpur painting, Kantilo bell-metal and Konark. The loom cover also carries an explicitly imaginative Gangadhar Meher homage.

Use optional story disclosures in the archive and cover gallery, preserving a quiet first view. Sources support cultural context; stories are original editorial writing. Historical issue contents are not inferred from new covers.

Editors should compare the last six covers before commissioning the next: change the principal subject, viewpoint and emotional note; rotate craft, ecology, landscape, everyday life and literary voices. Avoid reducing Odisha to repeated rain, vessels and doorways. The detailed ledger and future personality directions are in revision-19-cover-stories.


## Paper texture and future-use artwork — revision 20

Warm ivory now has a restrained paper grain and faint fibre texture across journal pages. Texture stays beneath content and is disabled for night reading, forced-colour mode and print. Pipili Chandua is preserved unchanged for a future edition. Issue 34 returns to Rain on the tiles, with a matching narrative. The current collection contains 47 covers and stories; the reserved Chandua artwork is additional.


## Editors and design attribution — revision 22

The design credit appears only on Our Story. A dedicated Editors landing page introduces Pradeep Biswal and Paresh Kumar Pattnaik, with separate detailed profiles, selected books and source-linked portraits. Editors is part of the shared navigation. Biographies draw on the author’s website, Setu, a published review, Puri Literature Festival and Shalandi’s catalogue. Changing publication totals and unverified award dates are omitted. Photo sources are credited; public-reuse permission remains to be established before launch. The research ledger and portrait provenance are in revision-22-editors.


## Selected page surfaces and closing row — revision 27

Cotton paper at 16% is the shared background for general journal pages. Poem readers receive either monsoon or earth wash at 18%, assigned pseudorandomly from their persistent poem ID so the result stays consistent on return visits and rebuilds. Phone washes soften to 12.6%. Textures disappear in night reading, forced colours and print.

The footer is one horizontal row with the author ownership note on the left and Our story, Send a poem and Contact on the right. The small boat remains above the rule. On narrow screens the note and right-aligned links wrap without shrinking type. The repeated Odia signature is omitted. This supersedes earlier footer-signature instructions.


## Current typography — Noto Serif Oriya throughout

Use Noto Serif Oriya for all Odia headings, poems, writer names, cover signatures, labels and controls. Regular 400 is the default; Medium 500 is reserved for emphasis. Preserve natural character spacing and source wording. English retains Source Serif 4 and interface sans; Hindi retains Tiro Devanagari Hindi. The selected homepage signature is the Quiet literary treatment, with a 50px desktop cap, 1.3 line height and a quieter English translation. The official font and its SIL Open Font License are bundled with the prototype.


## Current English type decision and editor’s note

Cormorant Garamond Medium (500) is approved for the English masthead, magazine masthead, headings and large quotations. Source Serif 4 remains the English reading face; navigation and small interface labels retain the clear sans-serif. This supersedes earlier English masthead font specifications. The design balances sculpted literary character at display sizes with comfortable sustained reading. See [Editor’s typeface note](brand-guide/TYPEFACE-EDITOR-NOTE.md).

Noto Serif Oriya and Tiro Devanagari Hindi are the approved Odia and Hindi families. The earlier comparison studies remain historical design references; the selected families are now applied to the prototype.

## Locked multilingual typography — 29 September 2026

Odia: Noto Serif Oriya. Hindi: Tiro Devanagari Hindi Regular 400 upright, for titles and reading with natural letter spacing and 1.8–2 line height. English: Cormorant Garamond Medium 500 for display, Source Serif 4 for sustained reading. Keep interface controls in the clear existing sans serif. Hindi and Odia selections are approved, not pending comparison.
