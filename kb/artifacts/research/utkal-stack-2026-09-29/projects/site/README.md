# Utkal Project website

**Rediscover Utkal. Reimagine Odisha.**

An Astro static website and brand review studio. This is a local review edition; its articles, refined logo and new artwork await Founder review. A manual GitHub Pages deployment workflow is prepared; there is no public submission endpoint.

## Run locally

Use Node 24 LTS (`.nvmrc`; dependency minimum 22.12) and npm 9.6.5 or later. From this directory:

```sh
npm ci
npm run dev
```

Open `http://127.0.0.1:4322/`. The brand choices are at `/brand-review/`. The development server binds to loopback only. With this version of Astro, `npx astro dev status`, `npx astro dev logs` and `npx astro dev stop` manage its local background server.

```sh
npm run build
npm test
npm run preview
```

Build before running the tests. Build output is in `dist/`. Generated content, dependencies and build output are ignored by Git. `ASTRO_TELEMETRY_DISABLED=1` can be set for local commands.

## What is included

- Homepage, about, founder and contribution guidance.
- Bhubaneswar Fresco gallery: 161 art images, five alternates and an eight-photo essay.
- Utkal Store is excluded from the main website: no introduction route or links. Its separate development app remains in `projects/store/`.
- Searchable collection of seven entries with topic links and shareable query URLs.
- Existing Samanta Chandrasekhar article, retaining its source and review limitations.
- Five short research notes selected from the project KB at build time.
- Separate English and Odia identity treatments, sea headings/buttons and laterite highlights.
- Local Noto Odia fonts with their original licences.

The project KB remains the source for research. `tools/select-content.mjs` explicitly selects five files; it does not publish the full KB, governance records or private contributor information. Adding a preview entry to this list is not editorial publication approval. Website code, build settings and public assets stay here; repository configuration stays at the root.

## Review and publication

See the [website brief](../../kb/specs/website-brand-foundation.md), [brand proposal](../../kb/reference/brand-foundation.md), [asset provenance and prompts](../../kb/records/brand-foundation-assets.json) and [verification record](../../kb/records/website-brand-checks.json).

`noindex` and `robots.txt` describe a review edition; they are not access controls. Keep deployment private until its content and publication are approved. GitHub project-path hosting will require an explicit base-path configuration or a domain-root deployment; current links assume the domain root.

Deferred: Firebase accounts/intake, photo uploads, Google Analytics, AI chat, final approval of the vector logo candidates, share-card exports and public launch. No API keys or paid services are needed to review this version locally. The domain and GitHub Pages connection are configured; the first website preview is published.

The earlier standalone preview is preserved locally. This site brings its article, pinned dependencies and useful colour/font assets into the canonical repository, then adds the collection and branding work.

## Fresco build and preservation

`tools/build-gallery.mjs` prepares gallery HTML from the explicit KB collection and maintained gallery template. The Astro route serves `/stories/bhubaneswar-fresco/` in development and builds the same static route. Originals and thumbnails are copied unchanged; checksums are in the KB import manifest. The original `Browse_Photos.html` and all 172 source images remain in the original archive. No source submission service or private inbox is imported.

[Direction 02](../../kb/reference/brand-direction-02.md) supersedes the earlier branding proposal.

## Vector candidates

Separate English/Odia, colour/one-ink/reverse SVG signatures and a simplified icon are in `public/assets/brand-v3/`. Lettering is outlined from the bundled Noto font. `python3 design/build-masters.py` regenerates these and Store artwork from checked-in path data; `design/outline-wordmarks.swift` records the macOS CoreText shaping step. See [refinement 03](../../kb/reference/brand-vector-03.md).

## GitHub Pages connection

The Founder authorized making `ahimanikya/utkal-project` public to enable Pages. GitHub Pages now uses GitHub Actions and the custom domain `utkalproject.org`. GoDaddy retains DNS management: four GitHub Pages A records and `www` pointing to `ahimanikya.github.io`. Other DNS records were preserved.

The repository-root `.github/workflows/publish-site.yml` builds only `projects/site`, runs its existing tests and uploads only its `dist` directory. The Store is not deployed by this workflow. No push-triggered publication is enabled. After the reviewed website and workflow reach `main`, the Founder can run **Publish Utkal Project** with the explicit release confirmation. The workflow checks the initiating account and main branch; the `github-pages` environment can provide additional repository-managed approval controls.

The first run succeeded on 28 September 2026: [live preview](https://utkalproject.org/) · [release evidence](../../kb/records/website-first-release.json). Editorial draft labels and `noindex` remain in this review edition; they are not access controls. DNS/certificate readiness is distinct from an actual website deployment.
