---
type: "Editorial audition plan"
title: "Natural poetic recitation: Hindi, Odia and English"
---

# Audition a performance, not just a voice

**Deferred by user — 30 September 2026.** Audio has been removed from the active reader prototype; translations remain. Subsequent Sarvam/Suno trials did not meet the desired naturalness, pacing and echo expectations. This document preserves the earlier plan, not current authorization or an active queue. Production records remain in `kb/production/`.

Ahimanikya rejected the first computer-like readings and requested natural, local poetic style. He selected **prepare an audition plan first**; no account setup, paid generation, voice cloning or service integration is authorized by this plan. The original files are preserved for comparison, removed from the active reader prototype, and marked rejected.

## One controlled audition

Use the same eight verse lines of **क्षणिका**, by Sabita Singh Meera, and the prototype's existing Odia/English translations. The language-translation feature is approved; this is not a substitute for a fluent editor checking performance and pronunciation. [Texts](../artifacts/review/poem-experience/content.json).

The scene moves from a deserted platform, rain and the train's tremor to remembered separation and unresolved hope. Let that emotional progression shape the delivery. Voice gender may follow the poet's preference/recorded identity, but accent, phrasing and interpretation determine suitability. We do not imitate or clone her voice.

## Proposed directions for this poem

These are audition briefs, not claims that each language has only one recitation style.

| Version | Direction | Listen closely for |
|---|---|---|
| Hindi | Intimate literary reading: observe the scene, allow a turn at “आज फिर”, then address the absent person gently. | Clear vowels and consonants, a natural connection across “धीमे-धीमे / गुजरती ट्रेन”, no automatic pause after every printed line, a restrained ending rather than a dramatic announcement. |
| Odia | Native Odia reading with the translation's own phrase lengths. Let the railway scene unfold, then soften into waiting. | Native vowel length and conjunct pronunciation; no imported Hindi cadence, misplaced stress, or rigid imitation of the Hindi timing. A fluent Odia listener must judge this. |
| English | Quiet spoken lyric, flowing across line endings when the thought continues; let “where you left me” carry the emotional turn. | Natural English stress and connected phrasing, clear consonants, no exaggerated breathiness or broadcast-style projection. Compare Indian English with another naturally spoken literary reading only if useful. |

Common brief: preserve every word; do not sing; no music, rain effects or soundscape; no imitation of a named performer. Avoid slowing the entire poem uniformly. Pauses belong to thought, breath and emotion. The final uncertainty should remain open.

## Candidate services to audition

**First candidate: Sarvam Bulbul v3.** Its documentation lists Hindi, Odia and Indian English, speaker choices and pace control. The REST API also provides temperature and pronunciation dictionaries. These controls are useful audition inputs, not proof of poetic delivery. Bulbul has no SSML support; do not assume actor-style instructions can be sent as an unsupported API prompt. Keep the text in its native script. [Model documentation](https://docs.sarvam.ai/api/getting-started/models/bulbul), [REST controls](https://docs.sarvam.ai/api-reference/text-to-speech/convert).

**Comparison candidate: ElevenLabs.** Current model documentation lists Odia, Hindi and English under Eleven v4; its v3 list includes Hindi/English but does not list Odia. Model/version selection matters. Audition the exact chosen voice in each language; advertised language coverage is not evidence of native recitation quality. [Official model and language reference](https://elevenlabs.io/docs/overview/models).

**Quality reference: a willing native-language poetry reader.** A short human reading of the same text gives us a useful listening benchmark. Obtain a supplied/licensed recording before any reuse; this plan does not contact anyone or authorize recording someone else's performance.

## Small batch, clear comparisons

1. Once account access and a bounded generation budget are authorized, shortlist two voices per language by listening to their samples. Do not choose from names alone.
2. Make two full-poem candidates per language: **A, intimate and conversational**; **B, gently more performative**. Six primary takes, about 20–40 seconds each, are enough for a first review. The timing is a target, not a reason to stretch words mechanically.
3. Use the same text, equivalent playback loudness and no music. Display the voice/model, language, date, settings and transcript with each take. Keep all rejected takes and reasons.
4. Review pronunciation/word fidelity, natural phrasing, emotional fit, native cadence and listening comfort on a 1–5 scale. Any changed/missing word, distracting artifact, or consistently wrong pronunciation rejects the take regardless of its average score.
5. Compare the winner against a human benchmark if available. Have one fluent listener for each language plus Ahimanikya approve before connecting a recording to the reader. If no synthetic take meets the bar, use a human recording or leave Listen unavailable.

[Prepared six-take audition sheet](../records/recitation-audition-plan.json). All audio slots are empty and explicitly marked planned.

## Record for each take

`poem_id`, `language`, `text_hash`, `provider`, `model`, `voice`, `direction`, `generation_settings`, `duration`, `local_audio_path`, `synthetic_disclosure`, `reviewer`, `scores`, `pronunciation_notes`, `word_fidelity`, `decision`, `reason`.

Store selected audio locally in the Git-hosted publication; do not synthesize on every reader visit. Keep secrets and generation tooling out of the website. The eventual reader should simply play the reviewed recording with its narration credit and a compact synthetic disclosure where applicable.

Status: **plan ready; no new recordings generated or providers connected**. Sources checked 30 September 2026. Provider claims have not been independently verified through an audition here.
