---
type: "Production playbook"
title: "Edition Sync Playbook"
---

# Edition Sync Playbook

Maintain Kabita Live’s replacement site while the editors continue publishing on the current journal. Each sync is an additive, reviewed import of a particular issue, not a mirror that overwrites our editorial work. Edition 48 is the first application. This playbook does not start a scheduled scraper or authorize publication by itself.

## Governing rules and responsibilities

Read the [website rulebook](../../reference/website-rulebook.md), [new-page checklist](../../review/new-page-checklist.md), current dashboard and working agreement before each issue. The pinned common website standard and [local extensions](../../reference/website-extensions.md) also apply. Ahimanikya and the magazine’s editors retain editorial authority. Research, translation, implementation and review passes by the same assistant must be labelled self-review, never independent approval.

Use Human Natural Translation in Poetic Natural mode for poetry; use the writer-profile, writer-portrait, Human Natural Image and imagegen skills for their respective work. Keep their exact prompts, evidence and limitations in the issue record. Use built-in image generation only. Do not invent missing faces, biographies, awards, locations or authorial intentions.

## 1. Discover and freeze the source

1. Open the current homepage and archive listing. Follow the actual issue link and record its URL, issue number, month/year, contents order and contributor links. Source archive IDs and displayed edition numbers are different: Edition 48 has archive ID 59. Never calculate one from the other. A cached search result is not proof of the latest issue.
2. Save unchanged HTML, original cover and contributor photographs under `kb/artifacts/edition-sync/edition-N/source/`. Each needs its URL, capture timestamp, content hash and byte count. Keep redirects and unsuccessful captures visible. If direct links redirect, follow the journal’s navigation and verify the rendered page before claiming capture.
3. Save full parsed poems and biographies under `kb/research/edition-sync/edition-N/`. Reconcile contents-list IDs with poem pages and writer IDs. Record omissions or conflicting identity evidence precisely; do not call metadata-only entries complete poems.
4. Preserve every source byte. Separate poem-ending marks, contact addresses and employment footnotes from verse only after inspecting the actual page. Save the exact removed matter and before/after hashes. Do not silently correct an author’s spelling, unconventional English, stanza boundaries or punctuation.

## 2. Compare with our publication

Use stable poem and writer IDs, not names or titles, as identity keys. Snapshot current destination records before applying the issue.

| Incoming item | Action |
| --- | --- |
| New issue and new poem ID | Create reviewed records; retain source order and exact verse. |
| Existing writer ID | Reuse identity, portrait and curated narrative; add the new contribution through the normal publication join. |
| New writer ID | Verify name, linked poem, biography and photograph together; research only identity-matched sources. |
| Same source already imported | Treat an identical package as a no-op. |
| Existing ID with changed source | Compare previous source, current local version and new source. Preserve all three; record a proposed reconciliation. Never overwrite automatically. |
| Item removed from source | Record it for editorial review; do not delete or archive our publication automatically. |

The additive helper `tools/edition_sync.py` dry-runs by default. Its reviewed JSON package supports new files, new dictionary keys and keyed list additions. It preflights the whole package, rejects conflicting identities and stale destination bytes, preserves unrelated entries and is safe to rerun after a partial interruption. It does not fetch, translate, generate images, build or publish. Do not rerun the historical whole-archive importer for a new issue.

## 3. Make an edition, not a pile of pages

- Reuse the established issue, poem and author templates. Add the edition to the contents index, cover catalogue and cover-layout manifest. Verify current-issue promotion on the homepage, recent-issue ordering, archive/search discovery and all reciprocal author/poem/issue links.
- Preserve the source cover as an original in the KB. Any new cover is a clearly documented editorial interpretation. Keep the English masthead, one-line Odia signature, issue/date and approved typography. Inspect the completed cover with its lettering, not only the painting.
- For newly synced editions, follow the Edition 48 approach: one distinct, theme-matched illustration for each poem. Read every poem in full and record its emotional anchor before choosing the image. Vary framing, subject, density and medium for a reason; never use unrelated imagery to fill space or randomly rotate poem illustrations. Record an explicit exception if a suitable image cannot be completed; do not silently substitute generic art or claim the image complete. This forward-looking rule does not regenerate older editions.
- Add issue-specific art outside the shared pool. Preserve versioned masters, exact prompts, source/output hashes, canonical captions and self-review. A photograph cannot be turned into an invented historical claim. Avoid repeated AI labels in ordinary captions; keep the central disclosure and provenance under current common rules.
- For a new contributor, preserve journal biography and research receipts. Publish only supported facts. A sparse honest profile is better than a same-name biography. Create a watercolor portrait only from an identified source photograph; compare likeness, age, complexion, pose and expression at normal size. Source-photo rights and independent likeness confirmation are separate from visual self-review.

