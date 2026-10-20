import fs from 'node:fs/promises';
import path from 'node:path';
import {createRequire} from 'node:module';
const root=process.cwd(), out=path.join(root,'kb/artifacts/social/facebook-ink-voice-2026-10-19');
const site=path.join(root,'projects/site');
const conf=path.join(out,'fonts.conf');
await fs.writeFile(conf,`<?xml version="1.0"?><!DOCTYPE fontconfig SYSTEM "urn:fontconfig:fonts.dtd"><fontconfig><dir>/System/Library/Fonts</dir><dir>/Library/Fonts</dir><dir>${site}/assets/fonts</dir><cachedir>/private/tmp/kbl-facebook-font-cache</cachedir></fontconfig>`);
process.env.FONTCONFIG_FILE=conf;
const require=createRequire(path.join(site,'package.json')),sharp=require('sharp');
const original=await fs.readFile(path.join(site,'assets/kabita-live-symbol-ink-voice.svg'),'utf8');
const paths=original.match(/<path\b[^>]+\/>/g).join('').replaceAll('currentColor','#713b55');
const logo=`<svg xmlns="http://www.w3.org/2000/svg" width="1024" height="1024" viewBox="0 0 1024 1024"><title>Kabita Live — mulberry leaf and aqua water</title><rect width="1024" height="1024" fill="#FAF7F7"/><g transform="translate(160 142) scale(2.75)">${paths}</g></svg>`;
const cover=`<svg xmlns="http://www.w3.org/2000/svg" width="1640" height="624" viewBox="0 0 1640 624"><title>Kabita Live — Ink and Voice</title>
<defs><linearGradient id="paper" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#FAF7F7"/><stop offset=".5" stop-color="#F5EFF2"/><stop offset="1" stop-color="#EADDE3"/></linearGradient></defs>
<rect width="1640" height="624" fill="url(#paper)"/>
<path d="M0 470C170 439 273 472 360 501S595 536 761 519S1054 482 1216 506S1499 564 1640 522" fill="none" stroke="#327E80" stroke-opacity=".23" stroke-width="2"/>
<path d="M0 493C155 466 292 488 388 516S652 556 811 535S1134 513 1301 543S1511 574 1640 548" fill="none" stroke="#713B55" stroke-opacity=".13" stroke-width="1.4"/>
<path d="M360 106H1280" stroke="#713B55" stroke-opacity=".3" stroke-width="1"/>
<g transform="translate(340 159) scale(.57)">${paths}</g>
<text x="514" y="270" font-family="Newsreader" font-weight="500" font-size="132" fill="#27222A">Kabita Live</text>
<text x="820" y="355" text-anchor="middle" font-family="Noto Serif Oriya" font-weight="400" font-size="44" fill="#713B55">ମାଟିର ମହକ · ହୃଦୟର ସ୍ବର</text>
<text x="820" y="413" text-anchor="middle" font-family="Newsreader" font-size="31" fill="#655A62">Monthly poetry · Odia, Hindi &amp; English</text>
</svg>`;
for(const [name,svg] of [['profile',logo],['cover',cover]]){
 await fs.writeFile(path.join(out,`${name}.svg`),svg);
 await sharp(Buffer.from(svg)).png().toFile(path.join(out,`${name==='cover'?'cover-font-fallback':name}.png`));
}
console.log('Rendered Facebook profile 1024×1024 and cover 1640×624.');
