---
type: "Editorial review"
title: "Full-collection Poetic Natural revision — local completion"
---

# Full-collection revision

All **1,574 baseline translation variants** received complete source-and-target readings in 185 sequential batches. **818 were revised**, **744 retained**, and **12 held unchanged** because material source questions prevent a defensible correction. No baseline variant remains unexamined.

This completes the authorized local revision pass. It is AI self-review, not independent linguistic or author approval. Every target remains a draft. Nothing was published by this workflow; original poems, authored translations and credits were preserved.

## Unresolved questions and scope

**1,312 variants carry recorded questions or provisional choices**, including the 12 held unchanged: 674 revised with holds and 626 retained with holds. This is a variant count, not a count of distinct questions. Corrections elsewhere in those poems do not resolve their source questions. The exact questions and previous uncertainty records are indexed in [unresolved-questions-final.json](unresolved-questions-final.json).

The original **24 missing targets** remain separately pending. The **22 Edition48 variants** imported concurrently after the authorization baseline were preserved but are outside this pass and receive no reading credit. Current site inventory is therefore 1,596 draft targets plus 24 pending targets; that is not the scope of this literary review.

## Evidence and verification

Exact source/current-target snapshots, before/after drafts, reasons, tradeoffs and reading evidence are preserved per batch. All 185 integrated batches have completed verification records. The final batch includes the Node24 build, five layout tests, ten queue/scope tests, full-edition checks, translation preservation checks, bundle validation and portable-handoff/storage verification. Browser review was used only where warranted; ordinary wording changes were checked through rendered payload and boundary parity without claiming a new browser inspection.

[Final totals](completion-2026-10-06.json) · [Queue](queue.json) · [Last batch verification](batch-185/verification.json) · [Edition1 checkpoint](issue-1-checkpoint.md)

## Lessons for future work

- Read agency and reference in full sentences: the one pointing finger in Reclusion became a misleading Hindi reciprocal expression. Restoring the finger and other person is contextual, not a universal pronoun substitution.
- Preserve degree and contrast: The Pain Of Unsaid Words uses billion versus million as poetic scales. Exact equivalents preserve that contrast without claiming statistical accuracy.
- Check title and recurring agreement together when personification is confirmed. Poem628's feminine village feedback does not establish narrator gender in other poems.
- Remove translation-created stiffness while preserving the source's strangeness. The broken moon in Yesterdays retains beauty despite brokenness; the chosen rendering's reduced explicit recovery nuance remains recorded.
- Keep uncertain source readings, dialect, kinship, gender and wordplay outside the poem as questions. Historical PNR-013's Kafka agency claim remains qualified, not reinstated as a proven error.

Next editorial stage: resolve the indexed source questions and obtain independent fluent-reader/author review. Publication requires separate authorization.

The completed recurring automation was deleted after full verification. Its last configuration is preserved in `completed-automation.toml`; no further wakeups are scheduled for this finished revision pass.
