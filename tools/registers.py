#!/usr/bin/env python3
"""Utkal register model 1.0.0 — validate sources and generate one portable view.
Created for Ahimanikya Satapathy's Utkal Blueprint with AI assistance.
No dependencies, network access, authority grants or publication actions.
"""
import argparse
import hashlib
import json
import re
from pathlib import Path

COLLECTIONS = ('projects','work','decisions','requirements','reviews','releases','sources','relationships')
WORK_STATES = {'proposed','ready','in_progress','blocked','awaiting_review','completed','deferred','cancelled'}
READINESS = {'concept','draft','reviewed','approved','applied','published'}
DECISIONS = {'proposed','approved','rejected','superseded','recorded_direction'}
REVIEWS = {'pass','pass_with_limitations','fail','not_tested'}

def require(condition, message):
    if not condition:
        raise ValueError(message)

def local_path(root, name):
    aliases_file = root / 'references/migration-paths.json'
    aliases = json.loads(aliases_file.read_text()) if aliases_file.exists() else {}
    direct = (root / name).resolve()
    p = direct if direct.is_file() else (root / aliases.get(name, name)).resolve()
    require(p.is_relative_to(root.resolve()), 'Path outside repository: '+name)
    require(p.is_file(), 'Missing record/evidence file: '+name)
    return p

def validate(root, data, events):
    require(data['schema_version'] == '1.0.0', 'Unsupported schema version')
    prefix = data['project']
    require(re.fullmatch(r'[A-Z]{3}', prefix), 'Invalid project prefix')
    require(bool(data.get('human_authority')), 'Missing human authority')
    rows = [r for c in COLLECTIONS for r in data[c]]
    by_id = {}
    for r in rows + events:
        require(re.fullmatch(prefix+r'-[A-Z]+-\d{3,}', r['id']), 'Invalid ID: '+r['id'])
        require(r['id'] not in by_id, 'Duplicate ID: '+r['id'])
        by_id[r['id']] = r
    external = data.get('external_refs', {})
    require(not set(by_id).intersection(external), 'External/local ID collision')
    for key, ref in external.items():
        require(bool(ref.get('location')), 'External reference needs location: '+key)
        if not ref['location'].startswith('https://'):
            local_path(root, ref['location'])
    for r in rows + events:
        for ref in r.get('refs', []):
            require(ref in by_id or ref in external, r['id']+' has dangling reference '+ref)
        for path in r.get('evidence', []):
            if not path.startswith('https://'):
                local_path(root, path)
    for home in data['record_homes'].values():
        local_path(root, home)
    for p in data['projects']:
        local_path(root,p['charter'])
        require(bool(p.get('human_owner')), 'Project needs human owner')
    for d in data['decisions']:
        require(d['status'] in DECISIONS, 'Unknown decision status')
        if d['status'] in {'approved','recorded_direction'}:
            require(d['actor']['kind']=='human', 'AI cannot grant approval: '+d['id'])
            require(bool(d.get('quote') or d.get('evidence')), 'Approval lacks source')
            require(bool(d.get('scope')), 'Approval lacks scope')
    def authorized(ref):
        if ref in external:
            d = external[ref]
            return d.get('kind') == 'decision' and d.get('actor_kind') == 'human' and d.get('status') in {'approved','recorded_direction'}  # Source authenticity still requires review.
        return any(d['id']==ref and d['actor']['kind']=='human' and d['status'] in {'approved','recorded_direction'} for d in data['decisions'])
    for w in data['work']:
        require(w['status'] in WORK_STATES, 'Unknown work status')
        require(w['readiness'] in READINESS, 'Unknown readiness')
        require(bool(w.get('human_owner')) and bool(w.get('next_action')), 'Work needs human owner and next action')
        require(authorized(w['authorization']), 'Work lacks valid authorization: '+w['id'])
        if w['status']=='blocked': require(bool(w.get('blockers')), 'Blocked work needs a reason')
        if w['readiness']=='published':
            require(any(w['id'] in r.get('refs',[]) and r['status']=='published' for r in data['releases']), 'Published work needs release evidence')
    for r in data['reviews']:
        require(r['status'] in REVIEWS and isinstance(r['independent'],bool), 'Invalid review/independence')
        if r['status'] in {'fail','pass_with_limitations','not_tested'}:
            require(bool(r.get('limitations')), 'Review needs limitations')
    for r in data['releases']:
        require(r['status'] in {'applied','published'}, 'Release must record an actual event')
        require(authorized(r['authorization']), 'Release lacks authorization')
        require(bool(r.get('destination')) and bool(r.get('evidence')), 'Release lacks destination/evidence')
    for s in data['sources']:
        require(bool(s.get('creator_credit')) and bool(s.get('rights')), 'Source needs credit/rights')
    for e in events:
        require(e['actor']['kind'] in {'human','persona','ai_assistant'}, 'Invalid event actor')
        require(bool(e.get('recorded_at')) and bool(e.get('summary')), 'Incomplete event')
    # Existing role assignments stay authoritative; humans may not report to AI.
    assignments = data['record_homes'].get('members_and_assignments','')
    if assignments.endswith('.json'):
        team=json.loads(local_path(root,assignments).read_text())
        human=team['human_owner']
        require(human['kind']=='human','Human owner kind invalid')
        for a in team['assignments']:
            require(a['kind'] in {'human','persona'},'Invalid member kind')
            if a['kind']=='persona':
                require(not a.get('human_reports'), 'Human cannot report to persona')
                require(a.get('human_supervisor')==human['full_name'],'Unknown human supervisor')
    return by_id

