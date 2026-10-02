---
type: "Interactive review"
title: "One poem: translations, recitation and pencil underlining"
---

# One poem, three ways to linger

[Open the prototype](http://127.0.0.1:8771/poem-experience.html). Source: **क्षणिका**, Sabita Singh Meera, edition 47. This is a separate local study; the 801 public poem readers are unchanged.

## Try it

1. Switch between **हिन्दी · Original**, **ଓଡ଼ିଆ · Translation**, and **English · Translation**. Both translations are AI-assisted drafts; fluent editorial review is outstanding. The source Hindi text, stanza break, end mark and place line are preserved.
2. Press **Listen** for Hindi or English. The real recordings support pause, seeking, volume and replay through the native audio player. Switching language stops the previous reading. There is no autoplay, background music, or claim that the recording is the poet herself. Odia audio is explicitly unavailable in this prototype.
3. Turn on **Underline**, then tap a line or focus it and press Space/Enter. Tap again to erase. Each language stores its own marks locally; refreshing preserves them. Clear marks affects only the selected language. If device storage is unavailable, marks remain for the current visit and the status says so.
4. Open **Your reading notes** to review translations, voice and decoration separately. Notes save locally; download the JSON review for a durable decision record. Browser review choices do not change other pages or authorize publication.

## Voice direction and limits

The journal-supplied author profile describes Sabita Singh Meera as a poetess. Feminine stock voices were selected for this review, not inferred from her photograph or name: Lekha for Hindi and Tara for Indian English. These are local macOS speech-synthesis previews with measured rates and line pauses. They demonstrate playback and pacing, not a finished culturally authenticated recitation. Pronunciation, emotion, language-specific poetic delivery and the poet's preferred voice remain editorial decisions. No cloning or imitation of the poet's own voice is involved.

Hindi recording: about 16.8 seconds. English recording: about 21.7 seconds. The voice reads the eight verse lines; the printed end mark and city remain on the page. An appropriate Odia voice/provider must be chosen before a three-language audio rollout.

## Files and preservation

- [Prototype content and translation drafts](../artifacts/review/poem-experience/content.json)
- [Review HTML](../artifacts/review/poem-experience/index.html)
- [Interaction source](../artifacts/review/poem-experience/prototype.js)
- [Prototype styling](../artifacts/review/poem-experience/prototype.css)
- [Voice scripts and audio masters](../artifacts/review/poem-experience/audio/)
- [Verification record](../records/poem-experience-verification.json)

Rebuild with `python3 tools/build_poem_experience.py` after changing the canonical poem reader or prototype inputs. The build checks the original Hindi against the source and its hash. The preview page and asset folder are relative aliases into this KB. Public build selection excludes the prototype and its draft/audio assets. Original site files, artwork, captions and old studies remain intact. The existing site theme, shared header, borderless artwork, right-aligned caption and navigation are inherited.

Same-assistant implementation and browser review; no independent linguistic or audio-performance review is claimed. Apply to additional poems only after Ahimanikya reviews this prototype.
