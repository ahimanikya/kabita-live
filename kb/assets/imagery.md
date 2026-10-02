---
type: "Asset knowledge"
title: "Imagery finder, canonical captions and reuse"
---

# Find and reuse an image

Start here when looking for earlier artwork. [Visual catalogue](http://127.0.0.1:8771/image-library-audit.html) · [Canonical image records](imagery-catalogue.json) · [Every file, alias and hash](image-inventory.json) · [Usage plan](image-usage-plan.md).

## Choose by purpose

- **Edition covers:** `cover-001` through `cover-047`, with edition/date filenames. Covers stay with their edition; never use them as poem scenery.
- **Poem illustrations:** 23 artworks. Search the caption, multilingual tags or artwork ID below. Match the poem’s imagery; consult [assignment evidence](../records/poem-art-match-evidence.json). Automatic suggestions still need editorial judgment.
- **Inner-page openings:** the 14 records tagged `section-opening`; these watercolor images may also accompany related poems.
- **Homepage:** `home-life-as-it-is`, reserved for the home identity.
- **Portraits:** use the identity map in the [writer system](../research/author-page-system.md) and [portrait source archive](../artifacts/artwork/portrait-sources/). Never select a portrait by visual similarity or generic theme.
- **Reserved:** [Pipili Chandua](../artifacts/artwork/reserved/) is preserved for future use and excluded from the automatic pool.
- **Earlier studies:** [artwork masters](../artifacts/artwork/masters/), [revision history](../history/index.md) and [recovered generation](../artifacts/artwork/recovered-studies/). These are historical, not automatic replacements.
- **Interface:** [icons](icon-catalogue.md) and [design reference](../reference/design-system.md) cover ornaments, background textures and branding.

## One image, one caption

`imagery-catalogue.json` is the caption authority. Its stable image IDs connect delivery files, master files, roles, themes, provenance and the current caption. A thumbnail, alternate format or compatibility filename is still the same artwork. Reused images keep the same caption, punctuation and capitalization. No per-page caption rewrites. Visible homepage, edition and poem artwork captions align right, with a 12px gap beneath the image on desktop and phones. Decorative placements may omit a caption; there is no need to add labels everywhere. Alt text describes what is visible; poem interpretation and cover stories remain separate contextual prose. Historical studies preserve their original wording and are not rewritten to match current records.

Edit a caption once in the canonical record. Run `python3 tools/imagery.py`, rebuild with `python3 projects/site/build.py`, then run `python3 tools/imagery.py --check`. Refresh the finder after the build to update page locations. The compatibility caption files are generated projections. `tools/audit_images.py` refreshes the complete file inventory and visual catalogue; it does not overwrite canonical captions. Sync the portable package after all checks.

## Border or paper edge

Current treatment: watercolor openings with soft paper edges blend into the background. All inner-page artwork, including edition covers and poem illustrations, is borderless under the user’s latest instruction. Only homepage artwork retains the approved fine warm keyline. Preserve the original bitmap; presentation belongs in CSS.

## Artwork records

Search this page for a place, motif, caption, edition, or image ID. Page locations below are discovered from current public HTML, not guessed from filenames. The full inventory also lists unused files and historical aliases.

### art-pond-at-dawn · Pond At Dawn

- Caption: The pond holds the morning quietly.
- Roles: poem; treatment: framed.
- Find by: dawn, lake, lotus, morning, pond, sunrise, water, कमल, झील, तालाब, भोर, सुबह, ପଦ୍ମ, ପୁଷ୍କରିଣୀ, ପୋଖରୀ, ପ୍ରଭାତ, ଭୋର, ସକାଳ, ସରୋବର.
- Delivery: `assets/poem-art/library/pond-at-dawn.png`.
- [Provenance](../records/poem-art-match-evidence.json).
- Used on 21 pages: [poem-132.html](http://127.0.0.1:8771/poem-132.html), [poem-156.html](http://127.0.0.1:8771/poem-156.html), [poem-160.html](http://127.0.0.1:8771/poem-160.html), [poem-225.html](http://127.0.0.1:8771/poem-225.html), [poem-226.html](http://127.0.0.1:8771/poem-226.html), [poem-250.html](http://127.0.0.1:8771/poem-250.html), [poem-254.html](http://127.0.0.1:8771/poem-254.html), [poem-299.html](http://127.0.0.1:8771/poem-299.html), [poem-311.html](http://127.0.0.1:8771/poem-311.html), [poem-362.html](http://127.0.0.1:8771/poem-362.html), [poem-40.html](http://127.0.0.1:8771/poem-40.html), [poem-423.html](http://127.0.0.1:8771/poem-423.html), [poem-540.html](http://127.0.0.1:8771/poem-540.html), [poem-555.html](http://127.0.0.1:8771/poem-555.html), [poem-625.html](http://127.0.0.1:8771/poem-625.html), [poem-706.html](http://127.0.0.1:8771/poem-706.html), [poem-765.html](http://127.0.0.1:8771/poem-765.html), [poem-782.html](http://127.0.0.1:8771/poem-782.html), [poem-787.html](http://127.0.0.1:8771/poem-787.html), [poem-789.html](http://127.0.0.1:8771/poem-789.html), [poem-811.html](http://127.0.0.1:8771/poem-811.html).

### art-kendu-light · Kendu Light

- Caption: In the woodland, light finds a leaf.
- Roles: poem; treatment: framed.
- Find by: forest, leaf, leaves, tree, woodland, जंगल, पत्त, पेड़, वृक्ष, ଅରଣ୍ୟ, ଗଛ, ଜଙ୍ଗଲ, ପତ୍ର, ପଲ୍ଲବ, ବଣ.
- Delivery: `assets/poem-art/library/kendu-light.png`.
- [Provenance](../records/poem-art-match-evidence.json).
- Used on 31 pages: [poem-137.html](http://127.0.0.1:8771/poem-137.html), [poem-150.html](http://127.0.0.1:8771/poem-150.html), [poem-166.html](http://127.0.0.1:8771/poem-166.html), [poem-201.html](http://127.0.0.1:8771/poem-201.html), [poem-265.html](http://127.0.0.1:8771/poem-265.html), [poem-273.html](http://127.0.0.1:8771/poem-273.html), [poem-30.html](http://127.0.0.1:8771/poem-30.html), [poem-309.html](http://127.0.0.1:8771/poem-309.html), [poem-325.html](http://127.0.0.1:8771/poem-325.html), [poem-333.html](http://127.0.0.1:8771/poem-333.html), [poem-367.html](http://127.0.0.1:8771/poem-367.html), [poem-380.html](http://127.0.0.1:8771/poem-380.html), [poem-382.html](http://127.0.0.1:8771/poem-382.html), [poem-388.html](http://127.0.0.1:8771/poem-388.html), [poem-406.html](http://127.0.0.1:8771/poem-406.html), [poem-480.html](http://127.0.0.1:8771/poem-480.html), [poem-495.html](http://127.0.0.1:8771/poem-495.html), [poem-505.html](http://127.0.0.1:8771/poem-505.html), [poem-55.html](http://127.0.0.1:8771/poem-55.html), [poem-57.html](http://127.0.0.1:8771/poem-57.html), [poem-574.html](http://127.0.0.1:8771/poem-574.html), [poem-593.html](http://127.0.0.1:8771/poem-593.html), [poem-607.html](http://127.0.0.1:8771/poem-607.html), [poem-668.html](http://127.0.0.1:8771/poem-668.html), [poem-68.html](http://127.0.0.1:8771/poem-68.html), [poem-680.html](http://127.0.0.1:8771/poem-680.html), [poem-693.html](http://127.0.0.1:8771/poem-693.html), [poem-72.html](http://127.0.0.1:8771/poem-72.html), [poem-745.html](http://127.0.0.1:8771/poem-745.html), [poem-792.html](http://127.0.0.1:8771/poem-792.html), [poem-90.html](http://127.0.0.1:8771/poem-90.html).

### art-thread-by-the-window · Thread By The Window

- Caption: A loose thread remembers the hands.
- Roles: poem; treatment: framed.
- Find by: cloth, cotton, saree, sari, thread, weav, weaving, कपड़, तंतु, धाग, बुन, साड़ी, ବସ୍ତ୍ର, ବୁଣା, ଶାଢ଼ୀ, ଶାଢି, ଶାଢୀ, ସୂତା.
- Delivery: `assets/poem-art/library/thread-by-the-window.png`.
- [Provenance](../records/poem-art-match-evidence.json).
- Used on 14 pages: [poem-167.html](http://127.0.0.1:8771/poem-167.html), [poem-179.html](http://127.0.0.1:8771/poem-179.html), [poem-364.html](http://127.0.0.1:8771/poem-364.html), [poem-376.html](http://127.0.0.1:8771/poem-376.html), [poem-412.html](http://127.0.0.1:8771/poem-412.html), [poem-424.html](http://127.0.0.1:8771/poem-424.html), [poem-440.html](http://127.0.0.1:8771/poem-440.html), [poem-521.html](http://127.0.0.1:8771/poem-521.html), [poem-551.html](http://127.0.0.1:8771/poem-551.html), [poem-562.html](http://127.0.0.1:8771/poem-562.html), [poem-627.html](http://127.0.0.1:8771/poem-627.html), [poem-669.html](http://127.0.0.1:8771/poem-669.html), [poem-699.html](http://127.0.0.1:8771/poem-699.html), [poem-764.html](http://127.0.0.1:8771/poem-764.html).

### art-koraput-morning · Koraput Morning

- Caption: The hills leave room for a breath.
- Roles: poem; treatment: framed.
- Find by: hill, hills, mist, mountain, ridge, कोहरा, पर्वत, पहाड़, କୁହୁଡ଼ି, କୁହୁଡି, ପର୍ବତ, ପାର୍ବତ୍ୟ, ପାହାଡ, ପାହାଡ଼.
- Delivery: `assets/poem-art/library/koraput-morning.png`.
- [Provenance](../records/poem-art-match-evidence.json).
- Used on 10 pages: [poem-152.html](http://127.0.0.1:8771/poem-152.html), [poem-158.html](http://127.0.0.1:8771/poem-158.html), [poem-209.html](http://127.0.0.1:8771/poem-209.html), [poem-242.html](http://127.0.0.1:8771/poem-242.html), [poem-252.html](http://127.0.0.1:8771/poem-252.html), [poem-267.html](http://127.0.0.1:8771/poem-267.html), [poem-432.html](http://127.0.0.1:8771/poem-432.html), [poem-468.html](http://127.0.0.1:8771/poem-468.html), [poem-635.html](http://127.0.0.1:8771/poem-635.html), [poem-816.html](http://127.0.0.1:8771/poem-816.html).

### art-courtyard-petals · Courtyard Petals

- Caption: A few petals. The afternoon stays.
- Roles: poem; treatment: framed.
- Find by: bloom, flower, flowers, monsoon, petal, rain, shower, wet, पुष्प, फूल, बरस, बारिश, भीग, वर्षा, सावन, ଆଷାଢ, କୁସୁମ, ପୁଷ୍ପ, ଫୁଲ, ବରଷା, ବର୍ଷା, ବାରିଧାରା, ବୃଷ୍ଟି, ଭିଜ, ଶ୍ରାବଣ.
- Delivery: `assets/poem-art/library/courtyard-petals.png`.
- [Provenance](../records/poem-art-match-evidence.json).
- Used on 62 pages: [poem-108.html](http://127.0.0.1:8771/poem-108.html), [poem-11.html](http://127.0.0.1:8771/poem-11.html), [poem-116.html](http://127.0.0.1:8771/poem-116.html), [poem-13.html](http://127.0.0.1:8771/poem-13.html), [poem-142.html](http://127.0.0.1:8771/poem-142.html), [poem-144.html](http://127.0.0.1:8771/poem-144.html), [poem-203.html](http://127.0.0.1:8771/poem-203.html), [poem-220.html](http://127.0.0.1:8771/poem-220.html), [poem-227.html](http://127.0.0.1:8771/poem-227.html), [poem-234.html](http://127.0.0.1:8771/poem-234.html), [poem-238.html](http://127.0.0.1:8771/poem-238.html), [poem-302.html](http://127.0.0.1:8771/poem-302.html), [poem-331.html](http://127.0.0.1:8771/poem-331.html), [poem-332.html](http://127.0.0.1:8771/poem-332.html), [poem-338.html](http://127.0.0.1:8771/poem-338.html), [poem-346.html](http://127.0.0.1:8771/poem-346.html), [poem-349.html](http://127.0.0.1:8771/poem-349.html), [poem-355.html](http://127.0.0.1:8771/poem-355.html), [poem-370.html](http://127.0.0.1:8771/poem-370.html), [poem-379.html](http://127.0.0.1:8771/poem-379.html), [poem-392.html](http://127.0.0.1:8771/poem-392.html), [poem-417.html](http://127.0.0.1:8771/poem-417.html), [poem-420.html](http://127.0.0.1:8771/poem-420.html), [poem-446.html](http://127.0.0.1:8771/poem-446.html), [poem-463.html](http://127.0.0.1:8771/poem-463.html), [poem-501.html](http://127.0.0.1:8771/poem-501.html), [poem-515.html](http://127.0.0.1:8771/poem-515.html), [poem-523.html](http://127.0.0.1:8771/poem-523.html), [poem-528.html](http://127.0.0.1:8771/poem-528.html), [poem-531.html](http://127.0.0.1:8771/poem-531.html), [poem-532.html](http://127.0.0.1:8771/poem-532.html), [poem-534.html](http://127.0.0.1:8771/poem-534.html), [poem-563.html](http://127.0.0.1:8771/poem-563.html), [poem-570.html](http://127.0.0.1:8771/poem-570.html), [poem-571.html](http://127.0.0.1:8771/poem-571.html), [poem-587.html](http://127.0.0.1:8771/poem-587.html), [poem-600.html](http://127.0.0.1:8771/poem-600.html), [poem-613.html](http://127.0.0.1:8771/poem-613.html), [poem-620.html](http://127.0.0.1:8771/poem-620.html), [poem-63.html](http://127.0.0.1:8771/poem-63.html), [poem-636.html](http://127.0.0.1:8771/poem-636.html), [poem-638.html](http://127.0.0.1:8771/poem-638.html), [poem-641.html](http://127.0.0.1:8771/poem-641.html), [poem-65.html](http://127.0.0.1:8771/poem-65.html), [poem-670.html](http://127.0.0.1:8771/poem-670.html), [poem-696.html](http://127.0.0.1:8771/poem-696.html), [poem-7.html](http://127.0.0.1:8771/poem-7.html), [poem-700.html](http://127.0.0.1:8771/poem-700.html), [poem-722.html](http://127.0.0.1:8771/poem-722.html), [poem-728.html](http://127.0.0.1:8771/poem-728.html), [poem-729.html](http://127.0.0.1:8771/poem-729.html), [poem-739.html](http://127.0.0.1:8771/poem-739.html), [poem-742.html](http://127.0.0.1:8771/poem-742.html), [poem-767.html](http://127.0.0.1:8771/poem-767.html), [poem-777.html](http://127.0.0.1:8771/poem-777.html), [poem-779.html](http://127.0.0.1:8771/poem-779.html), [poem-798.html](http://127.0.0.1:8771/poem-798.html), [poem-807.html](http://127.0.0.1:8771/poem-807.html), [poem-81.html](http://127.0.0.1:8771/poem-81.html), [poem-813.html](http://127.0.0.1:8771/poem-813.html), [poem-815.html](http://127.0.0.1:8771/poem-815.html), [poem-822.html](http://127.0.0.1:8771/poem-822.html).

### art-sea-breeze-cloth · Sea Breeze Cloth

- Caption: The breeze carries what words leave behind.
- Roles: poem; treatment: framed.
- Find by: breeze, coast, ocean, sea, shore, wave, wind, तट, पवन, लहर, समुद्र, सागर, हवा, ଢେଉ, ପବନ, ବାଆ, ବାୟୁ, ବେଳାଭୂମି, ଲହରୀ, ସମୁଦ୍ର, ସାଗର.
- Delivery: `assets/poem-art/library/sea-breeze-cloth.png`.
- [Provenance](../records/poem-art-match-evidence.json).
- Used on 56 pages: [poem-114.html](http://127.0.0.1:8771/poem-114.html), [poem-124.html](http://127.0.0.1:8771/poem-124.html), [poem-138.html](http://127.0.0.1:8771/poem-138.html), [poem-168.html](http://127.0.0.1:8771/poem-168.html), [poem-172.html](http://127.0.0.1:8771/poem-172.html), [poem-182.html](http://127.0.0.1:8771/poem-182.html), [poem-184.html](http://127.0.0.1:8771/poem-184.html), [poem-185.html](http://127.0.0.1:8771/poem-185.html), [poem-190.html](http://127.0.0.1:8771/poem-190.html), [poem-192.html](http://127.0.0.1:8771/poem-192.html), [poem-219.html](http://127.0.0.1:8771/poem-219.html), [poem-253.html](http://127.0.0.1:8771/poem-253.html), [poem-256.html](http://127.0.0.1:8771/poem-256.html), [poem-257.html](http://127.0.0.1:8771/poem-257.html), [poem-262.html](http://127.0.0.1:8771/poem-262.html), [poem-275.html](http://127.0.0.1:8771/poem-275.html), [poem-278.html](http://127.0.0.1:8771/poem-278.html), [poem-289.html](http://127.0.0.1:8771/poem-289.html), [poem-293.html](http://127.0.0.1:8771/poem-293.html), [poem-303.html](http://127.0.0.1:8771/poem-303.html), [poem-344.html](http://127.0.0.1:8771/poem-344.html), [poem-381.html](http://127.0.0.1:8771/poem-381.html), [poem-393.html](http://127.0.0.1:8771/poem-393.html), [poem-397.html](http://127.0.0.1:8771/poem-397.html), [poem-433.html](http://127.0.0.1:8771/poem-433.html), [poem-439.html](http://127.0.0.1:8771/poem-439.html), [poem-445.html](http://127.0.0.1:8771/poem-445.html), [poem-448.html](http://127.0.0.1:8771/poem-448.html), [poem-50.html](http://127.0.0.1:8771/poem-50.html), [poem-504.html](http://127.0.0.1:8771/poem-504.html), [poem-513.html](http://127.0.0.1:8771/poem-513.html), [poem-516.html](http://127.0.0.1:8771/poem-516.html), [poem-517.html](http://127.0.0.1:8771/poem-517.html), [poem-529.html](http://127.0.0.1:8771/poem-529.html), [poem-539.html](http://127.0.0.1:8771/poem-539.html), [poem-541.html](http://127.0.0.1:8771/poem-541.html), [poem-557.html](http://127.0.0.1:8771/poem-557.html), [poem-581.html](http://127.0.0.1:8771/poem-581.html), [poem-611.html](http://127.0.0.1:8771/poem-611.html), [poem-621.html](http://127.0.0.1:8771/poem-621.html), [poem-631.html](http://127.0.0.1:8771/poem-631.html), [poem-637.html](http://127.0.0.1:8771/poem-637.html), [poem-650.html](http://127.0.0.1:8771/poem-650.html), [poem-651.html](http://127.0.0.1:8771/poem-651.html), [poem-655.html](http://127.0.0.1:8771/poem-655.html), [poem-661.html](http://127.0.0.1:8771/poem-661.html), [poem-671.html](http://127.0.0.1:8771/poem-671.html), [poem-681.html](http://127.0.0.1:8771/poem-681.html), [poem-740.html](http://127.0.0.1:8771/poem-740.html), [poem-755.html](http://127.0.0.1:8771/poem-755.html), [poem-770.html](http://127.0.0.1:8771/poem-770.html), [poem-776.html](http://127.0.0.1:8771/poem-776.html), [poem-796.html](http://127.0.0.1:8771/poem-796.html), [poem-80.html](http://127.0.0.1:8771/poem-80.html), [poem-823.html](http://127.0.0.1:8771/poem-823.html), [poem-98.html](http://127.0.0.1:8771/poem-98.html).

### art-quiet-path · Quiet Path

- Caption: The path continues, softly.
- Roles: poem, section-opening; treatment: paper-edge.
- Find by: earth, footstep, journey, path, road, soil, travell, walk, walkway, wander, मिट्टी, यात्रा, रास्त, राह, सफर, ପଥ, ପଥିକ, ବାଟ, ମାଟି, ଯାତ୍ରା, ରାସ୍ତା.
- Delivery: `assets/section-art/quiet-path.webp`.
- [Original master](../artifacts/artwork/masters/section-art/quiet-path.png).
- [Provenance](../records/poem-art-match-evidence.json).
- Used on 116 pages: [not-found.html](http://127.0.0.1:8771/not-found.html), [poem-110.html](http://127.0.0.1:8771/poem-110.html), [poem-113.html](http://127.0.0.1:8771/poem-113.html), [poem-123.html](http://127.0.0.1:8771/poem-123.html), [poem-125.html](http://127.0.0.1:8771/poem-125.html), [poem-127.html](http://127.0.0.1:8771/poem-127.html), [poem-128.html](http://127.0.0.1:8771/poem-128.html), [poem-130.html](http://127.0.0.1:8771/poem-130.html), [poem-14.html](http://127.0.0.1:8771/poem-14.html), [poem-141.html](http://127.0.0.1:8771/poem-141.html), [poem-151.html](http://127.0.0.1:8771/poem-151.html), [poem-154.html](http://127.0.0.1:8771/poem-154.html), [poem-159.html](http://127.0.0.1:8771/poem-159.html), [poem-163.html](http://127.0.0.1:8771/poem-163.html), [poem-164.html](http://127.0.0.1:8771/poem-164.html), [poem-169.html](http://127.0.0.1:8771/poem-169.html), [poem-176.html](http://127.0.0.1:8771/poem-176.html), [poem-191.html](http://127.0.0.1:8771/poem-191.html), [poem-193.html](http://127.0.0.1:8771/poem-193.html), [poem-197.html](http://127.0.0.1:8771/poem-197.html), [poem-210.html](http://127.0.0.1:8771/poem-210.html), [poem-223.html](http://127.0.0.1:8771/poem-223.html), [poem-233.html](http://127.0.0.1:8771/poem-233.html), [poem-258.html](http://127.0.0.1:8771/poem-258.html), [poem-26.html](http://127.0.0.1:8771/poem-26.html), [poem-260.html](http://127.0.0.1:8771/poem-260.html), [poem-266.html](http://127.0.0.1:8771/poem-266.html), [poem-281.html](http://127.0.0.1:8771/poem-281.html), [poem-295.html](http://127.0.0.1:8771/poem-295.html), [poem-307.html](http://127.0.0.1:8771/poem-307.html), [poem-313.html](http://127.0.0.1:8771/poem-313.html), [poem-315.html](http://127.0.0.1:8771/poem-315.html), [poem-316.html](http://127.0.0.1:8771/poem-316.html), [poem-319.html](http://127.0.0.1:8771/poem-319.html), [poem-321.html](http://127.0.0.1:8771/poem-321.html), [poem-324.html](http://127.0.0.1:8771/poem-324.html), [poem-33.html](http://127.0.0.1:8771/poem-33.html), [poem-330.html](http://127.0.0.1:8771/poem-330.html), [poem-337.html](http://127.0.0.1:8771/poem-337.html), [poem-34.html](http://127.0.0.1:8771/poem-34.html), [poem-340.html](http://127.0.0.1:8771/poem-340.html), [poem-350.html](http://127.0.0.1:8771/poem-350.html), [poem-352.html](http://127.0.0.1:8771/poem-352.html), [poem-356.html](http://127.0.0.1:8771/poem-356.html), [poem-365.html](http://127.0.0.1:8771/poem-365.html), [poem-372.html](http://127.0.0.1:8771/poem-372.html), [poem-389.html](http://127.0.0.1:8771/poem-389.html), [poem-398.html](http://127.0.0.1:8771/poem-398.html), [poem-401.html](http://127.0.0.1:8771/poem-401.html), [poem-403.html](http://127.0.0.1:8771/poem-403.html), [poem-408.html](http://127.0.0.1:8771/poem-408.html), [poem-415.html](http://127.0.0.1:8771/poem-415.html), [poem-425.html](http://127.0.0.1:8771/poem-425.html), [poem-428.html](http://127.0.0.1:8771/poem-428.html), [poem-43.html](http://127.0.0.1:8771/poem-43.html), [poem-430.html](http://127.0.0.1:8771/poem-430.html), [poem-435.html](http://127.0.0.1:8771/poem-435.html), [poem-436.html](http://127.0.0.1:8771/poem-436.html), [poem-449.html](http://127.0.0.1:8771/poem-449.html), [poem-461.html](http://127.0.0.1:8771/poem-461.html), [poem-465.html](http://127.0.0.1:8771/poem-465.html), [poem-469.html](http://127.0.0.1:8771/poem-469.html), [poem-483.html](http://127.0.0.1:8771/poem-483.html), [poem-489.html](http://127.0.0.1:8771/poem-489.html), [poem-49.html](http://127.0.0.1:8771/poem-49.html), [poem-494.html](http://127.0.0.1:8771/poem-494.html), [poem-508.html](http://127.0.0.1:8771/poem-508.html), [poem-510.html](http://127.0.0.1:8771/poem-510.html), [poem-511.html](http://127.0.0.1:8771/poem-511.html), [poem-514.html](http://127.0.0.1:8771/poem-514.html), [poem-53.html](http://127.0.0.1:8771/poem-53.html), [poem-538.html](http://127.0.0.1:8771/poem-538.html), [poem-545.html](http://127.0.0.1:8771/poem-545.html), [poem-546.html](http://127.0.0.1:8771/poem-546.html), [poem-548.html](http://127.0.0.1:8771/poem-548.html), [poem-554.html](http://127.0.0.1:8771/poem-554.html), [poem-573.html](http://127.0.0.1:8771/poem-573.html), [poem-578.html](http://127.0.0.1:8771/poem-578.html), [poem-58.html](http://127.0.0.1:8771/poem-58.html), [poem-580.html](http://127.0.0.1:8771/poem-580.html), [poem-582.html](http://127.0.0.1:8771/poem-582.html), [poem-59.html](http://127.0.0.1:8771/poem-59.html), [poem-594.html](http://127.0.0.1:8771/poem-594.html), [poem-595.html](http://127.0.0.1:8771/poem-595.html), [poem-603.html](http://127.0.0.1:8771/poem-603.html), [poem-605.html](http://127.0.0.1:8771/poem-605.html), [poem-610.html](http://127.0.0.1:8771/poem-610.html), [poem-615.html](http://127.0.0.1:8771/poem-615.html), [poem-616.html](http://127.0.0.1:8771/poem-616.html), [poem-617.html](http://127.0.0.1:8771/poem-617.html), [poem-628.html](http://127.0.0.1:8771/poem-628.html), [poem-629.html](http://127.0.0.1:8771/poem-629.html), [poem-639.html](http://127.0.0.1:8771/poem-639.html), [poem-64.html](http://127.0.0.1:8771/poem-64.html), [poem-643.html](http://127.0.0.1:8771/poem-643.html), [poem-646.html](http://127.0.0.1:8771/poem-646.html), [poem-648.html](http://127.0.0.1:8771/poem-648.html), [poem-657.html](http://127.0.0.1:8771/poem-657.html), [poem-67.html](http://127.0.0.1:8771/poem-67.html), [poem-678.html](http://127.0.0.1:8771/poem-678.html), [poem-685.html](http://127.0.0.1:8771/poem-685.html), [poem-695.html](http://127.0.0.1:8771/poem-695.html), [poem-707.html](http://127.0.0.1:8771/poem-707.html), [poem-709.html](http://127.0.0.1:8771/poem-709.html), [poem-712.html](http://127.0.0.1:8771/poem-712.html), [poem-713.html](http://127.0.0.1:8771/poem-713.html), [poem-714.html](http://127.0.0.1:8771/poem-714.html), [poem-715.html](http://127.0.0.1:8771/poem-715.html), [poem-719.html](http://127.0.0.1:8771/poem-719.html), [poem-732.html](http://127.0.0.1:8771/poem-732.html), [poem-738.html](http://127.0.0.1:8771/poem-738.html), [poem-750.html](http://127.0.0.1:8771/poem-750.html), [poem-786.html](http://127.0.0.1:8771/poem-786.html), [poem-8.html](http://127.0.0.1:8771/poem-8.html), [poem-84.html](http://127.0.0.1:8771/poem-84.html), [poem-9.html](http://127.0.0.1:8771/poem-9.html).

### art-correspondence · Correspondence

- Caption: Some words wait by the window.
- Roles: poem, section-opening; treatment: paper-edge.
- Find by: envelope, letter, letters, message, खत, चिट्ठी, पत्र, संदेश, ଖବର, ଚିଟାଉ, ଚିଠି, ସନ୍ଦେଶ.
- Delivery: `assets/section-art/correspondence.webp`.
- [Original master](../artifacts/artwork/masters/section-art/correspondence.png).
- [Provenance](../records/poem-art-match-evidence.json).
- Used on 8 pages: [contact.html](http://127.0.0.1:8771/contact.html), [poem-29.html](http://127.0.0.1:8771/poem-29.html), [poem-291.html](http://127.0.0.1:8771/poem-291.html), [poem-460.html](http://127.0.0.1:8771/poem-460.html), [poem-697.html](http://127.0.0.1:8771/poem-697.html), [poem-720.html](http://127.0.0.1:8771/poem-720.html), [poem-743.html](http://127.0.0.1:8771/poem-743.html), [poem-791.html](http://127.0.0.1:8771/poem-791.html).

### art-reader-letters · Reader Letters

- Caption: A little warmth between the words.
- Roles: poem, section-opening; treatment: paper-edge.
- Find by: conversation, dialogue, friend, tea, चाय, दोस्त, बातचीत, मित्र, ଆଳାପ, କଥାବାର୍ତ୍ତା, ଚାହା, ବନ୍ଧୁ, ସାଙ୍ଗ.
- Delivery: `assets/section-art/reader-letters.webp`.
- [Original master](../artifacts/artwork/masters/section-art/reader-letters.png).
- [Provenance](../records/poem-art-match-evidence.json).
- Used on 14 pages: [feedback.html](http://127.0.0.1:8771/feedback.html), [poem-135.html](http://127.0.0.1:8771/poem-135.html), [poem-162.html](http://127.0.0.1:8771/poem-162.html), [poem-17.html](http://127.0.0.1:8771/poem-17.html), [poem-195.html](http://127.0.0.1:8771/poem-195.html), [poem-207.html](http://127.0.0.1:8771/poem-207.html), [poem-280.html](http://127.0.0.1:8771/poem-280.html), [poem-290.html](http://127.0.0.1:8771/poem-290.html), [poem-36.html](http://127.0.0.1:8771/poem-36.html), [poem-385.html](http://127.0.0.1:8771/poem-385.html), [poem-400.html](http://127.0.0.1:8771/poem-400.html), [poem-474.html](http://127.0.0.1:8771/poem-474.html), [poem-553.html](http://127.0.0.1:8771/poem-553.html), [poem-598.html](http://127.0.0.1:8771/poem-598.html).

### art-reading-room · Reading Room

- Caption: A page makes room for silence.
- Roles: poem, section-opening; treatment: paper-edge.
- Find by: meditat, reflection, silence, stillness, खामोश, चुप्पी, निस्तब्ध, मौन, ନିରବ, ନିର୍ଜନ, ନୀରବ, ମୌନ.
- Delivery: `assets/section-art/reading-room.webp`.
- [Original master](../artifacts/artwork/masters/section-art/reading-room.png).
- [Provenance](../records/poem-art-match-evidence.json).
- Used on 39 pages: [poem-106.html](http://127.0.0.1:8771/poem-106.html), [poem-117.html](http://127.0.0.1:8771/poem-117.html), [poem-121.html](http://127.0.0.1:8771/poem-121.html), [poem-178.html](http://127.0.0.1:8771/poem-178.html), [poem-19.html](http://127.0.0.1:8771/poem-19.html), [poem-200.html](http://127.0.0.1:8771/poem-200.html), [poem-244.html](http://127.0.0.1:8771/poem-244.html), [poem-268.html](http://127.0.0.1:8771/poem-268.html), [poem-270.html](http://127.0.0.1:8771/poem-270.html), [poem-279.html](http://127.0.0.1:8771/poem-279.html), [poem-296.html](http://127.0.0.1:8771/poem-296.html), [poem-323.html](http://127.0.0.1:8771/poem-323.html), [poem-326.html](http://127.0.0.1:8771/poem-326.html), [poem-328.html](http://127.0.0.1:8771/poem-328.html), [poem-335.html](http://127.0.0.1:8771/poem-335.html), [poem-345.html](http://127.0.0.1:8771/poem-345.html), [poem-360.html](http://127.0.0.1:8771/poem-360.html), [poem-363.html](http://127.0.0.1:8771/poem-363.html), [poem-441.html](http://127.0.0.1:8771/poem-441.html), [poem-472.html](http://127.0.0.1:8771/poem-472.html), [poem-478.html](http://127.0.0.1:8771/poem-478.html), [poem-559.html](http://127.0.0.1:8771/poem-559.html), [poem-568.html](http://127.0.0.1:8771/poem-568.html), [poem-584.html](http://127.0.0.1:8771/poem-584.html), [poem-597.html](http://127.0.0.1:8771/poem-597.html), [poem-614.html](http://127.0.0.1:8771/poem-614.html), [poem-622.html](http://127.0.0.1:8771/poem-622.html), [poem-645.html](http://127.0.0.1:8771/poem-645.html), [poem-666.html](http://127.0.0.1:8771/poem-666.html), [poem-687.html](http://127.0.0.1:8771/poem-687.html), [poem-761.html](http://127.0.0.1:8771/poem-761.html), [poem-783.html](http://127.0.0.1:8771/poem-783.html), [poem-800.html](http://127.0.0.1:8771/poem-800.html), [poem-802.html](http://127.0.0.1:8771/poem-802.html), [poem-803.html](http://127.0.0.1:8771/poem-803.html), [poem-806.html](http://127.0.0.1:8771/poem-806.html), [poem-820.html](http://127.0.0.1:8771/poem-820.html), [poem-83.html](http://127.0.0.1:8771/poem-83.html), [poems.html](http://127.0.0.1:8771/poems.html).

### art-voices · Voices

- Caption: A place kept for another voice.
- Roles: poem, section-opening; treatment: paper-edge.
- Find by: community, people, society, together, इंसान, मानव, लोग, समाज, ଜନତା, ମଣିଷ, ଲୋକମାନ, ସମାଜ.
- Delivery: `assets/section-art/voices.webp`.
- [Original master](../artifacts/artwork/masters/section-art/voices.png).
- [Provenance](../records/poem-art-match-evidence.json).
- Used on 33 pages: [current-contributors.html](http://127.0.0.1:8771/current-contributors.html), [poem-145.html](http://127.0.0.1:8771/poem-145.html), [poem-147.html](http://127.0.0.1:8771/poem-147.html), [poem-188.html](http://127.0.0.1:8771/poem-188.html), [poem-204.html](http://127.0.0.1:8771/poem-204.html), [poem-211.html](http://127.0.0.1:8771/poem-211.html), [poem-222.html](http://127.0.0.1:8771/poem-222.html), [poem-230.html](http://127.0.0.1:8771/poem-230.html), [poem-237.html](http://127.0.0.1:8771/poem-237.html), [poem-246.html](http://127.0.0.1:8771/poem-246.html), [poem-272.html](http://127.0.0.1:8771/poem-272.html), [poem-292.html](http://127.0.0.1:8771/poem-292.html), [poem-310.html](http://127.0.0.1:8771/poem-310.html), [poem-322.html](http://127.0.0.1:8771/poem-322.html), [poem-373.html](http://127.0.0.1:8771/poem-373.html), [poem-42.html](http://127.0.0.1:8771/poem-42.html), [poem-421.html](http://127.0.0.1:8771/poem-421.html), [poem-447.html](http://127.0.0.1:8771/poem-447.html), [poem-452.html](http://127.0.0.1:8771/poem-452.html), [poem-453.html](http://127.0.0.1:8771/poem-453.html), [poem-475.html](http://127.0.0.1:8771/poem-475.html), [poem-493.html](http://127.0.0.1:8771/poem-493.html), [poem-576.html](http://127.0.0.1:8771/poem-576.html), [poem-577.html](http://127.0.0.1:8771/poem-577.html), [poem-596.html](http://127.0.0.1:8771/poem-596.html), [poem-623.html](http://127.0.0.1:8771/poem-623.html), [poem-647.html](http://127.0.0.1:8771/poem-647.html), [poem-665.html](http://127.0.0.1:8771/poem-665.html), [poem-683.html](http://127.0.0.1:8771/poem-683.html), [poem-723.html](http://127.0.0.1:8771/poem-723.html), [poem-762.html](http://127.0.0.1:8771/poem-762.html), [poem-85.html](http://127.0.0.1:8771/poem-85.html), [poets.html](http://127.0.0.1:8771/poets.html).

### art-writer-profile · Writer Profile

- Caption: The chair remembers a presence.
- Roles: poem, section-opening; treatment: paper-edge.
- Find by: absence, absent, death, died, grief, loneliness, lonely, loss, अकेल, बिछड़, मृत्यु, मौत, विरह, शून्य, श्मशान, ଏକାକୀ, ଏକାନ୍ତ, ବିଦାୟ, ବିରହ, ମରଣ, ମଶାଣି, ମୃତ୍ୟୁ, ଶୂନ୍ୟ.
- Delivery: `assets/section-art/writer-profile.webp`.
- [Original master](../artifacts/artwork/masters/section-art/writer-profile.png).
- [Provenance](../records/poem-art-match-evidence.json).
- Used on 40 pages: [poem-131.html](http://127.0.0.1:8771/poem-131.html), [poem-139.html](http://127.0.0.1:8771/poem-139.html), [poem-15.html](http://127.0.0.1:8771/poem-15.html), [poem-18.html](http://127.0.0.1:8771/poem-18.html), [poem-187.html](http://127.0.0.1:8771/poem-187.html), [poem-216.html](http://127.0.0.1:8771/poem-216.html), [poem-218.html](http://127.0.0.1:8771/poem-218.html), [poem-240.html](http://127.0.0.1:8771/poem-240.html), [poem-277.html](http://127.0.0.1:8771/poem-277.html), [poem-306.html](http://127.0.0.1:8771/poem-306.html), [poem-374.html](http://127.0.0.1:8771/poem-374.html), [poem-404.html](http://127.0.0.1:8771/poem-404.html), [poem-410.html](http://127.0.0.1:8771/poem-410.html), [poem-418.html](http://127.0.0.1:8771/poem-418.html), [poem-427.html](http://127.0.0.1:8771/poem-427.html), [poem-46.html](http://127.0.0.1:8771/poem-46.html), [poem-486.html](http://127.0.0.1:8771/poem-486.html), [poem-491.html](http://127.0.0.1:8771/poem-491.html), [poem-492.html](http://127.0.0.1:8771/poem-492.html), [poem-506.html](http://127.0.0.1:8771/poem-506.html), [poem-512.html](http://127.0.0.1:8771/poem-512.html), [poem-566.html](http://127.0.0.1:8771/poem-566.html), [poem-583.html](http://127.0.0.1:8771/poem-583.html), [poem-588.html](http://127.0.0.1:8771/poem-588.html), [poem-60.html](http://127.0.0.1:8771/poem-60.html), [poem-612.html](http://127.0.0.1:8771/poem-612.html), [poem-70.html](http://127.0.0.1:8771/poem-70.html), [poem-701.html](http://127.0.0.1:8771/poem-701.html), [poem-718.html](http://127.0.0.1:8771/poem-718.html), [poem-727.html](http://127.0.0.1:8771/poem-727.html), [poem-730.html](http://127.0.0.1:8771/poem-730.html), [poem-735.html](http://127.0.0.1:8771/poem-735.html), [poem-737.html](http://127.0.0.1:8771/poem-737.html), [poem-741.html](http://127.0.0.1:8771/poem-741.html), [poem-753.html](http://127.0.0.1:8771/poem-753.html), [poem-76.html](http://127.0.0.1:8771/poem-76.html), [poem-771.html](http://127.0.0.1:8771/poem-771.html), [poem-790.html](http://127.0.0.1:8771/poem-790.html), [poem-818.html](http://127.0.0.1:8771/poem-818.html), [poem-94.html](http://127.0.0.1:8771/poem-94.html).

### art-our-story · Our Story

- Caption: The threshold remembers home.
- Roles: poem, section-opening; treatment: paper-edge.
- Find by: childhood, father, home, mother, village, गाँव, गांव, घर, पिता, बचपन, माँ, ଗାଁ, ଘର, ଜନ୍ମଭୂମି, ପିଲାଦିନ, ବାପା, ବାଲ୍ୟ, ବୋଉ, ମାଁ, ମାଆ.
- Delivery: `assets/section-art/our-story.webp`.
- [Original master](../artifacts/artwork/masters/section-art/our-story.png).
- [Provenance](../records/poem-art-match-evidence.json).
- Used on 51 pages: [about.html](http://127.0.0.1:8771/about.html), [poem-111.html](http://127.0.0.1:8771/poem-111.html), [poem-115.html](http://127.0.0.1:8771/poem-115.html), [poem-140.html](http://127.0.0.1:8771/poem-140.html), [poem-143.html](http://127.0.0.1:8771/poem-143.html), [poem-153.html](http://127.0.0.1:8771/poem-153.html), [poem-157.html](http://127.0.0.1:8771/poem-157.html), [poem-16.html](http://127.0.0.1:8771/poem-16.html), [poem-180.html](http://127.0.0.1:8771/poem-180.html), [poem-215.html](http://127.0.0.1:8771/poem-215.html), [poem-243.html](http://127.0.0.1:8771/poem-243.html), [poem-248.html](http://127.0.0.1:8771/poem-248.html), [poem-249.html](http://127.0.0.1:8771/poem-249.html), [poem-261.html](http://127.0.0.1:8771/poem-261.html), [poem-269.html](http://127.0.0.1:8771/poem-269.html), [poem-285.html](http://127.0.0.1:8771/poem-285.html), [poem-32.html](http://127.0.0.1:8771/poem-32.html), [poem-320.html](http://127.0.0.1:8771/poem-320.html), [poem-343.html](http://127.0.0.1:8771/poem-343.html), [poem-384.html](http://127.0.0.1:8771/poem-384.html), [poem-390.html](http://127.0.0.1:8771/poem-390.html), [poem-416.html](http://127.0.0.1:8771/poem-416.html), [poem-444.html](http://127.0.0.1:8771/poem-444.html), [poem-47.html](http://127.0.0.1:8771/poem-47.html), [poem-471.html](http://127.0.0.1:8771/poem-471.html), [poem-48.html](http://127.0.0.1:8771/poem-48.html), [poem-498.html](http://127.0.0.1:8771/poem-498.html), [poem-500.html](http://127.0.0.1:8771/poem-500.html), [poem-518.html](http://127.0.0.1:8771/poem-518.html), [poem-526.html](http://127.0.0.1:8771/poem-526.html), [poem-530.html](http://127.0.0.1:8771/poem-530.html), [poem-552.html](http://127.0.0.1:8771/poem-552.html), [poem-569.html](http://127.0.0.1:8771/poem-569.html), [poem-575.html](http://127.0.0.1:8771/poem-575.html), [poem-586.html](http://127.0.0.1:8771/poem-586.html), [poem-590.html](http://127.0.0.1:8771/poem-590.html), [poem-591.html](http://127.0.0.1:8771/poem-591.html), [poem-592.html](http://127.0.0.1:8771/poem-592.html), [poem-630.html](http://127.0.0.1:8771/poem-630.html), [poem-642.html](http://127.0.0.1:8771/poem-642.html), [poem-674.html](http://127.0.0.1:8771/poem-674.html), [poem-679.html](http://127.0.0.1:8771/poem-679.html), [poem-688.html](http://127.0.0.1:8771/poem-688.html), [poem-702.html](http://127.0.0.1:8771/poem-702.html), [poem-711.html](http://127.0.0.1:8771/poem-711.html), [poem-757.html](http://127.0.0.1:8771/poem-757.html), [poem-766.html](http://127.0.0.1:8771/poem-766.html), [poem-794.html](http://127.0.0.1:8771/poem-794.html), [poem-808.html](http://127.0.0.1:8771/poem-808.html), [poem-812.html](http://127.0.0.1:8771/poem-812.html), [poem-95.html](http://127.0.0.1:8771/poem-95.html).

### art-gatherings · Gatherings

- Caption: There is room to sit together.
- Roles: poem, section-opening; treatment: paper-edge.
- Find by: companionship, meeting, reunion, मिलन, मुलाकात, रिश्त, ବନ୍ଧନ, ମିଳନ, ସମ୍ପର୍କ, ସାକ୍ଷାତ.
- Delivery: `assets/section-art/gatherings.webp`.
- [Original master](../artifacts/artwork/masters/section-art/gatherings.png).
- [Provenance](../records/poem-art-match-evidence.json).
- Used on 13 pages: [highlight.html](http://127.0.0.1:8771/highlight.html), [highlights.html](http://127.0.0.1:8771/highlights.html), [poem-361.html](http://127.0.0.1:8771/poem-361.html), [poem-481.html](http://127.0.0.1:8771/poem-481.html), [poem-482.html](http://127.0.0.1:8771/poem-482.html), [poem-484.html](http://127.0.0.1:8771/poem-484.html), [poem-485.html](http://127.0.0.1:8771/poem-485.html), [poem-547.html](http://127.0.0.1:8771/poem-547.html), [poem-633.html](http://127.0.0.1:8771/poem-633.html), [poem-704.html](http://127.0.0.1:8771/poem-704.html), [poem-726.html](http://127.0.0.1:8771/poem-726.html), [poem-736.html](http://127.0.0.1:8771/poem-736.html), [poem-801.html](http://127.0.0.1:8771/poem-801.html).

### art-archive · Archive

- Caption: Time rests between the pages.
- Roles: poem, section-opening; treatment: paper-edge.
- Find by: history, memories, memory, past, remember, अतीत, इतिहास, याद, स्मृति, ଅତୀତ, ଇତିହାସ, ମନେ ପଡ, ମନେପଡ, ସ୍ମରଣ, ସ୍ମୃତି.
- Delivery: `assets/section-art/archive.webp`.
- [Original master](../artifacts/artwork/masters/section-art/archive.png).
- [Provenance](../records/poem-art-match-evidence.json).
- Used on 49 pages: [archive-2022.html](http://127.0.0.1:8771/archive-2022.html), [archive-2023.html](http://127.0.0.1:8771/archive-2023.html), [archive-2024.html](http://127.0.0.1:8771/archive-2024.html), [archive-2025.html](http://127.0.0.1:8771/archive-2025.html), [archive-2026.html](http://127.0.0.1:8771/archive-2026.html), [archive.html](http://127.0.0.1:8771/archive.html), [poem-155.html](http://127.0.0.1:8771/poem-155.html), [poem-175.html](http://127.0.0.1:8771/poem-175.html), [poem-183.html](http://127.0.0.1:8771/poem-183.html), [poem-25.html](http://127.0.0.1:8771/poem-25.html), [poem-259.html](http://127.0.0.1:8771/poem-259.html), [poem-334.html](http://127.0.0.1:8771/poem-334.html), [poem-342.html](http://127.0.0.1:8771/poem-342.html), [poem-378.html](http://127.0.0.1:8771/poem-378.html), [poem-391.html](http://127.0.0.1:8771/poem-391.html), [poem-394.html](http://127.0.0.1:8771/poem-394.html), [poem-414.html](http://127.0.0.1:8771/poem-414.html), [poem-426.html](http://127.0.0.1:8771/poem-426.html), [poem-437.html](http://127.0.0.1:8771/poem-437.html), [poem-438.html](http://127.0.0.1:8771/poem-438.html), [poem-442.html](http://127.0.0.1:8771/poem-442.html), [poem-450.html](http://127.0.0.1:8771/poem-450.html), [poem-456.html](http://127.0.0.1:8771/poem-456.html), [poem-462.html](http://127.0.0.1:8771/poem-462.html), [poem-502.html](http://127.0.0.1:8771/poem-502.html), [poem-507.html](http://127.0.0.1:8771/poem-507.html), [poem-51.html](http://127.0.0.1:8771/poem-51.html), [poem-567.html](http://127.0.0.1:8771/poem-567.html), [poem-585.html](http://127.0.0.1:8771/poem-585.html), [poem-618.html](http://127.0.0.1:8771/poem-618.html), [poem-619.html](http://127.0.0.1:8771/poem-619.html), [poem-62.html](http://127.0.0.1:8771/poem-62.html), [poem-652.html](http://127.0.0.1:8771/poem-652.html), [poem-656.html](http://127.0.0.1:8771/poem-656.html), [poem-659.html](http://127.0.0.1:8771/poem-659.html), [poem-672.html](http://127.0.0.1:8771/poem-672.html), [poem-69.html](http://127.0.0.1:8771/poem-69.html), [poem-691.html](http://127.0.0.1:8771/poem-691.html), [poem-698.html](http://127.0.0.1:8771/poem-698.html), [poem-708.html](http://127.0.0.1:8771/poem-708.html), [poem-721.html](http://127.0.0.1:8771/poem-721.html), [poem-73.html](http://127.0.0.1:8771/poem-73.html), [poem-734.html](http://127.0.0.1:8771/poem-734.html), [poem-763.html](http://127.0.0.1:8771/poem-763.html), [poem-775.html](http://127.0.0.1:8771/poem-775.html), [poem-785.html](http://127.0.0.1:8771/poem-785.html), [poem-793.html](http://127.0.0.1:8771/poem-793.html), [poem-817.html](http://127.0.0.1:8771/poem-817.html), [poem-86.html](http://127.0.0.1:8771/poem-86.html).

### art-book-reviews · Book Reviews

- Caption: A page waits for the light.
- Roles: poem, section-opening; treatment: paper-edge.
- Find by: book, knowledge, learn, learning, read, school, किताब, ज्ञान, पुस्तक, शिक्षा, स्कूल, ଜ୍ଞାନ, ପୁସ୍ତକ, ବହି, ବିଦ୍ୟାଳୟ, ଶିକ୍ଷା.
- Delivery: `assets/section-art/book-reviews.webp`.
- [Original master](../artifacts/artwork/masters/section-art/book-reviews.png).
- [Provenance](../records/poem-art-match-evidence.json).
- Used on 26 pages: [poem-149.html](http://127.0.0.1:8771/poem-149.html), [poem-170.html](http://127.0.0.1:8771/poem-170.html), [poem-229.html](http://127.0.0.1:8771/poem-229.html), [poem-298.html](http://127.0.0.1:8771/poem-298.html), [poem-336.html](http://127.0.0.1:8771/poem-336.html), [poem-359.html](http://127.0.0.1:8771/poem-359.html), [poem-375.html](http://127.0.0.1:8771/poem-375.html), [poem-407.html](http://127.0.0.1:8771/poem-407.html), [poem-487.html](http://127.0.0.1:8771/poem-487.html), [poem-536.html](http://127.0.0.1:8771/poem-536.html), [poem-579.html](http://127.0.0.1:8771/poem-579.html), [poem-634.html](http://127.0.0.1:8771/poem-634.html), [poem-654.html](http://127.0.0.1:8771/poem-654.html), [poem-667.html](http://127.0.0.1:8771/poem-667.html), [poem-75.html](http://127.0.0.1:8771/poem-75.html), [poem-77.html](http://127.0.0.1:8771/poem-77.html), [review-10.html](http://127.0.0.1:8771/review-10.html), [review-11.html](http://127.0.0.1:8771/review-11.html), [review-4.html](http://127.0.0.1:8771/review-4.html), [review-5.html](http://127.0.0.1:8771/review-5.html), [review-6.html](http://127.0.0.1:8771/review-6.html), [review-7.html](http://127.0.0.1:8771/review-7.html), [review-8.html](http://127.0.0.1:8771/review-8.html), [review-9.html](http://127.0.0.1:8771/review-9.html), [review.html](http://127.0.0.1:8771/review.html), [reviews.html](http://127.0.0.1:8771/reviews.html).

### art-editorial-desk · Editorial Desk

- Caption: The unwritten line is still listening.
- Roles: poem, section-opening; treatment: paper-edge.
- Find by: language, poet, poetry, word, write, writer, writing, written, कवि, कविता, भाषा, लेख, शब्द, କବି, କବିତା, ଭାଷା, ଲେଖ, ଶବ୍ଦ.
- Delivery: `assets/section-art/editorial-desk.webp`.
- [Original master](../artifacts/artwork/masters/section-art/editorial-desk.png).
- [Provenance](../records/poem-art-match-evidence.json).
- Used on 90 pages: [editorial-team.html](http://127.0.0.1:8771/editorial-team.html), [poem-10.html](http://127.0.0.1:8771/poem-10.html), [poem-103.html](http://127.0.0.1:8771/poem-103.html), [poem-104.html](http://127.0.0.1:8771/poem-104.html), [poem-107.html](http://127.0.0.1:8771/poem-107.html), [poem-118.html](http://127.0.0.1:8771/poem-118.html), [poem-126.html](http://127.0.0.1:8771/poem-126.html), [poem-133.html](http://127.0.0.1:8771/poem-133.html), [poem-134.html](http://127.0.0.1:8771/poem-134.html), [poem-136.html](http://127.0.0.1:8771/poem-136.html), [poem-148.html](http://127.0.0.1:8771/poem-148.html), [poem-165.html](http://127.0.0.1:8771/poem-165.html), [poem-181.html](http://127.0.0.1:8771/poem-181.html), [poem-189.html](http://127.0.0.1:8771/poem-189.html), [poem-196.html](http://127.0.0.1:8771/poem-196.html), [poem-198.html](http://127.0.0.1:8771/poem-198.html), [poem-20.html](http://127.0.0.1:8771/poem-20.html), [poem-202.html](http://127.0.0.1:8771/poem-202.html), [poem-208.html](http://127.0.0.1:8771/poem-208.html), [poem-22.html](http://127.0.0.1:8771/poem-22.html), [poem-228.html](http://127.0.0.1:8771/poem-228.html), [poem-231.html](http://127.0.0.1:8771/poem-231.html), [poem-236.html](http://127.0.0.1:8771/poem-236.html), [poem-245.html](http://127.0.0.1:8771/poem-245.html), [poem-251.html](http://127.0.0.1:8771/poem-251.html), [poem-263.html](http://127.0.0.1:8771/poem-263.html), [poem-27.html](http://127.0.0.1:8771/poem-27.html), [poem-28.html](http://127.0.0.1:8771/poem-28.html), [poem-294.html](http://127.0.0.1:8771/poem-294.html), [poem-297.html](http://127.0.0.1:8771/poem-297.html), [poem-304.html](http://127.0.0.1:8771/poem-304.html), [poem-305.html](http://127.0.0.1:8771/poem-305.html), [poem-308.html](http://127.0.0.1:8771/poem-308.html), [poem-31.html](http://127.0.0.1:8771/poem-31.html), [poem-312.html](http://127.0.0.1:8771/poem-312.html), [poem-317.html](http://127.0.0.1:8771/poem-317.html), [poem-318.html](http://127.0.0.1:8771/poem-318.html), [poem-329.html](http://127.0.0.1:8771/poem-329.html), [poem-347.html](http://127.0.0.1:8771/poem-347.html), [poem-35.html](http://127.0.0.1:8771/poem-35.html), [poem-354.html](http://127.0.0.1:8771/poem-354.html), [poem-369.html](http://127.0.0.1:8771/poem-369.html), [poem-37.html](http://127.0.0.1:8771/poem-37.html), [poem-387.html](http://127.0.0.1:8771/poem-387.html), [poem-395.html](http://127.0.0.1:8771/poem-395.html), [poem-402.html](http://127.0.0.1:8771/poem-402.html), [poem-409.html](http://127.0.0.1:8771/poem-409.html), [poem-411.html](http://127.0.0.1:8771/poem-411.html), [poem-431.html](http://127.0.0.1:8771/poem-431.html), [poem-457.html](http://127.0.0.1:8771/poem-457.html), [poem-459.html](http://127.0.0.1:8771/poem-459.html), [poem-464.html](http://127.0.0.1:8771/poem-464.html), [poem-466.html](http://127.0.0.1:8771/poem-466.html), [poem-467.html](http://127.0.0.1:8771/poem-467.html), [poem-470.html](http://127.0.0.1:8771/poem-470.html), [poem-477.html](http://127.0.0.1:8771/poem-477.html), [poem-497.html](http://127.0.0.1:8771/poem-497.html), [poem-519.html](http://127.0.0.1:8771/poem-519.html), [poem-535.html](http://127.0.0.1:8771/poem-535.html), [poem-542.html](http://127.0.0.1:8771/poem-542.html), [poem-550.html](http://127.0.0.1:8771/poem-550.html), [poem-556.html](http://127.0.0.1:8771/poem-556.html), [poem-558.html](http://127.0.0.1:8771/poem-558.html), [poem-560.html](http://127.0.0.1:8771/poem-560.html), [poem-565.html](http://127.0.0.1:8771/poem-565.html), [poem-599.html](http://127.0.0.1:8771/poem-599.html), [poem-604.html](http://127.0.0.1:8771/poem-604.html), [poem-606.html](http://127.0.0.1:8771/poem-606.html), [poem-608.html](http://127.0.0.1:8771/poem-608.html), [poem-609.html](http://127.0.0.1:8771/poem-609.html), [poem-61.html](http://127.0.0.1:8771/poem-61.html), [poem-624.html](http://127.0.0.1:8771/poem-624.html), [poem-632.html](http://127.0.0.1:8771/poem-632.html), [poem-644.html](http://127.0.0.1:8771/poem-644.html), [poem-660.html](http://127.0.0.1:8771/poem-660.html), [poem-682.html](http://127.0.0.1:8771/poem-682.html), [poem-689.html](http://127.0.0.1:8771/poem-689.html), [poem-705.html](http://127.0.0.1:8771/poem-705.html), [poem-724.html](http://127.0.0.1:8771/poem-724.html), [poem-744.html](http://127.0.0.1:8771/poem-744.html), [poem-748.html](http://127.0.0.1:8771/poem-748.html), [poem-752.html](http://127.0.0.1:8771/poem-752.html), [poem-758.html](http://127.0.0.1:8771/poem-758.html), [poem-774.html](http://127.0.0.1:8771/poem-774.html), [poem-778.html](http://127.0.0.1:8771/poem-778.html), [poem-784.html](http://127.0.0.1:8771/poem-784.html), [poem-79.html](http://127.0.0.1:8771/poem-79.html), [poem-91.html](http://127.0.0.1:8771/poem-91.html), [poem-96.html](http://127.0.0.1:8771/poem-96.html), [poem-97.html](http://127.0.0.1:8771/poem-97.html).

### art-next-issue · Next Issue

- Caption: A leaf opens beside a page.
- Roles: poem, section-opening; treatment: paper-edge.
- Find by: beginning, future, hope, new life, renewal, tomorrow, आशा, उम्मीद, नया, भविष्य, शुरुआत, ଆଗାମୀ, ଆରମ୍ଭ, ଆଶା, ନୂଆ, ନୂତନ, ଭବିଷ୍ୟ, ସମ୍ଭାବନା.
- Delivery: `assets/section-art/next-issue.webp`.
- [Original master](../artifacts/artwork/masters/section-art/next-issue.png).
- [Provenance](../records/poem-art-match-evidence.json).
- Used on 23 pages: [poem-102.html](http://127.0.0.1:8771/poem-102.html), [poem-105.html](http://127.0.0.1:8771/poem-105.html), [poem-161.html](http://127.0.0.1:8771/poem-161.html), [poem-177.html](http://127.0.0.1:8771/poem-177.html), [poem-247.html](http://127.0.0.1:8771/poem-247.html), [poem-264.html](http://127.0.0.1:8771/poem-264.html), [poem-282.html](http://127.0.0.1:8771/poem-282.html), [poem-357.html](http://127.0.0.1:8771/poem-357.html), [poem-358.html](http://127.0.0.1:8771/poem-358.html), [poem-38.html](http://127.0.0.1:8771/poem-38.html), [poem-39.html](http://127.0.0.1:8771/poem-39.html), [poem-396.html](http://127.0.0.1:8771/poem-396.html), [poem-44.html](http://127.0.0.1:8771/poem-44.html), [poem-451.html](http://127.0.0.1:8771/poem-451.html), [poem-454.html](http://127.0.0.1:8771/poem-454.html), [poem-524.html](http://127.0.0.1:8771/poem-524.html), [poem-716.html](http://127.0.0.1:8771/poem-716.html), [poem-731.html](http://127.0.0.1:8771/poem-731.html), [poem-773.html](http://127.0.0.1:8771/poem-773.html), [poem-795.html](http://127.0.0.1:8771/poem-795.html), [poem-799.html](http://127.0.0.1:8771/poem-799.html), [poem-92.html](http://127.0.0.1:8771/poem-92.html), [upcoming.html](http://127.0.0.1:8771/upcoming.html).

### art-search · Search

- Caption: Beyond the window, an open horizon.
- Roles: poem, section-opening; treatment: paper-edge.
- Find by: dream, fly, free, freedom, horizon, liberty, sky, wing, आकाश, आजादी, उड़, पंख, मुक्ति, सपना, स्वप्न, ଆକାଶ, ଉଡ଼, ଉଡି, ଦିଗନ୍ତ, ମୁକ୍ତି, ସ୍ବପ୍ନ, ସ୍ବାଧୀନ, ସ୍ୱପ୍ନ, ସ୍ୱାଧୀନ.
- Delivery: `assets/section-art/search.webp`.
- [Original master](../artifacts/artwork/masters/section-art/search.png).
- [Provenance](../records/poem-art-match-evidence.json).
- Used on 104 pages: [poem-100.html](http://127.0.0.1:8771/poem-100.html), [poem-101.html](http://127.0.0.1:8771/poem-101.html), [poem-112.html](http://127.0.0.1:8771/poem-112.html), [poem-119.html](http://127.0.0.1:8771/poem-119.html), [poem-120.html](http://127.0.0.1:8771/poem-120.html), [poem-171.html](http://127.0.0.1:8771/poem-171.html), [poem-174.html](http://127.0.0.1:8771/poem-174.html), [poem-186.html](http://127.0.0.1:8771/poem-186.html), [poem-199.html](http://127.0.0.1:8771/poem-199.html), [poem-205.html](http://127.0.0.1:8771/poem-205.html), [poem-21.html](http://127.0.0.1:8771/poem-21.html), [poem-214.html](http://127.0.0.1:8771/poem-214.html), [poem-221.html](http://127.0.0.1:8771/poem-221.html), [poem-224.html](http://127.0.0.1:8771/poem-224.html), [poem-23.html](http://127.0.0.1:8771/poem-23.html), [poem-232.html](http://127.0.0.1:8771/poem-232.html), [poem-235.html](http://127.0.0.1:8771/poem-235.html), [poem-239.html](http://127.0.0.1:8771/poem-239.html), [poem-24.html](http://127.0.0.1:8771/poem-24.html), [poem-241.html](http://127.0.0.1:8771/poem-241.html), [poem-274.html](http://127.0.0.1:8771/poem-274.html), [poem-276.html](http://127.0.0.1:8771/poem-276.html), [poem-283.html](http://127.0.0.1:8771/poem-283.html), [poem-284.html](http://127.0.0.1:8771/poem-284.html), [poem-288.html](http://127.0.0.1:8771/poem-288.html), [poem-300.html](http://127.0.0.1:8771/poem-300.html), [poem-301.html](http://127.0.0.1:8771/poem-301.html), [poem-327.html](http://127.0.0.1:8771/poem-327.html), [poem-341.html](http://127.0.0.1:8771/poem-341.html), [poem-351.html](http://127.0.0.1:8771/poem-351.html), [poem-353.html](http://127.0.0.1:8771/poem-353.html), [poem-366.html](http://127.0.0.1:8771/poem-366.html), [poem-371.html](http://127.0.0.1:8771/poem-371.html), [poem-377.html](http://127.0.0.1:8771/poem-377.html), [poem-383.html](http://127.0.0.1:8771/poem-383.html), [poem-386.html](http://127.0.0.1:8771/poem-386.html), [poem-399.html](http://127.0.0.1:8771/poem-399.html), [poem-405.html](http://127.0.0.1:8771/poem-405.html), [poem-41.html](http://127.0.0.1:8771/poem-41.html), [poem-419.html](http://127.0.0.1:8771/poem-419.html), [poem-422.html](http://127.0.0.1:8771/poem-422.html), [poem-429.html](http://127.0.0.1:8771/poem-429.html), [poem-434.html](http://127.0.0.1:8771/poem-434.html), [poem-443.html](http://127.0.0.1:8771/poem-443.html), [poem-455.html](http://127.0.0.1:8771/poem-455.html), [poem-458.html](http://127.0.0.1:8771/poem-458.html), [poem-473.html](http://127.0.0.1:8771/poem-473.html), [poem-476.html](http://127.0.0.1:8771/poem-476.html), [poem-479.html](http://127.0.0.1:8771/poem-479.html), [poem-488.html](http://127.0.0.1:8771/poem-488.html), [poem-490.html](http://127.0.0.1:8771/poem-490.html), [poem-499.html](http://127.0.0.1:8771/poem-499.html), [poem-503.html](http://127.0.0.1:8771/poem-503.html), [poem-509.html](http://127.0.0.1:8771/poem-509.html), [poem-52.html](http://127.0.0.1:8771/poem-52.html), [poem-522.html](http://127.0.0.1:8771/poem-522.html), [poem-525.html](http://127.0.0.1:8771/poem-525.html), [poem-527.html](http://127.0.0.1:8771/poem-527.html), [poem-533.html](http://127.0.0.1:8771/poem-533.html), [poem-537.html](http://127.0.0.1:8771/poem-537.html), [poem-543.html](http://127.0.0.1:8771/poem-543.html), [poem-544.html](http://127.0.0.1:8771/poem-544.html), [poem-56.html](http://127.0.0.1:8771/poem-56.html), [poem-561.html](http://127.0.0.1:8771/poem-561.html), [poem-564.html](http://127.0.0.1:8771/poem-564.html), [poem-572.html](http://127.0.0.1:8771/poem-572.html), [poem-602.html](http://127.0.0.1:8771/poem-602.html), [poem-649.html](http://127.0.0.1:8771/poem-649.html), [poem-653.html](http://127.0.0.1:8771/poem-653.html), [poem-66.html](http://127.0.0.1:8771/poem-66.html), [poem-662.html](http://127.0.0.1:8771/poem-662.html), [poem-663.html](http://127.0.0.1:8771/poem-663.html), [poem-673.html](http://127.0.0.1:8771/poem-673.html), [poem-684.html](http://127.0.0.1:8771/poem-684.html), [poem-694.html](http://127.0.0.1:8771/poem-694.html), [poem-703.html](http://127.0.0.1:8771/poem-703.html), [poem-71.html](http://127.0.0.1:8771/poem-71.html), [poem-710.html](http://127.0.0.1:8771/poem-710.html), [poem-717.html](http://127.0.0.1:8771/poem-717.html), [poem-725.html](http://127.0.0.1:8771/poem-725.html), [poem-733.html](http://127.0.0.1:8771/poem-733.html), [poem-74.html](http://127.0.0.1:8771/poem-74.html), [poem-746.html](http://127.0.0.1:8771/poem-746.html), [poem-747.html](http://127.0.0.1:8771/poem-747.html), [poem-749.html](http://127.0.0.1:8771/poem-749.html), [poem-754.html](http://127.0.0.1:8771/poem-754.html), [poem-756.html](http://127.0.0.1:8771/poem-756.html), [poem-759.html](http://127.0.0.1:8771/poem-759.html), [poem-760.html](http://127.0.0.1:8771/poem-760.html), [poem-769.html](http://127.0.0.1:8771/poem-769.html), [poem-772.html](http://127.0.0.1:8771/poem-772.html), [poem-78.html](http://127.0.0.1:8771/poem-78.html), [poem-780.html](http://127.0.0.1:8771/poem-780.html), [poem-781.html](http://127.0.0.1:8771/poem-781.html), [poem-788.html](http://127.0.0.1:8771/poem-788.html), [poem-797.html](http://127.0.0.1:8771/poem-797.html), [poem-804.html](http://127.0.0.1:8771/poem-804.html), [poem-819.html](http://127.0.0.1:8771/poem-819.html), [poem-82.html](http://127.0.0.1:8771/poem-82.html), [poem-87.html](http://127.0.0.1:8771/poem-87.html), [poem-88.html](http://127.0.0.1:8771/poem-88.html), [poem-93.html](http://127.0.0.1:8771/poem-93.html), [poem-99.html](http://127.0.0.1:8771/poem-99.html), [search.html](http://127.0.0.1:8771/search.html).

### art-send-a-poem · Send A Poem

- Caption: A quiet page, ready for a voice.
- Roles: poem, section-opening; treatment: paper-edge.
- Find by: ink, page, paper, pen, कलम, कागज, पन्ना, स्याही, କଲମ, କାଗଜ, କାଳି, ପୃଷ୍ଠା, ମସି.
- Delivery: `assets/section-art/send-a-poem.webp`.
- [Original master](../artifacts/artwork/masters/section-art/send-a-poem.png).
- [Provenance](../records/poem-art-match-evidence.json).
- Used on 27 pages: [poem-109.html](http://127.0.0.1:8771/poem-109.html), [poem-129.html](http://127.0.0.1:8771/poem-129.html), [poem-146.html](http://127.0.0.1:8771/poem-146.html), [poem-173.html](http://127.0.0.1:8771/poem-173.html), [poem-206.html](http://127.0.0.1:8771/poem-206.html), [poem-217.html](http://127.0.0.1:8771/poem-217.html), [poem-271.html](http://127.0.0.1:8771/poem-271.html), [poem-314.html](http://127.0.0.1:8771/poem-314.html), [poem-339.html](http://127.0.0.1:8771/poem-339.html), [poem-368.html](http://127.0.0.1:8771/poem-368.html), [poem-496.html](http://127.0.0.1:8771/poem-496.html), [poem-520.html](http://127.0.0.1:8771/poem-520.html), [poem-549.html](http://127.0.0.1:8771/poem-549.html), [poem-589.html](http://127.0.0.1:8771/poem-589.html), [poem-626.html](http://127.0.0.1:8771/poem-626.html), [poem-640.html](http://127.0.0.1:8771/poem-640.html), [poem-658.html](http://127.0.0.1:8771/poem-658.html), [poem-664.html](http://127.0.0.1:8771/poem-664.html), [poem-677.html](http://127.0.0.1:8771/poem-677.html), [poem-686.html](http://127.0.0.1:8771/poem-686.html), [poem-692.html](http://127.0.0.1:8771/poem-692.html), [poem-751.html](http://127.0.0.1:8771/poem-751.html), [poem-768.html](http://127.0.0.1:8771/poem-768.html), [poem-805.html](http://127.0.0.1:8771/poem-805.html), [poem-821.html](http://127.0.0.1:8771/poem-821.html), [poem-89.html](http://127.0.0.1:8771/poem-89.html), [submit.html](http://127.0.0.1:8771/submit.html).

### art-dokana · Dokana

- Caption: A closed doorway. Rain holds the silence.
- Roles: poem; treatment: framed.
- Find by: dokana, rain.
- Delivery: `assets/poem-art/dokana.webp`.
- [Original master](../artifacts/artwork/masters/poem-art/dokana.png).
- [Provenance](../records/poem-reader-a-approval.json).
- Used on 1 pages: [poem-dokana.html](http://127.0.0.1:8771/poem-dokana.html).

### art-kshanika · Kshanika

- Caption: An empty platform, waiting with the rain.
- Roles: poem; treatment: framed.
- Find by: kshanika, rain.
- Delivery: `assets/poem-art/kshanika.webp`.
- [Original master](../artifacts/artwork/masters/poem-art/kshanika.png).
- [Provenance](../records/poem-reader-a-approval.json).
- Used on 1 pages: [poem-kshanika.html](http://127.0.0.1:8771/poem-kshanika.html).

### art-drink · Drink

- Caption: A cup by the window; the night gathers on the water.
- Roles: poem; treatment: framed.
- Find by: drink, evening.
- Delivery: `assets/poem-art/drink.webp`.
- [Original master](../artifacts/artwork/masters/poem-art/drink.png).
- [Provenance](../records/poem-reader-a-approval.json).
- Used on 1 pages: [poem-drink.html](http://127.0.0.1:8771/poem-drink.html).

### cover-047 · After the rain

- Caption: Everyday Odisha: rain, earthen courtyards and the sensory memory of home.
- Roles: edition-cover; treatment: framed.
- Find by: Weather / renewal, September 2026, edition 47.
- Delivery: `assets/covers/editions/edition-047-2026-09.webp`.
- [Original master](../artifacts/artwork/masters/covers/by-edition/edition-047-2026-09.png).
- [Provenance](../records/edition-cover-filenames.json).
- Used on 4 pages: [archive-2026.html](http://127.0.0.1:8771/archive-2026.html), [archive.html](http://127.0.0.1:8771/archive.html), [index.html](http://127.0.0.1:8771/index.html), [issue-47.html](http://127.0.0.1:8771/issue-47.html).

### cover-046 · The colour before the story

- Caption: Raghurajpur is known for pattachitra, a painting tradition on prepared cloth. This is an imagined workshop and an original border study.
- Roles: edition-cover; treatment: framed.
- Find by: Craft / attention, August 2026, edition 46.
- Delivery: `assets/covers/editions/edition-046-2026-08.webp`.
- [Original master](../artifacts/artwork/masters/covers/by-edition/edition-046-2026-08.png).
- [Provenance](../records/edition-cover-filenames.json).
- Used on 4 pages: [archive-2026.html](http://127.0.0.1:8771/archive-2026.html), [archive.html](http://127.0.0.1:8771/archive.html), [index.html](http://127.0.0.1:8771/index.html), [issue-46.html](http://127.0.0.1:8771/issue-46.html).

### cover-045 · Evening on the water

- Caption: Odisha's lagoon landscapes and fishing livelihoods; an imagined waterside scene, not an identified boat or community.
- Roles: edition-cover; treatment: framed.
- Find by: Water / rest, July 2026, edition 45.
- Delivery: `assets/covers/editions/edition-045-2026-07.webp`.
- [Original master](../artifacts/artwork/masters/covers/by-edition/edition-045-2026-07.png).
- [Provenance](../records/edition-cover-filenames.json).
- Used on 4 pages: [archive-2026.html](http://127.0.0.1:8771/archive-2026.html), [archive.html](http://127.0.0.1:8771/archive.html), [index.html](http://127.0.0.1:8771/index.html), [issue-45.html](http://127.0.0.1:8771/issue-45.html).

### cover-044 · A threshold in rain

- Caption: Jhoti and chita provide the visual reference: restrained white threshold drawing within an imagined earthen home.
- Roles: edition-cover; treatment: framed.
- Find by: Home / welcome, June 2026, edition 44.
- Delivery: `assets/covers/editions/edition-044-2026-06.webp`.
- [Original master](../artifacts/artwork/masters/covers/by-edition/edition-044-2026-06.png).
- [Provenance](../records/edition-cover-filenames.json).
- Used on 3 pages: [archive-2026.html](http://127.0.0.1:8771/archive-2026.html), [archive.html](http://127.0.0.1:8771/archive.html), [issue-44.html](http://127.0.0.1:8771/issue-44.html).

### cover-043 · Room for water

- Caption: Everyday earthenware and the labour of pottery; no specific craft cluster is claimed for this imagined scene.
- Roles: edition-cover; treatment: framed.
- Find by: Craft / possibility, May 2026, edition 43.
- Delivery: `assets/covers/editions/edition-043-2026-05.webp`.
- [Original master](../artifacts/artwork/masters/covers/by-edition/edition-043-2026-05.png).
- [Provenance](../records/edition-cover-filenames.json).
- Used on 3 pages: [archive-2026.html](http://127.0.0.1:8771/archive-2026.html), [archive.html](http://127.0.0.1:8771/archive.html), [issue-43.html](http://127.0.0.1:8771/issue-43.html).

### cover-042 · The wind reads first

- Caption: Odisha's coastal landscape, interpreted through casuarina, sand and sea air.
- Roles: edition-cover; treatment: framed.
- Find by: Coast / listening, April 2026, edition 42.
- Delivery: `assets/covers/editions/edition-042-2026-04.webp`.
- [Original master](../artifacts/artwork/masters/covers/by-edition/edition-042-2026-04.png).
- [Provenance](../records/edition-cover-filenames.json).
- Used on 3 pages: [archive-2026.html](http://127.0.0.1:8771/archive-2026.html), [archive.html](http://127.0.0.1:8771/archive.html), [issue-42.html](http://127.0.0.1:8771/issue-42.html).

### cover-041 · A small red insistence

- Caption: Palash provides the botanical and seasonal starting point; the emotional reading is original.
- Roles: edition-cover; treatment: framed.
- Find by: Flora / resilience, March 2026, edition 41.
- Delivery: `assets/covers/editions/edition-041-2026-03.webp`.
- [Original master](../artifacts/artwork/masters/covers/by-edition/edition-041-2026-03.png).
- [Provenance](../records/edition-cover-filenames.json).
- Used on 3 pages: [archive-2026.html](http://127.0.0.1:8771/archive-2026.html), [archive.html](http://127.0.0.1:8771/archive.html), [issue-41.html](http://127.0.0.1:8771/issue-41.html).

### cover-040 · The loom remembers a voice

- Caption: An imaginative homage to Gangadhar Meher, the Odia poet born into a weaver family in Barpali. This is not his documented loom or workshop.
- Roles: edition-cover; treatment: framed.
- Find by: Literature / labour, February 2026, edition 40.
- Delivery: `assets/covers/editions/edition-040-2026-02.webp`.
- [Original master](../artifacts/artwork/masters/covers/by-edition/edition-040-2026-02.png).
- [Provenance](../records/edition-cover-filenames.json).
- Used on 3 pages: [archive-2026.html](http://127.0.0.1:8771/archive-2026.html), [archive.html](http://127.0.0.1:8771/archive.html), [issue-40.html](http://127.0.0.1:8771/issue-40.html).

### cover-039 · Before the field wakes

- Caption: Rice cultivation and rural mornings in Odisha; an imagined field, without assigning it to a named village.
- Roles: edition-cover; treatment: framed.
- Find by: Agrarian / stillness, January 2026, edition 39.
- Delivery: `assets/covers/editions/edition-039-2026-01.webp`.
- [Original master](../artifacts/artwork/masters/covers/by-edition/edition-039-2026-01.png).
- [Provenance](../records/edition-cover-filenames.json).
- Used on 3 pages: [archive-2026.html](http://127.0.0.1:8771/archive-2026.html), [archive.html](http://127.0.0.1:8771/archive.html), [issue-39.html](http://127.0.0.1:8771/issue-39.html).

### cover-038 · Enough light for one room

- Caption: An everyday earthen oil lamp, approached through intimacy rather than a claim about a particular ceremony.
- Roles: edition-cover; treatment: framed.
- Find by: Home / tenderness, December 2025, edition 38.
- Delivery: `assets/covers/editions/edition-038-2025-12.webp`.
- [Original master](../artifacts/artwork/masters/covers/by-edition/edition-038-2025-12.png).
- [Provenance](../records/edition-cover-filenames.json).
- Used on 3 pages: [archive-2025.html](http://127.0.0.1:8771/archive-2025.html), [archive.html](http://127.0.0.1:8771/archive.html), [issue-38.html](http://127.0.0.1:8771/issue-38.html).

### cover-037 · A boat for remembering

- Caption: A poetic reference to Kartika boat-floating traditions in Odisha; an imagined contemporary paper boat, not a reconstruction of an ancient vessel.
- Roles: edition-cover; treatment: framed.
- Find by: Living culture / passage, November 2025, edition 37.
- Delivery: `assets/covers/editions/edition-037-2025-11.webp`.
- [Original master](../artifacts/artwork/masters/covers/by-edition/edition-037-2025-11.png).
- [Provenance](../records/edition-cover-filenames.json).
- Used on 3 pages: [archive-2025.html](http://127.0.0.1:8771/archive-2025.html), [archive.html](http://127.0.0.1:8771/archive.html), [issue-37.html](http://127.0.0.1:8771/issue-37.html).

### cover-036 · The season in white

- Caption: Kans grass and the changing seasonal landscape; no single festival is asserted by the image.
- Roles: edition-cover; treatment: framed.
- Find by: Season / change, October 2025, edition 36.
- Delivery: `assets/covers/editions/edition-036-2025-10.webp`.
- [Original master](../artifacts/artwork/masters/covers/by-edition/edition-036-2025-10.png).
- [Provenance](../records/edition-cover-filenames.json).
- Used on 3 pages: [archive-2025.html](http://127.0.0.1:8771/archive-2025.html), [archive.html](http://127.0.0.1:8771/archive.html), [issue-36.html](http://127.0.0.1:8771/issue-36.html).

### cover-035 · Not yet a flower

- Caption: Lotus and pond life, familiar across Odisha and beyond; the narrative concerns anticipation rather than ritual symbolism.
- Roles: edition-cover; treatment: framed.
- Find by: Water / anticipation, September 2025, edition 35.
- Delivery: `assets/covers/editions/edition-035-2025-09.webp`.
- [Original master](../artifacts/artwork/masters/covers/by-edition/edition-035-2025-09.png).
- [Provenance](../records/edition-cover-filenames.json).
- Used on 3 pages: [archive-2025.html](http://127.0.0.1:8771/archive-2025.html), [archive.html](http://127.0.0.1:8771/archive.html), [issue-35.html](http://127.0.0.1:8771/issue-35.html).

### cover-034 · Rain on the tiles

- Caption: Terracotta roof tiles and a sheltered courtyard offer a study of everyday domestic architecture in Odisha.
- Roles: edition-cover; treatment: framed.
- Find by: Architecture / shelter, August 2025, edition 34.
- Delivery: `assets/covers/editions/edition-034-2025-08.webp`.
- [Original master](../artifacts/artwork/masters/covers/by-edition/edition-034-2025-08.png).
- [Provenance](../records/edition-cover-filenames.json).
- Used on 3 pages: [archive-2025.html](http://127.0.0.1:8771/archive-2025.html), [archive.html](http://127.0.0.1:8771/archive.html), [issue-34.html](http://127.0.0.1:8771/issue-34.html).

### cover-033 · The bowl holds a note

- Caption: Kantilo has a brass and bell-metal craft tradition. This concept specifically concerns kansa, bell-metal, rather than treating all yellow metals as interchangeable.
- Roles: edition-cover; treatment: framed.
- Find by: Craft / resonance, July 2025, edition 33.
- Delivery: `assets/covers/editions/edition-033-2025-07.webp`.
- [Original master](../artifacts/artwork/masters/covers/by-edition/edition-033-2025-07.png).
- [Provenance](../records/edition-cover-filenames.json).
- Used on 3 pages: [archive-2025.html](http://127.0.0.1:8771/archive-2025.html), [archive.html](http://127.0.0.1:8771/archive.html), [issue-33.html](http://127.0.0.1:8771/issue-33.html).

### cover-032 · When the lane turns fragrant

- Caption: The scent of rain on earth anchors the brand's ମାଟିର ମହକ theme through everyday experience.
- Roles: edition-cover; treatment: framed.
- Find by: Weather / arrival, June 2025, edition 32.
- Delivery: `assets/covers/editions/edition-032-2025-06.webp`.
- [Original master](../artifacts/artwork/masters/covers/by-edition/edition-032-2025-06.png).
- [Provenance](../records/edition-cover-filenames.json).
- Used on 3 pages: [archive-2025.html](http://127.0.0.1:8771/archive-2025.html), [archive.html](http://127.0.0.1:8771/archive.html), [issue-32.html](http://127.0.0.1:8771/issue-32.html).

### cover-031 · Summer, carried home

- Caption: Mango season and the everyday culture of bringing food home; no named cultivar or local origin is claimed.
- Roles: edition-cover; treatment: framed.
- Find by: Food / abundance, May 2025, edition 31.
- Delivery: `assets/covers/editions/edition-031-2025-05.webp`.
- [Original master](../artifacts/artwork/masters/covers/by-edition/edition-031-2025-05.png).
- [Provenance](../records/edition-cover-filenames.json).
- Used on 3 pages: [archive-2025.html](http://127.0.0.1:8771/archive-2025.html), [archive.html](http://127.0.0.1:8771/archive.html), [issue-31.html](http://127.0.0.1:8771/issue-31.html).

### cover-030 · Salt in the cotton

- Caption: Puri gamucha is the user's everyday cultural reference. This imagined cotton cloth is not presented as a certified weave, temple-issued cloth or prescribed ritual garment.
- Roles: edition-cover; treatment: framed.
- Find by: Textile / everyday life, April 2025, edition 30.
- Delivery: `assets/covers/editions/edition-030-2025-04.webp`.
- [Original master](../artifacts/artwork/masters/covers/by-edition/edition-030-2025-04.png).
- [Provenance](../records/edition-cover-filenames.json).
- Used on 3 pages: [archive-2025.html](http://127.0.0.1:8771/archive-2025.html), [archive.html](http://127.0.0.1:8771/archive.html), [issue-30.html](http://127.0.0.1:8771/issue-30.html).

### cover-029 · What the woodland holds

- Caption: Kendu woodland generally, as clarified by the user. Kendu leaves are an important forest produce and livelihood connection in Odisha; no particular forest or community is depicted.
- Roles: edition-cover; treatment: framed.
- Find by: Ecology / belonging, March 2025, edition 29.
- Delivery: `assets/covers/editions/edition-029-2025-03.webp`.
- [Original master](../artifacts/artwork/masters/covers/by-edition/edition-029-2025-03.png).
- [Provenance](../records/edition-cover-filenames.json).
- Used on 3 pages: [archive-2025.html](http://127.0.0.1:8771/archive-2025.html), [archive.html](http://127.0.0.1:8771/archive.html), [issue-29.html](http://127.0.0.1:8771/issue-29.html).

### cover-028 · The sari keeps the river

- Caption: Sambalpuri bandha is a tie-and-dye weaving tradition. This is generated textile interpretation, not an authenticated artisan sample or evidence of a particular motif's meaning.
- Roles: edition-cover; treatment: framed.
- Find by: Textile / memory, February 2025, edition 28.
- Delivery: `assets/covers/editions/edition-028-2025-02.webp`.
- [Original master](../artifacts/artwork/masters/covers/by-edition/edition-028-2025-02.png).
- [Provenance](../records/edition-cover-filenames.json).
- Used on 3 pages: [archive-2025.html](http://127.0.0.1:8771/archive-2025.html), [archive.html](http://127.0.0.1:8771/archive.html), [issue-28.html](http://127.0.0.1:8771/issue-28.html).

### cover-027 · The net before morning

- Caption: Coastal fishing work provides the setting; the scene avoids assigning a livelihood or identity to an invented named community.
- Roles: edition-cover; treatment: framed.
- Find by: Livelihood / preparation, January 2025, edition 27.
- Delivery: `assets/covers/editions/edition-027-2025-01.webp`.
- [Original master](../artifacts/artwork/masters/covers/by-edition/edition-027-2025-01.png).
- [Provenance](../records/edition-cover-filenames.json).
- Used on 3 pages: [archive-2025.html](http://127.0.0.1:8771/archive-2025.html), [archive.html](http://127.0.0.1:8771/archive.html), [issue-27.html](http://127.0.0.1:8771/issue-27.html).

### cover-026 · The warmth that stays

- Caption: The hearth and earthen kitchen express domestic memory; warmth is the subject, without idealising the burdens of cooking or fuel collection.
- Roles: edition-cover; treatment: framed.
- Find by: Home / continuity, December 2024, edition 26.
- Delivery: `assets/covers/editions/edition-026-2024-12.webp`.
- [Original master](../artifacts/artwork/masters/covers/by-edition/edition-026-2024-12.png).
- [Provenance](../records/edition-cover-filenames.json).
- Used on 3 pages: [archive-2024.html](http://127.0.0.1:8771/archive-2024.html), [archive.html](http://127.0.0.1:8771/archive.html), [issue-26.html](http://127.0.0.1:8771/issue-26.html).

### cover-025 · Steps down to the day

- Caption: River steps and water-carrying as an imagined everyday setting; no particular ghat or ritual is identified.
- Roles: edition-cover; treatment: framed.
- Find by: River / routine, November 2024, edition 25.
- Delivery: `assets/covers/editions/edition-025-2024-11.webp`.
- [Original master](../artifacts/artwork/masters/covers/by-edition/edition-025-2024-11.png).
- [Provenance](../records/edition-cover-filenames.json).
- Used on 3 pages: [archive-2024.html](http://127.0.0.1:8771/archive-2024.html), [archive.html](http://127.0.0.1:8771/archive.html), [issue-25.html](http://127.0.0.1:8771/issue-25.html).

### cover-024 · One flower after another

- Caption: Flower-threading and everyday acts of welcome and offering; no specific festival or sacred obligation is asserted.
- Roles: edition-cover; treatment: framed.
- Find by: Living culture / care, October 2024, edition 24.
- Delivery: `assets/covers/editions/edition-024-2024-10.webp`.
- [Original master](../artifacts/artwork/masters/covers/by-edition/edition-024-2024-10.png).
- [Provenance](../records/edition-cover-filenames.json).
- Used on 3 pages: [archive-2024.html](http://127.0.0.1:8771/archive-2024.html), [archive.html](http://127.0.0.1:8771/archive.html), [issue-24.html](http://127.0.0.1:8771/issue-24.html).

### cover-023 · The sky comes to the field

- Caption: Flooded paddy fields provide the Odisha agrarian reference; this is an imagined scene, not a record of a particular farm.
- Roles: edition-cover; treatment: framed.
- Find by: Agrarian / reflection, September 2024, edition 23.
- Delivery: `assets/covers/editions/edition-023-2024-09.webp`.
- [Original master](../artifacts/artwork/masters/covers/by-edition/edition-023-2024-09.png).
- [Provenance](../records/edition-cover-filenames.json).
- Used on 3 pages: [archive-2024.html](http://127.0.0.1:8771/archive-2024.html), [archive.html](http://127.0.0.1:8771/archive.html), [issue-23.html](http://127.0.0.1:8771/issue-23.html).

### cover-022 · Someone will be back

- Caption: A bicycle and a lived-in wall suggest everyday mobility and neighbourhood life, without turning poverty or age into decoration.
- Roles: edition-cover; treatment: framed.
- Find by: Everyday life / absence, August 2024, edition 22.
- Delivery: `assets/covers/editions/edition-022-2024-08.webp`.
- [Original master](../artifacts/artwork/masters/covers/by-edition/edition-022-2024-08.png).
- [Provenance](../records/edition-cover-filenames.json).
- Used on 3 pages: [archive-2024.html](http://127.0.0.1:8771/archive-2024.html), [archive.html](http://127.0.0.1:8771/archive.html), [issue-22.html](http://127.0.0.1:8771/issue-22.html).

### cover-021 · The leaf lets go

- Caption: A banana leaf after rainfall; a close natural study linked to gardens and familiar household landscapes.
- Roles: edition-cover; treatment: framed.
- Find by: Flora / release, July 2024, edition 21.
- Delivery: `assets/covers/editions/edition-021-2024-07.webp`.
- [Original master](../artifacts/artwork/masters/covers/by-edition/edition-021-2024-07.png).
- [Provenance](../records/edition-cover-filenames.json).
- Used on 3 pages: [archive-2024.html](http://127.0.0.1:8771/archive-2024.html), [archive.html](http://127.0.0.1:8771/archive.html), [issue-21.html](http://127.0.0.1:8771/issue-21.html).

### cover-020 · The swing waits for laughter

- Caption: A village swing and remembered play. It can suggest Odisha's seasonal celebrations without claiming that the depicted scene documents a specific festival.
- Roles: edition-cover; treatment: framed.
- Find by: Living culture / play, June 2024, edition 20.
- Delivery: `assets/covers/editions/edition-020-2024-06.webp`.
- [Original master](../artifacts/artwork/masters/covers/by-edition/edition-020-2024-06.png).
- [Provenance](../records/edition-cover-filenames.json).
- Used on 3 pages: [archive-2024.html](http://127.0.0.1:8771/archive-2024.html), [archive.html](http://127.0.0.1:8771/archive.html), [issue-20.html](http://127.0.0.1:8771/issue-20.html).

### cover-019 · The tree's patient gift

- Caption: Jackfruit in a home landscape; an original reflection on growth and shared food, without assigning a particular recipe or ritual.
- Roles: edition-cover; treatment: framed.
- Find by: Food / growth, May 2024, edition 19.
- Delivery: `assets/covers/editions/edition-019-2024-05.webp`.
- [Original master](../artifacts/artwork/masters/covers/by-edition/edition-019-2024-05.png).
- [Provenance](../records/edition-cover-filenames.json).
- Used on 3 pages: [archive-2024.html](http://127.0.0.1:8771/archive-2024.html), [archive.html](http://127.0.0.1:8771/archive.html), [issue-19.html](http://127.0.0.1:8771/issue-19.html).

### cover-018 · A breeze made by hand

- Caption: A palm-leaf hand fan and everyday craft; the imagined object is not attributed to a named maker or village.
- Roles: edition-cover; treatment: framed.
- Find by: Craft / relief, April 2024, edition 18.
- Delivery: `assets/covers/editions/edition-018-2024-04.webp`.
- [Original master](../artifacts/artwork/masters/covers/by-edition/edition-018-2024-04.png).
- [Provenance](../records/edition-cover-filenames.json).
- Used on 3 pages: [archive-2024.html](http://127.0.0.1:8771/archive-2024.html), [archive.html](http://127.0.0.1:8771/archive.html), [issue-18.html](http://127.0.0.1:8771/issue-18.html).

### cover-017 · A forest breathing softly

- Caption: Similipal's forests, streams, orchids and ferns ground this imagined ecological study. It is not a documentary photograph of a surveyed spot or a verified orchid species.
- Roles: edition-cover; treatment: framed.
- Find by: Place / ecology, March 2024, edition 17.
- Delivery: `assets/covers/editions/edition-017-2024-03.webp`.
- [Original master](../artifacts/artwork/masters/covers/by-edition/edition-017-2024-03.png).
- [Provenance](../records/edition-cover-filenames.json).
- Used on 3 pages: [archive-2024.html](http://127.0.0.1:8771/archive-2024.html), [archive.html](http://127.0.0.1:8771/archive.html), [issue-17.html](http://127.0.0.1:8771/issue-17.html).

### cover-016 · A language looks back

- Caption: An interpretive tribute to Fakir Mohan Senapati and his attention to common people in Odia prose. The narrative is original, not a quotation, historical scene or claim about this edition's contents.
- Roles: edition-cover; treatment: framed.
- Find by: Literature / witness, February 2024, edition 16.
- Delivery: `assets/covers/editions/edition-016-2024-02.webp`.
- [Original master](../artifacts/artwork/masters/covers/by-edition/edition-016-2024-02.png).
- [Provenance](../records/edition-cover-filenames.json).
- Used on 3 pages: [archive-2024.html](http://127.0.0.1:8771/archive-2024.html), [archive.html](http://127.0.0.1:8771/archive.html), [issue-16.html](http://127.0.0.1:8771/issue-16.html).

### cover-015 · What the hands have gathered

- Caption: Rice harvest and agricultural labour; gratitude does not erase the work or uncertainty that produced it.
- Roles: edition-cover; treatment: framed.
- Find by: Agrarian / gratitude, January 2024, edition 15.
- Delivery: `assets/covers/editions/edition-015-2024-01.webp`.
- [Original master](../artifacts/artwork/masters/covers/by-edition/edition-015-2024-01.png).
- [Provenance](../records/edition-cover-filenames.json).
- Used on 3 pages: [archive-2024.html](http://127.0.0.1:8771/archive-2024.html), [archive.html](http://127.0.0.1:8771/archive.html), [issue-15.html](http://127.0.0.1:8771/issue-15.html).

### cover-014 · The chair keeps a little warmth

- Caption: Domestic cloth, winter light and remembered companionship; an imagined home, not a named person's belongings.
- Roles: edition-cover; treatment: framed.
- Find by: Home / companionship, December 2023, edition 14.
- Delivery: `assets/covers/editions/edition-014-2023-12.webp`.
- [Original master](../artifacts/artwork/masters/covers/by-edition/edition-014-2023-12.png).
- [Provenance](../records/edition-cover-filenames.json).
- Used on 3 pages: [archive-2023.html](http://127.0.0.1:8771/archive-2023.html), [archive.html](http://127.0.0.1:8771/archive.html), [issue-14.html](http://127.0.0.1:8771/issue-14.html).

### cover-013 · A second moon

- Caption: An imagined Odisha lagoon at night; the emotional story concerns distance and companionship.
- Roles: edition-cover; treatment: framed.
- Find by: Water / distance, November 2023, edition 13.
- Delivery: `assets/covers/editions/edition-013-2023-11.webp`.
- [Original master](../artifacts/artwork/masters/covers/by-edition/edition-013-2023-11.png).
- [Provenance](../records/edition-cover-filenames.json).
- Used on 3 pages: [archive-2023.html](http://127.0.0.1:8771/archive-2023.html), [archive.html](http://127.0.0.1:8771/archive.html), [issue-13.html](http://127.0.0.1:8771/issue-13.html).

### cover-012 · The morning gathers quietly

- Caption: Night-flowering jasmine provides the floral starting point; the image does not claim a particular local devotional practice.
- Roles: edition-cover; treatment: framed.
- Find by: Flora / fleeting beauty, October 2023, edition 12.
- Delivery: `assets/covers/editions/edition-012-2023-10.webp`.
- [Original master](../artifacts/artwork/masters/covers/by-edition/edition-012-2023-10.png).
- [Provenance](../records/edition-cover-filenames.json).
- Used on 3 pages: [archive-2023.html](http://127.0.0.1:8771/archive-2023.html), [archive.html](http://127.0.0.1:8771/archive.html), [issue-12.html](http://127.0.0.1:8771/issue-12.html).

### cover-011 · The rain can stay outside

- Caption: A thatched veranda evokes vernacular domestic shelter. This is an imagined setting, not an architectural record of a named community's house.
- Roles: edition-cover; treatment: framed.
- Find by: Architecture / shelter, September 2023, edition 11.
- Delivery: `assets/covers/editions/edition-011-2023-09.webp`.
- [Original master](../artifacts/artwork/masters/covers/by-edition/edition-011-2023-09.png).
- [Provenance](../records/edition-cover-filenames.json).
- Used on 3 pages: [archive-2023.html](http://127.0.0.1:8771/archive-2023.html), [archive.html](http://127.0.0.1:8771/archive.html), [issue-11.html](http://127.0.0.1:8771/issue-11.html).

### cover-010 · The hour the stone remembers

- Caption: The carved chariot wheels of the Sun Temple at Konark are the reference. The generated close study is interpretive, not measured archaeological documentation.
- Roles: edition-cover; treatment: framed.
- Find by: Heritage / time, August 2023, edition 10.
- Delivery: `assets/covers/editions/edition-010-2023-08.webp`.
- [Original master](../artifacts/artwork/masters/covers/by-edition/edition-010-2023-08.png).
- [Provenance](../records/edition-cover-filenames.json).
- Used on 3 pages: [archive-2023.html](http://127.0.0.1:8771/archive-2023.html), [archive.html](http://127.0.0.1:8771/archive.html), [issue-10.html](http://127.0.0.1:8771/issue-10.html).

### cover-009 · The river takes its time

- Caption: An imagined Odisha river landscape; no precise river, village or conservation condition is asserted.
- Roles: edition-cover; treatment: framed.
- Find by: Landscape / change, July 2023, edition 9.
- Delivery: `assets/covers/editions/edition-009-2023-07.webp`.
- [Original master](../artifacts/artwork/masters/covers/by-edition/edition-009-2023-07.png).
- [Provenance](../records/edition-cover-filenames.json).
- Used on 3 pages: [archive-2023.html](http://127.0.0.1:8771/archive-2023.html), [archive.html](http://127.0.0.1:8771/archive.html), [issue-9.html](http://127.0.0.1:8771/issue-9.html).

### cover-008 · A small place to begin

- Caption: An everyday act of home growing and reuse, offered as a contemporary narrative rather than a named heritage practice.
- Roles: edition-cover; treatment: framed.
- Find by: Growth / nurture, June 2023, edition 8.
- Delivery: `assets/covers/editions/edition-008-2023-06.webp`.
- [Original master](../artifacts/artwork/masters/covers/by-edition/edition-008-2023-06.png).
- [Provenance](../records/edition-cover-filenames.json).
- Used on 3 pages: [archive-2023.html](http://127.0.0.1:8771/archive-2023.html), [archive.html](http://127.0.0.1:8771/archive.html), [issue-8.html](http://127.0.0.1:8771/issue-8.html).

### cover-007 · The shade knows everyone

- Caption: A tamarind tree as a shared village landscape; the story is imagined and does not document a particular meeting place.
- Roles: edition-cover; treatment: framed.
- Find by: Tree / community, May 2023, edition 7.
- Delivery: `assets/covers/editions/edition-007-2023-05.webp`.
- [Original master](../artifacts/artwork/masters/covers/by-edition/edition-007-2023-05.png).
- [Provenance](../records/edition-cover-filenames.json).
- Used on 3 pages: [archive-2023.html](http://127.0.0.1:8771/archive-2023.html), [archive.html](http://127.0.0.1:8771/archive.html), [issue-7.html](http://127.0.0.1:8771/issue-7.html).

### cover-006 · A little sky indoors

- Caption: A domestic still life of water, metal and flower; no prescribed religious symbolism is assigned.
- Roles: edition-cover; treatment: framed.
- Find by: Home / contemplation, April 2023, edition 6.
- Delivery: `assets/covers/editions/edition-006-2023-04.webp`.
- [Original master](../artifacts/artwork/masters/covers/by-edition/edition-006-2023-04.png).
- [Provenance](../records/edition-cover-filenames.json).
- Used on 3 pages: [archive-2023.html](http://127.0.0.1:8771/archive-2023.html), [archive.html](http://127.0.0.1:8771/archive.html), [issue-6.html](http://127.0.0.1:8771/issue-6.html).

### cover-005 · Where the hills exhale

- Caption: Deomali in Koraput, within the Eastern Ghats, is the geographical reference. This generated landscape is an artistic interpretation, not a location photograph.
- Roles: edition-cover; treatment: framed.
- Find by: Place / openness, March 2023, edition 5.
- Delivery: `assets/covers/editions/edition-005-2023-03.webp`.
- [Original master](../artifacts/artwork/masters/covers/by-edition/edition-005-2023-03.png).
- [Provenance](../records/edition-cover-filenames.json).
- Used on 3 pages: [archive-2023.html](http://127.0.0.1:8771/archive-2023.html), [archive.html](http://127.0.0.1:8771/archive.html), [issue-5.html](http://127.0.0.1:8771/issue-5.html).

### cover-004 · A world held in a thread

- Caption: Cuttack's tarakasi, or silver filigree, provides the craft reference. The generated ornament is an original interpretation, not a documented maker's piece.
- Roles: edition-cover; treatment: framed.
- Find by: Craft / delicacy, February 2023, edition 4.
- Delivery: `assets/covers/editions/edition-004-2023-02.webp`.
- [Original master](../artifacts/artwork/masters/covers/by-edition/edition-004-2023-02.png).
- [Provenance](../records/edition-cover-filenames.json).
- Used on 3 pages: [archive-2023.html](http://127.0.0.1:8771/archive-2023.html), [archive.html](http://127.0.0.1:8771/archive.html), [issue-4.html](http://127.0.0.1:8771/issue-4.html).

### cover-003 · The sea, held close

- Caption: A shore-found shell as a poetic object; this image makes no claim about a species, collection practice or ritual conch.
- Roles: edition-cover; treatment: framed.
- Find by: Coast / listening, January 2023, edition 3.
- Delivery: `assets/covers/editions/edition-003-2023-01.webp`.
- [Original master](../artifacts/artwork/masters/covers/by-edition/edition-003-2023-01.png).
- [Provenance](../records/edition-cover-filenames.json).
- Used on 3 pages: [archive-2023.html](http://127.0.0.1:8771/archive-2023.html), [archive.html](http://127.0.0.1:8771/archive.html), [issue-3.html](http://127.0.0.1:8771/issue-3.html).

### cover-002 · Enough to share

- Caption: Grain baskets connect woven utility, food and household memory; no specific basket tradition or community is asserted.
- Roles: edition-cover; treatment: framed.
- Find by: Food / keeping, December 2022, edition 2.
- Delivery: `assets/covers/editions/edition-002-2022-12.webp`.
- [Original master](../artifacts/artwork/masters/covers/by-edition/edition-002-2022-12.png).
- [Provenance](../records/edition-cover-filenames.json).
- Used on 3 pages: [archive-2022.html](http://127.0.0.1:8771/archive-2022.html), [archive.html](http://127.0.0.1:8771/archive.html), [issue-2.html](http://127.0.0.1:8771/issue-2.html).

### cover-001 · Before the first line

- Caption: An imagined writer's everyday table, opening the collection through attention rather than a biographical claim about an actual poet.
- Roles: edition-cover; treatment: framed.
- Find by: Literature / beginning, November 2022, edition 1.
- Delivery: `assets/covers/editions/edition-001-2022-11.webp`.
- [Original master](../artifacts/artwork/masters/covers/by-edition/edition-001-2022-11.png).
- [Provenance](../records/edition-cover-filenames.json).
- Used on 3 pages: [archive-2022.html](http://127.0.0.1:8771/archive-2022.html), [archive.html](http://127.0.0.1:8771/archive.html), [issue-1.html](http://127.0.0.1:8771/issue-1.html).

### home-life-as-it-is · LIFE AS IT IS

- Caption: LIFE AS IT IS
- Roles: homepage; treatment: framed.
- Find by: home, rain, courtyard, life.
- Delivery: `assets/home/life-after-rain.webp`.
- [Original master](../artifacts/artwork/masters/home/life-after-rain.png).
- [Provenance](../records/home-atmosphere-approval.json).
- Used on 1 pages: [index.html](http://127.0.0.1:8771/index.html).

