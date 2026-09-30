---
type: "Project record"
title: "Implementation and preservation map"
---

# Implementation and preservation map

The [storage layout](storage-layout.md) is the current file-organization guide. All non-site design sources, review pages, evidence, original artwork, histories and delivery packages now reside in the KB.

Website implementation remains at `output/kabitalive-design-proposal-2026-09-29/site`; `projects/site` points there. Preview: http://127.0.0.1:8771/ . Old review URLs retain that origin through relative compatibility links. Reader builders now read site-local content metadata. Public-only Astro export and cloud configuration are described in [the current architecture](site-architecture.md). Historical inputs stay in the KB.

Canonical brand-guide source: [brand guide](../artifacts/design/brand-guide/). Icon builder: [icon study generator](../artifacts/history/revisions/revision-40-literary-icons/build-study.py). Both generators locate the project through its configuration after the move. The design-system/icon KB views are maintained by `tools/sync_design_knowledge.py`.

The portable package remains `output/kabita-live-project`, with its own relative aliases and complete KB. Use `tools/sync_handoff.py` and `tools/check_storage.py`. Earlier standalone ZIPs stay in the [delivery archive](../artifacts/history/deliveries/).

Move inventory and hashes: [migration manifest](../records/storage-migration.json). Verification: [storage check](../records/storage-verification.json). Earlier [artifact inventory](../records/artifact-inventory.json) is historical and is superseded for current locations by the migration manifest.
