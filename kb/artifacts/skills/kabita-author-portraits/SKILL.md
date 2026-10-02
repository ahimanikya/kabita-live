---
name: kabita-author-portraits
description: Create faithful cotton-paper artistic portraits for Kabita Live writers from identified source photographs, preserve provenance, and connect reviewed images to author pages. Use for this journal's portrait work, not generic cover art or biographies.
---

# Kabita Live author portraits

Work within the Kabita Live workspace and its approved editor portrait treatment. Read the available imagegen skill and use the built-in image-generation tool, one edit per writer. A batch request does not authorize a different API or paid service.

Identify the writer by stable ID and the saved source mapping in `kb/research/writers/portrait-sources.json`. Inspect the source photograph before editing. Do not substitute a same-name internet portrait or invent a face for a missing photograph. Source photographs remain usable on the page while their artistic treatment is pending.

Preserve facial geometry, age, complexion, expression, hair, clothing, bindi, glasses and jewellery where present. Ask for a realistic face with delicate watercolor/graphite edges on warm ivory cotton paper, restrained sea and hearth washes, and a small laterite accent at the shoulders. No skin lightening, costume change, scenery, icons or text. The journal's Odisha roots do not imply that every author is Odia.

Keep the original source unchanged. Save each generated master under `kb/artifacts/artwork/writer-portraits/ID-earth-voice-vN.png`; copy the selected image or web derivative into `projects/site/assets/writers`. Record exact prompt, source path/hash, tool, master path/hash, source credit and likeness-review outcome under `kb/research/writers/portrait-edits.json`. Do not mark all portraits ready after completing only a sample batch.

Compare each result visually against its source before use. Correct material identity drift with a targeted edit; if fidelity remains uncertain, retain the original photograph and record the unresolved issue. Public availability does not establish publication rights; preserve the source's existing rights status. Local image work is not authority to publish the website.

Set `data/writer-portraits.json` only for reviewed, saved assets, with `src`, `kind: generated_portrait` and `credit`. Keep original/generated credit in Our Story and descriptive portrait alt text on the profile. Build and run `tools/check_author_pages.py`; check desktop and 360px crops. Preserve the KB master and synchronize the handoff.
