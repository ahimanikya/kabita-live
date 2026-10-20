---
type: "Website checklist template"
title: "Utkal website page checklist"
version: "0.1.0-draft.5"
status: "candidate_for_site_adoption"
---

# Utkal website page checklist

Use this checklist when adding a page, changing shared website behaviour or preparing a release. Follow the [shared website standard](../reference/website-standard.md). Record the relevant result as passed, failed, not checked or not applicable, with evidence or a reason. A checkbox is a prompt to verify, not proof that the page passes.

## Scope and identity

- [ ] **WEB-INHERIT-01:** Common rules are inherited from the pinned Blueprint baseline; the local rulebook identifies its own extensions and overrides.
- [ ] **WEB-INHERIT-02:** Each override names the affected rule/component, local value, rationale and actual decision. A local theme or layout change does not waive common privacy/content requirements.
- [ ] **WEB-INHERIT-03:** The base change has been checked against local extensions; adopted versions and any pinned offline copies remain traceable.

- [ ] **WEB-STRUCT-01:** The project is independently modelled as a Blueprint instance with its own root configuration, canonical KB, persona model, records, maintenance tools and source tree. It does not use a combined fleet KB or operating roster. Adoption status and any temporary compatibility paths are recorded.
- [ ] **WEB-STRUCT-02:** Blueprint persona definitions are linked or versioned; actual project assignments, human supervision and authorized scope are explicit. No activation or access is inferred from a copied template.
- [ ] **WEB-STRUCT-03:** The change respects KB/source/public boundaries. Internal records are excluded from the website export, and migration preserves source inputs, builders and saved data.
- [ ] Identify the site, page family, exact routes, content ID, changed sources and shared versions.
- [ ] Preserve the site's approved masthead, colours, signature, artwork and explicit theme overrides.
- [ ] Edit the maintained source or builder and regenerate pages; preserve original text, attribution, existing URLs and unrelated work.

## Type and surfaces

- [ ] **WEB-TYPE-01:** Semantic typography/spacing and recorded local exceptions preserve shaped scripts, verse/prose and readable enlargement.
- [ ] **WEB-DESIGN-01:** Pinned foundations and local themes preserve identity, masters, legibility and accessible utility icons.

- [ ] Display, reading and interface type use their correct roles. Published scripts have appropriate fonts, natural shaping and correct direction.
- [ ] Verse wording, punctuation, authored line breaks and stanza boundaries remain intact. Prose wraps naturally. Long titles and verse remain readable.
- [ ] Spacing, prose measure and page insets follow the shared foundation or a recorded site exception. Enlargement does not clip text or hide controls.
- [ ] Cotton paper and selected earth/sea washes remain legible. Check contrast on the actual background; quiet/night surfaces follow their texture rules.
- [ ] Utility icons have named actions; decorative line art is hidden from assistive technology and stays clear of text.

## Images and sharing on every public page

- [ ] **WEB-SHARE-01:** The page has an explicit image association: its artwork, cover, portrait, or an intentionally mapped section/site fallback. A text-led page stays text-led where intended.
- [ ] **WEB-SHARE-02:** Initial HTML contains page-specific title/description, canonical URL, Open Graph image and matching Twitter card metadata. Image URL, alternative text, dimensions and type are correct.
- [ ] The sharing image is in the public export and retrievable at its absolute HTTPS URL. It does not accidentally select a favicon, footer ornament or unrelated thumbnail.
- [ ] Private review, inbox and production pages are excluded from the public build, sitemap and sharing data. Review records do not appear among reader content.
- [ ] State separately whether metadata, public retrieval and an actual platform card were checked. Do not claim a platform cache has refreshed from a source check alone.

## Share on poems and articles

- [ ] **WEB-SHARE-03:** Each poem and article has a visible, named Share action and a Copy link fallback, using the permanent content URL and the selected available language.
- [ ] Native sharing, cancellation, clipboard failure and successful copying have sensible behaviour. Sharing works when analytics is declined and when the reader has no account.
- [ ] Controls remain usable on a phone and with a keyboard; focused reading has a clear path back to the work's permanent page.

## Firebase responses

