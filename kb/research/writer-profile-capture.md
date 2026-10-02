---
type: "Research and implementation record"
title: "427 writer profiles: browser capture and local contribution links"
---

# Writer profiles

The user requested dedicated pages for all 427 contributors, richer researched narratives, faithful artistic portraits and links to each writer's contributions. They then suggested: “Maybe use browser skill to capture them?”

## Capture result

Following Contributors from the homepage and then each visible writer link opened the real profiles. Direct requests had redirected to the homepage. The directory's hidden popups repeated Manju Chouhan's biography under unrelated names; these were excluded. All 427 individual profiles were captured by writer ID and checked against the directory URL before saving.

- 427 individual profiles; 381 non-empty biographies; 46 absent biographies.
- 778 distinct contribution links, with no duplicate poem IDs across captured writers.
- One poem, Yesterdays (poem 645, writer 426), has no edition metadata. Its local reader link is retained without inventing an issue.
- 426 original portrait files preserved, all decodable, with no duplicate image files. The directory asset inventory was capped, so the remaining photographs were saved from individual profiles. Manju Chouhan (writer 233) has an empty photograph URL; no likeness was invented.
- No independently researched biographies or new artistic portraits are claimed complete by this capture pass. Existing editor work remains intact.

## Reader integration

All writer routes now have the captured biography where available, title/year contribution filtering, and local poem and issue links. Existing editor pages keep their approved biographies and portraits, with their captured contribution lists added. Shared Our Story attribution explains that biographies reflect supplied journal records; no old-site links are exposed to readers. Full poem texts remain a separate import, and local reader pages disclose when text is absent.

No design foundation changed. No deployment or domain change was performed.

## Evidence and next work

- [Directory capture](writers/live-directory.json)
- [Individual profile captures](writers/captured-profiles.json)
- [Counts and gaps](writers/capture-summary.json)
- [Capture and research queue](writers/research-queue.json)
- [Portrait sources](writers/portrait-sources.json)
- [Reusable writer-profile skill](../artifacts/skills/kabita-writer-profiles/SKILL.md)
- [Research leads](writers/research-leads.json)
- [Validation](../records/writer-profile-verification.json)

Independently verify identities, current roles, awards and selected books before rewriting the biographies. Maintain supplied text separately from new narrative. Apply the approved editor treatment with identity checks; obtain a suitable reference for the one missing photograph. Record publication rights and source credits with each asset. Preserve and review absent biographies rather than filling them with generic claims.
