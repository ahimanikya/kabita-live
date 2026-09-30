#!/usr/bin/env python3
"""Check KBL's declared persona assignments; does not grant or enforce tool access."""
import argparse
import copy
import json
from pathlib import Path


def load(root):
    def read(path):
        return json.loads((root / path).read_text())
    return {
        'config': read('utkal.config.json'),
        'team': read('kb/team/assignments.json'),
        'identities': read('kb/team/identities.json'),
        'records': read('kb/registers/records.json'),
        'jml': read('kb/team/jml-events.json'),
    }


def validate(root, data):
    errors = []
    def need(ok, message):
        if not ok:
            errors.append(message)
    def file(path):
        p = (root / 'kb' / path).resolve()
        return p.is_relative_to((root / 'kb').resolve()) and p.is_file()

    team = data['team']
    owner = team['human_owner']
    need(owner['kind'] == 'human', 'Supervisor must be human')
    need(owner['full_name'] == data['config']['creator']['name'], 'Owner mismatch')
    cfg = data['config']['persona_configuration']
    need(cfg['execution_mode'] == 'on_demand_current_chat', 'Unexpected execution mode')
    need(cfg['autonomous_dispatch'] is False and cfg['background_execution'] is False,
         'Automatic dispatch or background execution is outside this setup')
    need(cfg['assignments'] == 'kb/team/assignments.json', 'Wrong assignment source')
    need(cfg['operating_guide'] == 'kb/team/operating-model.md', 'Wrong workflow source')
    identities = data['identities']['identities']
    names = {'Disha Dash', 'Anvesha Acharya', 'Samanta Chandrasekhar', 'Drishti Senapati'}
    need(len(identities) == 4 and {i['full_name'] for i in identities} == names,
         'Expected four pinned Blueprint identities')
    by_identity = {i['id']: i for i in identities}
    need(len(by_identity) == 4, 'Duplicate identity')
    assignments = team['assignments']
    need(len(assignments) == 4 and len({a['id'] for a in assignments}) == 4,
         'Expected four unique assignments')
    need({a['identity_id'] for a in assignments} == set(by_identity), 'Identity/assignment mismatch')
    decisions = {d['id']: d for d in data['records']['decisions']}
    works = {w['id'] for w in data['records']['work']}
    need(cfg['authorization'] == 'KBL-DEC-005', 'Wrong configuration authorization')
    events = data['jml']['events']
    need(len(events) == 4 and len({e['assignment_id'] for e in events}) == 4,
         'Expected one join event per assignment')
    coverage = set()
    for a in assignments:
        identity = by_identity.get(a['identity_id'], {})
        need(a['kind'] == identity.get('kind') == 'persona', 'Identity must be AI persona')
        need(a['full_name'] == identity.get('full_name'), 'Persona name mismatch')
        need(a['human_supervisor'] == owner['full_name'] and not a['human_reports'],
             'Invalid supervision or human reporting')
        need(a['project'] == team['project'] == 'KBL', 'Assignment outside KBL')
        need(a['status'] == 'active', 'Assignment is not active')
        need(a['execution_mode'] == cfg['execution_mode'] and a['runtime_state'] == 'no_separate_process',
             'Unconfigured runtime claimed')
        d = decisions.get(a['authorization'], {})
        need(a['authorization'] == cfg['authorization'] and d.get('status') == 'approved'
             and d.get('actor', {}).get('kind') == 'human'
             and d.get('actor', {}).get('name') == owner['full_name'] and bool(d.get('quote')),
             'Assignment lacks the scoped human decision')
        for key in ['jd_path', 'jml_ref', 'configuration_evidence']:
            need(file(a[key]), 'Missing or unsafe evidence: ' + a[key])
        if file(a['jd_path']):
            brief = (root / 'kb' / a['jd_path']).read_text()
            need(a['jd_id'] in brief and 'v' + a['jd_version'] in brief
                 and a['full_name'] in brief and a['id'] in brief, 'JD version/identity mismatch')
        access = a['permitted_access']
        need(access['added'] == [] and access['removed'] == [], 'Undeclared access change')
        need(bool(access['local_read']) and bool(access['local_write']) and bool(access['excluded']),
             'Missing access boundaries')
        need(a['first_assignment']['work_ref'] in works and bool(a['first_assignment']['brief']),
             'Missing bounded first task')
        joins = [e for e in events if e['assignment_id'] == a['id']]
        if len(joins) == 1:
            e = joins[0]
            need(e['identity_id'] == a['identity_id'] and e['jd_id'] == a['jd_id']
                 and e['jd_version'] == a['jd_version'] and e['authorization'] == a['authorization'],
                 'Join record mismatch')
            need(e['state'] in {'in_progress', 'verified_complete'}, 'Invalid join state')
            need(e['access_added'] == [] and e['access_removed'] == [], 'Unexpected join access delta')
        coverage.update(a['coverage'])
    need({'coordination', 'design', 'editorial_language', 'odisha_culture', 'engineering',
          'accessibility', 'archive', 'verification', 'handoff_sync'} <= coverage,
         'Missing requested responsibility coverage')
    return errors


def self_test(root, data):
    """Check that meaningful invalid scopes are rejected without changing real files."""
    cases = {
        'human_reports_to_ai': lambda d: d['team']['assignments'][0].update(human_reports=['A human']),
        'ai_approval': lambda d: next(x for x in d['records']['decisions']
                                    if x['id'] == 'KBL-DEC-005')['actor'].update(kind='persona'),
        'scope_expansion': lambda d: d['team']['assignments'][0]['permitted_access'].update(added=['deployment']),
        'background_dispatch': lambda d: d['config']['persona_configuration'].update(background_execution=True),
        'missing_role_brief': lambda d: d['team']['assignments'][0].update(jd_path='roles/missing.md'),
        'wrong_project': lambda d: d['team']['assignments'][0].update(project='UTP'),
    }
    result = {}
    for name, mutate in cases.items():
        candidate = copy.deepcopy(data)
        mutate(candidate)
        result[name] = bool(validate(root, candidate))
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--self-test', action='store_true')
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    try:
        data = load(root)
        errors = validate(root, data)
        negative = self_test(root, data) if args.self_test and not errors else {}
        passed = not errors and all(negative.values())
        print(json.dumps({'result': 'PASS' if passed else 'FAIL', 'personas': 4,
                          'errors': errors, 'invalid_configurations_rejected': negative,
                          'scope': 'Declared configuration only; no runtime isolation or new access grants.'}, indent=2))
        raise SystemExit(0 if passed else 1)
    except (OSError, ValueError, KeyError, TypeError) as e:
        print(json.dumps({'result': 'FAIL', 'errors': [str(e)]}))
        raise SystemExit(1)
