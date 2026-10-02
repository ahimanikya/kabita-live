---
type: "Interactive review"
title: "One poem: translations and pencil underlining"
---

# One poem, three languages

Current policy, 1 October 2026: missing original-language sources or source information do not block work. Use existing published text with its credits. Two composite poems have now been repaired and two unavailable records archived outside edition lists. There are 799 active readers, 1,574 translation drafts and 24 ready targets, with no source holds. Earlier dated hold/completion notes below are historical. See the [current content checklist](translation-source-holds.md) and [correction record](../records/poem-content-reconciliation.json).

## Current scope — 30 September 2026

Ahimanikya requested: “drop audio from now, but keep the transalation”. The prototype has no Listen button, player, voice-availability message or audio-review control. Translation tabs and partial underlining remain. The original version uses the existing poet byline and Original tab label without a duplicate credit sentence or empty credit row. Translation disclosure is centralized in Our Story → Credits & colophon → Translations; no attribution row is shown in the reader. Original/Translation labels and the poet byline remain. Audition prompts, recordings and links are preserved as historical evidence, not an active generation queue.

## Try it

1. Switch between **हिन्दी · Original**, **ଓଡ଼ିଆ · Translation**, and **English · Translation**. Ahimanikya approved the language-translation feature. AI assistance remains disclosed; this approval does not claim an independent linguistic certification. The source Hindi text, stanza break, end mark and place line are preserved in the content record. In the reader, the existing paddy ornament marks the ending instead of displaying the standalone ∎ character; the place line stays visible. No second decorative icon is added.
2. Select any word, phrase or passage, then use **Underline selection**. Select an underlined portion and choose **Erase** to remove only that portion. A selection may span lines. Indic grapheme boundaries protect conjuncts and vowel signs. Each language stores its own ranges locally; older full-line marks migrate without loss. On phones, use native long-press selection handles. Guidance and the live marked-passage count live in the underlined-U tooltip beside the three text-size controls. Hover, keyboard focus or tap opens it; Escape, a second tap or an outside tap dismisses it. Actual touch-device behavior still needs user testing.
3. Open **Your reading notes** to review translations and underlining separately. Notes save locally; download the JSON review for a durable decision record. Browser review choices do not change other pages or authorize publication.

## Preserved first voice trial — rejected

The journal-supplied author profile describes Sabita Singh Meera as a poetess. Feminine stock voices were selected for this review, not inferred from her photograph or name: Lekha for Hindi and Tara for Indian English. These rejected files are local macOS speech-synthesis previews with measured rates and line pauses. They demonstrate playback and pacing, not a finished culturally authenticated recitation. Pronunciation, emotion, language-specific poetic delivery and the poet's preferred voice remain editorial decisions. No cloning or imitation of the poet's own voice is involved.

Hindi recording: about 16.8 seconds. English recording: about 21.7 seconds. The voice reads the eight verse lines; the printed end mark and city remain on the page. An appropriate Odia voice/provider must be chosen before a three-language audio rollout.

## Files and preservation

- [Prototype content and translation drafts](../artifacts/review/poem-experience/content.json)
- [Review HTML](../artifacts/review/poem-experience/index.html)
- [Interaction source](../artifacts/review/poem-experience/prototype.js)
- [Prototype styling](../artifacts/review/poem-experience/prototype.css)
- [Voice scripts and audio masters](../artifacts/review/poem-experience/audio/)
- [Current partial-underlining verification](../records/poem-experience-v2-verification.json)
- [Historical first-prototype verification](../records/poem-experience-verification.json)

Rebuild with `python3 tools/build_poem_experience.py` after changing the canonical poem reader or prototype inputs. The build checks the original Hindi against the source and its hash. The preview page and asset folder are relative aliases into this KB. Public build selection excludes the prototype and its draft/audio assets. Original site files, artwork, captions and old studies remain intact. The existing site theme, shared header, borderless artwork, right-aligned caption and navigation are inherited.

Same-assistant implementation and browser review; no independent linguistic or audio-performance review is claimed. Translation and partial-underlining controls are approved for the shared poem reader; see the rollout record below. Audio is deferred at the user’s request; no further auditions or audio rollout are planned.

Artwork alignment: at Ahimanikya’s request, the prototype artwork sits 24px lower on desktop and 8px lower on narrow screens. Natural document flow retains room for its caption.


## Historical clean-reader preview — reverted

The user subsequently requested “revert”; the pre-trial layout is restored. The following describes the archived trial, not the current reader.

At Ahimanikya’s request (“try”), the trial hid review labels and the review form. Open `http://127.0.0.1:8771/poem-experience.html?review=1` to access those local review controls and saved decisions.

The opening has tighter title/byline/action spacing and removes the duplicate original-language metadata. Share stays in the opening; Write to the editor follows the verse. Original/Translation tabs stay visible. A 730px control row aligns with the poem: Aa opens the existing three text sizes, while the pencil opens help and Clear all marks. Phones use two rows. Selection actions are positioned beside the selected text; Remove appears only when the selection overlaps an underline. A thin muted-ink line replaces the heavier laterite underline. Escape and outside interaction close menus. Audio remains deferred; translation disclosure remains centralized.

Earlier layout source is preserved in `../artifacts/history/revisions/revision-60-reader-before-clean-preview/`. Existing saved marks and review keys are retained. This is a review option, not a full-site rollout or publication approval.

Verification: syntax and five existing range/grapheme tests pass. Browser checked text-size selection, menu closure, help and language switching. Desktop first-verse position improved from about 730px to 620px at a 1280×720 viewport; control and verse widths both measure 730px. A 360px iframe preview was visually reviewed. Native touch text selection and toolbar placement with real phone handles remain for user testing; no full accessibility certification claimed.

Revert scope: only the clean-reader trial was reversed. Translation tabs, central colophon disclosure, audio removal, info help tooltip, preserved source marker and lowered artwork remain as before the trial. The rejected trial and its generator are preserved in `../artifacts/history/revisions/revision-61-clean-reader-reverted/`.

Underline help refinement: the circled information glyph directly follows Underline with no layout gap. Clear marks follows the joined action/help group, so saved marks do not separate the icon from its label. Touch target and keyboard help behavior remain intact.

Underline action icon: uses an underlined U, drawn in the approved single-ink 24-unit utility style, instead of the editorial-feedback pencil. SVG source is `../artifacts/review/poem-experience/underline.svg`. The adjacent info icon and tooltip are unchanged.

Reading-controls alignment: the icon-only Underline action now sits directly after A/A+/A++, with an accessible name and hover title. Its info button stays attached. Clear marks can wrap independently on narrow screens.

Latest control decision: remove the info icon and visible Underline label. The single underlined-U action sits beside A/A+/A++; its accessible name and hover title remain. Earlier help-icon notes above are superseded.

Control scale: the underline SVG uses a 20px box so its U letterform matches the visual height of the adjacent 16px A. The 48px button target remains unchanged.

U help behavior: hover, keyboard focus or click/tap the underlined U to reveal selection guidance and the current saved-passage count. No separate info icon or persistent label is shown. Clicking U with a selected passage still underlines it. Escape, outside interaction or a second click dismisses pinned help.

Approved U interaction: retain A/A+/A++/U. Hover or keyboard focus reveals guidance; activation without selected text offers help. A successful underline or partial erasure dismisses the tooltip, leaving the verse unobscured. Saved-passage counts remain inside help. This supersedes the earlier behavior that pinned help after adding a mark.


## Shared rollout and first translation batch

The user approved applying the reader to all poem pages and requested translations in small batches in this chat. All 801 canonical poem pages now use the approved controls, without prototype review furniture. The separate prototype and its historical review records remain preserved. The rejected clean-reader trial has not been reapplied.

The first batch adds Hindi and English drafts for Issue 47 poems 809, 815, 818, 820 and 823. Together with poem 810, twelve translations are present; 1,590 target-language versions remain pending. Original texts are unchanged. Original/Translation labels remain visible; attribution is centralized. A release-only check blocks unreviewed translations from publication.

