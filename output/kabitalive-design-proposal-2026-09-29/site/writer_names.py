"""Apply reviewed display spellings while leaving captured records intact."""
import json


def display_names(root):
    return {int(key): value['display_name'] for key, value in
            json.loads((root / 'data/writer-name-corrections.json').read_text()).items()}


def writer_aliases(root):
    """Reviewed identities only; aliases never mutate captured contributor IDs."""
    groups = json.loads((root / 'data/writer-identities.json').read_text())['groups']
    aliases = {}
    for group in groups:
        canonical = group['canonical_id']
        assert canonical in group['member_ids']
        for member in group['member_ids']:
            assert member not in aliases, 'Writer belongs to multiple identity groups'
            aliases[member] = canonical
    return {member: canonical for member, canonical in aliases.items() if member != canonical}


def load_writer_profiles(root):
    profiles = json.loads((root / 'data/writer-profiles.json').read_text())
    names = display_names(root)
    for profile in profiles:
        if profile['id'] in names:
            profile['captured_name'] = profile['name']
            profile['name'] = names[profile['id']]
    return profiles
