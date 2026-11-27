#!/usr/bin/env python3
"""Negative tests for the document and evidence gates; synthetic evidence never leaves temp Git."""
import datetime
import json
import shutil
import subprocess
import tempfile
from pathlib import Path
from validate_docs import validate as docs
from validate_evidence import validate as evidence
ROOT=Path(__file__).resolve().parents[1]

def main():
    with tempfile.TemporaryDirectory() as tmp:
        root=Path(tmp)/'baseline'
        shutil.copytree(ROOT,root,ignore=shutil.ignore_patterns('__pycache__','.git'))
        state_path=root/'state/project-state.json';s=json.loads(state_path.read_text())
        s.update(currentWave=0,baseline='proposed',baselineCommit=None)
        initial=json.dumps(s);state_path.write_text(initial)
        assert not docs(root)
        assert not evidence(root)
        assert evidence(root,True)
        path=root/'requirements-matrix.csv'; original=path.read_bytes(); path.write_bytes(original+b'\ninvalid,row\n')
        assert any('CSV inconsistent' in e for e in docs(root));path.write_bytes(original)
        s=json.loads(initial);s['features'][0]['status']='local_pass';state_path.write_text(json.dumps(s))
        assert any('approved state without report' in e for e in evidence(root));state_path.write_text(initial)
        def git(*args):
            return subprocess.run(['git','-C',str(root),*args],check=True,capture_output=True,text=True).stdout.strip()
        git('init','-q');git('config','user.name','Synthetic fixture');git('config','user.email','fixture@example.invalid');git('add','.');git('commit','-qm','Baseline fixture')
        sha=git('rev-parse','HEAD'); data=json.loads((root/'docs/validation/traceability.json').read_text());f=data['features'][0];fid=f['id'];directory=root/f['path']/'reports';report=directory/'fixture.json';md=report.with_suffix('.md')
        items=[{'id':c['contract'],'verdict':'PENDING_INTEGRATION' if c['phase']=='integrated' else 'PASS','evidence':'Synthetic fixture, not product evidence'} for c in data['criteria']+data['cross'] if c.get('feature',c.get('consumer'))==fid]
        r={'feature':fid,'phase':'local','date':datetime.datetime.now(datetime.timezone.utc).isoformat(),'commit':sha,'tool':'fixture','model':'fixture','evaluatorSession':'fixture-evaluator','implementerSession':'fixture-builder','clean':True,'verdict':'PASS','items':items}
        artifact=directory/'fixture-output.txt';artifact.write_text('Synthetic artifact, not product evidence')
        import hashlib
        r['artifacts']={artifact.relative_to(root).as_posix():hashlib.sha256(artifact.read_bytes()).hexdigest()}
        report.write_text(json.dumps(r));md.write_text('# Synthetic fixture only\n\n```json\n'+json.dumps(r)+'\n```\n');s.update(currentWave=1,baseline='approved',baselineCommit=sha);s['features'][0].update(status='local_pass',latestEvaluation=report.relative_to(root).as_posix(),implementationCommit=sha,implementerSession='fixture-builder');state_path.write_text(json.dumps(s));git('add','.');git('commit','-qm','Synthetic evidence fixture')
        assert not docs(root),docs(root)
        assert not evidence(root),evidence(root)
        original_artifact=artifact.read_text();artifact.write_text('tampered')
        assert any('artifact hash mismatch' in e for e in evidence(root)),evidence(root)
        artifact.write_text(original_artifact)
        # State substitutions must fail even when both SHAs exist in Git.
        clean_state=state_path.read_text(); mutated=json.loads(clean_state)
        mutated['features'][0]['implementationCommit']=git('rev-parse','HEAD');state_path.write_text(json.dumps(mutated))
        assert any('local evaluated SHA differs' in e for e in evidence(root)),evidence(root)
        mutated=json.loads(clean_state);mutated['features'][0]['implementerSession']='wrong-builder';state_path.write_text(json.dumps(mutated))
        assert any('report implementer/candidate mismatch' in e for e in evidence(root)),evidence(root)
        mutated=json.loads(clean_state);mutated['features'][0].update(status='merged_local',mergedCommit='0'*40,pr='synthetic');state_path.write_text(json.dumps(mutated))
        assert any('merge does not contain evaluated implementation' in e for e in evidence(root)),evidence(root)
        state_path.write_text(clean_state)
        original_md=md.read_text();md.write_text(original_md.replace('fixture-evaluator','different-evaluator'))
        assert any('Markdown JSON mirror mismatch' in e for e in evidence(root)),evidence(root)
        md.write_text(original_md)
        r['evaluatorSession']=r['implementerSession'];report.write_text(json.dumps(r));errs=evidence(root);assert any('same evaluator' in e for e in errs) and any('report modified' in e for e in errs),errs
        git('add','.');git('commit','-qm','Tamper fixture');assert any('report history must have one commit' in e for e in evidence(root))
        print('PASS baseline negative tests: CSV mismatch, incomplete release, approved state without report, same session, SHA/session/merge mismatch, Markdown/artifact mismatch, dirty and committed report tampering.')
if __name__=='__main__':main()
