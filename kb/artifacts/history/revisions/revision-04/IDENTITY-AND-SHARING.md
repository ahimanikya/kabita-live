# Revision 04 — keep the name, renew the identity

**Retain Kabita Live. Use the exact Odia wordmark କବିତା ଲାଇଭ.**, including the final ASCII full stop. Keep Kabita Live as the Roman companion.

## Why retain the name?

Years of publishing give an established name familiarity and emotional value. The refresh should strengthen that recognition through typography, illustration and a more thoughtful reading experience. Jhara was an explored direction; it is no longer the recommended publication name.

## Two complementary poetic signatures

**Brand signature: ମାଟିର ମହକ। ମନର ସ୍ୱର।** (“The fragrance of earth. The voice of the heart.”)

Use this Odia line with the wordmark, in the footer and on branded social cards. The user selected it as an essential part of the identity.

**Retained literary epigraph: “Poetry is an echo, asking a shadow to dance.”**

Keep this exact existing wording as the journal’s literary epigraph on the homepage, About page and spacious issue openers. It supplies continuity and an invitation across the three languages. It is not newly written brand copy.

Brand hierarchy: **କବିତା ଲାଇଭ.** as the principal name; **Kabita Live** as the Roman companion; the Odia brand signature paired with the identity. Give the English epigraph a separate, quiet placement. The compact logo may omit the signature inside the lockup, but the shared header retains the Odia signature on a separate line. The earlier alternative “ଅକ୍ଷରେ ଅକ୍ଷରେ ଜୀବନ।” is no longer an active recommendation.

## Refresh without a rename

Keep the domain, publication name, social account names and all existing poem links. No “formerly” label or domain migration is needed. Coordinate the refreshed masthead, colours, typography and sharing artwork at launch. This is a local design proposal; nothing has been published to the live site.

## Logo: a leaf carrying a stream

`kabita-live-symbol.svg` replaces the earlier three-line secondary mark with an original vector concept. Two ink-coloured organic forms suggest a leaf or opened page. The negative space bends like a stream, and a restrained red-earth drop completes the movement. It suggests writing, water and growth without pretending to reproduce an Odia letter or a traditional sacred symbol.

The symbol is paired with real typeset **କବିତା ଲାଇଭ.**, never generated lettering. The wordmark remains readable when the artwork disappears. The small standalone symbol omits the tagline; create a simplified one-colour version for favicon testing before production. The supplied mark is a review concept; final spacing, optical adjustments and uniqueness review remain part of identity production.

## A poetic atmosphere with an Odisha connection

Use an airy watercolor edge composition: wetland reeds, a lotus bud, two birds and a small wooden boat. These connect to Odisha through a Chilika-inspired wetland setting, not through a collage of monuments. The illustration is interpretive, not a documentary depiction or claimed example of a named traditional craft.

Place the imagery at the outer edges of the homepage masthead and lightly in issue-opening or closing areas. Keep the name and signature in generous clear space. The poem column stays opaque and plain. Retain Odia, Hindi and English as equal reading choices.

“Floating” should first describe composition: detached, soft forms with abundant empty space. For motion, offer a reader-controlled **Breathe** action: one slow, small movement of the illustration, then rest. A 3–5 second cycle with 4–8px movement is enough. Keep **Still** as the default, honour reduced-motion preferences, and avoid scroll hijacking or continuous movement beside a poem. If continuous ambient motion is later requested, provide a persistent pause control and pause when the masthead is off-screen.

The preview uses the generated transparent illustration without changing its content; a compressed WebP copy is supplied for web presentation. No source photography or approved character assets from the separate poetry-film project are used.

Cultural reference: [Odisha Tourism on Chilika and its birds](https://odishatourism.gov.in/content/tourism/en/experience/event/chilika-bird-festival-2026.html). Odisha's [palm-leaf art tradition](https://www.works.odisha.gov.in/en/odisha-tourism/palm-leaf-painting) could inform a future commissioned manuscript drawing; the current image does not claim to reproduce it.

## Sharing is a primary reader action

Keep a labelled Share action beside the reading controls and repeat it after the poem. It should be easy to find without covering the text. On narrow screens, controls wrap; a floating rail is unnecessary.

### Mobile

One tap opens the device's native share sheet when supported. Provide the exact canonical poem link, full title and author. The reader chooses the app and recipient and completes the send. The website cannot guarantee which apps a device offers. If native sharing is unavailable, open the compact fallback panel immediately.

### Desktop and fallback

Show WhatsApp, Facebook, email and Copy link with visible labels. Support the publication's other existing channels where their current share mechanisms are verified. LinkedIn or X can sit under More if the editors want them; avoid five repeated icon bars. Preserve the intended sharing capability, while replacing the current `#` placeholders with working actions. Social-profile links in the footer remain separate from sharing the current poem.

Copy link should copy the canonical URL and report success only when clipboard access succeeds. On failure, show a selectable URL. Cancelling a native share is a normal dismissal, not an error. Never display “Posted” or “Sent” merely because a share window opened.

### What travels with the poem

- The complete title and exact author name, in the original script.
- Issue number and date, plus the canonical link to that poem.
- A well-typeset social preview image with the new identity and a quiet edge motif.
- A short excerpt only when the editor has approved its wording and use; do not automatically publish the whole poem in a graphic.

Production social card starting sizes: 1200×630 for link previews, 1080×1080 for square cards and 1080×1920 for optional story exports. The latter two are separately composed artwork, not automatic crops. Use server-generated or pre-rendered images with the selected script's real fonts; preserve title and author when they wrap. Always attach alt text where the destination supports it.

Instagram is not a generic webpage-link-share endpoint. Offer an approved card download or device file sharing where supported, with a caption and link the reader can use. Do not claim an Instagram post was made or guarantee image previews in every destination; platforms may cache or ignore supplied metadata.

### Technical handoff and acceptance

Use HTTPS, feature detection for `navigator.share`, and `navigator.canShare` before file sharing. Invoke the native share only from the user's click. Provide fallbacks for unavailable APIs, restrictive browser policies, clipboard rejection and offline state. Serve title/description/image metadata in the initial response, use a public image URL, and avoid duplicating URL fields in the share payload. [MDN Web Share API documentation](https://developer.mozilla.org/en-US/docs/Web/API/Navigator/share).

Test on iOS Safari, Android Chrome and desktop browsers with and without native sharing. Verify every language, a long title, a multi-author credit, cancellation, successful copy, copy failure, back/close behaviour and actual link-preview rendering. Test the existing canonical URLs after migration. Record a share intent rather than claiming a completed external post in analytics.

The current page prototype opens a branded share panel. Copy link and Copy caption attempt a real clipboard copy only when the reader selects them, with a selectable-text fallback. Native sharing and external share destinations also require a reader action; opening them never means a post was sent. Production must add verified metadata and generated social-preview images.
