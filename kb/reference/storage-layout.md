---
type: "Project record"
title: "Where project work lives"
---

# Where project work lives

**Kabita Live knowledge is canonical in `kb/`.** The user requested that everything we have done outside the website move here. This is the current organization; earlier path notes in archived documents describe their historical layout.

| Material | Canonical location |
|---|---|
| Design system, brand-guide source, editorial tools and proposal | [Design](../design/index.md) |
| Original artwork, portrait sources and reserved Pipili work | [Assets](../assets/index.md) |
| Interactive design studies, component reviews and browser audit fixtures | [Reviews](../review/index.md) |
| Revision snapshots, former branding and delivery ZIPs | [History](../history/index.md) |
| Captures, migration receipts and verification | [Evidence](../evidence/index.md) |
| Research, decisions, roles and work tracking | Existing `research/`, `records/`, `roles/`, `team/`, `registers/` |

`kb/artifacts/` stores original documents, exports and source assets without adding metadata inside historical files. Typed KB documents and section indexes explain these materials. The local Blueprint catalogue/link checker excludes raw artifacts from concept normalization, while the migration verifier checks their paths and hashes. The pinned upstream checker is preserved unchanged in the source snapshot.

## Website and tools

The running website stays at `output/kabitalive-design-proposal-2026-09-29/site`, with `projects/site` as its convenient entry point. Reader pages, required web images, fonts/licences, CSS, JavaScript, templates, content data and build code remain part of the website. Root `AGENTS.md`, `README.md`, configuration and maintenance tools remain operational entrypoints.

Old supporting-file locations are relative compatibility links into the KB. The same applies to local review URLs and artwork downloads. These are aliases, not competing source copies. The shared `localhost:8771` origin is unchanged; no browser decisions are read, cleared or migrated.

Do not treat every file reachable from the local preview as a public deployment package. The KB contains design history and internal review evidence; publishing the public journal remains a separate, scoped task.

## Working and handoff rules

Create new non-site deliverables in the appropriate KB section. Put their supporting binary/raw files under `kb/artifacts/`. Link substantive artifacts from a current KB document or section index. New website components belong in the site source; exported review versions can be served through compatibility links.

The portable handoff has its own complete `kb/`, site and tools, with relative links resolving inside the package. Synchronize with `tools/sync_handoff.py`; its canonical source is this workspace. Preserve or reject unexpected divergent handoff files rather than silently overwriting them. Historical ZIP snapshots remain untouched.

Use `tools/check_storage.py` to verify old paths, preserved hashes, the website file inventory and portable parity. Run the usual persona, register, catalogue and bundle checks after changes to the KB.
