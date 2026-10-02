---
type: "Content import evidence"
title: "Complete edition and poem capture"
---

# Complete edition and poem capture

User direction: “Now let's extract all editions and poems for each one of them and link them up. Keep the content organized by edition.”

## Captured publication

All 47 observed edition contents pages and their 796 poem links were captured. Writer contribution lists supplied five additional poem records. The resulting collection contains **801 full-text poem records**, of which **800 have explicit edition metadata**. These are source records, not a claim of 801 distinct literary works: identical texts and variants are preserved for editorial reconciliation.

The browser contents capture and raw HTML contents order agree on all 47 editions. Each edition retains that order. Four additional writer-listed records are appended to their explicitly recorded editions: 145 / Issue 4, 312 / Issue 13, 361 / Issue 17 and 424 / Issue 20. They are marked `listed: false` in content data rather than represented as original contents-table entries.

The reader site now provides complete poem readers, all edition contents, next-poem and return-to-edition navigation, reciprocal writer contributions, full-text/title/author search and reading-language filters. Existing approved artwork, type, masthead, footer and reading controls are retained. Two source-linked writers absent from the captured directory, Gargi Sarkhel Bagchi (258) and Nutan Sarawagi (416), have factual minimal profiles and contribution links. The reader directory therefore has 429 records; only 427 have individual profile captures. No biography or portrait was invented for the additional two.

## Organization and evidence

Canonical reader content lives in `projects/site/content/editions/issue-01` through `issue-47`, with an `edition.json` membership manifest and one `poem-ID.json` per poem. `index.json` is the collection manifest. The one unresolved source record remains under `unassigned`. Public content contains no source-site dependency. Raw HTML, receipts and research remain in the KB, outside the public build.

- [Browser edition capture](editions/captured-editions.json)
- [Source receipts: 848 pages](editions/source-receipts.json)
- [Preserved source files](../artifacts/content-import/editions/)
- [Import summary](editions/import-summary.json)
- [Normalization evidence](editions/normalization-evidence.json)
- [Explicit contact-line review](editions/contact-line-review.json)
- [Automated integrity checks](../records/edition-content-verification.json)
- [Browser review](../records/edition-browser-verification.json)

The source pages redirected when requested without their referring edition URL. Following the observed edition links, and using those same URLs as the HTTP Referer for read-only capture, returned the actual content. No authentication bypass or guessed private endpoints were used. Raw bytes and SHA-256 receipts preserve source evidence, including malformed UTF-8 in truncated contents-table labels. Reader titles come from the complete poem headings; none of the imported titles, bylines or bodies contains replacement-character decoding errors.

The importer isolates the source poem region before parsing HTML. This matters for poems 680 and 582, whose malformed Word-style markup otherwise swallowed comments and footer images. Those unrelated regions are excluded. Unicode text, line breaks, stanza boundaries and literary notes are retained. HTML presentation whitespace is normalized. Explicit appended phone/email contact lines and template end marks are removed from reader text with an evidence trail; the original source remains intact. Imported text still requires editorial proofreading.

Reproduce with Node 24: run `tools/import_editions.mjs`, then the site's normal build. `tools/check_editions.py` verifies manifests, exact normalized text/stanza parity, contents order, writer links, next/back links and all 848 source hashes. The capture tool is resumable and reuses hash-verified source files.

## Editorial reconciliation queue

| Record | Source evidence | Treatment |
|---|---|---|
| Poem 30, ଭଲ ପାଇଛି ବୋଲି | Issue 2 has no author name or usable author link | Display “Author not recorded”; no invented writer |
| Poem 645, Yesterdays, Nisha Raviprasad | No edition recorded; body is identical to poem 650 in Issue 36 | Preserve under unassigned; flag as possible duplicate rather than silently assigning/merging |
| Poems 268 and 304, Crossing | Identical body and writer, explicitly associated with Issues 11 and 13 | Preserve both edition appearances |
| Other repeated titles | May be revisions, variants or different poems | Preserve source IDs; no title-based merging |

The four supplementary entries and the two newly found writer identities are listed above for editorial review. Counts refer to captured records, and source identifiers remain stable.

## Verification and scope

All 47 edition manifests, 801 reader texts, 800 reciprocal writer links and 848 source hashes pass automated checks. The production-format static build passes public-link and source-dependency checks. Browser review verifies body-text search, language/no-result behavior, historical share metadata, writer directory filtering, and 360-pixel layouts in the three scripts at 32-pixel reading size. This is self-review, not accessibility certification or publication approval. Mobile measurements were taken from live DOM; screenshot scaling artifacts in the browser prevented reliable screenshot-based visual certification.

Execution followed Disha (scope), Anvesha (source capture), Samanta (implementation) and Drishti (verification) role passes within the same assistant. No independent agent review occurred. Remaining review texts, metadata reconciliation, biography/portrait enrichment, design approvals and service configuration remain separate launch work. No deployment, domain change or remote push was performed.
