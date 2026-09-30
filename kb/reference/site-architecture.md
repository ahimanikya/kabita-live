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
| Git | Local repository on `main`; ZIP archives assigned to Git LFS, with the local LFS hook enabled. Private remote `ahimanikya/kabita-live` created and connected; source upload status is tracked in the account setup record. |
| Hosting | GitHub Pages selected. Utkal-style manual GitHub Actions workflow prepared; uploads only the static site. No Firebase Hosting. |
| Publication | Local preview and production-format build only. Firebase project/web app created on Spark and anonymous Auth enabled. Firestore and GA4 remain pending. No website deployed or editorial login created. |

## Content readiness is a separate gate

The available inputs contain 47 issue records, 427 writer directory records, 45 known poem records and 8 review records. Only **three opening excerpts**, zero complete poem texts and zero complete review texts are available. Issue membership and writer biographies are incomplete. Generated metadata pages clearly state when reading content is unavailable; they are staging material, not a finished archive.

Firebase does not supply these missing texts. A full publication export or another authorized content source is still required. Preserve authored stanza breaks, script, byline, translator, date and issue relationships during import. Do not infer missing issue dates or invent biographies.

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

`build.py` creates reader HTML from local inputs. `standalone-support.py` and `standalone-pages.py` keep routes/copy self-contained. TypeScript feedback is bundled locally. `build-public.py` validates reader links and chooses only required web assets; Astro writes the deployable `dist` folder and Pagefind indexes it. Never publish the raw workspace, KB or the Python preview directory. The `localhost:8771` preview origin remains unchanged for design review.

Sync the portable source with `tools/sync_handoff.py`. Dependencies, generated staging folders, `dist`, debug logs and `.git` are excluded. Install dependencies and build inside the portable site when using it independently. Run `tools/check_storage.py` for current parity; `--migration` is specifically the historical unchanged-site baseline and is not applicable after intentional reader-site changes.

## GitHub storage and publishing

The repository stores maintained website source, editorial content, art, font licences, complete KB and preserved history. Four existing delivery ZIPs exceed 100 MiB; `*.zip` is assigned to Git LFS so those originals can be retained in GitHub too. Derived handoff duplicates, dependencies, generated build output and local debug logs remain reproducible/ignored. On a new clone, install Git LFS and run `git lfs pull` to retrieve historical archives. Website builds do not need those ZIPs.

Private feedback messages, authentication records and secrets are runtime data, not publication source. They stay in Firebase or the editorial email service, never a public repository. The repository is private. Its current plan requires an upgrade or a public repository for Pages. The user has been asked to choose separate public website delivery, whole-project visibility, or an account upgrade; no visibility change is authorized yet.

`.github/workflows/publish-site.yml` follows the [inspected Utkal workflow](../artifacts/research/utkal-stack-2026-09-29/publish-site.yml): manual dispatch, `main`, initiating repository owner, explicit release selection, `github-pages` environment, and separate build/deploy jobs. It uses Node 24, Python 3.12, Java 21 for local Firebase rule tests, locked npm dependencies, the release content gate, and the public `dist` artifact. There is no deployment on push. The portable handoff includes an equivalent workflow with `site/` paths.

Pages metadata supplies `SITE_URL` and `SITE_BASE` to Astro. The local default stays `/`; repository-path hosting and a later custom-domain root are supported without changing the existing localhost origin. Reader links and runtime configuration URLs are relative. GitHub Pages must use **GitHub Actions** as its publishing source. Repository/environment permissions and the domain still need actual remote setup; no workflow has run on GitHub yet.

[GitHub Pages workflow documentation](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages) and [large-file limits](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github) informed this setup. [Local verification](../records/github-pages-verification.json) records the build and release-gate checks.

## Configuration still needed

1. Firebase project `kabita-live` and web app are created; anonymous Auth is enabled. Create Firestore in the approved Mumbai region (`asia-south1`) once its empty region selector loads, then configure authorized domains. [Account setup record](../records/account-setup.json) tracks verified and pending steps.
2. Deploy the reviewed Firestore rules to that project, verify them against its real configuration, and restrict editor access through maintainer-issued custom claims. Publication job titles do not grant backend access. An editor inbox UI is not yet implemented.
3. Review retention and abuse controls before enabling intake. Current rules enforce field limits and a 60-second per-anonymous-UID interval, not a global spam barrier. App Check and broader rate protection are not configured. No file uploads, Storage or Cloud Functions are implemented.
4. Create a GA4 property/web stream and add its Measurement ID. Disable automatic enhanced measurement where it could collect unintended fields; verify the property settings and a consented test visit before launch.
5. Populate `runtime-config.json` with each service's public web configuration, allowed production hosts and enabled state only after setup/testing. Never put service-account keys or private credentials there. Firebase web configuration is not an authorization boundary; deployed rules are.
6. Import complete editorial content; complete the existing design reviews and enlarged-text check. Finish source upload and resolve the private-repository GitHub Pages restriction, review public output, then run the manual publishing workflow under release direction.

Analytics sends explicit page views with query strings/fragments removed and a limited set of share events. It does not send message text, names or email addresses. Opt-out disables further custom events and reloads the page. Google account/property settings still need review; local adapter tests are not proof of the eventual production configuration.

## Verification and limits

See [local implementation verification](../records/standalone-verification.json), [desktop/phone browser checks](../records/standalone-browser-checks.json), and [font source record](../records/source-serif-local.json). Three analytics tests and five Firestore emulator tests passed. Six representative reader routes passed automated checks at 1280px and 360px. The complete public build was checked for missing local links and forbidden legacy dependencies.

This is self-review. It does not certify accessibility, complete the 13 design decisions, resolve the prior 200% header concern, verify all three scripts editorially, or demonstrate a live cloud integration.

Primary implementation references: [Firebase web setup](https://firebase.google.com/docs/web/setup), [Firestore rule conditions](https://firebase.google.com/docs/firestore/security/rules-conditions), [Firestore emulator](https://firebase.google.com/docs/emulator-suite/connect_firestore), [GA4 developer guide](https://developers.google.com/analytics/devguides/collection/ga4), [Google consent guide](https://developers.google.com/tag-platform/security/guides/consent).
