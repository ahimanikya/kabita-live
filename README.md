# Kabita Live

[Open the knowledge base](kb/index.md) · [Work dashboard](kb/registers/DASHBOARD.md) · [Persona team](kb/team/operating-model.md)

The website is a self-contained replacement publication, built with Astro and published through GitHub Actions to GitHub Pages. GitHub is the source of truth for site content, artwork, the KB and project history; large delivery archives use Git LFS. [Architecture, setup and launch dependencies](kb/reference/site-architecture.md) document the Astro build, private Firebase feedback and consent-based GA4 integration. The public GitHub repository and Firebase project/web app exist; anonymous Auth is enabled. GitHub Pages is configured for manual Actions delivery. Mumbai Firestore and private-feedback rules are configured. The local archive contains 47 editions, 799 active full poem records and two preserved unavailable entries. All 427 researched profile narratives are applied. Book reviews are excluded from publication; analytics, live integration checks and remaining editorial reconciliation remain pending. [Account setup status](kb/records/account-setup.json).

All research, design documentation, artwork masters, studies, review evidence, historical revisions and delivery snapshots live in `kb/`. Start with [the storage map](kb/reference/storage-layout.md). For earlier images, captions and reuse, open the [imagery finder](kb/assets/imagery.md).

The website remains in `output/kabitalive-design-proposal-2026-09-29/site`; `projects/site` points to it. Preview: http://127.0.0.1:8771/ . Keep this origin to preserve local design-review decisions.

Old document and preview paths are compatibility links into the KB. Create new supporting work in the KB. The portable package is `output/kabita-live-project`, with its own site, KB, tools and relative links.

Run `python3 tools/sync_handoff.py` to sync the handoff. Check with `python3 tools/check_storage.py`, `python3 tools/check_personas.py`, `python3 tools/registers.py --check`, `python3 tools/catalog.py --check`, and `python3 tools/check_bundle.py`. Refresh the derived design/icon knowledge with `python3 tools/sync_design_knowledge.py`.

Blueprint baseline: 0.1.0-rc.1; OKF: 0.2; register model: 1.0.0. Four personas operate on demand under Ahimanikya’s supervision. Website publication remains separately authorized.

The current project is authorized for a GitHub Pages preview before DNS migration (KBL-DEC-037). The manually dispatched workflow distinguishes a noindex hosted preview from an editorially gated full release. See [hosting status](kb/records/github-pages-preview-deployment.json).

Hosted preview: [Kabita Live](https://ahimanikya.github.io/kabita-live/). The initial deployment passed on 2 October 2026; DNS is unchanged and search indexing remains disabled until release review. The deployment record identifies the exact live commit; subsequent local changes do not automatically publish.