- [Batch drafts](../production/translations/batch-001/drafts.json)
- [Ambiguous expressions and editorial notes](../production/translations/batch-001/review.json)
- [Edition-ordered translation queue](../production/translations/queue.json)
- [Rollout verification](../records/poem-reader-rollout-verification.json)

Browser checks confirmed language switching, 28px large text, help dismissal, existing saved-mark migration and an original-only English page without empty language tabs. The 360px iframe measured 360px content width with no horizontal overflow; actual native phone text-selection handles still need device testing. A stale cached HTML page required a fresh query URL during local testing. Independent linguistic review remains pending, especially the expressions identified in the batch notes.


## Continuous translation batches — 30 September 2026

Ahimanikya asked to start the next batch after finishing the current batch, without repeated approval. The [workflow record](../production/translations/workflow.json) captures this direction. Batches 002–007 added 58 drafts for 29 poems, bringing the total to 70 translations across 35 poems. Issue 47 has all 16 poems in three languages; Issue 46 has 19 of 20. Counts here describe this checkpoint; the [queue](../production/translations/queue.json) is the live authority.

Poem 797, “Girls without tongues,” explicitly credits its English text as a translation by Bandana Sahoo from Odia. No matching Odia original is present in this author’s local contributions. Both remaining versions are held for source/provenance reconciliation rather than presenting a reverse translation as the original. [Source hold and required resolution](../production/translations/source-holds.json). Continue other poems while this is unresolved.

Batch editorial notes retain ambiguity, uncertain speaker gender, source encoding damage and interpretive choices; these drafts are not independently certified. No original, named translator credit, artwork or approved reader styling was replaced. Translation credit remains centralized. The next batch starts Issue 45 with poems 774, 780, 781, 784 and 778. No background job or website publication was created.

- [Batch 002 notes](../production/translations/batch-002/review.json)
- [Batch 003 notes](../production/translations/batch-003/review.json)
- [Batch 004 notes](../production/translations/batch-004/review.json)
- [Batch 005 notes](../production/translations/batch-005/review.json)
- [Batch 006 notes](../production/translations/batch-006/review.json)
- [Batch 007 notes](../production/translations/batch-007/review.json)
- [Checks and counts](../records/translation-batches-002-007-verification.json)

Use `tools/apply_translation_batch.py batch-NNN` to validate both targets, original hashes and stanza/line coverage before adding a batch. It refuses conflicting replacements and is safe to rerun on identical data. Run `tools/translation_queue.py` afterwards, rebuild the site, check actual rendered translation payloads, and sync the portable handoff. Complete the current batch before creating another; do not treat native-review pending status as a request for per-batch approval.


## Scheduled edition loop — authorized 30 September 2026

Ahimanikya requested creating batches and looping through them until complete. This supersedes the earlier no-background-job state: the app confirmed active heartbeat `kabita-live-translation-loop`, returning to this chat every ten minutes. The [edition manifest](../production/translations/edition-batches.json) partitions all 1,602 target versions exactly once. At setup, 45 remaining edition batches and the unassigned-poem batch are actionable; Issue 46 has a separate source hold. Issue 47 is draft-complete.

Each run resumes its unfinished edition, translates directly in the chat in small internal groups, validates and integrates, records progress, and synchronizes the handoff. No external translation service, new agents, site publication or Git push is authorized by this loop. Prior role guidance describing no scheduled execution is superseded only for this explicitly requested translation task. Human editor approval and independent linguistic review remain separate.

