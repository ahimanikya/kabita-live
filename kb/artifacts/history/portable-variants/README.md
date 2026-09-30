## Blueprint persona operation

Disha Dash, Anvesha Acharya, Samanta Chandrasekhar and Drishti Senapati are configured for on-demand role passes under Ahimanikya’s supervision. Read [the team workflow](kb/team/operating-model.md). Roles add no separate background runtime. Run `python3 tools/check_personas.py --self-test` to check configuration.

# Blueprint project handoff

This portable copy includes the KBL knowledge base, source register, configuration and validators. [Start with the KB](kb/index.md). Site implementation is `site/`; `projects/site` points to it. Primary design files are at this handoff root, so the configuration adapts that path to `.`. New icon candidates: `site/icon-atelier.html`; literary research: `site/literary-study.html`. Prior large ZIP packages remain revision-39 snapshots.

# କବିତା ଲାଇଭ. · Kabita Live

Standalone design project · 29 September 2026 · Revision 06

**ମାଟିର ମହକ। ମନର ସ୍ୱର।**

This folder is ready to move into a dedicated Kabita Live project. It contains the editable design source, complete preview, branding assets, source metadata and handoff. It has no dependency on the surrounding poetry/video project. No repository, app project or deployment has been created.

## Start here

- `site/index.html`: journal homepage.
- `site/all-pages.html`: all 36 linked designs.
- `site/site-coverage.html`: existing-site route coverage and migration boundary.
- `brand-guide/BRANDING-GUIDE.html`: visual identity and usage guide.
- `brand-guide/editors-cheat-sheet.pdf`: one-page editorial reference.
- `PROJECT-HANDOFF.md`: source evidence, known issues and production sequence.
- `DESIGN-PROPOSAL.md`: editable complete proposal.

To preview locally, use Python 3:

```sh
python3 -m http.server 8772 --bind 127.0.0.1 --directory site
```

Then open `http://127.0.0.1:8772/`. Most pages can also be opened as files, but clipboard/device-sharing features need a supported secure context. Fonts currently load from Google Fonts; use licensed self-hosted fonts for production.

## Editing and rebuilding

`site/build.py` holds the shared layout and core pages. `site/expanded-pages.py` provides the complete public indexes and additional journeys. They use the standard Python library only.

```sh
python3 build-all.py
```

That rebuilds the journal, visual guide, proposal and copied companion documents. Edit `site/assets/style.css` and `site/assets/app.js` for styling and interaction. The generated HTML is for review; retain changes in the builders/templates so they survive a rebuild.

The existing one-page PDF is included. Its optional editable CoreText source is `editor-tools/editors-cheat-sheet.swift`; rebuilding it requires macOS Swift/CoreText and the indicated Odia font. The normal site build does not regenerate the PDF.

## Data and assets

- `revision-06/`: 47 issue records, 427 contributor name/profile records, 16 current poem title/credit records, eight review records, responsive-check evidence and audit handoff.
- `revision-05/`: three original generated cover studies, exact prompts, artwork provenance and three verified writer contribution histories.
- `revision-04/`: selected identity concept and editable symbol/lockup.
- `revision-02/`: watercolor source used by the guide.
- `brand-guide/assets/`: current logo variants, symbol variants and colour/type tokens.
- `evidence/`: earlier public-site screenshots and evidence notes.

Retain the exact Odia name and final dot. The masthead uses Kabita Live in English with a separate Odia signature; all three reading languages remain equally accessible. The English literary epigraph stays separate from the Odia signature. Historical covers and full poem text have not been replaced by these design studies.

## Status

This is a design prototype with complete public indexes and representative readers/profiles, not a production CMS or full content migration. Forms show local confirmation only. Older records mostly link to their original published pages. No login, private data, external posting, paid production service or live deployment is part of this package.

Layout QA covered 39 documents at 320px and 1280px: 78 layouts, zero recorded horizontal overflow or broken images. Name search, language filters, archive years and response previews were checked. See `site/VERIFICATION.md`; real-device and accessibility review remain production work.

