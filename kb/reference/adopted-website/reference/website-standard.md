---
type: "Website standard candidate"
title: "Utkal shared website standard"
version: "0.1.0-draft.5"
status: "draft_for_fleet_review"
---

# Utkal shared website standard

The Utkal website fleet shares readable pages, purposeful art, natural literary language and dependable reader tools. This proposed Blueprint extension gives Poem Without Borders / Free to Dream, Kabita Live, Singhasan and Utkal Project a common foundation while preserving their identities and content.

Website-standard versions are separate from Blueprint governance versions and design-system package versions. This draft defines the target experience; adoption is recorded per site and page family. The Founder's latest fleet direction governs the image, sharing, response and AI-disclosure targets below. Each site records when implementation catches up with those targets; an older rule excluding a requested feature is retained as history, not used to negate the new direction.

## Base definition and independent instances

**WEB-INHERIT-01** Blueprint is the abstract project definition. Each site is an independent instance with its own KB, identity, records, source tree and service configuration. Common rules and operating processes live primarily in Blueprint; project rulebooks reference that pinned baseline and add only local overrides and extensions. Shared implementation components have one canonical source and are versioned separately.

**WEB-INHERIT-02** A project extension adds domain behaviour, such as Singhasan's book reader or Free to Dream's listening collection. An override changes a named default, such as a masthead, palette or pagination choice. Record the affected base rule/component, local value, rationale, actual decision and adopted version. Preserve common requirements such as private pending comments, human authority and source integrity; a theme override does not waive those requirements. The user's explicit later instruction governs its scope and is reflected in both the appropriate common or local rule and its adoption record.

**WEB-INHERIT-03** Inherit common changes through a versioned adoption process. Review the base change against local overrides, test the affected behaviour and record the adopted version. A local copy can support offline reading but is a pinned reference, not a separately edited authority. Existing full project rulebooks can remain during migration; map their common provisions to Blueprint and preserve historical decisions before reducing them to extensions. Do not replace all working rulebooks in one unverified operation.

## Shared foundations and site identity

**WEB-STRUCT-01** Model each fleet project as an independent Blueprint instance. Blueprint supplies the reusable model; each project owns its own KB, persona model and assignments, decisions, history and source tree. There is no combined fleet KB or shared operating roster. Each has a root `utkal.config.json`, a canonical `kb/` with its own charter, working agreement, roles, assignments, registers and history, root maintenance `tools/`, and website source under `projects/site/`. The KB index and root project instructions provide the entry point for contributors.

**WEB-STRUCT-02** Use Blueprint persona definitions and role briefs as modelling templates. Each project maintains its own persona definitions or pinned references, locally adapted responsibilities and actual assignments. Record scope, human supervision and authorization in that project's team records. Adopting the definitions does not automatically dispatch agents, activate background work, appoint people or grant access. Existing authorized assignments remain intact.

**WEB-STRUCT-03** Keep project knowledge and internal provenance in the KB; keep implementation source, public assets and meaningful tests with the relevant project workspace. Export only intended public content and assets. Preserve existing builders, frameworks, source paths that need compatibility aliases, original texts, saved data and site-specific maintained assets during migration. Some current sites keep source inputs in a directory named `dist`; identify those before reorganizing it. Never delete such inputs as disposable output.

Each project keeps independent identity, records and adoption evidence. Use Blueprint as the common baseline without inheriting its maintenance history or another site's operating roster. Structure adoption, persona assignments, feature parity and live publication are separate coverage fields.

Use one maintained design-system source for reusable styles, icons and behaviour. Sites consume a pinned release or a recorded source revision, with a small theme adapter for their approved values. Do not maintain independently edited copies of common components.

Common roles include paper, reading surface, ink, muted ink, sea accent, earth accent, rule, focus, action and status. A theme supplies values for these roles. Existing Utkal and Kabita Live colours differ deliberately. Singhasan retains its throne identity and Anek Odia masthead. Logos, signatures, editorial artwork, credits and cultural motifs remain attached to their publication.

## Typography and spacing

**WEB-TYPE-01** Use semantic display, reading, interface and script font roles and a shared spacing scale with recorded local optical exceptions. Preserve shaped-script direction, verse breaks, continuous prose and complete enlarged text; no font or layout override changes authored content.

