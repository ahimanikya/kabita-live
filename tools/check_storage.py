#!/usr/bin/env python3
"""Verify KB ownership, compatibility paths and the relocatable handoff."""
import argparse
import hashlib
import json
import os
from pathlib import Path


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--migration', action='store_true', help='Also compare the original migration byte snapshot')
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    cfg = json.loads((root / 'utkal.config.json').read_text())
    primary = root / cfg['paths']['primary_design_source']
    portable = root / cfg['paths']['portable_handoff']
    handoff_mode = primary.resolve() == root
    manifest = json.loads((root / 'kb/records/storage-migration.json').read_text())
    updates = {u['file']: u for u in manifest.get('intentional_path_updates', [])}
    errors = []
    def need(ok, message):
        if not ok:
            errors.append(message)
    for move in manifest['moves']:
        current = root / move['new']
        need(current.exists(), 'Missing KB artifact: ' + move['new'])
        if not handoff_mode:
            old = root / move['old']
            need(old.is_symlink() and old.resolve() == current.resolve(), 'Broken compatibility path: ' + move['old'])
        for item in move['files']:
            new = root / item['new']
            need(new.is_file(), 'Missing preserved file: ' + item['new'])
            if args.migration and new.is_file():
                if item['new'] in updates:
                    update = updates[item['new']]
                    need(sha(root / update['original_preserved']) == item['sha256'], 'Original generator not preserved')
                    need(sha(new) == update['after_sha256'], 'Generator path update differs from verified candidate')
                else:
                    need(sha(new) == item['sha256'], 'Migration content changed: ' + item['new'])
    for difference in manifest['portable_differences']:
        need(sha(root / difference['preserved']) == difference['sha256'], 'Portable variant not preserved')
    for relative, before in manifest['site_before'].items():
        p = primary / 'site' / relative
        need(p.is_file(), 'Missing website file: ' + relative)
        if args.migration and p.is_file():
            need(sha(p) == before, 'Website changed during migration: ' + relative)
    # Every symlink inside the portable package must resolve inside it.
    link_count = 0
    for directory, dirs, files in os.walk(portable, followlinks=False):
        dirs[:] = [d for d in dirs if d != '__pycache__']
        for n in dirs + files:
            p = Path(directory) / n
            if p.is_symlink():
                link_count += 1
                need(p.exists() and p.resolve().is_relative_to(portable.resolve()),
                     'Handoff alias is broken or external: ' + str(p.relative_to(portable)))
    state = json.loads((portable / 'kb/records/handoff-sync-state.json').read_text())
    for relative, expected in state['files'].items():
        p = portable / relative
        if not p.exists():
            errors.append('Missing synchronized handoff file: ' + relative)
        else:
            actual = 'link:' + os.readlink(p) if p.is_symlink() else sha(p)
            need(actual == expected, 'Handoff drift since sync: ' + relative)
    if not handoff_mode:
        for folder in ['kb', 'tools']:
            for p in (root / folder).rglob('*'):
                if p.is_file() and '__pycache__' not in p.parts and p.suffix != '.pyc':
                    other = portable / p.relative_to(root)
                    need(other.is_file() and sha(other) == sha(p), 'Source/handoff mismatch: ' + str(p.relative_to(root)))
    result = {'result': 'FAIL' if errors else 'PASS', 'moved_files': manifest['moved_files'],
              'website_files_preserved': len(manifest['site_before']),
              'portable_links_checked': link_count, 'migration_hashes_checked': args.migration,
              'errors': errors}
    print(json.dumps(result, indent=2))
    return bool(errors)


if __name__ == '__main__':
    raise SystemExit(main())
