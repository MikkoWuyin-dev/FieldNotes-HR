#!/usr/bin/env python3
"""Canonical catalogue validation and deterministic, checked-in projections."""
from __future__ import annotations
import copy
import datetime
import json
from pathlib import Path
import re

REPO = Path(__file__).resolve().parents[2]
SRC = REPO / 'learning-library/src'

def load():
    data = json.loads((SRC / 'catalog.json').read_text())
    validate(data)
    return data

def validate(data):
    if data.get('schema_version') != 1:
        raise ValueError('unsupported catalogue schema')
    ledger = json.loads((SRC / 'progress-compatibility.json').read_text())
    if data['storage_id'] != ledger['storage_id']:
        raise ValueError('storage identity changed')
    seen = set()
    urls = {e['url'] for e in data['verification']['urls']}
    for stage in data['stages']:
        for item in [stage, *stage['resources']]:
            identity = item['id']
            if not re.fullmatch(r'[a-z][a-z0-9-]+', identity) or identity in seen:
                raise ValueError(f'duplicate or invalid id: {identity}')
            seen.add(identity)
        if not isinstance(stage['estimated_hours'], int) or stage['estimated_hours'] <= 0:
            raise ValueError('stage hours must be positive integers')
        for r in stage['resources']:
            datetime.date.fromisoformat(r['checked_at'])
            if r['url'] not in urls or not r['url'].startswith('https://'):
                raise ValueError('resource missing evidence URL')
            for field in ('title','provider','modality','cost','duration','why','action','access_note','link_label'):
                if not isinstance(r[field], str) or not r[field].strip():
                    raise ValueError(f'missing resource {field}')
            access = r['access']
            if access['study'] not in ('free','paid','conditional','not_verified'):
                raise ValueError('invalid study classification')
            if access['certificate'] not in ('free_completion','free_participation','paid_optional','paid_qualification','conditional','not_verified'):
                raise ValueError('invalid certificate classification')
            if access['account'] not in ('required','conditional','not_verified','not_required'):
                raise ValueError('invalid account classification')
            if not access['evidence_urls'] or not set(access['evidence_urls']) <= urls:
                raise ValueError('invalid access evidence')
    # The compatibility ledger is append-only: absent IDs are retained for later restoration.
    for kind in ('resources','stages'):
        aliases = [alias for values in ledger[kind].values() for alias in values]
        if len(aliases) != len(set(aliases)):
            raise ValueError('ambiguous legacy aliases')

def totals(data):
    stages = data['stages']; cards = [r for s in stages for r in s['resources']]
    evidence = {e['url']: e['status'] for e in data['verification']['urls']}
    return dict(stages=len(stages), cards=len(cards), urls=len({r['url'] for r in cards}),
                hours=sum(s['estimated_hours'] for s in stages),
                weeks=max(int(n) for s in stages for n in re.findall(r'\d+',s['duration'])),
                free=sum(r['access']['study']=='free' and evidence.get(r['url'])=='confirmed' for r in cards))

def load_app_copy(data):
    """Load short tracker copy without changing research or document wording."""
    copy_data = json.loads((SRC / 'app-copy.json').read_text())
    if copy_data.get('version') != 1:
        raise ValueError('unsupported app-copy version')
    stage_ids = {s['id'] for s in data['stages']}
    resource_ids = {r['id'] for s in data['stages'] for r in s['resources']}
    if set(copy_data.get('stages', {})) != stage_ids:
        raise ValueError('app-copy stages must match active catalogue')
    if set(copy_data.get('resources', {})) != resource_ids:
        raise ValueError('app-copy resources must match active catalogue')
    for identity, stage in copy_data['stages'].items():
        for field in ('title', 'description'):
            if not isinstance(stage.get(field), str) or not stage[field].strip():
                raise ValueError(f'app-copy stage {identity} missing {field}')
        outcomes = stage.get('outcomes')
        if not isinstance(outcomes, list) or not outcomes or any(not isinstance(x, str) or not x.strip() for x in outcomes):
            raise ValueError(f'app-copy stage {identity} has invalid outcomes')
    for identity, resource in copy_data['resources'].items():
        for field in ('why', 'action', 'access_summary'):
            if not isinstance(resource.get(field), str) or not resource[field].strip():
                raise ValueError(f'app-copy resource {identity} missing {field}')
        for field in ('cost', 'duration'):
            if field in resource and (not isinstance(resource[field], str) or not resource[field].strip()):
                raise ValueError(f'app-copy resource {identity} has invalid {field}')
    if not isinstance(copy_data.get('subtitle'), str) or not copy_data['subtitle'].strip():
        raise ValueError('app-copy subtitle is required')
    return copy_data