Separate display, sustained reading, interface and script-specific typography. Cormorant Garamond and Source Serif 4 are existing shared candidates for English display and reading. Noto Serif Oriya is the existing literary Odia reading choice. Preserve explicit site overrides and provide suitable fonts for every published script, including direction and shaping rules where needed.

Never synthesize slant or bold for Indic verse, add tracking to shaped scripts, or shrink text to force it into a fixed page. Preserve authored line breaks and stanza boundaries. Visual wrapping of a long verse line must remain distinguishable from an authored break. Prose wraps naturally and does not acquire artificial verse breaks.

The existing Utkal spacing scale is 4, 8, 12, 16, 24, 32, 48, 64 and 96px. Adopt it through semantic roles for control gaps, paragraph spacing, stanza spacing, page insets and section separation. Script rhythm, poetry and existing optical adjustments can have recorded exceptions. A shared scale does not require every site to use the same stanza gap or heading size.

Use bounded prose columns; Utkal's current reading measure is 68ch. Treat that as a starting specimen, not a reliable measure for every script. Preserve existing Kabita Live poem sizes and Singhasan page geometry during the first foundation pilot. Reader enlargement must keep text complete and controls usable.

## Paper surfaces and artwork

**WEB-DESIGN-01** Consume versioned shared semantic tokens and utility icons through a local theme adapter. Preserve approved identity and masters; keep cotton/earth/sea surfaces, quiet/night choices and artistic line art legible and clear of text.

Cotton paper gives the fleet its ordinary literary surface. Earth wash and sea or monsoon wash are selected treatments for appropriate pages and reader options. A page-family theme decides placement and intensity; do not copy one publication's opacity to every site. Quiet and night reading need clear surfaces, and night reading removes texture.

Artwork should serve the work's mood or help explain its subject. Keep utility pages compact so search, forms and browsing arrive promptly. Preserve full compositions where cropping would change meaning; reserve image dimensions and provide responsive delivery assets. Core text remains available while images load or fail.

**WEB-HUMAN-01** Use the Human Natural Image workflow for generated or edited imagery, with Poetic Natural guidance for literary work. Read the actual poem or article first. Preserve originals, source identity, exact prompts, versions and provenance. A generated view does not establish documentary evidence of a real place or person. Portraits need an identified source and a likeness comparison.

## Icons and line art

Use a coherent single-ink utility family for reading, search, language, sharing, saving and responses. Functional icons need a visible or accessible name; decoration is hidden from assistive technology. Prefer 20–24px utility glyphs within comfortable controls. The fleet target is at least 44 × 44 CSS pixels for standalone controls, retaining existing larger targets. Inline text links have their own spacing and context.

Editorial line drawings and cultural motifs have separate identities and placement rules. Use them where meaning and spare space support them. Do not overlay verse, fill every blank area or add pages merely to accommodate decoration. Keep original SVG sources and asset licences.

## Human Natural language and translation

Literary voice can be artistic and inviting. Action labels remain direct: Read, Listen, Search, Save, Comment and Change language. Give unfamiliar cultural imagery enough context to be understood without erasing it.

**WEB-HUMAN-02** Use Human Natural Translation for literary translation: Poetic Natural for poetry and the appropriate prose mode for articles. Carry meaning, emotional force, ambiguity and register into natural target-language expression. Preserve exact originals and attribution. Distinguish translation from cultural adaptation; record unresolved meanings rather than inventing them. Save before and after drafts and reasons for substantive revisions.

Drafting, assistant self-review, fluent-reader review, author acceptance and publication are distinct states. A shared skill or passing structural check does not certify every translation or authorize its publication. Blueprint links versioned editorial guidance; the site's own source texts and review decisions stay in its records.

## Reading experience

Offer text enlargement, clear language selection when translations exist, saved place and a quiet reading surface for substantial poems and articles. Preserve selectable text, headings, citations and source verse. Keep reader settings local unless a separately authorized account feature supplies synchronization.

Share settings and persistence contracts across adapters. A journal edition, single book, continuous article and listening collection keep appropriate layouts. Article reading must not inherit stanza pagination. Source anchors, rather than generated page numbers, should identify saved passages where reflow changes pages; preserve existing saved-data formats or provide an explicit migration.