### Poem imagery: theme first, medium open

Human Natural / Poetic Natural governs emotional truth, cultural fidelity, believable materials/light and purposeful composition. It does **not** prescribe watercolor. Choose ink, graphite, collage, painting or a photographic-style interpretation when it serves the poem; avoid a mandatory medium quota or a uniform AI-looking filter. Poet portraits retain their separately approved watercolor treatment.

Before generation, save a short brief for each poem: poem ID and full source snapshot/hash; theme and emotional anchor; meaningful imagery and ambiguity to preserve; chosen medium and rationale; composition and negative space; elements to avoid. An illustration should support the poem rather than explain every noun or assert an unsupported interpretation.

After generation, compare the result with the full poem at normal viewing size. Check emotional fit, anatomy/geometry, physical and cultural plausibility, deliberate variety across the edition, and readability in the actual page. Keep strong existing commissions, all originals, exact prompts, candidates and review reasons. Treat generated photographic-style scenes as interpretations, never documentary evidence. Integrate through the edition art manifest; use the selected illustration as that poem’s stable sharing preview.

### Editorial notes and supporting line art

When a new editorial is part of the authorized issue work, think and draft in Odia first, then render naturally in English and Hindi. Build a positive but grounded thread from the actual poems and contributors; do not force every poem into the festival theme. Preserve difficult emotions, verify quoted extracts, label translated excerpts and retain the original wording. Keep a visible draft label until editor approval and never invent an editor byline.

Use a few small line-art vignettes where they illuminate a specific passage, not repeated decoration or a drawing beside every paragraph. Record the passage-to-image relationship, localized alt text, canonical caption, source/prompt and review. Keep prose dominant: desktop placement must not crowd text, and phone layouts should allow full-width reading. Verify transparent edges, light/dark contrast, explicit dimensions and lazy loading. Keep the cover story visible, using the established issue layout rather than introducing a collapsible treatment.

## 4. Translate with meaning and restraint

For the current reader, supply the two other reading languages among Odia, Hindi and English. This does not authorize adding every language supported by the translation skill.

Read each complete source and target. Preserve emotional force, ambiguity, metaphor, refrain, religious and cultural context, address and natural wordplay. Distinguish grammatical gender, speaker/addressee gender and personification. Never infer a speaker’s gender from the poet’s name or photograph. Keep author-supplied translations and credits intact. The human-natural skill contains broader language guidance for future expansion.

Save exact first drafts, reviewed variants, reasons and unresolved questions. Translation text remains a draft for poet/editor feedback unless an actual approval is recorded. If lineation changes, provide and validate explicit target `reader_layout` with source/stanza hashes and checked verse/stanza boundaries. Do not copy source tail offsets into translations. New-issue translations are a separate scope from the older collection’s revision heartbeat; do not reset that queue or overwrite concurrent revisions.

## 5. Integrate locally and verify

For Edition 48 the reviewed package is `kb/research/edition-sync/edition-48/integration-package.json`:

```sh
python3 tools/edition_sync.py kb/research/edition-sync/edition-48/integration-package.json
python3 tools/edition_sync.py kb/research/edition-sync/edition-48/integration-package.json --apply
python3 tools/check_edition_sync.py 48
```

For each future issue create its own package and before snapshot. Never edit an old package into a new edition. Art delivery files are prepared separately without replacing masters. Register the new issue in `kb/production/edition-sync/imports.json` so collection checks retain the fixed historical baseline and independently check each additional import.

Run the additive-helper tests, translation-layout checks, author and edition checks, affected site tests and the complete Node 24 public build. Refresh responsive image derivatives before building. Verify:

- exact poem order, full verse, bylines, language labels and translation payloads;
- one distinct illustration per new-issue poem, a saved theme/medium rationale for every assignment, and precise exceptions rather than unreviewed substitutions;
- passage-specific editorial line art, localized alt text, preserved excerpts/draft status, readable phone layout and light/dark contrast;
- all returning authors’ new contributions and every new profile’s quote/portrait;
- homepage current edition, archive and issue navigation, language controls, larger text, bookmark, quiet reader, share, feedback/Likes/comments and the small poem-ending mark; no Previous/Next footer navigation;
- desktop and narrow phone layouts, keyboard access, dark theme, enlarged reading text and absent horizontal overflow;
- exactly one intentional static sharing image in initial HTML: poet portrait, poem illustration, or edition-cover fallback for a text-led poem; correct absolute URLs and public assets;
- preserved original poems, older cover entries, portraits, service configuration, explicit GA4 consent, noindex/content-release gates and DNS.

