---
type: "Architecture Diagram"
title: "Technical architecture diagrams"
description: "Launch and future architecture, editable diagrams and public/private data flows."
tags: ["utkala", "technology", "architecture", "publishing"]
status: "draft"
generated: {"by": "codex/gpt-6", "at": "2026-09-27T16:22:55-07:00"}
instruction_basis: "User-agreed launch architecture in the Odisha Tourism conversation, 27 September 2026. Future stages are proposals; no deployment or billing change is implied."
implementation_status: "not_deployed"
publication_status: "not_reviewed_for_publication"
sources: [{"id": "okf", "title": "Open Knowledge Format 0.2", "resource": "https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md"}]
---

# Technical architecture diagrams

## How to read these diagrams

The launch diagram records the agreed design, not an already running system. The growth diagram records optional future capabilities. Solid paths represent intended flows, not integrations that have been tested. Private submissions pass through editorial review before any public Git change.

## Launch architecture

![Launch architecture: maintainers publish reviewed OKF content through Astro and GitHub Pages; visitors contribute through private email or Firebase Spark.](../references/diagrams/launch-architecture.svg)

[Editable SVG](../references/diagrams/launch-architecture.svg) · [Mermaid source](../references/diagrams/launch-architecture.mmd)

```mermaid
flowchart LR
  M[Maintainers and reviewers] -->|Reviewed public changes| G[Canonical OKF and approved photos in Git]
  G --> B[Validation and Astro build]
  B --> P[GitHub Pages: pages, data and Pagefind]
  P --> V[Visitors on our domain]
  V -->|Photo form or email| R[Free relay candidate or direct email]
  R --> I[Private editorial inbox]
  I -->|Rights, evidence and credit review| M
  V --> A[Firebase Authentication: Spark]
  V -->|Rule-authorised text and user data| F[Firestore: Spark]
  F -->|Manual editorial review| M
```

Authentication supplies identity to Firestore rules; an arrow to Firestore does not imply public database access. Privileged roles are assigned by maintainers. The inbox contains photo attachments; Firestore does not automatically mirror it. Public pages and search do not depend on live Firestore reads.

GA4 is omitted from the drawing for clarity. It receives only approved public events after consent; it is not a content store or a copy of the private queue. Public DNS points to GitHub Pages. Assets and API requests remain separate.

## Future architecture

![Growth architecture: keep Git and the approved public release, adding managed uploads, review automation, cited AI or private recovery only as needed.](../references/diagrams/growth-architecture.svg)

[Editable SVG](../references/diagrams/growth-architecture.svg) · [Mermaid source](../references/diagrams/growth-architecture.mmd)

```mermaid
flowchart LR
  G[Git and OKF remain canonical] --> B[Approved versioned release]
  B --> W[Public website and data]
  U[Future private managed uploads] --> R[Future review service]
  R -->|Proposed Git change, then editorial approval| G
  B --> K[Future public-only AI retrieval index]
  K --> Q[Future Ask Utkala gateway]
  Q -->|Cited answer| W
  U --> C[Future private backup and restore]
  R --> C
```

Future services must not become an independent master encyclopedia. Private uploads, consent and account data remain excluded from public exports and AI retrieval. A paid plan, a free model tier or a proposed diagram does not by itself establish service availability, accuracy or recovery.

## Three operational sequences

1. **Read:** load a static page and its versioned data/search assets. User-specific features request only authorised private records.
2. **Contribute:** a photo arrives through the activated relay or email; a text proposal arrives in Firestore. An editor reviews it, then creates a public Git change. Only its approved content and credited media are published.
3. **Correct:** update the source concept, invalidate the affected approval, review the new content and publish a complete release. Retain redirects for renamed IDs and point saved entries to stable concepts.

## Failure behaviour

| Failure | Expected behaviour |
| --- | --- |
| Firebase unavailable or quota exhausted | Public reading/search continues; submission or account feature clearly reports failure |
| Relay rejects an upload | No false success; preserve entered text where feasible and offer direct email |
| Email accepted by relay but not delivered | No claim of inbox delivery; test mailbox routing and follow the manual receipt process |
| Build validation fails | Previous published release stays available |
| Private records are lost | No promised recovery while private backups are deferred |
| Future AI lacks evidence | Say the collection cannot answer; do not invent a source |

These diagrams are authored for Utkala · Odisha with AI assistance. They depict application architecture, not historical evidence or a formal OKF conformance certification.

[Stack and responsibilities](technical-stack.md) · [Growth triggers](growth-roadmap.md)
