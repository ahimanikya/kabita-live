# Kabita Live

Current publication: **November 2026 · Issue49**, 49 editions and 828 active full poems. December Issue50 is a private draft. See [latest editorial release](kb/records/editorial-release-2026-11-01.json). Counts and setup descriptions in the original overview below are historical checkpoints; use the current registers for outstanding work.

[Website rulebook](kb/reference/website-rulebook.md) · [New page checklist](kb/review/new-page-checklist.md) · [Open the knowledge base](kb/index.md) · [Work dashboard](kb/registers/DASHBOARD.md) · [Persona team](kb/team/operating-model.md)

The website is a self-contained replacement publication, built with Astro and published through GitHub Actions to GitHub Pages. GitHub is the source of truth for site content, artwork, the KB and project history; large delivery archives use Git LFS. [Architecture, setup and launch dependencies](kb/reference/site-architecture.md) document the Astro build, private Firebase feedback and consent-based GA4 integration. The public GitHub repository and Firebase project/web app exist; anonymous Auth is enabled. GitHub Pages is configured for manual Actions delivery. Mumbai Firestore and private-feedback rules are configured. The local archive contains 48 editions, 810 active full poem records and two preserved unavailable entries. All 432 researched profile narratives are applied. Edition 48 is included in the published discovery site; use the [Edition Sync Playbook](kb/production/edition-sync/PLAYBOOK.md) for subsequent imports. Book reviews are excluded from publication. Consent-based GA4 is live and verified. Firebase feedback, Likes and moderated public comments are active and verified. Per-page sharing previews are deployed; editorial reconciliation and translation review remain separate. [Account setup status](kb/records/account-setup.json).

All research, design documentation, artwork masters, studies, review evidence, historical revisions and delivery snapshots live in `kb/`. Start with [the storage map](kb/reference/storage-layout.md). For earlier images, captions and reuse, open the [imagery finder](kb/assets/imagery.md).

The website remains in `output/kabitalive-design-proposal-2026-09-29/site`; `projects/site` points to it. Preview: http://127.0.0.1:8771/ . Keep this origin to preserve local design-review decisions.

Old document and preview paths are compatibility links into the KB. Create new supporting work in the KB. The portable package is `output/kabita-live-project`, with its own site, KB, tools and relative links.

Run `python3 tools/sync_handoff.py` to sync the handoff. Check with `python3 tools/check_storage.py`, `python3 tools/check_personas.py`, `python3 tools/registers.py --check`, `python3 tools/catalog.py --check`, and `python3 tools/check_bundle.py`. Refresh the derived design/icon knowledge with `python3 tools/sync_design_knowledge.py`.

Blueprint baseline: 0.1.0-rc.1; OKF: 0.2; register model: 1.0.0. Four personas operate on demand under Ahimanikya’s supervision. Website publication remains separately authorized.

Live site: [Kabita Live](https://kabitalive.com/). The [Ink & Voice release record](kb/records/ink-voice-publication-2026-10-20.json) identifies the published commit and checks. Discovery publication remains separate from the unresolved full editorial release gate.

Every website publication requires **Ahimanikya Satapathy’s explicit approval of that release**. Editors and other contributors may push to Git within existing access; pushes do not publish the site. The manual owner-only workflow uses the protected github-pages environment with ahimanikya as sole required reviewer and no administrator bypass. [Publication policy](kb/records/website-publication-approval-2026-10-20.json) · [Confirmed editorial team](kb/team/publication-editors.json) · [Blueprint reconciliation](kb/records/blueprint-sync-editor-roles-2026-10-20.json).
