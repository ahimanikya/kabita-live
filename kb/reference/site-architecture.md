---
type: "Architecture decision"
title: "Standalone journal, private feedback and analytics"
---

# Standalone journal, private feedback and analytics

Kabita Live is the replacement publication website. Reader journeys, issue navigation, writer pages and sharing must be self-contained. Historical research belongs in the KB; public pages must not send readers to the former site or describe themselves as a comparison with it.

## Utkal Project comparison

Reviewed Utkal Project at commit `5ce3e2494488f7d5e273a035274108dc8b8861ae`. Its actual site uses Astro 7.3.5 and static GitHub Pages delivery. Its architecture records propose Firebase Auth/Firestore for private intake and GA4 with explicit consent; those integrations are planned there, not evidence of a working shared backend. The [pinned source files and hashes](../artifacts/research/utkal-stack-2026-09-29/SOURCE.json) distinguish implementation from plans.

The user confirmed GitHub as the project store and GitHub Pages as the website host. Kabita Live follows that separation: public content in Git and static pages; Firebase for private reader messages; no public comment collection. It has its own configuration and must not reuse another project's credentials, users or private records.

## What is implemented locally

| Area | Current state |
|---|---|
| Public website | Existing approved layouts generated into an Astro static build. Public-only selection prevents KB, review pages, builders and research from entering `dist`. |
| Content | Local metadata and local routes for issues, poems, writers and reviews. Original source URLs remain only in non-exported source/provenance inputs. |
| Search | Existing reader search remains. Pagefind produces an index during build; a new Pagefind search interface has not been added. |
| Sharing | Copy, caption, native sharing and social links use this site's local poem route. No legacy-site fallback. |
| Feedback | Private form; currently opens an email draft that the reader must send. Once configured, Firebase anonymous Auth and Firestore save messages privately. No public comments at launch. |
| Analytics | GA4 adapter prepared, disabled without a valid property and approved HTTPS host. Explicit opt-in is available in Our Story once configured. No tag loads without consent. |
| Fonts | Approved font choices retained. Source Serif 4 now loads locally with its OFL licence, alongside the other local fonts. |
| Git | Local repository on `main`; ZIP archives assigned to Git LFS, with the local LFS hook enabled. Public remote `ahimanikya/kabita-live` created and connected; initial source commit and all nine LFS archives uploaded. |
| Hosting | GitHub Pages selected. Utkal-style manual GitHub Actions workflow prepared; uploads only the static site. No Firebase Hosting. |
| Publication | Local preview and production-format build only. Firebase project/web app created on Spark and anonymous Auth enabled. Mumbai Firestore and tested private-feedback rules are deployed. GA4 remains pending. No website deployed or editorial login created. |

## Content readiness is a separate gate

The edition import now contains **47 edition contents, 799 active poem records and two archived entries**, with 798 active poems assigned to editions. The two unavailable entries are absent from edition navigation and the active reading/search lists; their existing URLs show a neutral poem-unavailable notice. The unavailable-record listing and Archived entries labels are omitted from reader pages at the user’s request; records remain in the KB. Original captures and separately headed works extracted from three composite entries are preserved in the KB. Glacier’s duplicated full-text block has also been reconciled to one intact copy, with matching translation ranges retained. See the [content reconciliation](../records/poem-content-reconciliation.json) and [writer-audit follow-up](../records/writer-audit-followup-2026-10-02.json). There are 429 writer records (427 individual profile captures plus two source-linked writers discovered in the poem archive). Reader routes, full-text search and reciprocal edition/writer links are local and self-contained. See the [capture and reconciliation record](../research/edition-content-import.md).

One source record has no edition, one has no author, and two pairs of identical texts await editorial reconciliation. Complete review texts and remaining biography/portrait work are still outstanding. Preserve source stanza breaks, script, byline, translator and edition relationships; do not infer absent metadata or silently merge duplicate records.

