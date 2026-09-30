# Blueprint entrypoint

Read `kb/index.md`, `kb/TEAM-CHARTER.md`, `kb/Working-Agreement.md`, `kb/registers/DASHBOARD.md` and the latest activity before substantive work. The root `utkal.config.json` identifies this KBL instance. Keep canonical records in `kb/`; preserve source and decision provenance. No human reports to AI. Four KBL persona assignments are explicitly authorized by KBL-DEC-005; read `kb/team/operating-model.md`, `kb/team/assignments.json` and the relevant `kb/roles/` brief before substantive work. Use these as on-demand roles in the current chat, not automatic subagent dispatch or background execution. Same-assistant role changes remain self-review. Run `python3 tools/check_personas.py` when team or role records change. Regenerate records with `python3 tools/registers.py` and `python3 tools/catalog.py`; check structure with `python3 tools/check_bundle.py`. The icon catalogue and design-system reference are refreshed with `python3 tools/sync_design_knowledge.py`; the design-guide source now lives in `kb/artifacts/design/brand-guide`.

# Kabita Live project

This project contains the magazine redesign and its complete design history.

- Use `output/kabitalive-design-proposal-2026-09-29` as the primary source. `output/kabita-live-project` is the portable handoff copy.
- Read the root README, `kb/reference/storage-layout.md` and `kb/artifacts/design/brand-guide/DESIGN-SYSTEM.md` before changing design decisions.
- Treat the site as the replacement publication: no reader-facing references or links to the former site. Keep provenance in the KB. Read `kb/reference/site-architecture.md` before changing routes, content, analytics or feedback.
- Launch engagement is social sharing and private feedback; no public comments. Firebase and GA4 remain disabled until project/property setup and real configuration checks. Never mark metadata-only pages as a complete archive.
- Follow Utkal Project’s GitHub stack: Astro/Node 24, GitHub repository, GitHub Actions and GitHub Pages. Firebase is only for private runtime features; publication content and the KB stay in Git. Keep ZIP archives in Git LFS and do not enable push-triggered publication.
- Export only the public Astro build, never the raw preview directory or KB. Keep the content-release gate and consent safeguards.
- Store all non-site work in the KB: design sources, research, review material, artwork masters, evidence, revision history and delivery snapshots. Old output paths are compatibility links only. Do not create new supporting files beside the site.
- Sync with `python3 tools/sync_handoff.py`; verify with `python3 tools/check_storage.py`.
- Preserve approved fonts, colours, English-only masthead, Odia signature, art and footer decisions. New component options await explicit user approval via discussion or the design-review desk.
- Browser preview decisions are local review records, not automatic authorization to publish the website.
- Preserve all artwork masters, historical studies, cultural narratives, portrait sources and font licenses. Never silently replace historical magazine originals.
- The existing localhost:8771 preview can remain in use. Keep the origin stable to preserve the user’s local review decisions.
- Do not import the unrelated Adigandha video/character instructions from Poem Without Borders.
- Keep the main and portable handoff files consistent when completing approved changes.