def app_data(data):
    app = copy.deepcopy(data)
    app.pop('verification'); app.pop('document')
    app_copy = load_app_copy(data)
    app['subtitle'] = app_copy['subtitle']
    for i,s in enumerate(app['stages'],1):
        stage_copy = app_copy['stages'][s['id']]
        s['title'] = f'Stage {i}: {stage_copy["title"]}'
        s['description'] = stage_copy['description']
        s['outcomes'] = stage_copy['outcomes']
        for r in s['resources']:
            resource_copy = app_copy['resources'][r['id']]
            for field in ('why', 'action', 'access_summary', 'cost', 'duration'):
                if field in resource_copy:
                    r[field] = resource_copy[field]
            r['verification_date'] = r.pop('checked_at')
            # The compact app action becomes one stable, required progress leaf.
            # The full catalogue wording remains unchanged for the library document.
            r['optional'] = False
            r['milestone_note'] = ''
            r['milestones'] = [{
                'id': f'first-iteration:{r["id"]}:action',
                'label': r['action'],
                'kind': 'task',
                'required': True,
                'url': None,
            }]
            r['learning_notes'] = []
            r['references'] = []
    app['verified_free_count'] = totals(data)['free']
    return app

def markdown(data):
    text = (SRC / 'library-narrative.md').read_text()
    t=totals(data)
    values={'overview':f'This library has {t["stages"]} stages and {t["cards"]} resource cards, with {t["hours"]} planned study hours across {t["weeks"]} weeks. Study budgets include practice and selected lessons, not every full course. Free study, certificates and professional qualifications are separate findings.',
            'roadmap-table':'| Stage | Weeks | Hours | Focus |\n|---|---|---|---|\n'+'\n'.join(f'| {i}. {s["short_title"]} | {s["duration"]} | {s["estimated_hours"]} | {s["focus"]} |' for i,s in enumerate(data['stages'],1)),
            'first-hour':data['stages'][0]['resources'][0]['action']+' Then read the Stage 1 outcomes and schedule your next study session.'}
    for i,s in enumerate(data['stages'],1):
        parts=[f'## Stage {i}: {s["title"]}',s['description'],f'**Level:** {s["level"]}',f'**Effort:** about {s["estimated_hours"]} hours across {s["duration"].lower()}.{s["effort_note"]}', '**Outcomes:**\n\n'+'\n'.join('- '+x for x in s['outcomes']),f'**Practice task:** {s["practice"]}',f'**Resources in this stage:** {len(s["resources"])}.']
        for r in s['resources']:
            parts += [f'### {r["title"]}',f'**Provider:** {r["provider"]}',f'**Link:** {r["url"]}',f'**Format:** {r["modality"]}',f'**Cost:** {r["cost"]}',f'**Time:** {r["duration"]}',f'**Why:** {r["why"]}',f'**Do this:** {r["action"]}',f'**Access and verification ({r["checked_at"]}):** {r["access_note"]}']
        values['stage:'+s['id']]='\n\n'.join(parts)
    for key,value in values.items():
        token='{{'+key+'}}'
        if text.count(token)!=1: raise ValueError(f'narrative slot missing/duplicated: {key}')
        text=text.replace(token,value)
    if '{{' in text: raise ValueError('unknown narrative slot')
    return text

def projections(data):
    manifest=copy.deepcopy(data['verification'])
    manifest['link_sweep']=json.loads((SRC/'history/first-link-sweep.json').read_text())
    result={SRC/'roadmap-app.json':json.dumps(app_data(data),indent=2,ensure_ascii=False)+'\n',
            SRC/'verification-manifest.json':json.dumps(manifest,indent=2,ensure_ascii=False)+'\n',
            SRC/'recruiter-talent-acquisition-library.md':markdown(data)}
    t=totals(data)
    summary=(f'{t["stages"]} stages, {t["cards"]} resource cards, {t["urls"]} distinct card URLs, {t["hours"]} planned hours.\n'
             f'{t["weeks"]} planned weeks; {t["free"]} cards have confirmed free-study evidence.\n'
             'Certificate, account and professional-qualification terms are separate; partial findings are not counted as verified free.')
    for rel in ('README.md','docs/SETUP.md','learning-library/README.md'):
        p=REPO/rel; text=p.read_text()
        pattern=r'<!-- content-summary:start -->.*?<!-- content-summary:end -->'
        if len(re.findall(pattern,text,re.S))!=1: raise ValueError(f'count slot missing/duplicated: {rel}')
        result[p]=re.sub(pattern,lambda _: '<!-- content-summary:start -->\n'+summary+'\n<!-- content-summary:end -->',text,flags=re.S)
    return result

def generate(check=False):
    stale=[]
    for path,text in projections(load()).items():
        if check:
            if not path.exists() or path.read_text()!=text: stale.append(str(path.relative_to(REPO)))
        else: path.write_text(text)
    if stale: raise ValueError('generated content drift: '+', '.join(stale))

if __name__=='__main__':
    import sys
    generate('--check' in sys.argv)