`data/content-status.json` records these gaps. `npm run check:release` currently refuses release. A build passing is not publication readiness. Local/staging pages retain `noindex`. `npm run build:release` regenerates and checks content readiness before producing an indexable public export; it currently refuses release. This does not change local preview pages.

## Build and handoff

Work in `projects/site` (alias to the primary site folder). Use Node 24 and Python 3. Run:

```sh
npm ci
npm run build
npm test
npm run test:rules
npm run check:release
# After content is complete and the release is approved:
npm run build:release
```

The rules command additionally requires Java 21+ and uses only the local `demo-kabita-live` emulator. It does not deploy rules or submit live feedback. The current machine's older default Java needs a suitable runtime selected for that command.

`build.py` creates reader HTML from local inputs. `standalone-support.py` and `standalone-pages.py` keep routes/copy self-contained. `edition-pages.py` renders the complete local edition manifests and full poem texts. TypeScript feedback is bundled locally. `build-public.py` validates reader links and chooses only required web assets; Astro writes the deployable `dist` folder and Pagefind indexes it. Never publish the raw workspace, KB or the Python preview directory. The `localhost:8771` preview origin remains unchanged for design review.

Sync the portable source with `tools/sync_handoff.py`. Dependencies, generated staging folders, `dist`, debug logs and `.git` are excluded. Install dependencies and build inside the portable site when using it independently. Run `tools/check_storage.py` for current parity; `--migration` is specifically the historical unchanged-site baseline and is not applicable after intentional reader-site changes.

## GitHub storage and publishing

The repository stores maintained website source, editorial content, art, font licences, complete KB and preserved history. Four existing delivery ZIPs exceed 100 MiB; `*.zip` is assigned to Git LFS so those originals can be retained in GitHub too. Derived handoff duplicates, dependencies, generated build output and local debug logs remain reproducible/ignored. On a new clone, install Git LFS and run `git lfs pull` to retrieve historical archives. Website builds do not need those ZIPs.

Private feedback messages, authentication records and secrets are runtime data, not publication source. They stay in Firebase or the editorial email service, never a public repository. The user explicitly approved making `ahimanikya/kabita-live` public for Pages. This exposes the source, KB and artwork history as well as the reader site. Visibility was changed and verified; no domain cutover or website deployment has occurred.

`.github/workflows/publish-site.yml` follows the [inspected Utkal workflow](../artifacts/research/utkal-stack-2026-09-29/publish-site.yml): manual dispatch, `main`, initiating repository owner, explicit release selection, `github-pages` environment, and separate build/deploy jobs. It uses Node 24, Python 3.12, Java 21 for local Firebase rule tests, locked npm dependencies, the release content gate, and the public `dist` artifact. There is no deployment on push. The portable handoff includes an equivalent workflow with `site/` paths.

Pages metadata supplies `SITE_URL` and `SITE_BASE` to Astro. The local default stays `/`; repository-path hosting and a later custom-domain root are supported without changing the existing localhost origin. Reader links and runtime configuration URLs are relative. GitHub Pages must use **GitHub Actions** as its publishing source. Pages is configured with `build_type=workflow`; no workflow has run or deployed. Environment release controls and the future custom domain still need launch review.

[GitHub Pages workflow documentation](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages) and [large-file limits](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github) informed this setup. [Local verification](../records/github-pages-verification.json) records the build and release-gate checks.

## Configuration still needed

