---
type: "Project record"
title: "Kabita Live website rulebook"
---

# Kabita Live website rulebook

Version 1.1 · 5 October 2026 · Maintained for Ahimanikya Satapathy, editors and future contributors working with AI.

Use this rulebook when creating a page, adding an edition, changing a shared component or preparing a release. It brings the journal’s established decisions into one working reference. The aim is a welcoming literary publication whose poetry, people and practical actions stay clear.

This is a consolidation of approved decisions and current implementation, not a redesign. A later explicit user instruction takes precedence within its scope. Follow the current rule below over a superseded historical example; retain the earlier record as history. Continue already-authorized work without repeating approval requests. New design directions and publication still follow the actual authorization for the task.

Start each page change with the [page checklist](../review/new-page-checklist.md). Record only relevant checks, with evidence and explicit reasons for anything not applicable. Counts and rollout status belong in the live catalogue and dashboard, not in permanent rules.

## 1 Give every page a clear purpose

**PAGE-01** Identify the page family, reader’s purpose and primary action before designing. Reuse its existing builder and shared components. Change source templates or data, then regenerate; a hand-edited output page will be lost on the next build.

**PAGE-02** Use direct labels for actions: Read this edition, Find a poem, Poets, Past editions, Contact the editors and Send a poem. Poetic language can introduce literature; it must not obscure a search field, form, link or result. Counts, issue dates, publication order and contributions come from the catalogue.

**PAGE-03** Do not add a control merely to explain decoration or internal production. Keep artwork research, prompts, audits and provenance in the KB and appropriate central credits. Avoid repeated headings, redundant navigation and decorative controls that compete with reading.

| Page family | Keep in the page | Sharing image |
|---|---|---|
| Home | Current edition, approved signature, one calm opening image, reading action, featured poems and editors | Stable courtyard image, regardless of the visitor’s selected homepage view |
| Edition | Correct issue/date, its own cover and cover story, publication-order contents, reader tools | That edition’s cover artwork |
| Illustrated poem | Exact verse and attribution, assigned illustration, reader tools, edition context and responses | The poem’s illustration, never its small byline portrait |
| Text-led poem | Deliberately quiet opening, verse and the same reader tools and responses | Its own edition’s cover artwork; retain the text-led reading page |
| Poet or editor profile | Source-checked biography, existing portrait, attributed quotation and contribution links | The full portrait shown on that profile |
| Search, directory, archive, contact and submissions | Compact, text-led opening; search, browsing or form action arrives promptly | Its own section art where present, otherwise the journal fallback |
| Our Story | Journal story, acknowledged contributors and consolidated credits | Its own section artwork |
| Editorial essay | Supplied prose and attribution where provided, purposeful lead illustration, captions, source links and accessible versions of data graphics | Its own lead illustration, marked `article-lead`; article description and article metadata |

For an unavailable poem, missing image or exceptional utility page, use the journal fallback and record the reason. Do not invent content or borrow an unrelated poet’s portrait. Existing archive entries and intentionally excluded book-review pages must not be presented as newly completed publication content.

Evidence: [naturalness decisions](../records/poetic-natural-variety-2026-10-03.json), [homepage restraint](../records/home-artwork-restraint-2026-10-04.json), [sharing implementation](../records/social-previews-2026-10-04.json).

## 2 Preserve identity and readable typography

**DESIGN-01** Reuse approved tokens and type families. English display uses Cormorant Garamond, sustained English reading uses Source Serif 4, Odia uses Noto Serif Oriya, and Hindi uses Tiro Devanagari Hindi. Keep Indic shaping upright and natural; do not introduce synthetic bold, slant or letter spacing. Retain local fonts and licences.

**DESIGN-02** The website masthead keeps the existing symbol and Cormorant 500. Magazine covers use the separately approved text-only Cormorant 600 masthead. Do not confuse these decisions. Preserve the English-only Kabita Live name and approved Odia signature. Preserve the one-line signature on social artwork; other placements follow their approved template.