Save actual results and screenshots. A successful build is not literary approval or proof that a social platform has refreshed its cache. Record unrelated baseline failures separately; do not silently change old poetry to make tests pass. Keep the local preview origin `http://127.0.0.1:8771/` stable.

Regenerate `tools/registers.py` and `tools/catalog.py`, run `tools/check_bundle.py`, then `tools/sync_handoff.py` and `tools/check_storage.py`. Preserve concurrent work. On a source-changing sync interruption, retry from the newer canonical data; on divergent handoff edits, preserve both and reconcile rather than forcing a copy.

## 6. Publish only the authorized issue scope

Once publication is authorized, use a clean release checkout from latest remote main. Carry only the verified issue changes and necessary generated/KB files. Do not publish other local translation drafts or unfinished work accidentally. Push normally and dispatch the existing manual public-only GitHub Pages workflow in the currently approved preview/release mode. No force push, automatic push-triggered deployment, DNS change or release-gate removal.

Wait for workflow success and verify live issue/home/poem/profile HTML, static share-image URLs and exact asset hashes. Save the commit, workflow, live evidence and any remaining holds. Do not label local integration “live”. Social posts and messages need their own authorization.

## 7. Close the sync and eventually stop it

Each issue record should state discovered/captured/reviewed/integrated/verified/published status separately; counts of original poems, translation variants, new/returning contributors and art; source/package hashes; open questions; and the exact next action. Retain first-source snapshots for later three-way comparisons.

When the editors move to the replacement site, record a cutover decision and final source watermark. Complete a final content comparison, then stop old-site imports. From that point the replacement repository/editorial workflow is authoritative. Preserve the sync history and original assets permanently; do not keep two competing sources of truth.

## First-sync revision: one illustration per poem and a new editorial

The later Edition 48 instruction supersedes its initial three-image plan: all 11 poems receive distinct illustrations. This was initially an issue-specific direction. The subsequent instruction to follow the same rules next time makes it the default for new edition syncs under section 3; it does not authorize regeneration of older editions. Preserve commissioned work and add only missing images. A new editorial absent from the source must be recorded as new work, drafted in Odia first for this issue, then translated into English/Hindi. Verify every original quotation against the frozen source; label translated excerpts and retain original wording alongside them. Do not invent an editor’s authorship or approval.

Use `data/poem-title-overrides.json` for authorized presentation-only casing corrections; assert the expected source title and leave captured source/verse unchanged. The Edition 48 cover story stays visible rather than collapsible.

Keep the initial import package immutable after later editorial revisions. It is historical evidence, not a package to force-replay over revised material. Record each subsequent revision with exact source/art baselines, explicit changes and a scoped verifier. The revision02 verifier belongs to its frozen historical checkpoint. After the 6 October opening-hierarchy refinement, run `python3 kb/artifacts/review/consistent-reader-controls-2026-10-06/verify.py` after building. It inherits revision03 content/art checks and verifies editorial-only quotation art, content-level controls and removal of site sizing tools; revision03 remains a historical layout checkpoint. Its checks preserve the original 11 poems, 22 translations, excerpts, older source/art files and other edition art directions while allowing the three reviewed image refinements and three editorial vignettes. Future issues need their own current scoped verifier. The older collection’s concurrent translation work remains separately owned and checked.

Rules promoted into the main workflow on 6 October 2026 after Ahimanikya instructed: “Also, update the playbook so we follow the same rule next time.” See KBL-DEC-055 and the [Edition48 theme review](../../research/edition-sync/edition-48/revision-03/theme-review.json).

### Language controls for every new issue

Keep the visible Original / ଓଡ଼ିଆ / हिन्दी / English row in the edition opening, on every poem page and at the top of quiet reading. Do not move it back into Aa/settings. Text size stays in the labelled secondary menu. Verify the edition choice updates titles, poem-link language, quiet-reader startup and any available editorial version. Check keyboard operation and narrow-phone layouts; preserve source-language fallback, unavailable-translation states and all existing reading tools.

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
