# Author page and data contract

The root AGENTS.md and approved design system take precedence. Resolve these paths from the Kabita Live workspace; in the portable handoff, `projects/site` is a local alias to `site`.

- `projects/site/author-pages.py`: shared author renderer, loaded by `standalone-pages.py` after publication contributions are joined.
- `data/writer-profiles.json`: captured biographies and names; do not overwrite them with researched prose.
- `content/editions/*/poem-*.json`: complete texts and authoritative writer/edition IDs, including unassigned source entries.
- `data/writer-enrichment.json`: object keyed by writer ID. Optional `intro`, `sections` (heading, paragraphs, language), `books` (title, detail, url) and `sources` (label, url). Claim notes and uncertainty belong in `kb/research/writers/enrichment/ID.json`.
- `data/writer-portraits.json`: object keyed by writer ID with `src`, `kind` (`journal_photo` or `generated_portrait`) and `credit`. Reference only existing local assets.
- Source portraits and receipts stay in `kb/research/writers/portrait-sources.json` and `kb/artifacts/artwork/portrait-sources/writers`.

Separate Roman and original-script names only when the captured name provides both; preserve source spelling and use the appropriate lang attribute. The masthead stays English. Never infer a person's language from their name: reading-language metadata comes from their poems.

Use the approved Clear story opening (name, native name, own-poem quotation and 60/40 portrait), supplied biography, optional visible verified book shelf beneath the portrait in the right column, beside the biography on desktop and complete contributions in the approved Option A quiet table with edition links. If a book bibliography is absent, omit the book shelf. Do not duplicate poems in a sidebar. No opening jump links, source/portrait footnote, All writers or Explore the editions links at the bottom. If biography is absent, use only publication facts derived from actual local contributions. Do not manufacture personal history, awards or literary themes to fill the page.

The contribution section uses `#contributions`, `.contribution-table` and one `[data-contribution]` table row per poem, newest editions first. Columns are Poem, Edition and Published. Below 700px dates move beneath titles; the desktop date column is hidden. Keep native-script titles, all poem/edition links, and a labelled table caption with scoped column headers. No year groups or search controls in this approved simple layout. Profiles with no poems keep the existing empty state. Keep one h1 and section headings h2; poem titles are table links. Long names and native-script glyphs must wrap without clipping.

Author references remain in `about.html#credits-writers` and `#credits-writer-ID`, reached through the shared Our Story footer link. Author pages no longer repeat a credit footnote. Keep selected-book external links visible, with the existing subtle external mark and accessible new-tab indication. Research provenance may include the source site in the KB; reader pages may not link back to it.

Stable aliases: writers 82, 337 and 257 use `poet-dokana.html`, `poet-kshanika.html`, `poet-drink.html`; editors 1 and 43 use `editor-pradeep.html`, `editor-paresh.html`.

Author quotations use `data/writer-quotes.json`, keyed by writer ID: poem_id, text_start, text_end and source-exact text. Preserve line breaks and original language. Select a meaningful coherent excerpt; avoid biographical metadata, translator credits, quoted third-party sayings or non-poetic commentary in captured text. Never correct source spelling silently. Link the poem title to its local reader. Omit the quotation for profiles without poems. Keep selection context and concerns in `kb/records/writer-quote-selections.json`; run the author checks after any selection edit.

The contribution count is integrated into its heading: “A voice in one poem.”, or “A voice across N poems.” for two or more. No separate count label. With zero works retain the generic heading and empty-state explanation. Quote treatment C, Earth & voice, is approved and applied; A and B remain comparison studies.
