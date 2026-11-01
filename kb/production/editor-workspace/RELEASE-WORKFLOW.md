---
type: "Editorial workflow"
title: "Editor Studio release workflow"
---

# Editor Studio release workflow

Prepared locally on 27 October 2026. New category, artwork and owner-review access rules require explicit activation approval; website publication is a separate approval.

## Editors

1. Choose Kabita Live or Toshali. Add a poem or transfer an existing submission, select its author, and sequence the entries with the arrows.
2. Open Translations & artwork to enter the other language versions and credits, and upload a permitted image with its description and credit. Record an explicit exception for an intentionally omitted language or text-only poem.
3. Use Review to open missing fields/checks. Preview includes the original, saved translations and saved artwork. It is a working proof; the built reader pages must also be checked.
4. Send the edition for review. This stores an immutable revision in the existing draft history. A subsequent edit clears the current submission flag. Selection and submission send no email.

## Owner

Release is visible only for the owner account. It lists submitted monthly drafts (latest 25 months) and Toshali. Open and check a revision, then Approve for production. The server allows only the existing owner to create a matching immutable revision approval; it grants no website-publishing access. Later edits invalidate the handoff. Download approved handoff is for inspection; the production helper independently reads the server record rather than trusting the downloaded file.

With the existing owner CLI account:

```
node kb/production/editor-workspace/prepare-release.mjs 2026-11 REVISION
node kb/production/editor-workspace/apply-release.mjs kb/artifacts/editor-releases/2026-11/revision-REVISION --check
node kb/production/editor-workspace/apply-release.mjs kb/artifacts/editor-releases/2026-11/revision-REVISION --apply
```

Use `toshali-2027` for the anthology. Preparation reads the current approved revision, checks real preparation content and exceptions, downloads immutable private artwork, and rechecks the source revision. It writes a private candidate with hashes. Application checks the owner approval, latest source revision, publication lock, cover and artwork hashes, then uses the existing additive edition importer. It never overwrites historical poems, existing author biographies, artwork or conflicting public identities. Shared author photographs still follow the existing reviewed portrait process; this importer does not publish private author photos automatically.

Monthly content enters the existing edition/poem/translation/cover catalogues. New contributions are added to existing authors without changing their details. Anthology content has a separate Git record and reader route `toshali-book-2027.html`; monthly issue numbering is untouched. Private notes, submission references and draft approval records stay in the KB/runtime, outside public content.

After applying locally: build, run site/access checks and inspect the complete reader pages. Resolve any global content-release gate separately; never disable it. Commit/push only the intended reviewed files. Obtain Ahimanikya's approval of that exact website release. Use the existing protected `Publish Kabita Live` manual workflow from main; only the owner may approve its protected environment. The Studio link opens that workflow; it does not dispatch or bypass it.

After successful publication, verify live pages/assets and run the existing next-draft helper for the live current monthly issue:

```
node kb/production/editor-workspace/next-draft.mjs ISSUE YYYY-MM SUCCESSFUL_RUN_ID --check
node kb/production/editor-workspace/next-draft.mjs ISSUE YYYY-MM SUCCESSFUL_RUN_ID --create
```

The existing draft is preserved. A missing prepared cover for the next month is a real hold: generate/review the candidate and update the prepared defaults; never copy the prior issue's poems or approvals. An anthology-only release must not advance the monthly issue number. Complete the anthology with `node kb/production/editor-workspace/complete-anthology-release.mjs REVISION SUCCESSFUL_RUN_ID --check`, then `--complete`. This verifies the successful main publication, the live content hash against that Git commit, and the exact current owner-approved draft. It atomically creates the publication lock and marks the anthology published with a concurrency check; it neither advances the monthly issue nor dispatches publication.

## Verification limits

Synthetic browser checks and local access emulators cover the two editor identities, owner-only handoff and outsider denial. They do not establish real iPhone Safari behaviour or production activation. A signed-in two-device acceptance run, production rule verification, and actual release/live-next-draft checks follow activation and owner publication approval. No real poet emails or publication were used for these tests.
