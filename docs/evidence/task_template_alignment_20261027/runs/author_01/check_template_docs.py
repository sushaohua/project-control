from pathlib import Path
import hashlib,json,re,subprocess
import yaml

root=Path('/home/sushaohua/workspace/ai_soc_project/project-control')
paths=['.agents/rules/templates/任务卡模板.md','.agents/rules/templates/角色任务提示词.md','docs/guides/templates/task_run_record.md','.agents/rules/templates/QA审查报告模板.md','.agents/rules/qa_audit_checklist_guide_20261013_115611.md','.agents/rules/codex_qa_review.md','docs/guides/minimc_v2_task_execution.md']
class UniqueLoader(yaml.SafeLoader):
    pass

def unique_mapping(loader,node,deep=False):
    mapping={}
    for key_node,value_node in node.value:
        key=loader.construct_object(key_node,deep=deep)
        if key in mapping:
            raise ValueError('duplicate YAML key: '+str(key))
        mapping[key]=loader.construct_object(value_node,deep=deep)
    return mapping
UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,unique_mapping)
checks=[]; hashes={}; documents={}
for relative in paths:
    path=root/relative; text=path.read_text(); documents[relative]=text
    hashes[relative]=hashlib.sha256(path.read_bytes()).hexdigest()
    blocks=[]
    if text.startswith('---\n'):
        blocks.append(text.split('---',2)[1])
    blocks.extend(re.findall(r'```yaml\n(.*?)\n```',text,re.S))
    parsed=[yaml.load(block,Loader=UniqueLoader) for block in blocks]
    checks.append({'path':relative,'yaml_blocks':len(parsed),'yaml_unique_keys':True})
    assert all(line == line.rstrip(' \t') for line in text.splitlines()),relative+' trailing spaces/tabs'
    for target in re.findall(r'(?<!!)\[[^\]]*\]\(([^)]+)\)',text):
        if '://' in target or target.startswith('#'):
            continue
        resolved=(path.parent/target.split('#',1)[0]).resolve()
        if not resolved.exists():
            raise AssertionError('broken link: '+relative+' -> '+target)
card=yaml.load(re.findall(r'```yaml\n(.*?)\n```',documents[paths[0]],re.S)[0],Loader=UniqueLoader)
run=yaml.load(re.findall(r'```yaml\n(.*?)\n```',documents[paths[2]],re.S)[0],Loader=UniqueLoader)
qa=yaml.load(re.findall(r'```yaml\n(.*?)\n```',documents[paths[3]],re.S)[0],Loader=UniqueLoader)
assert card['status']=='Backlog' and card['owner'] is None and card['verification_scope'] is None
assert card['review_assignments']['reviewer_sessions']==[] and card['acceptance']['record'] is None
assert run['actual_result']=='not-executed' and run['commands']==[] and run['case_results']==[]
assert qa['decision'] is None and qa['review_status']=='pending' and qa['actual_session'] is None
assert qa['process_audit']=='not-executed' and qa['result_check']=='not-executed'
assert '[x]' not in documents[paths[3]]
for relative in paths[:2]:
    data=(root/relative).read_bytes()
    assert data.count(b'\r\n')==data.count(b'\n'),relative+' line ending drift'
assert len(list((root/'.agents/kanban/microtasks/minimc_v2').glob('V2-*.md')))==20
command=['git','-c','core.whitespace=blank-at-eol,blank-at-eof,space-before-tab,cr-at-eol','-C',str(root),'diff','--check','--',*paths]
result=subprocess.run(command,text=True,capture_output=True)
if result.returncode:
    raise AssertionError(result.stdout+result.stderr)
report={'scope':'documentation checks only; not task readiness/approval or HIL','checks':checks,'blank_defaults_safe':True,'template_CRLF_preserved':True,'active_v2_count':20,'markdown_links_exist':True,'diff_check':{'command':command,'exit_code':result.returncode,'stdout':result.stdout,'stderr':result.stderr},'candidate_sha256':hashes}
print(json.dumps(report,ensure_ascii=False,indent=2))
