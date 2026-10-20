---
type: "Website platform contract candidate"
title: "Utkal website platform contracts"
version: "0.1.0-draft.1"
status: "local_candidate_for_site_adoption"
---

# Utkal website platform contracts

These contracts extend the [common website rulebook](website-standard.md). They define shared boundaries and process before implementation; they are not claims that every site already supports them. Blueprint owns these definitions; one separately versioned implementation supplies common modules, with project-local adapters. Detailed reader schema, Firebase access tests and Analytics adapters follow their own implementation batches.

## Modules and configuration

| Module | Shared responsibility | Site adapter responsibility |
| --- | --- | --- |
| Design foundations | Semantic tokens, spacing roles, utility icons and accessible base components | Palette, masthead, script typography, surface placement and editorial art |
| Reader | Settings, ordered navigation, logical anchors, language fallback, local persistence interface | Public content loader, poem/prose/book layout, source links, audio, legacy saved-data compatibility and contextual exit |
| Responses | Like/unlike, pending submission, public comment retrieval, private feedback, status/retry and moderation field boundaries | Dedicated Firebase project/config, content-key mapping, local moderation and actual deployed access rules |
| Analytics | Consent adapter, event vocabulary, firing rules and excluded fields | Dedicated property/stream, configuration, privacy copy and verification evidence |
| Sharing | Initial-HTML metadata contract and Share/Copy behavior | Canonical routes, available-language URLs and page-image mapping |

No adapter imports another site’s project/property ID, reader database or operating roster. Config references stay in the site record. Public service configuration is distinct from privileged credentials; no secrets are stored in adoption templates. Common code receives explicit site configuration rather than embedding one publication’s identity.

## Stable content identity

A content reference has a site namespace, immutable local content ID, content kind (`poem` or `article`), canonical permanent route, source language and available variants. Display titles, generated page numbers and collection order do not form identities. Existing IDs are retained through adapter mappings. If an existing service uses route-derived IDs, preserve it behind the mapping until a deliberate tested migration is recorded.

A collection has a stable collection ID, kind (`book`, `edition`, `topic`, `category`, `location`), title, entry context and an explicitly ordered list of available public content references. The same article retains its content reference in every collection. Source citations and truthful review/adaptation context travel with the content. Local source collections, drafts and excluded articles are not fetched into the public reader.

## Firebase response process

Each site owns its Firebase project and moderation records. A shared response adapter exposes read-like-state, set-like-state, list-public-comments, submit-comment and submit-private-feedback operations. Transport details and actual access rules belong in the implementation contract; this document does not prescribe a database layout before current schemas are inspected.

| Operation | Required behavior | Verification |
| --- | --- | --- |
| Like/unlike | Desired state for stable content/browser identity; retries do not double-count | Repeat and failed operations preserve coherent state/count; distinguish browser identity from unique humans |
| Comment submission | Private pending item; server-controlled public/moderation fields | Reader cannot approve or read other pending items; public retrieval contains only permitted moderated fields |
| Public comments | Reviewed public content only | Access-rule and adapter tests exclude pending/private/contact fields |
| Private feedback | Separate private channel with bounded local context | Public reads denied; authorized moderation access and failure recovery checked |
| Retry/error | Retain typed input on failure, avoid accidental duplicates; success only after accepted write | Offline/denied/repeated submission cases; no fabricated success |

Use existing working services while replacements are tested. Record current schema/config, IDs, moderation/access boundaries and migration before adoption. Preserve reader records; no implicit data copy across sites. Test with synthetic fixtures and local emulation where available. Record local checks, cloud-rule deployment and live verification separately; none substitutes for another.

## Google Analytics process

Each site owns its property/stream. Measurement follows its consent adapter: unknown, declined or withdrawn means no event collection; granted permits only the documented non-advertising measurement scope. Withdrawing consent stops subsequent events; do not replay pre-consent events or private payloads. Preserve current privacy signals and verify provider-specific behavior during implementation. Reading, sharing and responses remain usable in every consent state and when measurement scripts are blocked.

| Event | Trigger | Allowed context |
| --- | --- | --- |
| `content_view` | Public permanent content becomes readable; once per view | Stable content ID, kind, available language |
| `language_change` | Reader explicitly selects an available language | Stable content ID and selected language |
| `reader_open` | Reader entry succeeds | Collection/content ID, mode, language |
| `reader_close` | Reader exits explicitly | Collection/content ID, mode; no saved passage text |
| `share_complete` | Native share resolves successfully | Stable content ID, method; cancellation sends no completion |
| `copy_link_complete` | Clipboard operation succeeds | Stable content ID, available language |
| `listen_start` | Reader-initiated playback begins | Stable content/recording ID and language |
| `listen_progress` | Documented 25/50/75/100 percent milestone crossed, once per playback session | Stable content/recording ID and milestone; seeking semantics verified by adapter |

Event names above define the target vocabulary; map existing events deliberately rather than duplicating emissions. Allowed fields are an allowlist, not permission to send arbitrary page/form data. Never collect comment/contact/feedback/search text, private contribution data, saved passages, names, email addresses, device-local identity tokens or raw URLs carrying private parameters. Validate event payloads and granted/declined/withdrawn/blocked cases before reporting adoption. Account/property creation and live DebugView checks remain actual site-specific dependencies.

## Adoption, overrides and evidence

Record base version plus content hash or immutable revision, contract version, shared-module source/version, local configuration references, page-family coverage and named overrides/extensions. An override lists the affected rule/module, local value, rationale, actual human decision and verification; it cannot waive source integrity, human authority or private pending feedback. A pinned offline copy is a reference, not a forked common authority.

Use the [adoption template](../templates/website-adoption.json) and [page checklist](../review/website-page-checklist.md). An untested field stays untested. Preserve the previous version and recovery instructions. Local preparation, local integration, remote publication, provider setup and live feature verification have separate states. Drift checks report differences; they do not deploy or overwrite local decisions.
