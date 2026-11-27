#!/usr/bin/env python3
"""Check planning artifact consistency; never infer product behavior from documents."""
import csv
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
PRD_ROW_PATTERN = r'^\|\s*[AXP]\d\d\s*\|'


def table_rows(text: str, pattern: str) -> list[tuple[str, ...]]:
    return [
        tuple(cell.strip() for cell in line.strip('|').split('|'))
        for line in text.splitlines()
        if re.match(pattern, line)
    ]

def validate(root: Path) -> list[str]:
    errors = []
    def check(condition, message):
        if not condition:
            errors.append(message)
    def read(path):
        p = root / path
        if not p.is_file():
            errors.append(f'missing {path}')
            return ''
        return p.read_text(encoding='utf-8-sig')
    required = ['proposal.md','design.md','requirements-matrix.md','tasks.md','README.md','AGENTS.md','CLAUDE.md','docs/prd/PRD.md','docs/interfaces/internal.md','docs/interfaces/web.md','docs/validation/release-contract.md','docs/validation/test-catalog.md','docs/validation/evaluator-flow.md']
    for p in required: read(p)
    try:
        d = json.loads(read('docs/validation/traceability.json'))
        state = json.loads(read('state/project-state.json'))
        api = json.loads(read('docs/interfaces/partner.openapi.json'))
        fs = {x['id']: x for x in d['features']}
        items = d['criteria'] + d['cross'] + d['process']
    except (ValueError, KeyError, TypeError) as exc:
        return errors + [f'invalid JSON/schema: {exc}']
    # Reviewed W0 normative snapshot. Changes require explicit amendment and review,
    # not automatic regeneration after a failing gate.
    try:
        manifest = json.loads(read('docs/validation/normative-lock.json'))
        for path, digest in manifest['sha256'].items():
            content = read(path)
            check(hashlib.sha256(content.encode('utf-8')).hexdigest() == digest,
                  'normative drift (review/amendment required): '+path)
        mandatory = {'docs/prd/PRD.md','docs/interfaces/partner.openapi.json','docs/validation/traceability.json'}
        check(mandatory <= set(manifest['sha256']), 'normative lock incomplete')
    except (ValueError, KeyError, TypeError) as exc:
        errors.append(f'invalid normative lock: {exc}')
    check(len(fs) == len(d['features']) >= 5,'feature count/unique IDs')
    prd, tasks, cat, mat = (read(p) for p in ['docs/prd/PRD.md','tasks.md','docs/validation/test-catalog.md','requirements-matrix.md'])
    check('Fora de escopo' in prd,'scope absent')
    edges = set()
    for f in fs.values():
        check(f['id'] in prd and f['provides'] and f['consumes'],'missing feature contract '+f['id'])
        for dep in f['dependsOn']:
            edges.add((dep,f['id']))
            check(dep in fs and fs[dep]['wave'] < f['wave'],f'invalid dependency {dep}->{f["id"]}')
        for name in ['spec.md','plan.md','contract.md']:
            read(f'{f["path"]}/{name}')
    check(max(Counter(f['wave'] for f in fs.values()).values(),default=0)>=2,'no parallel wave')
    check(edges == {(x['provider'],x['consumer']) for x in d['cross'] if x['kind']=='dependency'},'dependency criterion mismatch')
    check(edges == set(re.findall(r'^\s*(F\d+) --> (F\d+)\s*$',prd,re.M)),'PRD Mermaid edges mismatch')
    for key in ('id','contract','test'):
        check(len({c[key] for c in items}) == len(items),f'duplicate {key}')
    rules={r for c in items for r in c['rules']}
    check({f'R{i:02}' for i in range(1,14)} <= rules,'missing R01–R13')
    expected=[]
    for c in items:
        ident=c['id']; fid=c.get('feature',c.get('consumer','RELEASE'))
        check(c['phase'] in ('local','integrated','release'),'bad phase '+ident)
        check(c['phase']==('integrated' if c.get('kind')=='integration' else 'release' if ident.startswith('P') else 'local'),'bad phase mapping '+ident)
        check(all(c.get(k) for k in ['precondition','procedure','oracle','acceptance','evidence','level']),f'incomplete test definition {ident}')
        check(re.search(rf'\b{ident}\b',prd) is not None, f'PRD absent {ident}')
        check(f'## {c["test"]} | {ident}' in cat, f'test absent {ident}')
        test_section=re.search(r'(?m)^## '+re.escape(c['test'])+r' \| '+ident+r'\s*$(.*?)(?=^## |\Z)',cat,re.M|re.S)
        check(test_section is not None and all(c[k] in test_section.group(1) for k in ('precondition','procedure','oracle','evidence')), 'test content mismatch '+ident)
        check(c['task'] in tasks, f'task absent {ident}')
        path=f'{fs[fid]["path"]}/contract.md' if fid in fs else 'docs/validation/release-contract.md'
        con=read(path)
        check(f'{c["contract"]} ({ident})' in con and c['test'] in con, f'contract mapping absent {ident}')
        for r in c['rules']:
            expected.append((r,ident,fid,c['phase'],c['contract'],c['test'],c['task'],c['acceptance']))
            check(f'| {r} | {ident} | {fid} | {c["phase"]} |' in mat, f'matrix missing {r}/{ident}')
    try:
        with (root/'requirements-matrix.csv').open(encoding='utf-8-sig',newline='') as f:
            rows=list(csv.reader(f))[1:]
        check(Counter(map(tuple,rows))==Counter(expected),'CSV inconsistent')
        check(len(re.findall(r'^\| (?:R\d\d|H\d\d|API|SDD|EVAL|STATE|PAR|DELIVERY) \|',mat,re.M))==len(expected),'Markdown matrix row count mismatch')
    except OSError as exc: errors.append(str(exc))
    matrix_rows = table_rows(mat, r'^\| (?:R\d\d|H\d\d|API|SDD|EVAL|STATE|PAR|DELIVERY) \|')
    check(Counter(matrix_rows) == Counter(expected), 'Markdown matrix content inconsistent')
    prd_rows = table_rows(prd, PRD_ROW_PATTERN)
    prd_expected = []
    for c in items:
        if c['id'].startswith('A'):
            prd_expected.append((c['id'], ', '.join(c['rules']), c['acceptance']))
        elif c['id'].startswith('X'):
            prd_expected.append((c['id'], c['provider']+' → '+c['consumer'], c['phase'], ', '.join(c['rules']), c['acceptance']))
        else:
            prd_expected.append((c['id'], c['acceptance']))
        fid = c.get('feature', c.get('consumer'))
        if fid:
            rows = table_rows(read(fs[fid]['path']+'/spec.md'), r'^\| [AX]\d\d \|')
            check((c['id'], c['phase'], c['acceptance']) in rows, 'FDD acceptance mismatch '+c['id'])
        contract = read(fs[fid]['path']+'/contract.md' if fid else 'docs/validation/release-contract.md')
        section = re.search(r'(?m)^#{2,3} '+re.escape(c['contract'])+r' \('+c['id']+r'\)\s*$(.*?)(?=^## |^### |\Z)', contract, re.M|re.S)
        check(section is not None and all(v in section.group(1) for v in (c['precondition'],c['procedure'],c['oracle']) + ((c['evidence'],) if fid else ())), 'contract content mismatch '+c['id'])
    check(Counter(prd_rows)==Counter(prd_expected),'PRD acceptance/rules mismatch')
    wave=state.get('currentWave')
    check(state.get('schemaVersion')==2,'invalid state schema version')
    check(type(wave) is int and 0<=wave<=6,'invalid currentWave')
    baseline=state.get('baselineCommit')
    check((wave==0 and baseline is None and state.get('baseline')=='proposed') or
          (type(wave) is int and wave>0 and bool(re.fullmatch(r'[0-9a-f]{40}',str(baseline))) and state.get('baseline')=='approved'), 'wave/baseline approval mismatch')
    check(state.get('releaseStatus') in ('planned','completed'),'invalid releaseStatus')
    if state.get('releaseStatus')=='completed':
        check(wave==6 and all(f['status']=='completed' for f in state['features']),'release before completion')
    status_by_id={f['id']:f['status'] for f in state['features']}
    check({x['id'] for x in state['features']}==set(fs) and len(state['features'])==len(fs),'state feature IDs mismatch')
    for f in state['features']:
        if f['id'] not in fs: continue
        check(f.get('wave')==fs[f['id']]['wave'],'state feature wave mismatch '+f['id'])
        if type(wave) is int:
            if f['wave']>wave: check(f['status']=='planned','future feature started '+f['id'])
            if f['wave']<wave and wave>0: check(f['status'] in ('merged_local','completed') or (f['status'] in ('needs_fix','implementing','ready_for_review','local_pass') and bool(f.get('mergedCommit'))),'previous wave not delivered '+f['id'])
        if f['status']!='planned':
            check(all(status_by_id.get(dep) in ('merged_local','completed') for dep in fs[f['id']]['dependsOn']) or f['status'] in ('needs_fix','merged_local','completed'), 'provider not merged '+f['id'])
        check(f['status'] in {'planned','implementing','ready_for_review','local_pass','merged_local','completed','needs_fix'},'bad state '+f['id'])
        if f['status']=='planned': check(not any(f.get(k) for k in ['latestEvaluation','implementationCommit','mergedCommit','pr','branch','implementerSession']), 'planned with evidence '+f['id'])
        if f['status']=='completed': check(all(f.get(k) for k in ['latestEvaluation','implementationCommit','mergedCommit','pr']), 'completed without evidence '+f['id'])
        if f.get('latestEvaluation'):
            p=(root/f['latestEvaluation']).resolve(); check(p.is_relative_to(root.resolve()) and p.is_file(),'invalid report path '+f['id'])
        check(f['integratedRequired']==any(c.get('consumer')==f['id'] and c['phase']=='integrated' for c in d['cross']),'integration state mismatch '+f['id'])
    expected_api={'/api/partner/events':('get',{'200','401'}),'/api/partner/events/{eventId}/purchases':('post',{'202','401','422','404','409'}),'/api/partner/tickets/{ticketId}':('get',{'200','401','404'})}
    try:
        check(set(api['paths'])==set(expected_api),'API routes mismatch')
        check(api['components']['securitySchemes']['PartnerKey']['name']=='X-Api-Key','API key header')
        for path,(method,codes) in expected_api.items():
            check(set(api['paths'][path][method]['responses'])==codes,'API status mismatch '+path)
    except KeyError as exc: errors.append(f'API incomplete {exc}')
    skills={p.parent.name for p in (root/'.agents/skills').glob('*/SKILL.md')}
    check(len(skills)>=10,'skills incomplete')
    for skill in skills: check(skill in tasks or skill in read('.agents/skills/README.md'),'skill not registered '+skill)
    # Relative Markdown links only, ignore code placeholders and remote sources.
    for path in root.rglob('*.md'):
        for target in re.findall(r'\]\(([^\s)]+)\)',path.read_text(encoding='utf-8')):
            if target.startswith(('http://','https://','#','mailto:')): continue
            target=target.split('#',1)[0]
            if target: check((path.parent/target).exists(), f'broken link {path.relative_to(root)} -> {target}')
    return errors

if __name__=='__main__':
    try: errors=validate(ROOT)
    except (ValueError, KeyError, TypeError, OSError) as exc: errors=[f'invalid document/state: {exc}']
    if errors:
        print('\n'.join('FAIL '+e for e in errors),file=sys.stderr);sys.exit(1)
    d=json.loads((ROOT/'docs/validation/traceability.json').read_text())
    print(f'PASS structural: {len(d["features"])} features; {len(d["criteria"])} local criteria; {len(d["cross"])} cross criteria; {len(d["process"])} process criteria')
    print('No runtime, independent evaluation, Mermaid rendering or PR history verified.')
