---
name: kabita-writer-profiles
description: Build and maintain Kabita Live author pages in the approved editor-page style, with sourced biographies, local portraits and edition-linked contributions. Use for this journal's author pages and identity-checked research, not unrelated people research.
---

# Kabita Live writer profiles

Work from the Kabita Live project root. Read its AGENTS.md and `kb/reference/site-architecture.md`; preserve approved typography, masthead, paper, art and footer. Maintained reader source is `projects/site`; research and original images belong in `kb`.

## Build author pages

Read [the page and data contract](references/author-pages.md) before layout or data changes. Reuse the approved editor components: 60/40 identity and portrait opening, reading-width biography, visible selected-book links when available, and complete contributions below. The approved Clear story layout removes repeated recent-poem sidebars, introductory labels, jump links and bottom navigation. The user's request to adapt the editor design authorizes this reuse; it does not require another design approval. New unrelated component directions remain candidates.

Apply the shared renderer to all author records. Use local source photographs where no generated portrait exists, and an honest initials treatment where no photograph is available. Do not block usable pages on biography enrichment. Keep captured biographies separate from authored enrichment; render only source-backed enrichment. A complete layout does not mean every biography has been independently researched.

Publication poem JSON is now authoritative for contribution membership and full text. Join on stable writer ID. The earlier writer capture list is evidence and may omit later-linked poems. Preserve all local aliases, especially the three featured writers and two editors. Editors keep their existing narrative and portrait.

## Capture and identify

Use the browser skill for the live magazine. Open the homepage, follow Contributors, and capture visible writer cards (name, profile URL, image URL). Direct navigation can redirect to the homepage. Follow each observed profile link from the directory, wait for its author heading, and verify the resulting writer ID before saving. Return through the Contributors navigation. Retry a failed navigation once after inspecting state; checkpoint every successful record. Never use hidden application state or browser network requests.

The directory's hidden biography popups repeat Manju Chouhan's biography under unrelated writers. Ignore them. Individual profile content is in `.achieve__content__item`; contribution links point to `poemview.php`. Inspect current DOM before relying on these observed selectors. Capture names, biography text, portrait source and contribution labels/URLs in `kb/research/writers/captured-profiles.json`. Keep source IDs stable; do not merge people by name alone.

Run `python3 tools/writer_profiles.py` to normalize the captured records, validate contribution relationships, and regenerate the research queue. Missing biographies, ambiguous names, portrait problems and contribution conflicts remain explicit gaps. An empty capture is not evidence of no published work.

The normalizer creates an initial research queue. Once independent research or portrait generation begins, preserve that progress in separate per-writer research records; do not treat a regenerated capture queue as the research authority. Source portraits are indexed in `kb/research/writers/portrait-sources.json`. Prefer the browser's documented pageAssets inventory/bundle capability to preserve observed images. Its inventory can be capped; a missing inventory item does not prove the portrait is unavailable. Check image MIME types: this site sometimes serves WebP bytes under JPG URLs.

## Research and narrative

Use author, publisher, university, literary festival and award-organizer sources. Match the journal identity using language, work, place or professional context before attaching a source. Record the URL, access date, supported claims and unresolved contradictions in the writer's research record. Name matches alone are insufficient. Prefer a short factual narrative over an inflated biography; omit unverified accolades, current roles supported only by old CVs, personal contacts and inferred beliefs or literary themes.

Maintain the supplied journal biography separately from newly written narrative. A source capture is not independent verification. Write compact paragraphs about the writer's literary practice, selected books and relevant background; derive literary themes from actual writing or attribute them to a cited critic. Keep original-language names. Do not turn a native-script biography into an unreviewed translation.

## Portraits

Use the companion `kabita-author-portraits` skill at `kb/artifacts/skills/kabita-author-portraits/SKILL.md` for identity-preserving image edits. It defines the source-to-master-to-reader workflow and invokes the built-in image-generation skill. Never treat a CSS frame as a generated artistic portrait.

Preserve the original, source page/image URL, credit, reuse status, exact prompt and generated master. Public availability is not a licence; unresolved publication rights remain recorded. Use existing initials when no identifiable photo is available. Inspect the generated result against the original before adding a web derivative. Keep background art separate from author identity.

## Integrate and verify

Each directory writer resolves to one local profile; editors retain their existing profiles. Profile contributions link to local poems and editions. Count known contributions honestly; missing complete poem text remains a content-import gap. Keep research/portrait progress in the KB, not in the reader interface. Consolidate source and image credits in Our Story, reached through the shared footer. The user removed author-page source/portrait footnotes; retain editor-specific source links.

Run `python3 tools/check_author_pages.py` and `python3 tools/check_editions.py` after rebuilding. Include a missing-portrait profile, a missing-biography profile, the longest biography and the three scripts in browser review. Report layout coverage, original portraits, generated portraits and enriched narratives separately.

Build the reader site, check every profile/contribution route, and inspect a long biography and all three scripts at desktop and 360px. Verify no old-site runtime links, raw contact details or research files enter the public export. Run KB/register checks and `tools/sync_handoff.py`. Report captured, researched, portrait-ready and unresolved counts separately. Local profile work does not authorize website deployment.
