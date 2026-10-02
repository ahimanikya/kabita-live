---
type: "Implementation and skill record"
title: "Author pages in the editor profile language"
---

# Author pages in the editor profile language

User direction: “Now, I want to fix the author's page as we did for 2 editors - let's make the author's page something similar. Build skills and use them to build”. This authorizes adaptation of the approved editor components and reusable local skills; it does not authorize website publication.

## Applied result

All 427 non-editor author pages now reuse the editor profile language: 60/40 text and portrait opening, native-script name where supplied, the Odia signature, biography at reading width, a quiet sidebar, and complete contributions grouped by year with edition links. The two approved editor pages retain their portraits, narratives and books. Total writer directory coverage is 429.

Portrait coverage is 421 unchanged journal photographs, three new artistic portraits, and three initials fallbacks (writers 233, 258 and 416). The two editor portraits are additional existing assets. Source photographs for all 426 originally captured profiles with images remain preserved in the KB. No generic scenery is presented as an author portrait.

Three featured narratives were expanded: Narmada Nilotpala (82), Sabita Singh Meera (337) and Majrooh Rashid (257). Other supplied biographies remain verbatim. Missing biographies use only contribution facts; no awards, books, birthplace or career were invented. Where book references are verified, the sidebar lists selected books. Elsewhere it offers recent poems, avoiding empty bibliography scaffolding.

Names in Roman and original scripts are separated where the source provides both. Noto Serif Oriya, Tiro Devanagari Hindi, Source Serif 4 and the approved display type remain unchanged. Credits and generated-portrait disclosure are consolidated in Our Story; each profile has one small source/portrait footnote. Reference deep links open the appropriate collapsed colophon section.

## Reusable skills

- [Author pages and source research](../artifacts/skills/kabita-writer-profiles/SKILL.md), with a [page/data contract](../artifacts/skills/kabita-writer-profiles/references/author-pages.md).
- [Identity-preserving artistic portraits](../artifacts/skills/kabita-author-portraits/SKILL.md).

Both skills passed the skill-creator validator and are installed as links from the local Codex skills directory to their canonical KB folders. The handoff includes the canonical skills; machine-local discovery links are not portable installation claims. A temporary PyYAML dependency was used for validation, without adding website dependencies.

The author renderer is `projects/site/author-pages.py`; the public inputs are `data/writer-enrichment.json` and `data/writer-portraits.json`. The renderer is called by the existing build. Contributions are joined from the complete edition content rather than the incomplete earlier profile capture lists. The maintained validator is `tools/check_author_pages.py`.

## Sources and portrait stewardship

- [Narmada research note](writers/enrichment/82.json)
- [Meera research note](writers/enrichment/337.json)
- [Majrooh research note](writers/enrichment/257.json)
- [Original portrait index](writers/portrait-sources.json)
- [Exact portrait prompt](writers/portrait-prompt.txt)
- [Per-writer edit receipts, hashes and likeness checks](writers/portrait-edits.json)
- [Three generated portrait masters](../artifacts/artwork/writer-portraits/)

Bibliographic information for Narmada comes from a retailer's publication listing. Meera's identity is corroborated by overlapping poem titles and pen name in Jay Vijay's author archive; she is not conflated with the similarly named feminist scholar. Majrooh's historical university CV supports his teaching and selected bibliography, without treating old employment as a current role. Reader references are in the colophon. Expanded text is a local editorial draft, not author approval.

The built-in image-generation tool created the three portraits as separate identity-preserving edits. Reference and result were visually compared. Originals, generated masters, exact prompt and source rights status remain separate. Artistic versions for the other writers and independent research across the entire directory remain in KBL-WORK-012; this pass does not claim that work complete.

## Verification and remaining review

[Automated profile checks](../records/author-page-verification.json) cover 429 unique profile headings, actual publication contribution counts, portrait presence, original-photo byte equality, supplied biography retention, section/credit targets and generated-master hashes. [Edition checks](../records/edition-content-verification.json) continue to pass all 801 poem texts and 800 reciprocal writer links.

[Browser checks](../records/author-page-browser-verification.json) cover desktop presentation, 360px layout in six representative profiles, the longest biography, both native scripts, missing photograph/biography cases, Unicode contribution filtering, empty results and credit deep links. The production-format static build passes public link/asset checks and excludes the KB. Both skills passed their frontmatter/scaffold validator.

This is same-assistant Samanta/Anvesha implementation and Drishti self-review, not independent review or accessibility certification. Full biography proofreading, portrait likeness approval, remaining research/artistic portraits and the existing design-review queue are still open. No deployment, Git push or domain change occurred. Primary and portable copies are synchronized at handover.

## Research expansion — 1 October 2026

The first new research group adds twelve sourced narrative drafts: Manorama Choudhury, Debarati Sen, Paramita Mukherjee Mullick, Tejaswini Patil, Prabhanjan K. Mishra, Rashmi Mohapatra, Varsha Saran, Sujit Kumar Satapathy, Alok Kumar Ray, Anamika Nath, Prahallad Satapathy and Antara Mukherjee. Fifteen of427 non-editor profiles now have enriched drafts;412 remain. Three of those have partial identity investigations, not publishable enrichment.

The [enrichment register](writers/enrichment-progress.json) records every writer separately from the historical capture queue. Claim sources, identity matches and limitations are preserved in per-writer dossiers. No newly generated portraits are claimed. References remain in the central colophon, which now uses the actual portrait credit and research date for each profile.

The [research and mockup record](../records/writer-enrichment-review.json) links the verification evidence. [Review A and B](http://127.0.0.1:8771/poet-enrichment-review.html) with real biographies, short and long profiles, and missing-content cases. These layout proposals are not approved or applied. Option A retains the short biography; Option B expands additional biography on phones. Both preserve desktop book placement.