def cell(value):
    if isinstance(value,list): value='; '.join(str(x) for x in value)
    return str('—' if value is None or value == '' else value).replace('|','\\|').replace('\n',' ')

def render(data, events, digest):
    lines=['---','type: Generated register',f"title: {json.dumps(data['name']+' dashboard')}",'---','',f"# {data['name']} · dashboard",'',f"Generated from `records.json` and `activity.jsonl`. Source SHA-256: `{digest}`.",'',f"Accountable human: **{data['human_authority']}**. Model {data['model_version']}. This view reports records; it grants no authority.",'']
    def table(title, heads, rows):
        lines.extend(['## '+title,'','| '+' | '.join(heads)+' |','|'+'|'.join('---' for _ in heads)+'|'])
        for row in rows: lines.append('| '+' | '.join(cell(v) for v in row)+' |')
        if not rows: lines.append('| No records |'+' — |'*(len(heads)-1))
        lines.append('')
    table('Work and readiness',['ID / work','Status','Readiness','Human owner','Next action','Blockers'],[[w['id']+' · '+w['title'],w['status'],w['readiness'],w['human_owner'],w['next_action'],w['blockers']] for w in data['work']])
    table('Pending human review and decisions',['Record','Reason / scope'],[[w['id'],w['next_action']] for w in data['work'] if w['status']=='awaiting_review']+[[d['id'],d['scope']] for d in data['decisions'] if d['status']=='proposed'])
    table('Decisions',['ID / decision','Status','Human / proposer','Scope'],[[d['id']+' · '+d['title'],d['status'],d['actor']['name'],d['scope']] for d in data['decisions']])
    table('Reviews',['ID','Outcome','Independent','Limitations'],[[r['id'],r['status'],r['independent'],r.get('limitations',[])] for r in data['reviews']])
    table('Publication and application history',['ID / event','Status','Destination','Authorization'],[[r['id']+' · '+r['title'],r['status'],r['destination'],r['authorization']] for r in data['releases']])
    table('Sources and assets',['ID / title','State','Credit','Rights'],[[s['id']+' · '+s['title'],s['status'],s['creator_credit'],s['rights']] for s in data['sources']])
    table('Relationships',['ID / relationship','State','Next action'],[[r['id']+' · '+r['title'],r['status'],r.get('next_action')] for r in data['relationships']])
    table('Project / requirements index',['ID / title','State','References'],[[r['id']+' · '+r['title'],r['status'],r.get('refs',[])] for c in ['projects','requirements'] for r in data[c]])
    table('Canonical record homes',['Record','Location'],[[k,f'[{v}](../{v})'] for k,v in data['record_homes'].items()])
    table('Latest activity and handovers',['Event','Recorded at','Summary','Next action'],[[e['id'],e['recorded_at'],e['summary'],e.get('next_action')] for e in events[-10:]])
    lines += ['## Deferred extensions','']+[f"- {k}: {'active' if v['enabled'] else 'inactive'} — {v['activation']}." for k,v in data['optional_extensions'].items()]
    lines += ['','Generated views may lag edits until regeneration. Run `python3 tools/registers.py --check` to detect drift. External URLs are evidence pointers, not network-verified by this tool.','']
    return '\n'.join(lines)

def run(root, check=False):
    config=json.loads((root.parent/'utkal.config.json').read_text())
    home=config['record_directory']
    require(home in {'maintenance','registers'}, 'Invalid configured record directory')
    source=root/home/'records.json'; ledger=root/home/'activity.jsonl'
    raw=source.read_bytes(); activity=ledger.read_bytes()
    data=json.loads(raw); events=[json.loads(line) for line in activity.splitlines() if line.strip()]
    require(config['prefix']==data['project'], 'Configuration identity conflicts with registers')
    validate(root,data,events)
    output=render(data,events,hashlib.sha256(raw+b'\n'+activity).hexdigest())
    target=root/home/'DASHBOARD.md'
    if check:
        require(target.exists() and target.read_text()==output,'Dashboard stale; regenerate')
    else: target.write_text(output,encoding='utf-8')
    print(f"{data['project']}: valid; {sum(len(data[c]) for c in COLLECTIONS)} records, {len(events)} events; dashboard {'current' if check else 'generated'}")

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    try: run(Path(__file__).resolve().parents[1]/'kb', args.check)
    except (ValueError,KeyError,TypeError,OSError) as exc:
        parser.exit(1,'Register check failed: '+str(exc)+'\n')
