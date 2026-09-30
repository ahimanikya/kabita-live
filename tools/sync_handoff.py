#!/usr/bin/env python3
"""Synchronize the portable package, rebasing aliases and detecting divergent edits."""
import argparse
import hashlib
import json
import os
import shutil
from pathlib import Path


def digest(p):
    if p.is_symlink():
        return 'link:' + os.readlink(p)
    return hashlib.sha256(p.read_bytes()).hexdigest()


def entries(base):
    for directory, dirs, files in os.walk(base, followlinks=False):
        dirs[:] = [d for d in dirs if d not in {'__pycache__','node_modules','.astro','.generated','.public','dist','.git'}]
        for n in files + [d for d in dirs if (Path(directory) / d).is_symlink()]:
            p = Path(directory) / n
            if p.suffix != '.pyc' and not p.name.endswith('-debug.log'):
                yield p


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--initialize', action='store_true', help='Establish the first baseline during the authorized migration')
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    config = json.loads((root / 'utkal.config.json').read_text())
    primary = (root / config['paths']['primary_design_source']).resolve()
    portable = (root / config['paths']['portable_handoff']).resolve()
    if primary == root or portable == root:
        raise SystemExit('Run synchronization from the source workspace, not inside the handoff.')
    state_path = Path('kb/records/handoff-sync-state.json')
    old_path = portable / state_path
    if not old_path.exists() and not args.initialize:
        raise SystemExit('No handoff baseline; inspect the package before using --initialize.')
    previous = json.loads(old_path.read_text())['files'] if old_path.exists() else {}
    operations = {}

    def add(source, relative):
        if source.is_symlink():
            actual = source.resolve(strict=True)
            if actual.is_relative_to(root / 'kb'):
                target = portable / 'kb' / actual.relative_to(root / 'kb')
            elif actual.is_relative_to(primary):
                target = portable / actual.relative_to(primary)
            else:
                raise ValueError('Alias leaves project: ' + str(source))
            value = os.path.relpath(target, (portable / relative).parent)
            operations[str(relative)] = ('link', value)
        else:
            operations[str(relative)] = ('file', source)

    for folder in ['kb', 'tools', '.github']:
        for source in entries(root / folder):
            relative = source.relative_to(root)
            if relative != state_path:
                add(source, relative)
    for source in entries(primary):
        add(source, source.relative_to(primary))
    cfg = json.loads(json.dumps(config))
    cfg['paths']['primary_design_source'] = '.'
    cfg['paths']['portable_handoff'] = '.'
    operations['utkal.config.json'] = ('text', json.dumps(cfg, ensure_ascii=False, indent=2) + '\n')
    guide = (root / 'AGENTS.md').read_text().replace(
        'Use `output/kabitalive-design-proposal-2026-09-29` as the primary source. `output/kabita-live-project` is the portable handoff copy.',
        'This is the portable package: website `site/`, knowledge `kb/`, tools `tools/`. The source workspace maintains the editable primary copy.')
    operations['AGENTS.md'] = ('text', guide)
    for name in ['.gitattributes', '.gitignore']:
        operations[name] = ('text', (root / name).read_text())
    workflow = root / '.github/workflows/publish-site.yml'
    if workflow.exists():
        operations['.github/workflows/publish-site.yml'] = ('text', workflow.read_text().replace('projects/site', 'site'))
    operations['README.md'] = ('text', '# Kabita Live · portable handoff\n\n'
        '[Knowledge base](kb/index.md) · [Storage map](kb/reference/storage-layout.md) · [Team](kb/team/operating-model.md) · [Architecture and setup](kb/reference/site-architecture.md)\n\n'
        'The website is `site/`; all supporting work lives in `kb/`. Compatibility links are relative and stay inside this package. '
        'Run the validation tools here; run handoff synchronization from the original source workspace. '
        'The public site and local design reviews remain unpublished prototypes.\n')
    expected = {}
    conflicts = []
    for relative, (kind, value) in operations.items():
        target = portable / relative
        wanted = ('link:' + value if kind == 'link' else
                  hashlib.sha256(value.encode()).hexdigest() if kind == 'text' else digest(value))
        expected[relative] = wanted
        exists = target.exists() or target.is_symlink()
        if exists:
            actual = digest(target)
            if actual != wanted and not args.initialize and previous.get(relative) != actual:
                conflicts.append(relative)
    if conflicts:
        raise SystemExit('Handoff has divergent edits; preserve/reconcile before sync:\n' + '\n'.join(conflicts))
    for relative, (kind, value) in operations.items():
        target = portable / relative
        if (target.exists() or target.is_symlink()) and digest(target) == expected[relative]:
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        # Never follow an old alias while replacing a regular file.
        if target.is_symlink():
            target.unlink()
        if kind == 'link':
            if target.exists():
                if target.is_dir():
                    raise ValueError('Unexpected directory replacement: ' + str(target))
                target.unlink()
            target.symlink_to(value)
        elif kind == 'text':
            target.write_text(value)
        else:
            shutil.copy2(value, target)
    for relative, wanted in expected.items():
        assert digest(portable / relative) == wanted, relative
    state = json.dumps({'version': '1.0', 'files': expected}, ensure_ascii=False, indent=2) + '\n'
    (portable / state_path).parent.mkdir(parents=True, exist_ok=True)
    (root / state_path).write_text(state)
    (portable / state_path).write_text(state)
    print(f'Handoff synchronized: {len(expected)} entries; relative aliases rebased; hashes verified.')


if __name__ == '__main__':
    main()