The recurring task pauses when all drafts are done, or when only unresolved source holds remain; the latter must be reported as incomplete. Runtime interruptions preserve a resume point and do not mark batches complete. Keep the computer powered on and the app running for local scheduled work; see [official scheduled-task guidance](https://learn.chatgpt.com/docs/automations?surface=app).


## Issue 45 scheduled run

The first scheduled run integrated batches 008–010: 28 new drafts for 14 poems. Full original hashes, source line/stanza coverage, rendered catalogue parity and the public site build pass. Overall total is now 98 draft translations, with 1,504 still pending. These counts are a historical checkpoint; use the live queue for current status.

Poem 784 is a published Odia adaptation credited to Pradeep Biswal under author Tasneem Hossain. The underlying original is not identified in local records. It joins poem 797 in the source-hold list; neither was silently reverse-translated or credited as an original. The loop remains active and moves to Issue 44.

[Issue 45 verification](../records/translation-issue-45-verification.json) · [Batch 008 editorial notes](../production/translations/batch-008/review.json) · [Batch 009 editorial notes](../production/translations/batch-009/review.json) · [Batch 010 editorial notes](../production/translations/batch-010/review.json).


## Issue 44 scheduled run

Batches 011–013 added 22 draft translations for all 11 poems in Issue 44. Source hashes, full stanza and line coverage, rendered catalogue parity, edition integrity and the public build pass. The historical checkpoint is 120 drafts and 1,482 remaining versions, including four held versions for poems 797 and 784. No new source hold arose in this edition.

Editorial notes preserve uncertain grammar, speaker-gender choices and cultural name spellings. The historical and legendary claims in the Sashisena poem are translated as part of the poem, not certified as historical evidence. All versions still need independent linguistic review. Original content, artwork and reader presentation remain unchanged. No publication or push. The active loop resumes Issue 43 with batch 014.

[Issue 44 verification](../records/translation-issue-44-verification.json) · [Batch 011 notes](../production/translations/batch-011/review.json) · [Batch 012 notes](../production/translations/batch-012/review.json) · [Batch 013 notes](../production/translations/batch-013/review.json).


## Issue 43 scheduled run

Batches 014–016 added 30 draft translations for all 15 poems in Issue 43. Full source hashes, stanza and line coverage, rendered catalogue parity, edition integrity and the public build pass. This checkpoint has 150 drafts and 1,452 remaining target versions, including the four previously held versions. No new source/provenance hold was found.

Regional expressions, ambiguous phrasing and provisional Hindi grammatical gender are recorded in the batch notes. The phrases “suspect prime” and “fair outsider” especially need author or native-language review; no definitive interpretation is claimed. Original text, closing addresses and marks, existing credits, artwork and reader design are preserved. All translations remain drafts pending independent linguistic review. No publication or push. The active loop resumes Issue 42 with batch 017.

[Issue 43 verification](../records/translation-issue-43-verification.json) · [Batch 014 notes](../production/translations/batch-014/review.json) · [Batch 015 notes](../production/translations/batch-015/review.json) · [Batch 016 notes](../production/translations/batch-016/review.json).


## Issue 42 scheduled run

Batches 017–019 added 28 draft translations for all 14 poems in Issue 42. Source hashes, complete stanza and line coverage, post-build rendered catalogue parity, edition integrity and public build pass. The historical checkpoint is 178 drafts and 1,424 remaining target versions, including four held versions. No additional source/provenance hold was found.

“Spiral thoughts” needs substantial linguistic review because several source expressions are semantically unsettled; provisional readings are listed in batch 018. Other notes preserve cultural terms, ambiguous images, grammatical gender choices and miniature-poem structure without claiming metrical equivalence. Originals, source closing material, credits, artwork and reader design remain unchanged. All new versions are drafts, with independent linguistic review pending. No publication or push. The active loop resumes Issue 41 with batch 020.

[Issue 42 verification](../records/translation-issue-42-verification.json) · [Batch 017 notes](../production/translations/batch-017/review.json) · [Batch 018 notes](../production/translations/batch-018/review.json) · [Batch 019 notes](../production/translations/batch-019/review.json).


## Issue 41 scheduled run

Batches 020–021 added 20 draft versions for ten poems with usable sources. One entry remains held: poem 727, “Presence in Absence,” credited to Dilip Mohapatra, has an initial “Time” line followed by the exact text of poem 761, “Time,” credited to Divya K Unni. Both preserved HTML captures contain this conflict. No distinct matching-title original was found locally. The correct poem and authorship require editorial confirmation; no translation was created under the conflicting attribution. Existing 761 drafts were preserved, and their batch 016 notes now flag this finding.

Same-author repeated works “Selfie” and “Holi” retain their own edition structures. The three Holi stanzas exactly match the corresponding source stanzas in poem 736; existing draft wording was reused after full reading and comparison, without importing that edition’s additional opening or credit.

Source hashes, complete line/stanza coverage, rendered parity, archive integrity and public build pass for all twenty added versions. Historical checkpoint: 198 drafts; 1,404 target versions remain, including six source-held versions across three poems. Independent linguistic review remains pending. No publication or push. The active loop resumes Issue 40 with batch 022.

[Issue 41 verification and source conflict](../records/translation-issue-41-verification.json) · [Batch 020 notes](../production/translations/batch-020/review.json) · [Batch 021 notes](../production/translations/batch-021/review.json).


## Issue 40 scheduled run

Batches 022–024 added 28 draft translations for all 14 poems in Issue 40. Original hashes, full line/stanza coverage, post-build rendered catalogue parity, edition integrity and the public build pass. Poem 719 retains its 36 single-line stanzas. Historical checkpoint: 226 drafts and 1,376 remaining target versions, including the six versions on existing source holds. No new source hold arose.

Editorial notes preserve regional imagery, literary allusions, rhetorical violence, religious argument and ambiguous source grammar without asserting independent factual verification. Native review is particularly important for the regional images in poem 720. During self-review, ladybug was transliterated rather than guessing an insect name, and moonless kept literal rather than inferring a lunar phase. All originals, closing material, credits, artwork and reader styling remain unchanged. No publication or push. Independent linguistic review is pending. The active loop resumes Issue 39 with batch 025.

[Issue 40 verification](../records/translation-issue-40-verification.json) · [Batch 022 notes](../production/translations/batch-022/review.json) · [Batch 023 notes](../production/translations/batch-023/review.json) · [Batch 024 notes](../production/translations/batch-024/review.json).

## Issue 39 scheduled run

Batches 025–029 added 34 draft translations for all 17 entries in Issue 39, including the complete Hindi novella. Original hashes, complete stanza and line coverage, post-build rendered catalogue parity, edition integrity and the public build pass. Historical checkpoint: 260 drafts and 1,342 remaining target versions, including six versions on existing source holds. No new source hold arose.

The novella retains all 38 prose/verse blocks. “Glacier” retains its 35-block source structure, including a repeated body confirmed in both preserved HTML and JSON; editorial reconciliation is explicitly pending. “Bunyan Tree” has a damaged opening quotation, and “Bustle of Life” needs substantial linguistic review for unclear source expressions and its ending. Provisional readings and cultural terms are recorded in the batch reviews. Nothing was invented to fill missing wording. Originals, credits, artwork and reader design remain unchanged. All generated versions remain drafts pending independent linguistic review. No publication or push. The active loop resumes Issue 38 with batch 030.

[Issue 39 verification](../records/translation-issue-39-verification.json) · [Batch 025 notes](../production/translations/batch-025/review.json) · [Batch 026 notes](../production/translations/batch-026/review.json) · [Batch 027 notes](../production/translations/batch-027/review.json) · [Batch 028 notes](../production/translations/batch-028/review.json) · [Batch 029 notes](../production/translations/batch-029/review.json).


## Issue 38 scheduled run

Batches 030–032 added 26 draft translations for all 13 poems in Issue 38. Original hashes, full line/stanza coverage, post-build rendered catalogue parity, edition integrity and the public build pass. “Dilemma” retains sixteen one-line stanzas; isolated endings and repeated refrains elsewhere remain intact. Historical checkpoint: 286 drafts and 1,316 remaining target versions, including six versions on existing source holds. No new source hold arose.

Review notes record the compressed imagery in the Odia poems, ambiguous fragments in “Dilemma,” grammatical narrator choices, and the supplied painter-name spellings in “Dark Matters After All.” Literary, historical and social claims were translated as the poets present them, without invented context or factual certification. Self-review removed an unnecessary love-song genre gloss and clarified the eagle term. All originals, existing credits, artwork and reader styling are preserved. Independent linguistic review remains pending. No publication or push. The active loop resumes Issue 37 with batch 033.

[Issue 38 verification](../records/translation-issue-38-verification.json) · [Batch 030 notes](../production/translations/batch-030/review.json) · [Batch 031 notes](../production/translations/batch-031/review.json) · [Batch 032 notes](../production/translations/batch-032/review.json).


## Issue 37 scheduled run

Batches 033–036 added 38 draft translations for all 19 entries in Issue 37. Source hashes, full stanza/line coverage, rendered catalogue parity in both preview and public output, edition integrity and the public build pass. Historical checkpoint: 324 drafts and 1,278 remaining target versions, including six versions on the three existing source holds. No new hold arose.

“Father” retains eleven stanzas, household food terms and kite/granary imagery; regional terms remain flagged for native review. “प्रहार” retains its embedded poem headings, “The Man in White” its chorus and epilogue, and “Autumn Returning” its single forty-line stanza. Religious, scientific-sounding, historical and social claims are preserved as poetry, not independently certified assertions. Pronoun and terminology choices are documented; amber was clarified as a colour during self-review. All originals, named credits, artwork and reader styling remain unchanged. No publication or push. Independent linguistic review is pending. The active loop resumes Issue 36 with batch 037.

[Issue 37 verification](../records/translation-issue-37-verification.json) · [Batch 033 notes](../production/translations/batch-033/review.json) · [Batch 034 notes](../production/translations/batch-034/review.json) · [Batch 035 notes](../production/translations/batch-035/review.json) · [Batch 036 notes](../production/translations/batch-036/review.json).


## Issue 36 continued run

Batches 037–040 added 34 draft translations for all 17 entries in Issue 36. Original hashes, complete stanza/line coverage, preview and public-output catalogue parity, edition integrity and the public build pass. Historical checkpoint: 358 drafts and 1,244 remaining target versions, including six versions on existing source holds. No new hold arose.

The five haiku retain their three-line forms and bullet separators without a claim of syllabic equivalence. Long narrative lines and separate final lines remain intact. For poem 644, the preserved HTML states that the author writes in both Chinese and English; no poem-specific translator credit or conflicting original was found, so the supplied English was used without constructing another original. Notes flag unresolved phrases in poems 642 and 655, regional/cultural vocabulary, and provisional grammatical voice choices. No unmentioned war, deity, biography or social event was added. Existing originals, credits, artwork and reader design remain unchanged. No publication or push. Independent linguistic review is pending. Continue Issue 35 with batch 041.

[Issue 36 verification](../records/translation-issue-36-verification.json) · [Batch 037 notes](../production/translations/batch-037/review.json) · [Batch 038 notes](../production/translations/batch-038/review.json) · [Batch 039 notes](../production/translations/batch-039/review.json) · [Batch 040 notes](../production/translations/batch-040/review.json).


## Issue 35 continued run

Batches 041–046 added 54 draft translations for all 27 entries in Issue 35. Original hashes, complete stanza/line coverage, preview and public-output catalogue parity, edition integrity and public build pass. Historical checkpoint: 412 drafts and 1,190 remaining target versions, including six versions on existing source holds. No new source hold arose.

Poetic testimony about Manipur, other conflicts and Kedarnath retains the authors’ named places and claims without invented incidents or factual certification. Dense imagery in poems 630/632 and damaged grammar in 629 require linguistic review. Poem 626 retains the trailing BIO source marker as a separate translated line for explicit editorial reconciliation; the incomplete phone fragment in 616 is not repaired. Haiku forms, miniature lines, closing material and all repetitions are preserved. No claim of metrical equivalence or independent native review. Originals, credits, artwork and reader design remain unchanged. No publication or push. Continue Issue 34 with batch 047.

[Issue 35 verification](../records/translation-issue-35-verification.json) · [Batch 041 notes](../production/translations/batch-041/review.json) · [Batch 042 notes](../production/translations/batch-042/review.json) · [Batch 043 notes](../production/translations/batch-043/review.json) · [Batch 044 notes](../production/translations/batch-044/review.json) · [Batch 045 notes](../production/translations/batch-045/review.json) · [Batch 046 notes](../production/translations/batch-046/review.json).

## Issue 34 continued run

Batches 047–050 added 38 draft translations for all 19 entries in Issue 34. Original hashes, full stanza/line coverage, preview and public-output catalogue parity, edition integrity and public build pass. Historical checkpoint: 450 drafts and 1,152 remaining target versions, including six versions on existing source holds. No new hold arose.

Pahalgam testimony and political satire retain the authors’ images and claims without adding factual certification or unnamed actors. Regional games, food, plants, recurrent refrains, symbols and closing credits remain. The unusual “tinkling of the bees” in poem 600 is preserved, not silently repaired. Unresolved conditional grammar in 606 and mixed metaphors/awkward phrases in 608 need linguistic review; grammatical gender choices and culturally specific words are documented in the batch notes. All originals, existing credits, artwork and reader design are preserved. No publication or push. Independent linguistic review remains pending. Continue Issue 33 with batch 051.

[Issue 34 verification](../records/translation-issue-34-verification.json) · [Batch 047 notes](../production/translations/batch-047/review.json) · [Batch 048 notes](../production/translations/batch-048/review.json) · [Batch 049 notes](../production/translations/batch-049/review.json) · [Batch 050 notes](../production/translations/batch-050/review.json).

## Issue 33 continued run

Batches 051–054 added 38 draft translations for all 19 entries in Issue 33. Original hashes, complete stanza/line coverage, preview and public-output catalogue parity, edition integrity and public build pass. Historical checkpoint: 488 drafts and 1,114 remaining target versions, including six versions on existing source holds. No new hold arose.

Dense butter-figurine imagery, regional expressions, damaged spelling and provisional grammatical gender need linguistic review. Pahalgam testimony and retaliatory imagery are preserved as source poetry, without added actors or factual certification. The many one-line stanzas of poem 588 and alternating short stanzas of 582 remain. Poem 585 abruptly turns into a radio passage: the preserved HTML confirms the complete text under the same title/author, and no separate matching local record was found. All lines and the repeated opening are retained for explicit editorial reconciliation. No source reconstruction, silent split, publication or push. Originals, credits, artwork and reader design remain unchanged. Independent linguistic review pending. Continue Issue 32 with batch 055.

[Issue 33 verification](../records/translation-issue-33-verification.json) · [Batch 051 notes](../production/translations/batch-051/review.json) · [Batch 052 notes](../production/translations/batch-052/review.json) · [Batch 053 notes](../production/translations/batch-053/review.json) · [Batch 054 notes](../production/translations/batch-054/review.json).

## Issue 32 continued run

Batches 055–058 added 38 draft translations for all 19 entries in Issue 32. Original hashes, complete stanza/line coverage, preview and public-output catalogue parity, edition integrity and public build pass. Historical checkpoint: 526 drafts and 1,076 remaining target versions, including six versions on existing source holds. No new source hold arose.

Regional tribal/youth-house vocabulary and the damaged tribute line in 560 need linguistic review. Single-line stanzas, long prose-like lines, ghazal couplets, copyright credit and refrains are retained. Poem 566 retains its damaged title suffix for explicit editorial cleanup. Sloppy hills in 563 and vegan/pagan, humane reach and other unusual phrases in 574 are marked provisional; source originals remain unchanged. War, environmental and devotional imagery is translated as literary content without factual certification. Independent linguistic review pending. No publication, push or change to reader design/artwork. Continue Issue 31 with batch 059.

[Issue 32 verification](../records/translation-issue-32-verification.json) · [Batch 055 notes](../production/translations/batch-055/review.json) · [Batch 056 notes](../production/translations/batch-056/review.json) · [Batch 057 notes](../production/translations/batch-057/review.json) · [Batch 058 notes](../production/translations/batch-058/review.json).

## Issue 31 continued run

Batches 059–060 added 14 draft translations for all seven entries in Issue 31. Original hashes, full stanza/line coverage, preview and public-output catalogue parity, edition integrity and public build pass. Historical checkpoint: 540 drafts and 1,062 remaining target versions, including six versions on existing source holds. No new hold arose.

Poem 550 retains a literal br> source fragment for explicit editorial cleanup; lips/adhar word-register change and regional play term need review. Poem 551 retains named heritage references and literary historical/devotional claims without certification. Poem 552 contains extensively unclear grammar; interpretations are provisional and the unresolved hit least fragment stays quoted rather than silently reconstructed. All source lines and closing material remain. Independent linguistic review pending. Originals, existing credits, artwork and reader design unchanged; no publication or push. Continue Issue 30 with batch 061.

[Issue 31 verification](../records/translation-issue-31-verification.json) · [Batch 059 notes](../production/translations/batch-059/review.json) · [Batch 060 notes](../production/translations/batch-060/review.json).

## Issue 30 continued run

Batches 061–062 added 16 draft translations for all eight entries in Issue 30. Original hashes, complete stanza/line coverage, preview and public-output catalogue parity, edition integrity and public build pass. Historical checkpoint: 556 drafts and 1,046 remaining target versions, including six versions on existing source holds. No new hold arose.

All seven spring refrains, the 34-line editor poem and original stanza forms remain. Cultural vocabulary, ambiguous descriptors and provisional grammatical gender choices are documented. Glass-shell imagery in 543 is retained literally. Mole in 544 was transliterated in both targets during self-review to avoid conflating species; the poem’s behavioural and symbolic assertions are not independently certified. Originals, credits, artwork and reader design remain unchanged. Independent linguistic review pending. No publication or push. Continue Issue 29 with batch 063.

[Issue 30 verification](../records/translation-issue-30-verification.json) · [Batch 061 notes](../production/translations/batch-061/review.json) · [Batch 062 notes](../production/translations/batch-062/review.json).

## Issue 29 continued run

Batches 063–066 added 36 draft versions for all 18 entries in Issue 29. Original hashes, full stanza/line coverage, preview and public-output catalogue parity, edition integrity and public build pass. Historical checkpoint: 592 drafts and 1,010 remaining target versions, including six versions on existing source holds. No new hold arose.

Poem 521 includes two conversational paragraphs, confirmed in the preserved original HTML; they are retained as source data, never followed as instructions, and flagged as probable drafting residue. Poem 526 shares an exact eight-stanza prefix with same-author poem 552: existing draft wording and caveats were reused, and the additional titled street narrative was translated in full. The records remain distinct. All ten haiku in 527 remain despite a five-haiku title, with no syllabic-equivalence claim. The calendar note in 528 and statistics in 524 are preserved as source claims, not independently verified current facts. Local provenance for 534 supports using the supplied English; no missing original was reconstructed. Ambiguous expressions and grammatical gender choices remain for linguistic review. No publication or push; originals, credits, artwork and reader design preserved. Continue Issue 28 with batch 067.

[Issue 29 verification](../records/translation-issue-29-verification.json) · [Batch 063 notes](../production/translations/batch-063/review.json) · [Batch 064 notes](../production/translations/batch-064/review.json) · [Batch 065 notes](../production/translations/batch-065/review.json) · [Batch 066 notes](../production/translations/batch-066/review.json).

## Issue 28 continued run

Batch 067 added 10 draft versions for all five entries in Issue 28. Original hashes, full stanza/line coverage, preview and public-output catalogue parity, edition integrity and public build pass. Historical checkpoint: 602 drafts and 1,000 remaining target versions, including six versions on existing source holds. No new hold arose.

The nautical sense of SHORING, wishes/horses proverb and ambiguous light/granite expressions need independent idiom review. Meru, four tusks, named sites, twelve thousand craftsmen and twelve years are retained as poetic source claims, not independently certified facts. The trailing !< in the title of poem 518 remains for explicit editorial cleanup. The lesser-God metaphor in 519 needs sensitive native-language review. No publication or push; originals, credits, artwork and reader design preserved. Continue Issue 27 with batch 068.

[Issue 28 verification](../records/translation-issue-28-verification.json) · [Batch 067 notes](../production/translations/batch-067/review.json).

## Issue 27 continued run

Batches 068–069 added 16 draft versions for eight entries in Issue 27. One additional record (506) remains source-held, so this edition is not wholly complete. Original hashes, full stanza/line coverage, preview/public catalogue parity, edition integrity and public build pass. Historical checkpoint: 618 drafts and 984 remaining target versions, including eight held versions across four records.

The preserved original HTML confirms that The lovelorn crane, attributed to Paramita Mukherjee Mullick, appends the title Cheerio, an explicit Gopal Lahiri credit, and seven couplets. A local search found no separate Cheerio record. Resolve the two intended poem records, boundaries and authors before translating this mixed record under one author. No content or credits were removed.

Poem 512 retains pistoled pier literally and interprets wamp tentatively; both require editorial confirmation. Prose-poem 514 preserves its [1,1,3] line structure and unusual syntax. Ero in 507 remains as printed. The explicit negation in 508 remains a negation; the unusual verb substances in 511 has a documented tentative reading. All versions require independent linguistic review. No publication, push or reader-design change. Continue actionable Issue 26 with batch 070.

[Issue 27 verification](../records/translation-issue-27-verification.json) · [Batch 068 notes](../production/translations/batch-068/review.json) · [Batch 069 notes](../production/translations/batch-069/review.json).

## Issue 26 continued run

Batches 070–071 added 20 draft versions for all ten poems in Issue 26, translating directly from three Odia, two Hindi and five English sources. Original hashes, complete stanza/line coverage, preview/public catalogue parity, edition integrity and public build pass. Historical checkpoint: 638 drafts and 964 remaining target versions, including eight held versions across four earlier records. No new source hold arose.

The ambiguous monetary token ପାଁଶ in 500 is retained literally rather than assigned an unverified amount. Its abusive first-person satire remains intact without endorsement; tone and idiom require native review. Poem 499 has damaged imperative syntax and a Majaz fragment; these are explicitly flagged without inventing missing words. Affiliations in 497 and 500 and the location in 498 remain in their source positions. Barial in 501 and charred colloids in 503 are retained without unsupported corrections. The half-cycle temporal phrase in 504 and long lines in 505 remain intact. All translations require independent linguistic review. No publication, push, source change, artwork change or reader-design change. Continue Issue 25 with batch 072.

[Issue 26 verification](../records/translation-issue-26-verification.json) · [Batch 070 notes](../production/translations/batch-070/review.json) · [Batch 071 notes](../production/translations/batch-071/review.json).

## Issue 25 continued run

Batches 072–074 added 26 draft versions for all thirteen poems in Issue 25, directly from four Odia, three Hindi and six English sources. Original hashes, complete stanza/line coverage, preview/public catalogue parity, edition integrity and public build pass. Historical checkpoint: 664 drafts and 938 remaining target versions, including eight held versions across four earlier records. No new source hold arose.

The source word corpses in 494 remains literal, without substituting words. The uncertain ଈଶିକାର in 483 and seatherny in 486 remain verbatim; the unusual ଅର୍ବୁଦତା in 484 has a provisional reading. The source Hindi–Muslim pairing in 493 is flagged as a likely typo without silently changing it. Poem 495 keeps its entire three-line footnote, named bhakti poets and literal br> residue for explicit cleanup review. Poem 488 retains its economic assertion as a source claim without presenting independent verification. All versions need independent linguistic review. No publication, push, source change, artwork change or reader-design change. Continue Issue 24 with batch 075.

[Issue 25 verification](../records/translation-issue-25-verification.json) · [Batch 072 notes](../production/translations/batch-072/review.json) · [Batch 073 notes](../production/translations/batch-073/review.json) · [Batch 074 notes](../production/translations/batch-074/review.json).

## Issue 24 continued run

Batches 075–078 added 34 draft versions for seventeen poems in Issue 24. One poem remains source-held, so the edition is not wholly complete. Original hashes, full stanza/line coverage, preview/public catalogue parity, edition integrity and public build pass. Historical checkpoint: 698 drafts and 904 remaining target versions, including ten held versions across five records.

The Temple of Afruza Akhtar (472), attributed to Nilim Kumar, explicitly credits Bibekananda Choudhury as translator. The preserved original HTML confirms this credit. A local catalogue search found no matching underlying original; do not reconstruct one from the English translation or relabel that translation as original. Obtain the original and its language, then reconcile labels and preserve the translator credit before continuing this record.

Ritual imagery in 470 retains tahia, goti-pahandi and charamala with native cultural review pending. The logical ambiguity in 465 remains. The ambiguous groove in 473 remains verbatim after self-review removed a speculative grove reading; the three-letter word is not invented. Other metaphor and grammatical-gender choices are documented in batch reviews. No publication, push, source change, artwork change or reader-design change. Continue Issue 23 with batch 079.

[Issue 24 verification](../records/translation-issue-24-verification.json) · [Batch 075 notes](../production/translations/batch-075/review.json) · [Batch 076 notes](../production/translations/batch-076/review.json) · [Batch 077 notes](../production/translations/batch-077/review.json) · [Batch 078 notes](../production/translations/batch-078/review.json).

## Issue 23 continued run

Batches 079–081 added 22 draft versions for all eleven poems in Issue 23, directly from five Odia, one Hindi and five English sources. Original hashes, complete stanza/line coverage, preview/public catalogue parity, edition integrity and public build pass. Historical checkpoint: 720 drafts and 882 remaining target versions, including ten held versions across five earlier records. No new hold arose.

Archaic and ambiguous imagery in 460 is documented; ରାତିହାସ remains verbatim and the Sanskrit fragment is not expanded into an unverified quotation. The Lost Princess (455) shares author/title and imagery with poem 503 in Issue 26, but its 35-line single-stanza source was read and translated separately; matching phrases align while the distinct source structure remains. Neither record was merged or replaced. The unresolved charred-colloids expression retains its earlier caveat. The source contradiction about dreams taking root in 458 remains intact, and twenty-four in 459 is not assigned an invented date or age. Independent linguistic review remains necessary. No publication, push, source change, artwork change or reader-design change. Continue Issue 22 with batch 082.

[Issue 23 verification](../records/translation-issue-23-verification.json) · [Batch 079 notes](../production/translations/batch-079/review.json) · [Batch 080 notes](../production/translations/batch-080/review.json) · [Batch 081 notes](../production/translations/batch-081/review.json).

## Issue 22 continued run

Batches 082–084 added 24 draft versions for all twelve poems in Issue 22, directly from two Odia, two Hindi and eight English sources. Original hashes, complete stanza/line coverage, preview/public catalogue parity, edition integrity and public build pass. Historical checkpoint: 744 drafts and 858 remaining target versions, including ten held versions across five earlier records. No new hold arose.

The masked insult in 444 remains masked; its critique of misogyny is translated without endorsement or embellishment. Atypical words in 443 and 442 have context-based readings flagged for native review. The mythological account and 28-month period in 446 remain the source claims, not independently verified history. The fourteen stanzas of 1971, Noakhali (450), including cross-stanza sentences, remain intact; sexual violence is conveyed soberly without invented detail. Unfinished (451) ends with the incomplete We as published. Independent linguistic review remains necessary. No publication, push, source change, artwork change or reader-design change. Continue Issue 21 with batch 085.

[Issue 22 verification](../records/translation-issue-22-verification.json) · [Batch 082 notes](../production/translations/batch-082/review.json) · [Batch 083 notes](../production/translations/batch-083/review.json) · [Batch 084 notes](../production/translations/batch-084/review.json).

## Issue 21 continued run

Batches 085–088 added 34 draft versions for all 17 poems: six Odia, two Hindi and nine English originals. Original hashes, full line/stanza coverage, preview/public catalogue parity, edition integrity and public build pass. Historical checkpoint: 778 drafts, 824 remaining target versions, including ten versions across five existing source holds. No new hold arose.

Uncertain Odia expressions, Tripura-vijayi, singular poetic hum, the source artifact ¬¬¬, awkward English grammar in poem 433 and approximate thrills/trills wordplay remain explicitly flagged in batch reviews. Mythic, scientific and event claims remain the poets’ claims. One newly drafted Hindi line in poem 436 was corrected to remove an invented realm of death. All versions remain drafts; same-assistant checks do not replace independent linguistic review. Originals, existing credits, artwork and reader design preserved; no publication or push. Continue Issue 20 with batch 089.

[Issue 21 verification](../records/translation-issue-21-verification.json) · [Batch 085 notes](../production/translations/batch-085/review.json) · [Batch 086 notes](../production/translations/batch-086/review.json) · [Batch 087 notes](../production/translations/batch-087/review.json) · [Batch 088 notes](../production/translations/batch-088/review.json).

## Issue 20 continued run

Batches 089–091 added 22 draft versions for all 11 entries: three Odia, one Hindi and seven English originals. Original hashes, exact line/stanza coverage, preview/public catalogue parity, edition integrity and public build pass. Historical checkpoint: 800 drafts, 802 remaining target versions, including ten versions across five existing source holds. No new hold arose.

Poem 416 has 42 stanzas, mostly individual lines; that structure is preserved explicitly for later editorial spacing review. Poem 418 contains the internal heading Deaths and the Accountant, confirmed in the local HTML under the same author: full captured text is translated, with editorial segmentation pending. Source place-name spelling, ambiguous draught-bitten/winded phrasing and the land-of-the-leal reference are flagged. Poem 424 retains the speaker change central to its critique of victim-blaming. All translations remain drafts awaiting independent linguistic review. Originals, credits, artwork and reader design preserved; no publication or push. Continue Issue 19 with batch 092.

[Issue 20 verification](../records/translation-issue-20-verification.json) · [Batch 089 notes](../production/translations/batch-089/review.json) · [Batch 090 notes](../production/translations/batch-090/review.json) · [Batch 091 notes](../production/translations/batch-091/review.json).

## Issue 19 continued run

Batches 092–094 added 24 draft versions for all 12 entries: seven Odia, three Hindi and two English originals. Original hashes, exact line/stanza coverage, preview/public catalogue parity, edition integrity and public build pass. Historical checkpoint: 824 drafts, 778 remaining target versions, including ten versions across five existing source holds. No new hold arose.

Missing source word spaces in Bhitarkanika remain unchanged; translation segmentation and uncertain expressions are recorded. Three Short Poems retains all three numbered sections. The strī/long-ī wordplay, uncertain शाम and शबनम/ज्योति senses, title/body gender discrepancy in poem 412, and surreal long-line imagery in poem 411 need independent linguistic review. An unnamed sal-forest demoness has not been assigned an invented identity. All versions remain drafts; original poems, existing credits, artwork and reader design are preserved. No publication or push. Continue Issue 18 with batch 095.

[Issue 19 verification](../records/translation-issue-19-verification.json) · [Batch 092 notes](../production/translations/batch-092/review.json) · [Batch 093 notes](../production/translations/batch-093/review.json) · [Batch 094 notes](../production/translations/batch-094/review.json).

## Issue 18 continued run

Batches 095–100 added 46 draft versions for 23 actionable entries. One entry remains incomplete: poem 385, ଅମ୍ଲାନ ବନ୍ଧୁତ୍ୱ by Monalisa Dash Dwibedy, has only the repeated title in both the JSON and preserved original HTML. Obtain the complete Odia original or explicit editorial confirmation of an intentional one-line poem. This is a source hold, not completed translation work.

Original hashes, exact line/stanza coverage, preview/public catalogue parity, edition integrity and public build pass. All 24 rendered originals, including the held entry, remain unchanged. Historical checkpoint: 870 drafts, 732 remaining target versions, including twelve versions across six source holds.

The Last Faith retains all 134 lines, uneven source stanza divisions and literal separators; layered mythological names, rootfall/loom/hood and ecological imagery need independent review. Plums versus Pullum includes a second titled section, confirmed in the same preserved author page; full text retained with editorial segmentation pending. Source uncertainties and language wordplay are recorded in each batch review. Existing credits, artwork and reader design preserved. No publication or push. Continue Issue 17 with batch 101; resolve the held source separately.

[Issue 18 verification](../records/translation-issue-18-verification.json) · [Source holds](../production/translations/source-holds.json).

## Issue 17 continued run

Batches 101–104 added 38 draft versions for all 19 entries: two Odia, four Hindi and thirteen English originals. Original hashes, exact line/stanza coverage, preview/public catalogue parity, edition integrity and public build pass. Historical checkpoint: 908 drafts, 694 remaining target versions, including twelve versions across six existing source holds. No new hold arose.

Uncertain slang in poem 367 and damaged nitihata in poem 369 are retained in quoted transliteration and explicitly flagged. The unknowable preserves all 78 lines and its nine-creature list, including the source’s lion/tiger distinction; vulnerability-fire and mind-tongues imagery need specialist review. Non-graphic abuse critique in poem 360 and conditional patriotic rhetoric in 374 are preserved without added detail or advice. Original poems, existing credits, artwork and reader design are unchanged; all new versions await independent linguistic review. No publication or push. Continue Issue 16 with batch 105.

[Issue 17 verification](../records/translation-issue-17-verification.json) · [Batch 101 notes](../production/translations/batch-101/review.json) · [Batch 102 notes](../production/translations/batch-102/review.json) · [Batch 103 notes](../production/translations/batch-103/review.json) · [Batch 104 notes](../production/translations/batch-104/review.json).

## Issue 16 continued run

Batches 105–106 added 20 draft versions for all ten entries: four Odia and six English originals. Original hashes, exact line/stanza coverage, preview/public catalogue parity, edition integrity and public build pass. Historical checkpoint: 928 drafts, 674 remaining target versions, including twelve versions across six existing source holds. No new hold arose.

Bali Jatra retains local names, foods, shola boat imagery, its embedded lyric and source address block. Smita Hasa preserves source tensions and final separator/location. Damaged phrasing in poem 355 is flagged; peacock flower remains transliterated to avoid unsupported species identification. Hyderabad monument/devotional claims in 354 are translated as the poem’s claims without asserting independent verification. Originals, existing credits, artwork and reader design preserved; all generated versions remain drafts awaiting independent linguistic review. No publication or push. Continue Issue 15 with batch 107.

[Issue 16 verification](../records/translation-issue-16-verification.json) · [Batch 105 notes](../production/translations/batch-105/review.json) · [Batch 106 notes](../production/translations/batch-106/review.json).

## Issue 15 continued run

Batches 107–108 added 14 draft versions for all seven entries: two Odia and five English originals. Original hashes, exact line/stanza coverage, preview/public catalogue parity, edition integrity and public build pass. Historical checkpoint: 942 drafts, 660 remaining target versions, including twelve versions across six existing source holds. No new hold arose.

Local ecological imagery and place names in 340 remain unexpanded where uncertain; both Odia poems retain their source address blocks. Gender and religious assertions in 343 remain the author’s critique, not independently verified claims. Abstract philosophical syntax in 346 is flagged for linguistic review; lotus and lily imagery remain distinct. Poem 347 retains R kakima, its chronology and anxiety imagery without inventing a diagnosis. All originals, existing credits, artwork and reader design preserved. All generated versions await independent linguistic review. No publication or push. Continue Issue 14 with batch 109.

[Issue 15 verification](../records/translation-issue-15-verification.json) · [Batch 107 notes](../production/translations/batch-107/review.json) · [Batch 108 notes](../production/translations/batch-108/review.json).

## Issue 14 continued run

Batches 109–112 added 34 draft versions for 17 usable entries: two Odia, two Hindi and thirteen English originals. Original hashes, exact line/stanza coverage, preview/public catalogue parity, edition integrity and public build pass. All 18 original rendered texts remain unchanged, including the held record. Historical checkpoint: 976 drafts, 626 remaining target versions, including fourteen versions across seven source holds.

Issue 14 is not fully complete: poem 332 combines You Will Come Again by Nurul Hoque with a separately titled Lethe explicitly credited to Pritha Chakraborty. Preserved HTML confirms the mixture. Lethe in Issue 27 (507) is a different version and cannot substitute for the appended text. Confirm record boundaries and authorship; do not translate both as a single-author work.

Manika/curd/ring, Konark, namabali and kalisi references are retained without added legend. Nirvana retains all thirteen blocks. Abstract wording in 331, angora skin in 335, and provisional gender/kinship choices are flagged in batch notes. The complete source footnote in 333 is preserved. All generated versions await independent linguistic review. Originals, existing credits, artwork and reader design preserved. No publication or push. Continue Issue 13 with batch 113.

[Issue 14 verification](../records/translation-issue-14-verification.json) · [Source holds](../production/translations/source-holds.json).

## Issue 13 continued run

Batches 113–116 added 34 draft versions for 17 usable entries: five Odia, two Hindi and ten English originals. Original hashes, exact line/stanza coverage, preview/public catalogue parity, edition integrity and public build pass. All 18 original rendered texts remain unchanged, including the held record. Historical checkpoint: 1010 drafts, 592 remaining target versions, including sixteen versions across eight source holds.

Issue 13 is not fully complete: The Solar Path (319) by Tuhinamshu Rath explicitly credits Prof. Raj Kishore Mishra as translator; preserved HTML confirms. No identity-matched underlying original or original-language identification is present locally. An Odia-poetry biography does not prove the source language of this particular poem. Obtain the original and reconcile labels; preserve the published translation and credit.

Dialect terms in Nadanaibedya (309) remain transliterated and flagged rather than invented. Rural references in Village (320) and the long social narrative in 318 preserve full lineation. Poem 311 is a distinct same-author edition variant of 327, with 28 rather than 31 lines; neither is merged or overwritten. Residual p> in 312 is omitted only from translation, original untouched. All generated versions await independent linguistic review. Originals, existing credits, artwork and reader design preserved. No publication or push. Continue Issue 12 with batch 117.

[Issue 13 verification](../records/translation-issue-13-verification.json) · [Source holds](../production/translations/source-holds.json).

## Issue 12 continued run

Batches 117–120 added 34 draft versions for all seventeen entries: three Odia, three Hindi and eleven English originals. Original hashes, exact line/stanza coverage, preview/public catalogue parity, edition integrity and public build pass. Historical checkpoint: 1044 drafts, 558 remaining target versions, including sixteen versions across eight existing source holds. No new hold arose.

Chhinnamastika retains all ten quatrains and its repeated final couplet, translating the author’s religious and gender rhetoric without endorsement or added instructions. Naubath Pahad retains its own 29-line edition version, separate from poem 354. Observation retains the source hearing/listening inversion with an explicit review note. The Jayanta Mahapatra tribute’s unqualified first-Indian award claim is preserved as authored verse and flagged for factual/editorial review before publication. All originals, existing credits, artwork and reader design preserved; all generated versions await independent linguistic review. No publication or push. Continue Issue 11 with batch 121.

[Issue 12 verification](../records/translation-issue-12-verification.json) · [Batch 119 notes](../production/translations/batch-119/review.json).

## Issue 11 continued run

Batches 121–124 integrated 34 draft versions for all seventeen entries: two Odia, three Hindi and twelve English originals. Thirty-two versions were newly translated; two reuse the directly translated poem-304 drafts after confirming exact source text, title, author and hash equality for Crossing (268). Edition records remain separate. Original hashes, exact line/stanza coverage, preview/public catalogue parity, edition integrity and public build pass. Historical checkpoint: 1078 drafts, 524 remaining target versions, including sixteen versions across eight existing source holds. No new hold arose.

The fifteen deeply enjambed couplets of Of The Human Soul remain intact. Let us run away retains all 44 lines, including its two different repeated sequences. Unlikely man preserves unclear documentary syntax and bought a book fair instead of silently rewriting these. Odia idioms in 278 and temporal tak clauses in 269 are flagged. All originals, existing credits, artwork and reader design preserved; all generated versions await independent linguistic review. No publication or push. Continue Issue 10 with batch 125.

[Issue 11 verification](../records/translation-issue-11-verification.json) · [Batch 122 provenance](../production/translations/batch-122/review.json).

## Issue 10 continued run

Batches 125–129 integrated 46 draft versions for all 23 entries: seven Odia, four Hindi and twelve English originals. Original hashes, exact line/stanza coverage, preview/public catalogue parity, edition integrity and public build pass. Historical checkpoint: 1124 drafts, 478 remaining target versions, including sixteen versions across eight existing source holds. No new hold arose.

Long lines, enjambment and repeated sequences remain intact. Cultural references include Meru, Draupadi, wooden sandals, chautisha, Anganwadi and floral adornments. Ambiguous words and constructions are recorded per poem: panikacha, Amber, nectar in a bund, diagnostic phrasing in Anger and the steaming volcano metaphor. Provisional Hindi grammatical gender is flagged where the English leaves it unspecified. Quotation artifacts normalized only in target text. All originals, existing credits, artwork and reader design preserved; all generated versions await independent linguistic review. No publication or push. Continue Issue 9 with batch 130.

[Issue 10 verification](../records/translation-issue-10-verification.json).

## Issue 9 continued run

Batches 130–132 integrated 26 draft versions for all thirteen entries: two Odia, five Hindi and six English originals. Original hashes, exact line/stanza coverage, preview/public catalogue parity, edition integrity and public build pass. Historical checkpoint: 1150 drafts, 452 remaining target versions, including sixteen versions across eight existing source holds. No new hold arose.

Dhauli, Daya, Chandashoka/Dharmashoka and the Nandighosha image remain identifiable; no speakers were added to the unnamed historical quotations. Ten ghazal couplets preserve meaning without claiming metrical equivalence. All ten numbered haiku remain in the source’s nine blocks, with the joined sixth/seventh block explicitly flagged for editorial reconciliation. The five long lines of Vicharon ki Udaan remain intact. Social irony about educated daughters is preserved, as are ambiguous boons/adversary in In This Body. All originals, credits, artwork and reader design preserved; all generated versions await independent linguistic review. No publication or push. Continue Issue 8 with batch 133.

[Issue 9 verification](../records/translation-issue-09-verification.json).

## Issue 8 continued run

Batches 133–136 integrated 32 draft versions for sixteen actionable entries: five Odia, three Hindi and eight English sources. Issue 8 remains incomplete: Swing (219) explicitly credits a Telugu original by Raghu Seshabhattar and the English translation by Elanaaga; the preserved HTML confirms this and no matching Telugu original was found in the local catalogue. Held both target tasks and preserved text/credit. No original was reconstructed.

Original hashes, exact line/stanza coverage, preview/public catalogue parity, edition integrity and public build pass. All seventeen existing texts remain unchanged in rendered output, including the held English translation. Historical checkpoint: 1182 drafts, 420 remaining target versions, including eighteen versions across nine source holds.

Ahalya and twelve-cubit sari imagery, the Sanskrit prayer, tiger allegory, liquor imagery, Wellington and Najifa remain in their source contexts. Ambiguous burden, cult, narrator shifts and Hindi gender/kinship choices are recorded for linguistic review. All originals, credits, artwork and reader design preserved; all generated versions await independent linguistic review. No publication or push. Continue Issue 7 with batch 137.

[Issue 8 verification](../records/translation-issue-08-verification.json) · [Source holds](../production/translations/source-holds.json).

## Issue 7 continued run

Batches 137–140 integrated 38 draft versions for nineteen actionable entries: ten Odia, two Hindi and seven English sources. Issue 7 remains incomplete: Art (197) credits Gabor Gyukics and Afghanistan (203) credits Shyamashri Ray Karmakar as translators. Preserved HTML confirms each credit; no identity-matched underlying originals or source-language identification was found locally. Held four targets, preserving each published English translation and credit. No original reconstructed.

Original hashes, exact line/stanza coverage, preview/public catalogue parity, edition integrity and public build pass. All 21 existing texts remain unchanged in rendered output, including both held translations. Historical checkpoint: 1220 drafts, 382 remaining target versions, including 22 versions across eleven source holds.

The fifteen-part Prasanna poem, 67-line Deepavali invocation, economic poem dedication and section marker, long-line teardrop poem, song-poet refrains and river couplets retain their structures. Odisha ritual terms and uncertain idioms are recorded; source typos are interpreted only in target drafts. All originals, credits, artwork and reader design preserved; all generated versions await independent linguistic review. No publication or push. Continue Issue 6 with batch 141.

[Issue 7 verification](../records/translation-issue-07-verification.json) · [Source holds](../production/translations/source-holds.json).

## Issue 6 continued run

Batches 141–145 integrated 46 draft versions for all 23 entries: six Odia, two Hindi and fifteen English originals. Original hashes, exact line/stanza coverage, preview/public catalogue parity, edition integrity and public build pass. Historical checkpoint: 1266 drafts, 336 remaining target versions, including 22 versions across eleven existing source holds. No new hold arose.

The standalone semicolon block in Monday blues on a Friday is explicitly retained pending editorial reconciliation. New Generation preserves its copyright/name/location block; Playing Jenga preserves its explanatory footnote. Cultural terms, long lines, poem refrains and source mythic/historical claims remain in context, with no new biographical or factual assertions. Uncertain spellings and constructions including cuckoon, might/night, draught/drought, and Invisible Scars syntax are recorded for linguistic review. All originals, credits, artwork and reader design preserved; all generated versions await independent linguistic review. No publication or push. Continue Issue 5 with batch 146.

[Issue 6 verification](../records/translation-issue-06-verification.json).

## Issue 5 continued run

Batches 146–149 integrated 36 draft versions for all 18 entries. Original hashes, exact line/stanza coverage, preview/public catalogue parity, edition integrity and public build pass. Historical checkpoint: 1302 drafts, 300 remaining target versions, including 22 versions across eleven existing source holds. No new hold arose.

Preserved the cultural references in the Odia poems, Misfit wordplay, Caretaker imagery and measurements, and the full lineation of Playing the Magician and Woman interrupted. Compressed or unclear expressions including half lord, soily-dusk, Dicy guffaws, and barks of river are explicitly recorded for independent linguistic review. The political and religious proposals in Mother Bharati remain the source speaker’s claims, without added endorsement or historical assertions. All originals, credits, artwork and reader design preserved. No publication or push. Continue Issue 4 with batch 150.

[Issue 5 verification](../records/translation-issue-05-verification.json).

## Issue 4 continued run

Batches 150–158 integrated 84 draft versions for 42 actionable entries. Issue 4 remains incomplete: Mahanirvana (130) by Trishna Basak explicitly credits Bappaditya Roy Biswas as English translator. Preserved HTML confirms this, and no matching underlying original or source-language identification was found in the local edition catalogue. Both requested targets held; published text and credit preserved. No original reconstructed.

Original hashes, exact line/stanza coverage, preview/public catalogue parity, edition integrity and public build pass. All 43 existing source texts remain unchanged in rendered output. Historical checkpoint: 1386 drafts, 216 remaining target versions, including 24 across twelve source-held records.

Grouped same-author works (Two poems; An Incomprehensible Process/First Rain in Vienna), section headings, refrains and college/address blocks remain complete. Source145 and source147 are separate versions of Kash: exact author/line comparison allowed reuse of this run’s translations, omitting only the one refrain absent from source145 and preserving its single-block layout. Thus 82 versions were newly translated and two reused after line-by-line source verification. Uncertain expressions, botanical claim in Amazing Evolution, curdling and other nonstandard language in Miraculous Tone, and ambiguous pronouns are recorded for independent linguistic review. Same-run self-review corrected two botanical transliterations. Original texts, credits, artwork and reader design unchanged; no publication or push. Continue Issue 3 with batch159.

[Issue 4 verification](../records/translation-issue-04-verification.json) · [Source holds](../production/translations/source-holds.json).

## Issue 3 continued run

Batches 159–167 integrated 88 directly translated draft versions for 44 actionable entries. Issue 3 remains incomplete: Let poems be simple (78) by Makhan Kalita explicitly credits Dr. Binod Kumar Gogoi as English translator. Preserved HTML confirms this; no matching underlying original or source-language identification was found in the local edition catalogue. Both requested targets held; published text and credit preserved. No original reconstructed.

Original hashes, exact line/stanza coverage, preview/public catalogue parity, edition integrity and public build pass. All 45 source texts remain unchanged in rendered output. Historical checkpoint: 1474 drafts, 128 remaining target versions, including 26 across thirteen source-held records.

Regional fishing implements, dense Odia compounds in 104, opaque images, botanical references and provisional grammatical gender are recorded for independent linguistic review. Grouped pieces in 70 and all 86 lines of Passing (83) remain complete. Sea My solace (80) has a stray terminal c block, preserved verbatim in both drafts and flagged for explicit reconciliation. No missing text was invented or source text silently repaired. Same-assistant review only; no publication or push. Continue Issue 2 with batch168.

[Issue 3 verification](../records/translation-issue-03-verification.json) · [Source holds](../production/translations/source-holds.json).

## Issue 2 continued run

Batches 168–173 integrated 60 directly translated draft versions for 30 actionable entries. Issue 2 remains incomplete: Two Poems (47) by Nilim Kumar explicitly credits Nirendra Nath Thakuria as translator. Preserved HTML confirms this; the local catalogue has other works by the author but neither underlying original for Let us go to eat out today or The Curve, nor explicit source-language identification. Both requested target versions held; both published pieces and credit preserved. No original reconstructed.

Original hashes, exact line/stanza coverage, preview/public catalogue parity, edition integrity and public build pass. All 31 source texts remain unchanged in rendered output. Historical checkpoint: 1534 drafts, 68 remaining target versions, including 28 across fourteen source-held records.

The missing author for30 remains unassigned. Opaque images in27, provisional Hindi narrator/kinship choices, maizes read as mazes in41, Chilila interpreted as Chilika in52, and ictus in56 require independent linguistic review. Meru and other mythological details in43 are preserved as source statements, not silently harmonized with other versions. Jhoti, ritual offerings, source addresses, signatures, full war/grief imagery and social criticism retained. Same-assistant review only; no publication or push. Continue Issue 1 with batch174.

[Issue 2 verification](../records/translation-issue-02-verification.json) · [Source holds](../production/translations/source-holds.json).

## Issue 1 continued run

Batches174–177 integrated38 direct draft translations for all19 records. All source hashes, line/stanza vectors and preview/public render parity pass, as do edition integrity and public build. 1572 drafts overall;30 targets remain,28 already source-held.

Poem9 is captured as one paragraph: full contents preserved without inventing verse line breaks; intended lineation requires reconciliation. Related same-author Odia poem8 differs in details and ending and remains a separate original record; neither was replaced with a reconstruction. Dense compounds in18, halant image17, koili kernel/cuckoo pun7, alinda and sadhaba bohu26, and provisional Hindi gender choices require independent language review. All original signatures/addresses and grouped poems retained. Same-assistant review only; no publication. Next unassigned645 using batch178.

[Issue1 verification](../records/translation-issue-01-verification.json).

## All actionable translations drafted; loop paused

Batch178 added Odia and Hindi drafts for unassigned Yesterdays(645), preserving its19+1line source structure and its unassigned edition metadata. Overall:1574 drafts across787 records;28 requested targets across14 records remain source-held. All801 source records render unchanged in preview and public output; all1574 draft versions match the catalogue; source hashes and global line/stanza vectors pass without exceptions. Original prototype810 records draft status in its existing review text rather than a variant status field; preserved unchanged. Edition integrity and public build pass. Independent linguistic review remains pending.

Automation update confirmed PAUSED after the actionable queue reached zero. This is partial overall completion; no held work is called complete. No publication, deployment or push. [Exact source checklist](translation-source-holds.md) · [Final verification](../records/translation-actionable-completion-verification.json). Resume after source reconciliation, rebuild queues, use next unused batch179.

