// Reproduce app icons from the approved logo; preserve its geometry and colours.
import sharp from 'sharp';
import {fileURLToPath} from 'node:url';
import {readFile} from 'node:fs/promises';
const source = new URL('../assets/kabita-live-symbol-ink-voice.svg', import.meta.url);
const svg = await readFile(source);
for (const size of [180, 192, 512]) {
  await sharp(svg).resize(size, size).flatten({background:'#faf7f7'})
    .png().toFile(fileURLToPath(new URL(`../assets/editor-app-${size}.png`, import.meta.url)));
}