**DESIGN-03** Use the shared paper, ink, sea, laterite and muted colours by their existing roles. Keep dark-mode contrast and its texture-free reading surface. Retain the approved reading sizes, stanza spacing, browser-managed enlargement and responsive hierarchy. Do not reduce legibility to squeeze a long title into a fixed box.

**DESIGN-04** Use the existing single-ink icon family. Familiar controls need a clear accessible name and at least the existing 44px target; do not shrink larger approved navigation targets. Cultural motifs need meaning and breathing room. A mark beside every heading is not required.

Detailed tokens and placement exceptions remain in the [design system](../artifacts/design/brand-guide/DESIGN-SYSTEM.md). See the distinct [website](../records/website-masthead-a-selected-2026-10-04.json) and [cover](../records/cover-masthead-b-publication-2026-10-04.json) decisions.

## 3 Make artwork purposeful and preserve its history

**ART-01** Read the actual poem before assigning or creating its illustration. Choose an emotional relationship, not a collage of every noun. Artwork stays attached to its intended poem or edition; no random poem-image rotation. Do not reuse a previous issue’s cover as a new issue’s identity.

**ART-02** For editions, continue the approved direction of roughly three poem-informed interior artworks and suitable text-led openings. This is an editorial target, not a quota. Existing purposeful artwork may remain. A sharing image does not require adding visible artwork to a text-led poem.

**ART-03** Apply Human Natural / Poetic Natural when generating literary art: believable light and materials, selective detail, varied composition and breathing room. Preserve cultural meaning and the original medium. Watercolor should retain its painted edges; do not automatically turn it into a photograph. Added dirt, grain, gloom and clutter do not make an image more human.

**ART-04** Portrait edits require an identified source and likeness comparison. Preserve identity, pose, expression and source limitations. Do not invent missing faces. Existing generic placeholders must remain clearly described as generic artwork, not portraits based on a photograph.

**ART-05** Preserve originals and all candidates. Save versioned masters, exact prompts, source/output hashes, placement rationale and the actual review result in the KB. Use only the generation method authorized for the task. A failed or uncertain image remains held; it is not complete merely because a file exists.

**ART-06** Home selects among courtyard, field, water and bridge on each fresh page load, excluding the last view when session storage is available. Back/forward cache restores the existing view; artwork stays still while reading. No slideshow, timer, artwork buttons or animation. Palm and street studies are preserved outside that selection. Inner artwork is borderless; retain the approved homepage keyline and portrait frames. Keep imagery uncropped at its intended aspect ratio and provide responsive derivatives.

Evidence: [edition strategy](../records/edition-art-rollout-2026-10-04.json), [homepage selection](../records/home-curation-2026-10-04.json), [portrait refinement](../records/portrait-human-natural-2026-10-03.json), [generic placeholders](../records/generic-portrait-placeholders-2026-10-04.json).

## 4 Give every public page an intentional sharing preview

**SHARE-01** Each exported reader page must contain one static Open Graph image association, matching Twitter card metadata, a useful title and description, descriptive image alt text and its canonical page URL. Put these in the initial HTML head; sharing crawlers must not depend on browser scripts, consent clicks or sign-in to discover them.

**SHARE-02** Apply the page-family mapping above. Use a full portrait rather than a byline thumbnail. Never allow a masthead symbol, decorative footer image or unrelated listing thumbnail to become the accidental preview. Keep generic-artwork disclosures in the image description.

**SHARE-03** The current implementation produces uncropped 1200 × 630 JPEG copies on a paper background. Keep the image below the checked 5 MB ceiling. Content-hashed filenames change when the assigned source changes; originals are untouched. Shared source artwork may serve more than one appropriate page. One assigned image per page does not mean every page requires a unique generated picture.

**SHARE-04** Derive absolute image and page URLs from `SITE_URL` and `SITE_BASE`. Test both repository-path hosting and a future domain root. Verify the image is included in the public build, retrievable and associated with the right page. Preserve general noindex/content-release restrictions. Existing sharing-agent exceptions do not authorize broader indexing or DNS changes.

