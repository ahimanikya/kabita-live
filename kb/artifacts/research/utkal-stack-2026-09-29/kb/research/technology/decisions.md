---
type: "Architecture Decisions"
title: "Architecture decision register"
description: "Current decisions, superseded proposals and unresolved implementation inputs."
tags: ["utkala", "technology", "architecture", "publishing"]
status: "draft"
generated: {"by": "codex/gpt-6", "at": "2026-09-27T16:22:55-07:00"}
instruction_basis: "User-agreed launch architecture in the Odisha Tourism conversation, 27 September 2026. Future stages are proposals; no deployment or billing change is implied."
implementation_status: "not_deployed"
publication_status: "not_reviewed_for_publication"
sources: [{"id": "okf", "title": "Open Knowledge Format 0.2", "resource": "https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md"}]
---

# Architecture decision register

## Current decisions

These decisions record the user's instructions and the accepted plan in this conversation on 27 September 2026. They do not assert human factual verification or completed implementation. Concept status stays draft until documentation review; public publication approval is separate.

| ID | Decision | Status and rationale |
| --- | --- | --- |
| ADR-001 | Keep the canonical public KB in Git and OKF 0.2 | Agreed. Portable, reviewable source with preserved concept paths and provenance. |
| ADR-002 | Publish visitor-read-only knowledge from that source | Agreed. Visitors can propose changes, not modify the authoritative public dataset directly. |
| ADR-003 | Use Astro + TypeScript, selective React, shared CSS and Pagefind | Agreed stack direction. Use existing content and brand; validate Odia behaviour. |
| ADR-004 | Use GitHub Pages with a user-owned domain | Agreed. Supersedes the Firebase Hosting launch recommendation. Domain registration renews. |
| ADR-005 | Start Firebase on Spark for accounts and private dynamic text | Agreed. Blaze is deferred until a specific capability or quota need justifies it. |
| ADR-006 | Receive photos by email and publish accepted copies through Git | Agreed. A free FormSubmit relay is an untested candidate; direct email is the fallback. Supersedes paid Firebase upload storage and automatic Git export for launch. |
| ADR-007 | Defer AI chat unless an acceptable free alternative is established | Agreed. Keep architecture and evaluations as future work; search is the launch interface. |
| ADR-008 | Defer paid private backups | Agreed. Keep local KB/Git copies; make no private-data recovery guarantee. |
| ADR-009 | Target $0/month in incremental launch services within free limits | Agreed cost direction. Domain renewal, labour and existing coding subscriptions are separate. |
| ADR-010 | Keep evidence review and publication approval distinct from automated checks | Existing project rule retained. No draft data or private fields leak via pages, search or downloads. |

## Inputs to resolve during implementation

- Final repository name, visibility and public-file selection. `ahimanikya` is the intended owner; `odisha-encyclopedia` remains proposed.
- Domain registration, chosen canonical hostname and DNS access.
- Editorial inbox address and form activation; sample attachment delivery must pass before enabling uploads.
- Firebase project, region, authorised domain, maintainer accounts and Security Rules; no billing account is required by the Spark launch design.
- Named editorial responsibilities, publication permissions and reuse licences for content, code and images.
- GA4 property and consent/event configuration, without recording private text.
- Package versions and supported runtime to pin when implementing; no untested model selection.

## Changes deliberately not made

No cloud account, repository remote, paid plan, DNS record, public deployment, email delivery or new monitoring schedule was created by this documentation task. Current architecture replaces earlier proposals; retain the conversation and project log as history, not as parallel active instructions.

[Technical stack](technical-stack.md) · [Growth plan](growth-roadmap.md) · [Diagrams](architecture.md)
