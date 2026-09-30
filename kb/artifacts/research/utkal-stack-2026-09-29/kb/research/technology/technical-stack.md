---
type: "Technical Architecture"
title: "Technical stack for Utkala · Odisha"
description: "Agreed launch stack, data ownership, photo intake, publishing and operating limits."
tags: ["utkala", "technology", "architecture", "publishing"]
status: "draft"
generated: {"by": "codex/gpt-6", "at": "2026-09-27T16:22:55-07:00"}
instruction_basis: "User-agreed launch architecture in the Odisha Tourism conversation, 27 September 2026. Future stages are proposals; no deployment or billing change is implied."
implementation_status: "not_deployed"
publication_status: "not_reviewed_for_publication"
sources: [{"id": "astro", "title": "Astro content collections", "resource": "https://docs.astro.build/en/guides/content-collections/"}, {"id": "pagefind", "title": "Pagefind", "resource": "https://pagefind.app/"}, {"id": "pages", "title": "GitHub Pages limits", "resource": "https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits"}, {"id": "domain", "title": "GitHub Pages custom domains", "resource": "https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site"}, {"id": "firebase", "title": "Firebase pricing plans", "resource": "https://firebase.google.com/docs/projects/billing/firebase-pricing-plans"}, {"id": "formsubmit", "title": "FormSubmit file uploads and delivery", "resource": "https://formsubmit.co/documentation"}, {"id": "formsubmit-free", "title": "FormSubmit free service", "resource": "https://formsubmit.co/"}, {"id": "okf", "title": "Open Knowledge Format 0.2", "resource": "https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md"}]
---

# Technical stack for Utkala · Odisha

## Agreed direction

Use Astro and TypeScript to publish a reading-focused encyclopedia from the existing OKF knowledge collection. Git stores reviewed public knowledge and approved display photos. GitHub Pages delivers the static website through a user-owned domain. Firebase Spark supports identity and private dynamic text data. Photo contributions arrive by email, optionally through a free form relay; editors publish accepted material through Git.

The incremental launch service target is **$0/month within free allowances**, using an existing inbox. Domain registration and renewal are separate. Development time and existing coding subscriptions are excluded. Free allowances are limits, not a permanent guarantee. No remote repository, domain, form service or Firebase project was configured by this documentation update.

| Layer | Launch choice | Scope |
| --- | --- | --- |
| Content and version history | GitHub + the existing OKF 0.2 bundle | Markdown concepts, sources, JSON/CSV tables and approved media |
| Website | Astro + TypeScript | Static article, directory, gallery and data pages |
| Interactive UI | React only where useful; shared CSS variables | Forms and reviewer/account screens using the existing brand |
| Public data | Versioned JSON; optional generated SQLite | Visitor-read-only tables and research exports |
| Search | Pagefind | Browser search of published pages |
| Delivery | GitHub Pages + GitHub Actions | Build validation, production artifact, custom domain and HTTPS |
| User identity | Firebase Authentication on Spark | Guest sessions and editor/contributor accounts; avoid SMS |
| Dynamic text data | Firestore Standard on Spark | Proposals, review metadata, preferences and bookmarks |
| Photo intake | Editorial email; FormSubmit candidate | No paid upload storage; activate and test before showing an upload control |
| Publishing | Manual editorial review followed by Git change | No browser-held Git write credential or automatic publication |
| Analytics | GA4 with explicit consent and safe event fields | No raw messages, emails or family details in analytics |
| Local verification | Existing KB validators, Firebase emulators, focused UI tests | Content structure, permission boundaries and real submission handling |

