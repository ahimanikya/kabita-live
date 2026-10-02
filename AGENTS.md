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

# Scoped background-work authorization

On 2026-10-01, Ahimanikya explicitly approved the writer-enrichment loop and confirmed “keep going in background”. The active `kabita-live-writer-enrichment` heartbeat may resume this same chat every 30 minutes and edit writer narratives and their KB records in sequential batches, with verification and handoff sync. This is a scoped exception to the default background-execution restriction above; it does not authorize subagent dispatch, publication, new portraits, new design choices, spending or messaging. See `kb/records/writer-enrichment-loop.json` and `kb/research/writers/enrichment-batches.json`.

## Scoped watercolor-portrait background authorization

On 2026-10-02, after approving watercolor artwork for every poet, Ahimanikya explicitly instructed: “ok run a batch mode and keep doing it auto mode till it is done - without getting trigger from me”. This authorizes a recurring heartbeat in this same chat every 20 minutes to continue the existing portrait queue without further prompts or batch approvals. Scope includes built-in image edits from identified saved source photographs, visual likeness comparisons, saving masters/provenance, integrating reviewed portrait assets locally, build/verification and KB/handoff updates. Work sequentially in groups of five; no overlapping workers or subagents. Preserve source photographs and all unrelated content. Do not invent missing faces or integrate material identity drift. No paid API fallback, new accounts, publication, push/deploy, new design choices or messaging. Save exact progress on interruption. Pause the portrait heartbeat when all actionable photographs are processed and verified; report missing-photo and likeness holds separately. The earlier writer-enrichment and translation automations remain paused. See `kb/records/poet-watercolor-loop.json` and `kb/research/writers/portrait-batches.json`.

## Portrait rollout final deployment authorization

On 2026-10-02, Ahimanikya additionally instructed: “Keep doing the loop once all done update git and website”. This supersedes the portrait loop's push/deploy prohibition only for the final rollout update, after all actionable portraits are processed and all integrated batches are verified. Commit and push the authorized portrait changes and necessary generated records to the existing GitHub repository, then deploy the public-only Astro build through the established manual GitHub Pages workflow and verify the live pages/assets. Preserve current preview/release gates, noindex settings, disabled services and DNS/custom-domain state unless separately authorized. No intermediate-batch deployment, force push or unrelated changes. Missing-photo and likeness holds retain their existing photos/initials and must be reported separately; independent author/editor review remains pending. Pause the portrait heartbeat only after successful final deployment and live verification; persist an exact resume point if interrupted. See `kb/records/poet-watercolor-loop.json`.
