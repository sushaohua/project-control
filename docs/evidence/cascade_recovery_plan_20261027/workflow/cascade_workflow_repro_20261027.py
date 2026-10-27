import copy
import hashlib
import importlib.util
import json
import shutil
import subprocess
from pathlib import Path
import yaml
ROOT=Path('/home/sushaohua/workspace/ai_soc_project')
TMP=Path('/tmp/cascade_workflow_fixture_20261027')
TMP.mkdir(exist_ok=True)
for name in ('project-control/.agents','project-control/docs'):
    dst=TMP/name
    if not dst.exists():
        shutil.copytree(ROOT/name,dst)
for name in ('soc-ap','mcu-p3','test_harness'):
    dst=TMP/name
    if not dst.exists(): dst.symlink_to(ROOT/name,target_is_directory=True)
ms=TMP/'project-control/.agents/kanban/milestones/marlin_ms07_20261007_214108.md'
s=ms.read_text()
s=s.replace('  acknowledgement: COORD accepted MS-07: Genuine physical MCU HIL closed-loop verified under HW-G5 with 0 noise, 10/10 valid response frames (RTT avg 6.14ms)', '  acknowledgement: "COORD accepted MS-07: Genuine physical MCU HIL closed-loop verified under HW-G5 with 0 noise, 10/10 valid response frames (RTT avg 6.14ms)"')
ms.write_text(s)
spec=importlib.util.spec_from_file_location('graph',ROOT/'project-control/tools/check_task_graph.py')
g=importlib.util.module_from_spec(spec); spec.loader.exec_module(g)
cards,report=g.check(TMP)
print('baseline_with_only_MS07_yaml_quoted',json.dumps({'errors':report['errors'],'count':len(cards),'MCQ_scanned':[k for k in cards if k.startswith('MCQ')],'MS07_Done':cards['MS-07']['status'],'MS07_prerequisites':{k:cards[k]['status'] for k in cards['MS-07']['depends_on']}}))
# In-memory readiness probe: keep assigned distinct sessions; replace bindings by bogus strings and expired lease.
c=copy.deepcopy(cards['V2-P01A'])
c['base_commit']='not-a-commit';c['dispatch_binding']['source_commit']='not-a-commit';c['dispatch_binding']['workspace_diff_sha256']='not-a-sha256'
c['lease']['expires_at']='2000-01-01T00:00:00+08:00'
c['blocked']=True
print('opaque_expired_blocked_readiness',g.readiness_blockers(c,cards))
# Every dependency passes with no real accepted file/version.
c=copy.deepcopy(cards['V2-P01C'])
for d in c['dependency_conditions']:
    d['accepted_version']='not-an-accepted-version';d['acceptance_evidence']='nonexistent-report.md'
print('bogus_dependency_binding_readiness',g.readiness_blockers(c,cards))
# Done state is accepted even with author-as-reviewer, REJECTED and absent report.
p=TMP/'project-control/.agents/kanban/microtasks/minimc_v2/V2-P01A.md'
original=p.read_text(); c=g.read_header(p)
c['review_assignments']['reviewer_sessions'][0].update(session=c['owner'],decision='REJECTED',artifact_version=None,evidence='missing-review-report.md')
p.write_text('---\n'+yaml.safe_dump(c,allow_unicode=True,sort_keys=False)+'---\nfixture\n')
_,r=g.check(TMP)
print('Done_with_self_rejected_missing_review_errors',r['errors'])
p.write_text(original)
# Two independent cards: wildcard and concrete child both write same file but no equal string.
paths=[TMP/'project-control/.agents/kanban/microtasks/minimc_v2'/f'{k}.md' for k in ('V2-P01A','V2-P01B')]
originals=[p.read_text() for p in paths]
for p,scope in zip(paths,('docs/specs/**','docs/specs/protocol_selection_20261020.md')):
    c=g.read_header(p); c['write_scope']['project-control']=[scope];c['allowed_paths']=[repo+'/'+item for repo,items in c['write_scope'].items() for item in items]
    p.write_text('---\n'+yaml.safe_dump(c,allow_unicode=True,sort_keys=False)+'---\nfixture\n')
_,r=g.check(TMP)
print('glob_scope_overlap_errors',r['errors'])
for p,s in zip(paths,originals):p.write_text(s)
# Candidate with arbitrary/bogus repository pins is accepted by artifact check.
p=TMP/'project-control/docs/releases/minimc_v2_offline_candidate.yaml'; original=p.read_text(); d=yaml.safe_load(original)
d['repositories']={'soc-ap':{'commit':'0'*40},'test_harness':{'commit':'1'*40},'project-control':{'commit':'2'*40}}
p.write_text(yaml.safe_dump(d,allow_unicode=True,sort_keys=False))
r=g.artifact_check(cards['V2-P0506'],TMP)
print('nonexistent_candidate_commits_artifact_errors',r['errors'])
p.write_text(original)