1. Firebase project `kabita-live` and web app are created; anonymous Auth is enabled. Firestore is created in Mumbai (`asia-south1`); only anonymous Auth is enabled. Review domain authorization if OAuth providers are introduced; the client production-host guard remains empty until launch checks. [Account setup record](../records/account-setup.json) tracks verified and pending steps.
2. Reviewed Firestore rules are published and reloaded text matches the tested source. Complete a live end-to-end intake test and restrict editor access through maintainer-issued custom claims. Publication job titles do not grant backend access. An editor inbox UI is not yet implemented.
3. Review retention and abuse controls before enabling intake. Current rules enforce field limits and a 60-second per-anonymous-UID interval, not a global spam barrier. App Check and broader rate protection are not configured. No file uploads, Storage or Cloud Functions are implemented.
4. Create a GA4 property/web stream and add its Measurement ID. Disable automatic enhanced measurement where it could collect unintended fields; verify the property settings and a consented test visit before launch.
5. Populate `runtime-config.json` with each service's public web configuration, allowed production hosts and enabled state only after setup/testing. Never put service-account keys or private credentials there. Firebase web configuration is not an authorization boundary; deployed rules are.
6. Finish review-text import, metadata reconciliation and editorial proofreading; complete the existing design reviews and enlarged-text check. Source and LFS history are uploaded; GitHub Pages uses Actions. Review its launch controls, review public output, then run the manual publishing workflow under release direction.

Analytics sends explicit page views with query strings/fragments removed and a limited set of share events. It does not send message text, names or email addresses. Opt-out disables further custom events and reloads the page. Google account/property settings still need review; local adapter tests are not proof of the eventual production configuration.

## Verification and limits

See [local implementation verification](../records/standalone-verification.json), [desktop/phone browser checks](../records/standalone-browser-checks.json), and [font source record](../records/source-serif-local.json). Three analytics tests and five Firestore emulator tests passed. Six representative reader routes passed automated checks at 1280px and 360px. The complete public build was checked for missing local links and forbidden legacy dependencies.

This is self-review. It does not certify accessibility, complete the 13 design decisions, resolve the prior 200% header concern, verify all three scripts editorially, or demonstrate a live cloud integration.