An unavailable translation falls back visibly. Respect reduced motion. Sound and playback require reader action; returning to a language must not unexpectedly start audio. Keep service failures from blocking reading. The opening and exit paths retain language and reading context where supported by the page family.

### Reusable reader and ordered collections

**WEB-READER-01** Maintain one versioned reader core for poems, continuous articles and ordered collections. A collection may be a book, magazine edition, topic, category or location. Its local adapter supplies available public entries, explicit ordering, source language, variants, permanent routes and citations. Keep a work’s stable identity across collections; do not present missing/unpublished material as completed coverage. Utkal topic/category/location entries open the relevant collection in focused reading.

**WEB-READER-02** The common core supplies settings, language fallback, content navigation, stable logical anchors and persistence boundaries. Adapters preserve book/journal geometry, verse and prose handling, audio and local identity. Keep current saved-data keys/formats working or implement a tested migration with recovery. No generated page number becomes a permanent anchor; article prose must remain continuous rather than inheriting stanza pagination.

**WEB-READER-03** Focused reading preserves selectable complete text, sources, citations and truthful attribution while folding distracting site navigation and responses. Keep a contextual exit to the entry route, language and place. Test entry/exit, unavailable language, enlargement/reflow, reduced motion, storage failure and enhancement failure. Reader entry must not autoplay, silently change publication state or fetch every hidden illustration/media file.

## Page load and delivery

**WEB-PERF-01** Record reproducible before/after measurements for representative home, permanent poem/article and reader pages. Capture revision, route/language/mode, viewport, device/network/cache conditions, delivery environment, repeat count and raw evidence. Compare the same conditions, report variability and distinguish an asset inventory or local build from measured browser loading. Establish baseline-specific budgets; do not invent universal speed claims or conflate fewer bytes with faster observed loading.

**WEB-PERF-02** Deliver responsive images with reserved dimensions and correct priority for visible content; defer off-screen art and nonessential code. Preserve approved artwork masters/composition and stable derivative URLs on text-only builds. Deliver appropriate licensed script fonts, avoid unnecessary font variants and keep core text readable during loading. Quiet reading avoids eager interior artwork; reader/audio assets load only as needed. Verify caching and transfer behavior on the actual delivery path before making claims about it.

**WEB-PERF-03** Performance changes must preserve source/translation coverage, language shaping, keyboard access, readable enlargement, sharing metadata, anchors and service failure behavior. Record asset budgets and comparable loading evidence in the site’s adoption record; improve observed bottlenecks before broad refactoring. A compression or lazy-loading change does not authorize replacing source art, dropping script glyphs or omitting content.

## Comments and likes

**WEB-RESP-01** Every public poem and article has one Like control and a compact Comments disclosure. This includes Utkal Project articles and illustrated or text-led poems. The permanent page hosts responses outside focused reading. A utility page without a poem or article can record this as not applicable; articles cannot use that exception.

Use stable content identifiers, an explicit moderation state and clear success or failure messages. Keep text on failed submission and prevent accidental duplicate submissions. Pending submissions and private correspondence remain private; only reviewed public fields reach public comments. Anonymous likes are browser-identity responses, not verified-person votes.

**WEB-RESP-02** Use Firebase for likes, comments and private feedback. Readers submit and read permitted responses on the website; do not send them to GitHub Issues, Git forms or repository discussions. Git remains an internal publishing/development tool. The public interface does not expose moderation inboxes, production queues, prompts or administrative dashboards.

**WEB-RESP-03** Use the same Firebase operating process and compatible service contract across the fleet: content IDs, like state, pending submissions, reviewed public comments, private feedback, failure recovery, access-rule verification and moderation. Each site owns its Firebase project, configuration, authentication settings, reader records and moderation decisions. Shared code receives site configuration; it does not hard-code another site's project identity. Do not copy another site's credentials or automatically publish comments during adoption. Existing services remain available until the tested replacement is ready; do not remove a working response path before its replacement exists.

## AI use and attribution

**WEB-AI-01** Maintain one public page per site explaining how AI is used for imagery and translation, the Human Natural approach, human editorial responsibility and review limitations. Link it once through ordinary site navigation, such as About or the footer. An existing colophon can serve this purpose; do not create competing disclosure pages.