- [ ] **WEB-RESP-01:** Every public poem and article, including Utkal articles, has one Like control and a compact Comments area on its permanent page. Do not mark an article not applicable.
- [ ] **WEB-RESP-02:** Comments and feedback stay on the website through Firebase. No GitHub submission requirement, public issue inbox or developer dashboard appears in the reader flow.
- [ ] Like state/counts and unlike behaviour use the site's stable content ID and tested service contract. Do not present browser identities as unique people.
- [ ] A submitted comment is private and pending until moderation. Readers cannot publish their own submission or access another reader's private data. Only the permitted fields reach public comments.
- [ ] Private feedback is separate from public comments and remains private. Success appears only after a successful write; failure retains the typed message and allows recovery without accidental duplicates.
- [ ] **WEB-RESP-03:** The site's own Firebase configuration and service rules are used. Check signed-out/unavailable service behaviour and the affected access rules before adoption.
- [ ] A replacement response path is tested before removing the working path. Existing reader records and content IDs are preserved or deliberately migrated.

## AI explanation and editorial integrity

- [ ] **WEB-HUMAN-01:** Image workflow uses the actual source meaning/identity, preserves approved masters and records provenance/review without presenting generated art as documentary proof.
- [ ] **WEB-HUMAN-02:** Translation preserves source meaning, emotional turn, culture and uncertainty; drafting/self-review/fluent review/acceptance/publication remain distinct.

- [ ] **WEB-AI-01:** One public AI-use page or colophon explains image and translation assistance, the Human Natural approach and human review responsibility. It is reachable through normal navigation.
- [ ] **WEB-AI-02:** Poems, articles, bylines, captions and routine footers do not repeat generic AI badges, model credits or disclosure links. Human credits, licences and specific attribution obligations are retained.
- [ ] **WEB-AI-03:** Necessary content context distinguishes depiction, translation and adaptation without claiming documentary evidence or human review that does not exist.
- [ ] Original sources, drafts, prompts, image versions and actual review status are preserved in the appropriate internal records, outside the public export.

## Reader and analytics

- [ ] **WEB-READER-01:** Shared core and local adapters support explicitly ordered available public book/edition/topic/category/location entries, with stable identities and sources.
- [ ] **WEB-READER-02:** Settings, fallback, anchors and legacy saved data remain compatible across poem/prose layouts; migration has recovery evidence.
- [ ] **WEB-READER-03:** Focused reading retains complete text/citations and contextual exit; enlargement, reduced motion, unavailable language/storage and enhancement failure are checked.

- [ ] Reader entry, enlargement, quiet surface, language fallback, saved place and exit behaviour work for the affected page family. Article prose does not use poem pagination.
- [ ] Existing saved-data formats still work or have a tested migration. Source text remains selectable and complete when enhancement scripts fail.
- [ ] Motion follows reduced-motion preferences; sound and playback require reader action. Artwork failure does not prevent reading.
- [ ] **WEB-ANALYTICS-01:** The shared Analytics process uses this site's own property/data stream and measurement configuration. Event meanings and firing rules match the shared contract.
- [ ] Google measurement follows the site's consent choice and privacy rules. Declining or withdrawing consent leaves reading, listening, sharing and responses usable.
- [ ] Events use stable content identifiers and the common vocabulary; no comment, feedback, contact or other private text is sent to analytics.

## Loading performance

- [ ] **WEB-PERF-01:** Comparable before/after browser evidence records revision, route/mode/language, viewport, delivery/cache/network/device conditions, repetitions and variability. Asset inventories are labelled separately.
- [ ] **WEB-PERF-02:** Visible content has deliberate image/font priority and reserved dimensions; responsive derivatives preserve composition/stable URLs. Hidden reader art/media and nonessential scripts load only when needed.
- [ ] **WEB-PERF-03:** Optimization preserves source/script coverage, readable enlargement, focus, metadata, anchors and service resilience. Baseline-derived budgets and residual issues are recorded without unsupported speed claims.

## Verification and release

- [ ] Inspect desktop, phone, 320px reflow and 200% enlarged text for the affected layouts. Check keyboard focus, names, reading order and actual surface contrast.
- [ ] Run relevant existing content/build checks and behaviour tests. For service changes, verify the affected failure paths and access rules; old results are not evidence for new code.
- [ ] Record which checks were automated, reviewed by the implementing assistant, reviewed independently or reviewed by a fluent human.
- [ ] Update the site rulebook, adoption record, exceptions and release evidence together. Record local preparation, repository publication, cloud-rule deployment and live verification separately.

Documentation-only changes need link and consistency checks. Do not require browser or service tests when their implementation has not changed. A passing checklist does not grant publication authority or establish whole-site accessibility conformance.
