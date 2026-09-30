# Kabita Live · Utkal Blueprint project

[Project knowledge](kb/index.md) · [Work dashboard](kb/registers/DASHBOARD.md) · [Icon catalogue](kb/assets/icon-catalogue.md) · [Adoption record](kb/reference/adoption.md)

Blueprint baseline 0.1.0-rc.1 and register model 1.0.0 are applied locally, with existing artwork and primary source paths preserved. `projects/site` points to the working static site.

Icon review: http://127.0.0.1:8771/icon-atelier.html · Research: http://127.0.0.1:8771/literary-study.html

The icon studies are candidates; application across the journal awaits design review. Earlier complete delivery ZIPs remain revision-39 snapshots; the new icon pack is versioned separately.

## Preserved project guide

A dedicated project for the Kabita Live magazine redesign.

## Start here

- Main working files: `output/kabitalive-design-proposal-2026-09-29/`
- Website: `output/kabitalive-design-proposal-2026-09-29/site/`
- Interactive approval desk: `site/design-system-review.html` inside the main working folder.
- Design system and branding: `brand-guide/` inside the main working folder.
- Portable handoff copy: `output/kabita-live-project/`
- All 47 cover artworks, previous design studies, editorial research, verification evidence and delivery ZIPs remain in the main working folder.

## Preview

The existing preview runs at http://127.0.0.1:8771/. To start it again from this project, run:

```sh
python3 -m http.server 8771 --bind 127.0.0.1 --directory output/kabitalive-design-proposal-2026-09-29/site
```

Review entry: http://127.0.0.1:8771/design-system-review.html#spacing

## Decisions and current status

Typography is locked: Noto Serif Oriya for Odia, Tiro Devanagari Hindi Regular for Hindi, Cormorant Garamond Medium for English display and Source Serif 4 for English reading. Keep the English-only Kabita Live masthead, approved earthy palette, paper surfaces and simple footer. Design, font and artwork credits are consolidated on Our Story.

The review desk contains 18 groups, five locked foundations and 13 groups awaiting review. Browser approvals are saved by origin; keep the same localhost address and port to retain them. Download decisions for a durable handoff. They do not automatically apply changes or publish the site.

## Move record

Both design folders were moved from Poem Without Borders and verified by SHA-256 before and after. Compatibility symlinks remain at the old paths so earlier chat links and the current preview continue working. No unrelated poetry or video files were moved. See FILE-MOVE-RECEIPT.json.

The existing chat, “Redesign Kabita Live magazine”, is now assigned to Kabita Live. Its working directory and project assignment were verified after the move. Continue work in this project.