**WEB-AI-02** Remove repeated generic “AI-generated”, “AI-assisted” and model-credit notices from poems, articles, bylines, image captions and routine page footers. Do not replace them with per-page links or badges that recreate the same clutter. Keep detailed prompts, versions and assistant contributions in internal provenance. Preserve human author, translator and photographer credits, actual licences and any asset-specific attribution obligations.

**WEB-AI-03** Central disclosure does not turn an illustration into documentary evidence. Describe content accurately when its status changes the meaning: a reconstructed scene should not be presented as a historical photograph, and an adaptation should not be presented as the exact original. These contextual descriptions serve the work; they are not repetitive tool credits. Do not claim that every translation has human review when it has not.

## Google usage analytics

**WEB-ANALYTICS-01** Use the same Google Analytics setup, consent, event and verification process across the fleet. Each site has its own Analytics property/data stream and measurement configuration. Shared code receives the site configuration; analytics data remains in that site's property. Common event names, field meanings and firing rules make comparable measures possible without sharing a property or reader database. Reading and listening work when analytics is declined or blocked. Preserve current privacy signals, consent withdrawal and advertising restrictions in each site's implementation.

Use a common vocabulary for content views, language choices, reader entry, sharing and listening milestones. Define when each event fires and which stable content identifier it uses. Do not send comment text, contact fields, search text or private contribution content. Statistics describe measurable activity, not the whole audience.

## Accessibility and sharing

Use semantic headings, named controls, visible keyboard focus, readable status messages and useful image alternatives. Test narrow screens, keyboard operation, enlarged text and every supported script. Informative media needs alternatives suited to its content. Decorative backgrounds must not compromise contrast.

Check ordinary text at 4.5:1 contrast and qualifying large text at 3:1, following [W3C contrast guidance](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html). Check ordinary page reflow at 320 CSS pixels; content that requires two-dimensional layout needs an appropriate handling strategy under [W3C reflow guidance](https://www.w3.org/WAI/WCAG22/Understanding/reflow.html). The fleet's 44px standalone-control target is a design choice; [WCAG 2.2 minimum target guidance](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html) defines 24px with specified exceptions. These checks do not establish full accessibility conformance.

**WEB-SHARE-01** Every public page has an intentionally associated sharing image, including home, poem, article, profile, catalogue and utility pages. Use the page's own illustration, cover or portrait where appropriate. A section or site fallback is allowed when intentionally mapped; a sharing image does not require adding visible art to a deliberately text-led page or generating a unique image for every URL.

**WEB-SHARE-02** Render a useful title, description, canonical URL, Open Graph image and matching large-image Twitter card metadata in the initial HTML. Image URLs are absolute public HTTPS URLs, with descriptive alternative text and correct dimensions/type. Verify the exported asset is retrievable. Keep private and editorial routes out of public sharing metadata and release exports. A correct metadata tag does not prove that a sharing platform has refreshed its cached card.

**WEB-SHARE-03** Every poem and article has a labelled Share action and a Copy link fallback. Share the permanent content URL, preserving the selected available language where applicable. Cancelled sharing is not an error; announce successful copying and handle unavailable clipboard access. Sharing works without analytics consent, sign-in or a GitHub account. Reader-mode placement can vary, but each work's permanent page supplies the action.

## Adoption and maintenance

Each site records its shared versions, page-family coverage, theme values, overrides, source evidence and relevant checks. Common module boundaries and operating contracts are defined in [website platform contracts](website-platform-contracts.md). Site-specific implementations and live configuration are adopted separately.

Use the companion [adoption template](../templates/website-adoption.json) and [page checklist](../review/website-page-checklist.md). Distinguish observed implementation, documented behaviour, unverified areas, intentional differences and work still needed.

Trial one foundation change across representative pages before expanding it. Check actual rendering and behaviour, then update the site rulebook and adoption record together. Publish a change log with compatibility, affected pages and recovery instructions. Drift checks flag differences for review; they do not overwrite site decisions or deploy changes.

### Source principles

This draft draws on the maintained Utkal Design System rc.5, Kabita Live's website rulebook and design guide, Singhasan's current book rulebook and design system, and Free to Dream's privacy and listening implementation. The fleet review pack preserves source paths and hashes. Project-specific approvals and artwork are not transferred by this document.