Primary implementation references: [Firebase web setup](https://firebase.google.com/docs/web/setup), [Firestore rule conditions](https://firebase.google.com/docs/firestore/security/rules-conditions), [Firestore emulator](https://firebase.google.com/docs/emulator-suite/connect_firestore), [GA4 developer guide](https://developers.google.com/analytics/devguides/collection/ga4), [Google consent guide](https://developers.google.com/tag-platform/security/guides/consent).

## Unified poem browsing and search · 1 October 2026

`poems.html` is the single navigation destination for browsing and searching all poems. `search.html` remains a lightweight compatibility redirect, preserving query/fragment when JavaScript is available. The no-script fallback links/redirects to Poems. Keep internal recovery links on Poems and omit the duplicate Search menu entry. Historical mock URLs are retained for provenance. See [approval and checks](../records/unified-poems-search.json).

## Book-review section retired from reader publication · 1 October 2026

At the user’s request, Book reviews is omitted from journal navigation and its ten routes are excluded from the public build and search index. Captured review metadata, local pages, artwork and builder history remain preserved. Existing content-release safeguards stay unchanged; removing a section does not certify publication readiness. See `kb/records/poets-art-and-review-retirement.json`.

## Quiet-reader collections · 2 October 2026

The build generates a lightweight `assets/reading-library.json` with edition/poet labels, counts and local data URLs. Complete prepared reading payloads live in `assets/reading-editions/issue-N.json` and `assets/reading-authors/poet-N.json`, explicitly included by the public exporter. Author collections preserve edition-descending/publication order and include unassigned contributions last. No biography research or KB data is exported. Device bookmarks are preserved across collection switches; reads fetch on demand and failed loads leave the active poem usable. Evidence: `kb/records/quiet-reader-library.json`.

## Direct collection reading · 2 October 2026

Poems and edition routes embed one prepared fallback entry plus an edition/all-collection payload URL and the shared quiet-reader template. `assets/reading-all.json` contains799unique prepared reader records in descending edition/publication order, with the unassigned contribution last. It is explicitly exported. Reader payloads include only existing public portrait URLs; measurement placeholders avoid preloading the complete portrait library. Collection Share uses its own page URL in the existing share dialog. No external share is sent by opening the dialog.

## Design contributor profile · 2 October 2026

`ahimanikya-satapathy.html` is a dedicated profile linked from Our Story credits, generated by `designer-profile.py`. It does not add a magazine contributor ID or editorial appointment. Research and access limitations remain in `kb/research/people/ahimanikya-satapathy/sources.json`; the literature fund is aspirational.

## Reviewed writer display names

Three evidence-backed display spellings are applied through `data/writer-name-corrections.json`: Nitish Raj, Soumen Roy and Mandakini Bhattacherya. `writer_names.py` supplies consistent profile, directory, reader, sharing and edition names while preserving captured contributor and poem records. Former spellings remain searchable in the poet directory. Stable profile URLs and contribution ownership are unchanged.

## Grouped contributor identities

`data/writer-identities.json` records three evidence-backed groups:192/224,256/366and255/449. Canonical profiles192,256and449show complete combined contributions. Original contributor IDs and poem assignments remain untouched in captured data; the build groups identities in memory. The directory,poem filters and reader library show one entry per group. All429profile URLs remain usable,with426distinct directory identities; duplicate pages carry canonical links and are excluded from search indexing. Old reader-collection payload URLs return the complete grouped collection. Portraits and quote selections are preserved for every source record. See [identity resolution](../records/writer-identity-resolution.json); verify with `python3 tools/check_writer_identities.py`.

Ma Yongbo replaces the captured Youngbo Ma display spelling through the same reviewed-name mechanism,after a Chinese-original poem match. English translation credit remains unverified; no translator name is inferred.


## Authorized pre-DNS hosting · 2 October 2026

KBL-DEC-037 authorizes pushing the current project and hosting its public-only Astro build at the existing GitHub Pages address for review before DNS migration. The manual workflow now offers `preview` and `release` modes. Preview retains `noindex,nofollow` and robots exclusion; release retains all existing content and translation checks. Hosting approval does not mark outstanding editorial facts or draft translations reviewed. Firebase and analytics remain disabled. No custom domain or DNS change is included. See [hosting record](../records/github-pages-preview-deployment.json).

## Firebase engagement activated · 4 October 2026

Firebase private feedback, reversible poem Likes and editor-moderated public comments are now enabled for `ahimanikya.github.io`. Explicit Firebase CLI scope approval was received, deployed rules match the tested source, the comments index is READY, and all14 production checks passed with exact cleanup. The manual Pages preview workflow37180414812 published commit`e0b9b1c`; live controls, runtime flags and bundle hashes were verified. GA4 consent, preview noindex and DNS are unchanged.

Moderation currently uses the project owner’s Firebase Console: submissions remain private in `commentSubmissions`; only approved name/message/poemId/publishedAt fields enter `publicComments`. Private feedback remains in `feedback`. A dedicated staff inbox and staff account provisioning remain deferred. The [activation record](../records/engagement-activation-2026-10-04.json) includes the exact owner workflow, test evidence and remaining limitations. Earlier dated disabled-service notes are historical.


## Per-page sharing images · 4 October 2026

The public export now assigns one static Open Graph / Twitter preview to every reader page. Poet/editor profiles use their existing full portrait; illustrated poems use their assigned illustration; text-led poems use their own edition cover artwork. Issue pages use cover artwork, the homepage uses a stable courtyard, and section pages use their own art or the journal fallback. `social_metadata.py` reads the generated page structure; `tools/build-social-images.mjs` creates uncropped 1200×630 JPEGs with content-hashed paths. Source images and reader layouts are unchanged. Metadata URLs follow `SITE_URL` and `SITE_BASE`, including future domain-root hosting. The public build keeps its noindex gate; selected sharing bots have publication-path robots exceptions while general crawling remains disallowed. On repository-path hosting, this cannot override the origin-root robots policy. Platform preview caches/layouts remain external. Evidence and page mapping: `kb/records/social-previews-2026-10-04.json`.