**SHARE-05** Verify metadata separately from platform display. Record which public pages/assets were fetched and whether an actual sharing service was tested. A correct tag does not prove Facebook or WhatsApp has refreshed its cache. Do not promise instant replacement of previously shared cards.

Implementation: `projects/site/social_metadata.py`, `projects/site/tools/build-social-images.mjs`, `projects/site/build-public.py`; tests: `projects/site/tests/test_social_metadata.py`. [Published evidence](../records/social-previews-2026-10-04.json) and [Open Graph reference](https://ogp.me/).

## 5 Protect poetry and reading tools

**READ-01** Preserve original wording, punctuation, script, line breaks, stanza boundaries, authorship and translator attribution. Keep research sources in the KB. Lack of a source URL alone is not a reason to hold available poem content; unresolved meaning, identity or missing text is a separate editorial question.

**READ-02** Translation work follows Human Natural Translation in Poetic Natural mode: read the full source and target, preserve emotional force, register and ambiguity, avoid unsupported kinship or gender, and save before/after wording with reasons. Verify explicit target line/stanza mappings when relineating. Never present assistant self-review as independent linguistic approval. Local translation revisions are not automatically cleared for publication.

**READ-02a** Preserve personification when choosing grammatical gender in translation. Check noun choice, pronouns, possessives and verb agreement across the whole poem; the poet’s gender does not establish the speaker’s or addressee’s gender. Load recorded poet feedback before revision, distinguish a suggested word from approval of a full translation, and retain meaningful regional usage. See the [poet-feedback workflow](../production/translation-revisions/WORKFLOW.md#poet-feedback-and-personification).

**READ-03** Illustrated and text-led poems retain language controls, browser-managed text enlargement, bookmarks, quiet reading, sharing, edition navigation and editor links. The regular poem ending uses the small botanical mark: do not restore the removed Previous/Next row. Quiet-reader pagination is a different feature and remains.

**READ-04** Quiet-reader animation and paper sound default off; reduced-motion preferences override animation. Preserve keyboard operation, focused menus/popovers, readable enlarged text, mobile flow and device-local bookmarks. No autoplay or ornamental motion to signal that a page is interactive.

Evidence: [poem endings](../records/poem-ending-simplification-2026-10-04.json), [translation workflow](../production/translation-revisions/WORKFLOW.md), and the current reading rules in the design system.

## 6 Keep responses simple and consent meaningful

**SERVICE-01** Likes, moderated public comments and private Firebase feedback are active. Preserve the verified runtime configuration and rules; older setup notes describing them as disabled are historical. Public comments use one textarea and Post comment, with the adjacent review note. Do not add name fields, checkboxes or an immediate-publication promise without a new requirement.

**SERVICE-02** Preserve the private submission queue, approved-public-comment separation and throttling. Do not turn private feedback into public comments. GA4 remains opt-in with withdrawal; do not load analytics before consent or put private reader data in Git, previews or the KB. Bookmarks remain device-local; reader accounts and a dedicated editor moderation inbox are not implied features.

**SERVICE-03** Keep the shared footer organized. The decorative boat is hidden on phones; the global footer links remain. Do not confuse the removed poem Previous/Next row with the global footer navigation.

Evidence: [activation](../records/engagement-activation-2026-10-04.json), [single-field comments](../records/single-field-comments-2026-10-04.json), [mobile footer](../records/mobile-footer-boat-2026-10-04.json).

## 7 Verify and publish within the actual scope

**DELIVERY-01** Review desktop and narrow-phone layouts, long names/titles, all affected scripts, theme, keyboard focus, enlarged text, image loading and navigation. Check the relevant forms or reader tools. Automated checks support review; they do not certify full accessibility or literary quality.

**DELIVERY-02** Run the relevant existing tests and the public build with Node 24. `npm --prefix projects/site test` includes sharing-selection tests; `npm --prefix projects/site run build` generates the public sharing images. Check a new page family against the image selector: the journal fallback prevents a broken preview but does not prove the chosen artwork is appropriate. Record deliberate fallback choices.

**DELIVERY-03** Keep non-site material in `kb/`. Regenerate registers/catalogue, validate the bundle, synchronize the portable handoff and check storage. Never overwrite divergent handoff edits. Preserve concurrent translation, portrait and artwork work. An interrupted batch resumes from saved evidence, not a blind regeneration.

**DELIVERY-04** Publication requires authorization covering the actual changes; do not ask again when it is already given. Use a clean release checkout based on latest remote main, include only authorized changes, build the public export and run the established manual Pages workflow. Preserve preview/noindex gates, consent, services and DNS unless explicitly changing them. Never deploy the raw preview folder or KB; do not enable push-triggered publishing.

**DELIVERY-05** Report the difference between saved locally, verified, pushed, deployed and live-checked. Verify the published page and its intended image. Compare exact files where reproducible; if encoders differ, record actual hashes and a justified decoded-image comparison rather than claiming false byte equality. Save the release reference, workflow result, findings and any outstanding platform check.

**DELIVERY-06** Load only the selected homepage artwork. Use native responsive image candidates and explicit image dimensions; retain existing below-fold lazy loading and purposeful alt/captions. Tiny inline previews stay static, without shimmer or reveal animation. Keep originals and static sharing associations unchanged. Serve full-glyph WOFF2 copies of approved fonts, retain source TTFs/licences, and verify Indic shaping and variable-font tables when repackaging. `npm run prepare:images` maintains content-hashed derivatives; `npm run build` runs it automatically. Direct Python preview builds use the saved manifest, so refresh it after adding artwork. Evidence: [loading and rotation](../records/page-loading-2026-10-05.json).

## 8 Keep this rulebook current

When a user changes a rule, update this document, its linked checklist and the responsible component or data source. Record the new decision, scope, verification and what it supersedes; retain earlier evidence. Use the [dashboard](../registers/DASHBOARD.md) for current work and the [page-type review](../review/page-type-checklist.md) for closure status. This rulebook does not silently close their open reviews.

Future work should leave one short record answering: what changed, which existing rules applied, what exception was authorized, what was checked, and where the result is available. Documentation-only maintenance does not itself require a website deployment.

## Blueprint inheritance update — 6 October 2026

Common website rules now come from `kb/reference/website-extensions.md` and its hash-pinned Blueprint references. This existing document retains project-specific requirements and historical implementation context during migration; its repeated common provisions are compatibility references, not a competing common-rule authority. The current shared targets for Firebase feedback, poem/article responses, sharing and one AI-use explanation govern wherever earlier implementation guidance differs. Pending features remain pending; adoption is not deployment.

## Incremental edition imports

For issues arriving before editorial cutover, follow the [Edition Sync Playbook](../production/edition-sync/PLAYBOOK.md). Import by stable source IDs, preserve captured originals and existing local edits, and compare conflicting revisions instead of overwriting. Edition 48 is the first verified local application; publication remains a separately recorded step. See [first-sync evidence](../records/edition-sync-48.json), KBL-DEC-053.

## Edition 48 editorial revision

For Edition 48 only, the latest user direction replaces the three-interior/text-led plan: each of its 11 poems has one distinct poem-informed illustration, also used for that poem’s static sharing image. Preserve the first three commissioned images. Other editions retain their recorded directions; do not randomly rotate poem imagery. The issue’s cover story is ordinary visible prose on desktop and phone.

Normalize the two all-caps English titles through source-checked display overrides, retaining exact source records and verse. Carry the display title through contents, author contributions, search, reading payloads and sharing metadata. Never apply blanket title-casing to intentional abbreviations or poetry.

The new Durga Puja editorial is authored in Odia first, with English and Hindi renderings, verified excerpts linked to their poems, all 11 contributors represented and no invented editor byline. Keep its draft status visible until actual editorial approval. Excerpt translations appear alongside the exact originals and are identified as translations; they do not replace the poem translations. See [revision evidence](../research/edition-sync/edition-48/revision-02/scope.json).

## Poem-first imagery and editorial line art — 6 October 2026

Human Natural / Poetic Natural is an approach to meaning, composition and believable treatment, **not a watercolor requirement**. Read the complete poem before assigning or generating its image. Record the emotional anchor, relevant imagery, cultural context and why the chosen medium serves them. Avoid generic mood matches, literal noun inventories and forced variation. Ink, graphite, collage, painterly work and photographic-style interpretations may all be appropriate. Retain strong existing matches; do not regenerate just to meet a medium quota. Portrait watercolor authorization is separate.

Edition 48 revision03 refines three poem assignments (825, 826, 833), retaining the other eight. This supersedes the revision02 preservation instruction only for the selected 826 image; earlier candidates remain preserved. Each poem still has one stable unique illustration and its corresponding sharing image. Photographic-style generated scenes remain imaginative interpretations, never documentary evidence.

Editorial line art should illuminate a specific passage and leave the prose dominant. Use a few restrained vignettes at meaningful turns, localized alt text, explicit dimensions, lazy loading and transparent edges that work in both themes. Keep small-screen prose comfortably readable. Edition48 uses listening, shelter and companionship motifs; its Odia-first prose, excerpts and draft-review status remain unchanged. Evidence: `kb/research/edition-sync/edition-48/revision-03/`.

Future edition syncs follow the same poem-first, medium-open imagery and passage-specific editorial line-art workflow, now embedded in section 3 of the [Edition Sync Playbook](../production/edition-sync/PLAYBOOK.md). One distinct illustration per poem is the default for newly synced editions; existing older editions are not retroactively changed.

## Language is a primary reading choice — 6 October 2026

Show Original, ଓଡ଼ିଆ, हिन्दी and English directly on poem pages and in the edition opening, with a clear active state. Keep the same visible language row at the top of the quiet reader. Language must not be hidden inside Aa/settings. The secondary control is labelled Text size and retains enlargement, bookmarks and other reader tools. Unavailable poem translations stay disabled; Original resolves to the true source language.

Edition language selection updates contents titles and poem-link language, carries into quiet reading and follows through to an available editorial version. Preserve the separate editorial language links and explicit editorial deep links. Shared collection controls use the same visible pattern. Check keyboard operation, 320px/390px layouts, both themes and repagination after language/size changes. See `kb/records/visible-reading-language-2026-10-06.json`.

## Edition reading flow — 6 October 2026

Editorial notes use the full edition content width within the established page gutters. Separate the opening, poem entries and editorial through spacing and typography, without repeated row rules, decorative contents dividers or editorial/quotation borders. Retain visible selected-language and keyboard-focus indicators. Check desktop and phone layouts without changing the poetry, excerpts or passage illustrations.

## Edition opening hierarchy — 6 October 2026

Keep issue identity and date first, visible language choices second, and a compact action row third: Read poems is primary, Editorial note is secondary when present, and Reading tools contains text size, sharing and quiet reading. Archive navigation already exists in the breadcrumb/header; avoid repeating it in the action row. Keep controls at least 44px high, selected-language and keyboard-focus cues, and restore focus to Reading tools when closing quiet reading opened from that menu. Use a small relevant line-art vignette in available right-column space below the cover; move its existing placement rather than duplicate it. On phones it follows the cover in normal flow. Preserve the full-width editorial and borderless edition contents.

### Direct edition icons — superseding the tools pop-up, 6 October 2026

The user's subsequent review replaces the edition Reading tools disclosure with direct 44px icon controls beside the primary Read poems link: pen for Editorial note where present, Aa for text size, Share, and Read quietly. Language remains visible above. Aa cycles Standard → Large → Extra large → Standard, exposes the current/next value in its accessible name and tooltip, and announces each change. Tooltips appear on hover or keyboard focus; keyboard focus takes precedence so labels do not overlap. Quiet reading returns focus to its visible icon. No edition tools panel, close button or reset action is needed. This supersedes the preceding disclosure/focus-to-menu rule; shared Poems/search and individual-poem settings remain unchanged.

### Quiet-reader space and editorial-only line art — 6 October 2026

Quiet reading uses one top bar, with three script buttons ଅ / अ / A immediately left of the bookmark, followed by the compact Aa settings icon. Do not add a separate language row or a visible Text size label to that header. Keep language names in accessible labels/tooltips, a selected-state underline and 44px targets. The original-per-poem mode remains available in reading settings; source fallback and unavailable-translation handling remain. Edition and regular poem language rows stay unchanged.

Line-art vignettes belong only inside the editorial, beside the quoted passages on the right; do not place them under the edition cover or in its opening. Edition48 pairs listening chairs with Saswati Hota’s silence excerpt, fallen flowers with Sabita Singh Meera’s excerpt, and shared tea with Bishnu Charan Parida’s love excerpt. Keep exact quotes/translations/attribution intact and move art below its quote on phones when side-by-side placement would crowd verse. This supersedes the earlier opening-vignette placement and quiet-reader language-row rules.

### Edition links and content controls — 6 October 2026

Only Read Poems and, where an editorial exists, Read Editorial remain beneath the edition title. Both are visible text links. Move reading language, Aa, Share and Quiet reading to the top of the poem contents, before its first entry. Keep one set of controls per edition, with existing accessible labels/tooltips, text-size cycling and language inheritance. This supersedes earlier placement of controls in the edition opening; quiet-reader and editorial quotation-art rules remain unchanged.


## Browser-managed text sizing — 6 October 2026

The user removed the site-specific text-size tool. Do not add Aa size buttons, Standard/Large/Extra large selectors, size popups or stored font-size overrides to editions, the Poems catalogue, poem pages or quiet reading. This supersedes all earlier sizing-control requirements, including the Aa control in the quiet-reader header. Browser zoom and preferred-font enlargement own sizing; use relative units for reading text, allow wrapping, retain stanza boundaries and never disable zoom. Quiet reading must repaginate on viewport changes and remain scrollable when a passage exceeds the available height.

Keep language choices, bookmarks/saved passages, sharing and quiet reading. The regular poem bookmark panel uses a bookmark icon; quiet-reader settings use the existing menu icon for library, original-language mode and saved reading preferences. Keep Read Poems / Read Editorial above, language and remaining actions at the top of edition contents, and line art only beside editorial quotations. Verify default and enlarged text, narrow reflow, focus return, language changes and reader pagination.


### Reviewed editorial and reader appearance — 6 October 2026

After Ahimanikya explicitly reviews an editorial and asks to remove its draft notice, record that user review and suppress the review notice in all language versions. Preserve the text, excerpts and provenance; do not infer publication-editor approval or clear other content-release gates. Edition48 is user-reviewed under this instruction.

Quiet reading retains a directly accessible shared System/Light/Dark theme control in its existing bottom bar. Use the site preference and established icons, accessible current/next-state labels and 44px targets; do not add another toolbar row. Verify theme changes inside the modal, after exit and across reloads, plus narrow layouts.


### One magazine reader with optional illustrations — 6 October 2026

Keep one quiet-reader experience. Show illustrations is an optional Reading settings switch, off on each new page load; switching it repaginates around the current poem/reading anchor. When enabled, show only the existing assigned poem-page image at that poem's opening, with its recorded alt text. Text-led poems remain text-led. No random imagery or newly generated art is needed. Do not load illustration images while the option is off; measurement uses a same-sized placeholder.

Use subtle existing cotton-paper texture and a restrained gutter/page shadow in light mode, with clean texture-free leaves in dark mode. Center each folio beneath its own page and center the overall visible-page range/total across the full book, independently of the theme/arrow controls. Reserve folio space during pagination; oversized text remains scrollable. Two pages on wide screens, one on phones, with existing languages, bookmarks, theme, reader settings and source text preserved. Page totals are responsive reading positions, not historical print pagination.


### Consistent reader actions and poem-language shortcuts — 6 October 2026

A reader action always uses the same canonical icon across page types. Read quietly uses the approved footer-story manuscript icon through reader_icons.quiet_reader_icon() on editions, the Poems catalogue and poem pages; do not draw a separate book icon for the same action. Different accessible labels must not disguise the same action as a different symbol.

Poem pages use exactly three language shortcuts: ଅ / अ / A, matching the quiet-reader script vocabulary, with language-name hover/focus tooltips, accessible tab names and 44px targets. Initially select the actual source language and identify Original in its tooltip; unavailable translations remain disabled. Keep keyboard tab navigation, translated titles/verse, bookmarks and existing lang=original links working. Edition collection language labels remain unchanged. This supersedes earlier four-choice poem-page language rows.


### Compact poem actions and top reader theme — 6 October 2026

Place the quiet-reader System/Light/Dark toggle immediately before the menu/settings icon in its existing top row. Keep 44px targets and a single row at 320px; the bottom bar contains only pagination, centered across the book. This supersedes its earlier bottom placement.

Regular poem-page actions are icon-only: bookmark, share, canonical Read quietly and Like, with hover/focus tooltips and accessible names. Keep one actual Like button backed by the existing reversible Firebase transaction; count/state belong in its tooltip and accessible feedback. Comments remain below the verse. Preserve host/HTTPS/service gates: local previews show a disabled Like and explain availability; do not enable production writes for preview testing. Language stays visible as ଅ / अ / A. No text-size controls return.


### One combined poem toolbar — 6 October 2026

The three language shortcuts and four action icons share one horizontal row: ଅ, अ, A, bookmark, share, Read quietly, Like. Use one subtle vertical separator between language and action groups. Omit the visible Read in label; retain language tab semantics, action groups and tooltips. Preserve44px targets at320px by using the available page gutters, with no wrapping or page overflow. This supersedes the separate language/action rows.


### Edition icon toolbar — 6 October 2026

At the top of edition contents, group all language and action controls on one line with44px targets and one subtle vertical separator. Use Original-language reset icon, ଅ, अ, A, then Share and the canonical Read quietly icon. Accessible names and hover/focus tooltips explain every control; retain per-poem original fallback, translated links, and editorial/reader language inheritance. Read Poems and Read Editorial remain text links in the opening. The Poems catalogue keeps its current controls. This supersedes the full-word edition language labels and separated action placement.


### Printed magazine cover treatment — 6 October 2026

Present issue covers on the home page, edition pages and archive/year pages as restrained printed magazines: a slim left binding fold, a shallow paper edge at right/bottom, and a soft static shadow. Keep the approved cover SVG, masthead, signature, complete artwork and 2:3 ratio unchanged. Apply through the shared cover renderer’s route-scoped `magazine-object` class and `assets/magazine-covers.css`; no new bitmap or script is needed. Do not add tilt animations, page-turn effects, frames around poem artwork, or this treatment to the homepage landscape. Preserve original social-preview assets and cover history. Check narrow phones, compact home cards, light/dark themes and printed output. This is a cover-only exception to the earlier borderless-inner-artwork wording; poem illustrations remain borderless.


### Matching poem and edition tools — 6 October 2026

Poem action icons use the same canonical Earth Voice assets as edition controls through `reader_icons.reader_action_icon`: Share and Read quietly must not have separately drawn variants. Bookmark uses the existing approved bookmark asset. Match 23px symbols inside 44px controls, restrained hover fill, script typefaces, tooltip spacing and focus treatment. Keep the three poem language tabs, one group separator, Bookmark, Share, Read quietly and Like on one row; only one tooltip is visible across language and action groups when keyboard focus is present. Retain the real Like service gates and existing comments.


### Poems catalogue icon toolbar — 6 October 2026

The Poems listing (`poems.html`) reuses the edition icon toolbar at the top of its contents: Original-language reset, ଅ / अ / A, a subtle group separator, Share poems and Read quietly. All six controls stay on one row with44px targets, native-name/accessibility labels and hover/focus tooltips. Preserve the search field, poet/edition filters, pagination, language-aware links and full-collection quiet reading. This supersedes the earlier instruction to keep the catalogue full-word controls unchanged.

## Odia signature — 6 October 2026

Use the exact approved wording **ମାଟିର ମହକ / ହୃଦୟର ସ୍ବର** everywhere the journal signature appears. Preserve each placement’s established two-line or single-line layout; the spelling of ସ୍ବର is explicit. Applies to website, edition covers, generated cards/captions and current branding assets. Historical source captures, dated decision evidence and earlier delivery snapshots remain preserved. See [tagline update](../records/tagline-2026-10-06.json).


## Language essay scope — 6 October 2026

The journal’s language essay focuses on Odia, Hindi and English. Use “Three languages and the journey of a poem” in its visible title, homepage feature and sharing metadata. Retain cultural-detail and translation/adaptation discussion; omit the former worldwide language survey and population infographics. Preserve the earlier supplied article and artwork as provenance. The published article route stays stable for existing links. See [current revision](../records/three-languages-article-2026-10-06.json).


### Article response presentation — 7 October 2026

Article comments follow the approved single-text-box form: publish as “Reader” after moderation, with the publication-consent notice beside the submit action. Match the essay’s reading-column width, site colours and44px minimum controls; avoid a full-width unstyled block. Keep private feedback distinct and preserve service/receipt gates. See [verified correction](../records/article-comments-layout-2026-10-07.json).

## Search and AI discovery — 10 October 2026

The user explicitly authorizes searchable publication of the existing public reader site, superseding its blanket preview noindex restriction for discovery deployments. `discovery` is separate from full editorial `release`: it must not certify translations, remove draft labels, import unpublished local content or clear unresolved source records. Keep unavailable/unattributed/unassigned poem records, duplicate aliases, redirects and utility forms noindex and outside the sitemap.

Generate HTTPS canonical URLs, a canonical-only sitemap, visible-content-based structured data and an `llms.txt` navigation aid. Public original text remains ordinary HTML for all readers and crawlers; never cloak or invent author/date/review metadata. Search and citation crawlers may access public pages; training-crawler policy is explicit in `data/discovery.json`. Robots directives are voluntary crawl instructions, not bot authentication or access control.

Firebase bot protection uses domain-restricted reCAPTCHA Enterprise through App Check. Ship and verify all clients before enabling Firestore enforcement. Preserve private submissions, moderation, server cooldowns, Analytics opt-in and readable static pages when services fail. Keep billing disabled under the present authorization. Public security/privacy disclosure belongs in Our Story. Record quota limits, actual enforcement and verification separately from code readiness.


## Translation publication and separate review desk — 11 October 2026

The user authorizes publishing the remaining local changes, including the 818 revised translation variants. Reader pages must not label these translations as drafts or display pending-review notices. Keep original/translation identification, contributor credits and the centralized preparation explanation. Preserve actual review states, source holds and before/after evidence in the KB; this presentation decision does not assert independent linguistic certification or clear the full editorial release gate.

Publish a dedicated `translation-review.html` reference with actual review status and source questions. Keep it unlinked from public navigation and other reader pages, noindex, outside the sitemap, site-search index, Analytics route catalogue and LLM guide. Crawlers must be able to fetch its noindex directive; do not block that URL in robots.txt. Direct-link availability is not access control. This instruction supersedes the earlier draft-label preservation requirement for this scope.

## Public credits and development review material — 11 October 2026

The user requested removal of AI credits from every public page and cleanup of published development review material. This supersedes the earlier public AI-preparation explanation requirement, including the inherited disclosure target, for Kabita Live. Preserve human author/translator credits, source acknowledgements, font licences, generic-artwork labels and historical provenance in the KB. Do not claim artistic adaptations are original documentary photographs.

Public export accepts only named reader routes and numbered poem, poet, issue and archive routes; new page families must be deliberately registered. Development mockups, samples, audits, proposals and review material remain local, regardless of whether their files are symlinks. The previously requested translation-review.html is the explicit exception: direct-link only, noindex, absent from site search, sitemap, LLM guide and analytics.