Astro provides content collections; Pagefind indexes static output. These choices serve our content-heavy design without making ordinary readers query a live database. See [Astro](https://docs.astro.build/en/guides/content-collections/) and [Pagefind](https://pagefind.app/).

## Data ownership

The canonical collection remains `outputs/odisha-kb/`. Preserve existing concept-path IDs. OKF is the document format; CSV/JSON are application data linked by those concepts. Our schema versions and publication fields are local extensions, not additional OKF requirements. See [the recorded method](../about/research-method.md).

Public tables include places, alternate names, periods, sources, claims, claim-source links, historical relationships, media and public organisations. Include source, period, geography, evidence class and revision where relevant. Keep uncertainty explicit. Generate SQLite from editable text rather than editing two competing databases.

Firestore contains private working data. Bookmarks refer to public concept IDs rather than copied articles. Never commit contact details, consent records, pending photos, account data or credentials to public branches. A public pull request is already public even before merge. Existing research also needs explicit publication selection; lifecycle `stable` is not publication approval.

## Contributions and permissions

Guests may submit text using anonymous Authentication and narrowly scoped Firestore Security Rules. They may create permitted fields, but not self-approve, assign roles or read another person's private record. Rules provide enforcement on Spark; hiding an admin screen is not security. Assign reviewer roles through a controlled maintainer operation. Test invalid writes, repeated requests, expired sessions and cross-user reads with emulators. Client-side checks improve usability but do not provide server-side rate limiting.

Photos use a separate inbox path. A free FormSubmit relay is a candidate, not yet an operational dependency. Its documentation specifies a 10 MB total attachment limit and no recovery of uploaded files from its submission archive. Propose three JPEG/PNG files and 8 MB combined as our smaller UI limit. Keep a direct-email fallback. See [upload documentation](https://formsubmit.co/documentation) and [service description](https://formsubmit.co/).

Collect a caption, approximate date/location if known, public credit, private reply address and explicit permission to publish. Explain that the form forwards details to the editorial inbox. Report successful relay acceptance as “sent for review”, not published or guaranteed inbox delivery. A mailto link only opens an email draft. Activate the recipient and test a real permitted sample before enabling the form.

Editors inspect files, confirm rights and credit, remove unwanted private metadata from display copies, preserve accepted originals locally and add approved copies to Git. Email is the photo queue; any Firestore review record is entered manually at launch. There is no assumed automatic inbox-to-database integration.

## Build and release

A reviewed Git change triggers checks and a static build. Validate IDs, sources, data relationships, media rights and approval tied to the actual content digest. Export only permitted public fields. Emit pages, search data and a release manifest containing Git revision and schema version; version the exported data files together. Failed checks leave the previous release available. Retain a known-good release for public rollback.

Keep untrusted contribution checks isolated from deployment credentials. GitHub Actions uploads only the generated website artifact. Do not copy the entire local KB, private inbox exports or development folders into the public website. At setup, choose a public release repository scope that excludes confidential research from Git history as well as from website output.

GitHub Pages handles static delivery; Firebase SDK requests go separately to Firebase. Add the chosen domain to authorised Authentication settings as applicable. No Firebase Hosting API rewrites are available on GitHub Pages. Public reading and search remain available if Firebase or the mail relay fails.

## Boundaries and launch gates

Deferred: Firebase Blaze, Firebase Storage, Cloud Functions, AI chat and paid private backups. Spark can be upgraded later; it requires no payment method for the supported free features. Storage and server functions need billing-enabled services if added later. See [Firebase plans](https://firebase.google.com/docs/projects/billing/firebase-pricing-plans).

The first complete feature is Bhubaneswar's Painted Streets: credited gallery, searchable story, correction/photo intake, editorial review, Git change and published update. Verify mobile/keyboard use, Odia names and search examples, domain/HTTPS, permission rules, quota failure messages, accurate submit status, source attribution and public rollback. If upload relay testing fails, use email; a working contribution path remains a launch requirement. AI and private backup restoration are not launch gates while deferred.

Keep local KB/Git copies. Private Firebase/inbox recovery is not guaranteed while independent backups are deferred. GA4 remains off until its property and consent behaviour are tested. No raw search queries, form text or lineage details should enter analytics.

[Architecture diagrams](architecture.md) · [Growth roadmap](growth-roadmap.md) · [Decision register](decisions.md)
