"""Apply reviewed display spellings while leaving captured records intact."""
import json


def display_names(root):
    return {int(key): value['display_name'] for key, value in
            json.loads((root / 'data/writer-name-corrections.json').read_text()).items()}


def load_writer_profiles(root):
    profiles = json.loads((root / 'data/writer-profiles.json').read_text())
    names = display_names(root)
    for profile in profiles:
        if profile['id'] in names:
            profile['captured_name'] = profile['name']
            profile['name'] = names[profile['id']]
    return profiles
