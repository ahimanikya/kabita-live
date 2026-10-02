"""Save a manually inspected built-in image edit and its provenance; never generates images."""
import argparse
import hashlib
import json
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
p = argparse.ArgumentParser()
p.add_argument('writer_id', type=int)
p.add_argument('image', type=Path)
p.add_argument('prompt', type=Path)
p.add_argument('review', help='Actual visual comparison against the identified source')
a = p.parse_args()
ident = str(a.writer_id)
def read(path): return json.loads((ROOT / path).read_text())
def write(path, value): (ROOT / path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
mapping = read('projects/site/data/writer-portraits.json')
assert mapping[ident]['kind'] == 'journal_photo', 'Do not replace an existing reviewed artistic portrait.'
source = next(s for s in read('kb/research/writers/portrait-sources.json') if s['writer_id'] == a.writer_id)
master = Path(f'artifacts/artwork/writer-portraits/{ident}-earth-voice-v1.png')
target = ROOT / 'kb' / master
assert not target.exists(), 'Preserve existing master; use an explicit new revision instead.'
assert a.image.is_file() and a.prompt.is_file() and a.review.strip()
shutil.copy2(a.image, target)
script = '''const sharp=require('./projects/site/node_modules/sharp');
(async()=>{const [id,input]=process.argv.slice(1);for(const size of [600,128,64])await sharp(input).resize(size,size,{fit:'inside'}).webp({quality:90}).toFile(`projects/site/assets/writers/${id}-earth-voice-v1${size===600?'':'-'+size}.webp`);})().catch(e=>{console.error(e);process.exit(1)});'''
subprocess.run(['/Users/ahimanikya/.nvm/versions/node/v24.15.0/bin/node', '-e', script, ident, str(target)], cwd=ROOT, check=True)
previous = mapping[ident]
mapping[ident] = {'src': f'assets/writers/{ident}-earth-voice-v1.webp', 'kind': 'generated_portrait', 'credit': 'AI-assisted artistic portrait from the journal-supplied photograph', 'width': 600, 'height': 600}
edits = read('kb/research/writers/portrait-edits.json')
edits.append({'writer_id': a.writer_id, 'source': source, 'source_sha256': sha(ROOT / 'kb' / source['file']), 'style_reference': 'projects/site/assets/editors/pradeep-biswal-artistic-v1.webp', 'master': str(master), 'master_sha256': sha(target), 'prompt': a.prompt.read_text().strip(), 'tool': 'built-in image_gen', 'review': a.review, 'independent': False, 'status': 'integrated_pending_build', 'previous_asset': previous, 'publication_rights': source['rights']})
write('kb/research/writers/portrait-edits.json', edits)
write('projects/site/data/writer-portraits.json', mapping)
print(f'Saved writer {ident}; build and independent likeness review pending.')
