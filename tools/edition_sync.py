#!/usr/bin/env python3
"""Apply reviewed additive edition packages. Dry-run by default; never replace old entries."""
import argparse
import copy
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def encoded(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode()

def plan(root, package):
    planned = {}
    for op in package['operations']:
        path = (root / op['path']).resolve()
        if not path.is_relative_to(root.resolve()) or path.suffix != '.json':
            raise ValueError('Only project JSON destinations are allowed')
        if path in planned:
            raise ValueError(f'Duplicate destination: {path}')
        before = path.read_bytes() if path.exists() else None
        current = json.loads(before) if before is not None else None
        if op['mode'] == 'new_file':
            if current is not None and current != op['value']:
                raise ValueError(f'Existing file differs: {op["path"]}')
            after = op['value']
        else:
            after = copy.deepcopy(current)
            target = after
            for key in op.get('at', []):
                target = target[key]
            if op['mode'] == 'add_keys':
                for key, value in op['value'].items():
                    if key in target and target[key] != value:
                        raise ValueError(f'Existing key differs: {op["path"]}:{key}')
                    target[key] = value
            elif op['mode'] == 'append_author_works':
                known = {str(item['id']): item for item in target}
                for profile in op['value']['newProfiles']:
                    ident = str(profile['id'])
                    if ident in known and known[ident] != profile:
                        raise ValueError('Existing author differs: ' + ident)
                    if ident not in known:
                        target.append(copy.deepcopy(profile)); known[ident] = target[-1]
                for ident, works in op['value']['works'].items():
                    if ident not in known:
                        raise ValueError('Unknown author: ' + ident)
                    saved = known[ident].setdefault('works', [])
                    for work in works:
                        prior = [x for x in saved if x['id'] == work['id']]
                        if prior and any(x != work for x in prior):
                            raise ValueError('Existing author work differs')
                        if not prior: saved.append(copy.deepcopy(work))
            elif op['mode'] == 'append_records':
                key = op['key']
                known = {}
                for item in target:
                    known.setdefault(str(item[key]), []).append(item)
                additions = []
                for value in op['value']:
                    ident = str(value[key])
                    if ident in known and any(old != value for old in known[ident]):
                        raise ValueError(f'Existing record differs: {op["path"]}:{ident}')
                    if ident not in known:
                        additions.append(value)
                    known[ident] = [value]
                if op.get('prepend'):
                    target[:0] = additions
                else:
                    target.extend(additions)
            else:
                raise ValueError(f'Unsupported operation {op["mode"]}')
        if current != after:
            planned[path] = (before, encoded(after))
    return planned

def apply(planned):
    # Check the whole plan before the first write, then check each destination again.
    for path, (before, _) in planned.items():
        if (path.read_bytes() if path.exists() else None) != before:
            raise ValueError(f'Concurrent change: {path}')
    for path, (before, after) in planned.items():
        if (path.read_bytes() if path.exists() else None) != before:
            raise ValueError(f'Concurrent change; stop and resume by dry-run: {path}')
        path.parent.mkdir(parents=True, exist_ok=True)
        temp = path.with_name(path.name + '.edition-sync.tmp')
        with temp.open('xb') as handle:
            handle.write(after)
        temp.replace(path)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('package', type=Path)
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    package = json.loads(args.package.read_text())
    planned = plan(ROOT, package)
    if args.apply:
        apply(planned)
    print(json.dumps({'mode': 'applied' if args.apply else 'dry_run',
                      'changed_files': [str(p.relative_to(ROOT)) for p in planned],
                      'package_sha256': hashlib.sha256(args.package.read_bytes()).hexdigest()}, indent=2))

if __name__ == '__main__':
    main()
