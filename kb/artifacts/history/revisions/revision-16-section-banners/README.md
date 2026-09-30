# A quiet banner for every part of the journal

The inner-page opening uses 60% of its width for text on the left and 40% for art on the right. Spacing comes from padding inside the text column, so the artwork column really occupies 40% of the banner. Below 600 px, headings and artwork stack; the artwork stays right-aligned. Magazine covers retain their portrait proportions within the right-hand area.

Each section has its own watercolor illustration. Related pages share their section's illustration: the archive and its year pages, the review listing and review detail, and the poets directory and current contributors. Writer profiles have a separate personal writing-corner illustration. Individual poems retain their own illustrations; each issue retains its own cover. Design-review utility pages keep the original water-and-reeds illustration. The footer keeps the shared site watercolor.

## Section artwork

| Page family | Illustration |
|---|---|
| Poems | A notebook at a low indigo reading table |
| Poets and current contributors | Empty chairs gathered beneath a tree |
| Writer profiles | A chair, shoulder bag and notebook |
| Archive and year pages | Clothbound journals and a cotton bookmark |
| About | An earthen home and welcoming threshold |
| Send a poem | A pen and a waiting notebook |
| Contact | An envelope beside a rain-lit window |
| Reader letters | Letters and a cup at a low table |
| Book reviews | An open book, reading glasses and bookmark |
| Highlights and announcements | A courtyard prepared for a gathering |
| Editorial team and editor profiles | A quietly ordered editorial desk |
| Search | An open shutter and a stream to follow |
| Upcoming issue | An unfurling leaf and a closed book |
| Missing page | A path dissolving into mist |

All 14 new illustrations use the built-in image_gen tool with transparent backgrounds. PROMPTS.json records the complete prompts. Originals and optimized WebP copies are in site/assets/section-art/. The route-to-art map is site/section-art.json. Decorative banner images use empty alternative text; page headings communicate the purpose. They are imagined artwork and are not documentary records of named places or real writers' homes.

## Homepage caption

The title is now **LIFE AS IT IS**. The credit reads **Generated artwork**, without the Odisha-inspired prefix, in a subdued warm grey (#6F6D63). The image and its relaxed, lived-in mood remain. The credit colour is checked against the warm paper background; small lettering must still meet normal-text contrast requirements.

The original poem text, language filters, sharing links and masthead typography remain unchanged.


## Verification

All 40 HTML documents passed automated axe A/AA checks at 1280 and 320 CSS px: zero rule violations, zero broken images, zero horizontal page overflow. Every measured inner-page artwork column was 40% of its desktop banner. Synthetic 200% text enlargement and expanded text spacing also completed without page overflow or clipped banner content. The reported clipping diagnostics are intentional screen-reader-only text, decorative guide artwork and horizontally scrollable reference tables. Automated checks do not certify accessibility; existing cover text overlays and assistive-technology behavior retain their manual review requirements.

Visual review covered the full 14-illustration family, the reading-room banner, an editorial profile, a narrow-phone contributor banner, and the updated one-page editor PDF. Original poem data was compared with the prior source and is unchanged.
