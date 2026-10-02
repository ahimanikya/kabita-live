---
type: "Asset audit"
title: "Image inventory and usage plan"
---

# Image inventory and usage plan

[Imagery finder and canonical captions](imagery.md) · [Open the visual catalogue](http://127.0.0.1:8771/image-library-audit.html) · [Complete file inventory](image-inventory.json) · [Cover filename mapping](../records/edition-cover-filenames.json) · [Poem matching evidence](../records/poem-art-match-evidence.json)

Inventoried **1384 physical image files**, **881 exact unique file contents**, and **317 compatibility aliases**. These counts include masters, delivery formats, thumbnails and evidence screenshots; they are not counts of unique artworks. The portable handoff and generated/dependency directories are excluded as copies. Historical ZIP contents were not unpacked.

| Intended role | Policy |
|---|---|
| Edition covers | 47 active identities, named `edition-NNN-YYYY-MM.webp`; `-480.webp` thumbnails; matching named master aliases. Each belongs to its own edition. Never selected for poems. |
| Poem artwork | 9 dedicated images, plus 14 previously generated inner-page illustrations reused where text motifs support them. Preserve original captions and provenance. |
| Inner pages | 14 existing watercolor openings. Can support related poem motifs; no cover reuse. |
| Homepage | LIFE AS IT IS remains the homepage identity. |
| People | Identity-bound writer/editor portraits and original reference photographs; never randomized. |
| Reserved | Pipili Chandua retained for future use, excluded from all automatic selection. |
| Textures, icons and brand | Interface assets, separate from editorial illustrations. |
| History and evidence | Alternate covers, early photographic concepts, superseded treatments and screenshots retained unchanged. |

## Earlier generations

All 96 image outputs in this chat’s generation folder were compared by SHA-256: 95 already had an exact copy in the project. The remaining early evening-water output is now preserved under `artifacts/artwork/recovered-studies/`. It closely resembles the earlier photographic cover concept; it is retained as a historical variant, not introduced as poem art.

## Poem connections

Title and body motifs are matched in Odia, Hindi and English, with evidence stored per poem. The current issue has targeted context-reviewed overrides, including rain → wet courtyard, a departed poet → empty chair, writing → notebook/pen, and freedom → open window. The remaining automated links are assisted suggestions, not a claim of full native-language editorial review. Neutral reading imagery is used where no clear motif is found. Relevant imagery takes priority over avoiding repeats.

## Preservation and review

No historical originals, portrait sources, cover studies or generation outputs were deleted. Exact duplicates are reported, not destructively deduplicated. Active cover delivery names changed with compatibility aliases retained. This is current-assistant self-review (`independent: false`), not publication approval.

## File counts by role

| Role | Files |
|---|---:|
| Other preserved material | 15 |
| Brand and interface | 15 |
| Portrait sources | 430 |
| Poem illustrations | 18 |
| Portraits | 448 |
| Reserved | 2 |
| Historical studies | 99 |
| Homepage artwork | 3 |
| Edition covers | 231 |
| Inner-page illustrations | 42 |
| Review evidence | 22 |
| Paper textures | 3 |
| Icons | 56 |