Revision 07: Odisha-informed cover commissioning, shared leaf-and-water dividers and a page-by-page poetic atmosphere guide. Existing cover artwork remains intact. See `revision-07/EDITOR-ART-DIRECTION.md`.

Revision 08: compact navigation, one homepage reading invitation, fewer repeated brand blocks, quiet still imagery and secondary tools in footer disclosures.

Archived banner exploration (Revision 09): Kabita Live leads in ink serif lettering, with smaller terracotta Odia beneath. This trial is applied to the website header/footer; branding-guide and cover lockups retain the previous direction pending review. See `revision-09-masthead-trial/README.md`.

Selected direction, introduced in Revision 10: English-only Kabita Live masthead and a coordinated symbol/name on all three magazine covers. Odia signature remains separate. Front/contents/back-cover study: `site/magazine-branding.html`. Now 37 linked designs; the guide and logo assets now match this direction in Revision 13.


Accessibility update: main navigation is 17 px with 48 px targets. Read [the accessibility review](revision-11-accessibility/ACCESSIBILITY-REVIEW.md) for the 40-page desktop/mobile results, remaining manual checks and editor sizing rules.


## Current UI and UX review — Revision 13
All 40 HTML pages were reviewed. Selective poetic headings, local filter counts/reset, archive reading paths and shared branding are updated. Navigation remains 17 px and language selection stays beside poem lists. See `revision-13-ui-ux/UI-UX-AUDIT.md` for individual page decisions and verification. Earlier revision notes document history.


## Revision 14 — illustrated openings
The signature uses a middle dot on one line and no punctuation on two lines. Site artwork sits to the right of inner-page openings and in the footer; issue covers remain distinct. Three sample poems now have individual generated illustrations beside their titles. See revision-14-artful-openings/ART-DIRECTION.md for usage and prompts. Poem text remains unchanged.


## Revision 15 — Homepage artwork and arrival

The homepage now pairs its Odia signature with a large realistic Odisha-inspired scene: a rain-washed courtyard, indigo doorway, brass vessel and luminous fields. The caption is “Life, after rain.” This newly generated artwork replaces the faint decorative watercolor in the homepage opening. Text remains on warm paper beside the image; on mobile, the image follows the signature. The existing epigraph and Read this issue action remain. Inner-page headers retain their established artwork. Original and optimized files are in site/assets/home/; the prompt and verification are in revision-15-homepage/.


## Revision 16 — Section banners

Inner-page banners now use 60% text left and 40% artwork right, stacking on narrow phones. Fourteen new soft illustrations give the main sections their own imagery. Related pages share section art; poems and issues keep individual artwork. The homepage caption is LIFE AS IT IS, with a subtle Generated artwork credit. The editor guide and cheat sheet include the new layout rule. See revision-16-section-banners for prompts, provenance, page mapping and verification.


## Revision 17 — Shared header and quieter footer

All journal pages now use the homepage masthead without an extra inner-page tagline row. The footer has the Odia signature, three links and one author-credit line. Secondary journal links live on Our story; design-review links live on All page designs. See revision-17-header-footer/ for verification.


Revision 18: all 47 editions now have distinct generated cover artwork, responsive web versions and editable SVG covers. The attached Colours of home palette guides the interface and updated branding materials. A small shared leaf-and-water header separator appears on all 37 journal designs. Cover prompts and provenance are in revision-18-covers/manifest.json. Archive filtering and year galleries retain all verified issue dates and source links.

Revision 19: all 47 covers have distinct poetic stories and cultural notes. Ten new heritage, craft, ecology and literary artworks replace repeated motifs in the active catalogue. Editor cover-story card: site/editor-cover-card.html. Sources, prompts and provenance: revision-19-cover-stories.

Revision 20: warm ivory paper texture across journal pages; off in night reading and print. Pipili Chandua is preserved in site/assets/art-library for future use. Issue 34 returns to Rain on the tiles. Current cover stories and generation provenance: revision-20-paper.

Revision 22: dedicated Editors landing page and detailed profiles, source-linked portraits and selected books. Design attribution appears only on Our Story. Research and portrait rights notes: revision-22-editors.
