#!/usr/bin/env python3
"""Check evaluation metadata, phase, coverage, Git history and project state; not evidence truth."""
import argparse
import datetime
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from validate_docs import validate as validate_documents
ROOT=Path(__file__).resolve().parents[1]

def validate(root, release=False):
    errors=validate_documents(root)
    def require(cond,msg):
        if not cond: errors.append(msg)
    def git(*args):
        return subprocess.run(['git','-C',str(root),*args],text=True,capture_output=True)
    data=json.loads((root/'docs/validation/traceability.json').read_text())
    state=json.loads((root/'state/project-state.json').read_text())
    sts={s['id']:s for s in state['features']}
    items=data['criteria']+data['cross']
    in_git=git('rev-parse','--is-inside-work-tree').returncode==0
    def ancestor(a,b):
        return bool(a and b and re.fullmatch('[0-9a-f]{40}|HEAD',str(a)) and re.fullmatch('[0-9a-f]{40}|HEAD',str(b)) and git('merge-base','--is-ancestor',a,b).returncode==0)
    def full_sha(value):
        return isinstance(value,str) and re.fullmatch('[0-9a-f]{40}',value) is not None
    baseline=state.get('baselineCommit')
    if state.get('currentWave',0)>0:
        require(in_git and full_sha(baseline) and ancestor(baseline,'HEAD'),'approved baseline not ancestor of HEAD')
    evaluator_sessions=set()
    historical_implementers=set()
    if release: require(in_git,'release requires Git history')
    if in_git: require(git('rev-parse','--is-shallow-repository').stdout.strip()=='false','full Git history required')
    for f in data['features']:
        fid=f['id']; s=sts[fid]; directory=root/f['path']/'reports'
        contracts={c['contract']:c['phase'] for c in items if c.get('feature',c.get('consumer'))==fid}
        valid_reports=[]
        for path in sorted(directory.glob('*.json')):
            rel=path.relative_to(root).as_posix(); md=path.with_suffix('.md'); prefix=f'{fid}/{path.name}'
            try: r=json.loads(path.read_text())
            except ValueError: errors.append(prefix+': invalid JSON');continue
            required=('feature','phase','date','commit','tool','model','evaluatorSession','implementerSession','clean','verdict','items')
            if not all(k in r for k in required): errors.append(prefix+': missing field');continue
            require(r['feature']==fid,prefix+': feature')
            require(r['phase'] in ('local','integrated'),prefix+': phase')
            try:
                date=datetime.datetime.fromisoformat(r['date'].replace('Z','+00:00'));require(date.utcoffset()==datetime.timedelta(0),prefix+': date must be UTC')
                require(date<=datetime.datetime.now(datetime.timezone.utc)+datetime.timedelta(minutes=5),prefix+': date in future')
            except (ValueError,TypeError): errors.append(prefix+': invalid date');continue
            require(bool(re.fullmatch('[0-9a-f]{40}',str(r['commit']))),prefix+': full SHA required')
            require(r['clean'] is True,prefix+': dirty checkout')
            require(all(isinstance(r[k],str) and r[k].strip() and '<' not in r[k] for k in ['tool','model','evaluatorSession','implementerSession']),prefix+': metadata empty')
            require(r['evaluatorSession']!=r['implementerSession'],prefix+': same evaluator/implementer session')
            require(r['evaluatorSession'] not in evaluator_sessions,prefix+': evaluator session reused')
            evaluator_sessions.add(r['evaluatorSession'])
            historical_implementers.add(r['implementerSession'])
            require(md.is_file(),prefix+': human report absent')
            if md.is_file():
                blocks=re.findall(r'(?ms)^```json[ \t]*\n(.*?)^```[ \t]*$',md.read_text())
                try: require(len(blocks)==1 and json.loads(blocks[0])==r,prefix+': Markdown JSON mirror mismatch')
                except ValueError: errors.append(prefix+': invalid Markdown JSON mirror')
            artifacts=r.get('artifacts',{})
            if not isinstance(artifacts,dict): errors.append(prefix+': invalid artifacts');continue
            artifact_paths=[]
            for name,digest in artifacts.items():
                artifact=(root/name).resolve()
                safe=artifact.is_relative_to(directory.resolve()) and artifact.is_file() and artifact not in (path.resolve(),md.resolve())
                require(safe,prefix+': artifact path absent/outside reports '+name)
                if safe:
                    require(hashlib.sha256(artifact.read_bytes()).hexdigest()==digest,prefix+': artifact hash mismatch '+name)
                    artifact_paths.append(artifact)
            if not isinstance(r['items'],list) or not all(isinstance(i,dict) and 'id' in i for i in r['items']): errors.append(prefix+': malformed items');continue
            ids=[i['id'] for i in r['items']]
            require(len(ids)==len(set(ids)) and set(ids)==set(contracts),prefix+': missing/duplicate/unexpected contract item')
            passed=True
            for i in r['items']:
                verdict=i.get('verdict');phase=contracts.get(i['id']);pending=r['phase']=='local' and phase=='integrated'
                if pending: require(verdict=='PENDING_INTEGRATION',prefix+': local report cannot pass integrated item');continue
                require(verdict in ('PASS','FAIL','BLOCKED'),prefix+': invalid item verdict')
                require(isinstance(i.get('evidence'),str) and bool(i['evidence'].strip()),prefix+': no evidence '+str(i['id']))
                if verdict!='PASS':passed=False
            require(r['verdict']==('PASS' if passed else 'FAIL'),prefix+': overall verdict inconsistent')
            if in_git:
                require(git('cat-file','-e',str(r['commit'])+'^{commit}').returncode==0,prefix+': SHA not found')
                creation_commits=[]
                for p in [path,md,*artifact_paths]:
                    pp=p.relative_to(root).as_posix(); log=git('log','--all','--format=%H','--',pp)
                    require(log.returncode==0 and len(set(log.stdout.splitlines()))==1,prefix+': report history must have one commit '+p.name)
                    require(git('diff','--quiet','HEAD','--',pp).returncode==0,prefix+': report modified')
                    if len(set(log.stdout.splitlines()))==1:
                        creation=log.stdout.strip();creation_commits.append(creation)
                        require(ancestor(r['commit'],creation) and ancestor(creation,'HEAD'),prefix+': report creation not descended from evaluated SHA or not in HEAD')
                require(len(set(creation_commits))==1,prefix+': report and artifacts not committed together')
                if baseline: require(ancestor(baseline,r['commit']),prefix+': evaluation predates baseline')
                if s.get('mergedCommit') and release:
                    require(git('merge-base','--is-ancestor',str(s['mergedCommit']),'HEAD').returncode==0,prefix+': merge not ancestor of release')
            else: require(False,prefix+': report present without Git')
            valid_reports.append((date,rel,r))
        for md in directory.glob('*.md'): require(md.with_suffix('.json').is_file(),f'{fid}: report JSON absent {md.name}')
        # Detect deleted reports from history, not merely existing files.
        if in_git:
            deleted=git('log','--all','--diff-filter=D','--name-only','--format=','--',f['path']+'/reports').stdout.splitlines()
            require(not any(x.endswith(('.md','.json')) for x in deleted),f'{fid}: report deletion detected')
        if valid_reports:
            newest=max(valid_reports,key=lambda x:(x[0],x[1]));require(s.get('latestEvaluation')==newest[1],fid+': state not pointing to newest JSON report')
            require(len({x[0] for x in valid_reports})==len(valid_reports),fid+': duplicate evaluation timestamp')
            r=newest[2]; candidate=s.get('implementationCommit'); merged=s.get('mergedCommit')
            if s['status'] in ('local_pass','merged_local','completed'):
                require(full_sha(candidate) and r['implementerSession']==s.get('implementerSession'),fid+': report implementer/candidate mismatch')
                if r['phase']=='local': require(r['commit']==candidate,fid+': local evaluated SHA differs from implementationCommit')
                else:
                    require(s['status']=='completed' or s['status']=='merged_local',fid+': integrated report before merge')
                    require(any(x[2]['phase']=='local' and x[2]['commit']==candidate and x[2]['verdict']=='PASS' and x[2]['implementerSession']==s.get('implementerSession') and x[0]<newest[0] for x in valid_reports),fid+': missing prior local PASS for candidate')
                    require(ancestor(merged,r['commit']) and ancestor(r['commit'],'HEAD'),fid+': integrated SHA not on merged release history')
                    for provider in sts.values():
                        require(ancestor(provider.get('mergedCommit'),r['commit']),fid+': integrated SHA missing merged '+provider['id'])
                if s['status'] in ('merged_local','completed'):
                    require(full_sha(merged) and ancestor(candidate,merged) and ancestor(merged,'HEAD'),fid+': merge does not contain evaluated implementation')
                    require(bool(s.get('pr')),fid+': missing PR')
                if release: require(ancestor(r['commit'],'HEAD'),fid+': evaluated SHA not ancestor of release')
            if s['status'] in ('local_pass','merged_local','completed'):
                require(newest[2]['verdict']=='PASS',fid+': state approved but report failed')
            if s['status']=='completed' and s['integratedRequired']:
                require(newest[2]['phase']=='integrated',fid+': integrated report required')
        else:
            require(not s.get('latestEvaluation'),fid+': dangling report pointer')
            require(s['status'] not in ('local_pass','merged_local','completed'),fid+': approved state without report')
        if release:
            require(s['status']=='completed' and bool(valid_reports),fid+': release incomplete')
            require(all(s.get(k) for k in ('mergedCommit','implementationCommit','pr')),fid+': missing merge/PR evidence')
    require(not (evaluator_sessions & ({s.get('implementerSession') for s in sts.values()} | historical_implementers)),'evaluator session also used as implementer')
    if release: require(state.get('releaseStatus')=='completed' and state.get('currentWave')==6,'release state incomplete')
    return errors

def main():
    p=argparse.ArgumentParser();p.add_argument('--release',action='store_true');a=p.parse_args()
    try: errors=validate(ROOT,a.release)
    except (ValueError,KeyError,TypeError,OSError) as exc: errors=[f'invalid evidence/state: {exc}']
    if errors: print('\n'.join('FAIL '+e for e in errors),file=sys.stderr);return 1
    print('PASS evidence structure/history for requested phase. No authenticity or GitHub PR overlap inferred.');return 0
if __name__=='__main__':sys.exit(main())
