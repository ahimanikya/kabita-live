"""Validate the exact generated service graph before public asset selection."""
import hashlib,json,re
from pathlib import Path
ENTRIES={'assets/engagement.js','assets/private-feedback.js'}
def service_assets(root, manifest_name='.service-build.json'):
    root=Path(root).resolve()
    manifest=root/manifest_name
    if not manifest.exists():return set()  # Preserved legacy monolithic packaging.
    data=json.loads(manifest.read_text())
    if data.get('version')!=1 or set(data.get('entries',[]))!=ENTRIES:
        raise ValueError('Invalid public service entries')
    files=data.get('files')
    if not isinstance(files,dict) or not files or len(files)>32:
        raise ValueError('Invalid service graph')
    for name,node in files.items():
        if name not in ENTRIES and not re.fullmatch(r'assets/services/[A-Za-z][A-Za-z0-9_.-]*\.js',name):
            raise ValueError('Service asset outside public service boundary')
        p=root/name
        if not p.is_file() or not p.resolve().is_relative_to(root):
            raise ValueError('Missing or escaping service asset')
        # Symlinks cannot turn a nominal public path into private source content.
        if p.resolve()!=p.absolute():raise ValueError('Symlink service asset')
        if not isinstance(node,dict) or hashlib.sha256(p.read_bytes()).hexdigest()!=node.get('sha256'):
            raise ValueError('Stale service asset hash')
        imports=node.get('imports')
        if not isinstance(imports,list) or any(not isinstance(n,str) or n not in files for n in imports):
            raise ValueError('Missing service dependency')
    reached=set();pending=list(ENTRIES)
    while pending:
        name=pending.pop()
        if name in reached:continue
        if name not in files:raise ValueError('Missing service entry')
        reached.add(name);pending.extend(files[name]['imports'])
    if reached!=set(files):raise ValueError('Unreferenced service asset')
    return reached
