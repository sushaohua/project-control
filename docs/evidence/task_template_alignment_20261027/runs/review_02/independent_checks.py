from pathlib import Path
import difflib
import hashlib
import json
import re
import sys
import yaml


class UniqueLoader(yaml.SafeLoader):
    pass


def mapping(loader, node, deep=False):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        assert key not in result, 'duplicate YAML key: ' + str(key)
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


def digest(data):
    return hashlib.sha256(data).hexdigest()


def parse_blocks(content):
    blocks = re.findall(r'^```yaml\n(.*?)^```', content, re.M | re.S)
    if content.startswith('---\n'):
        blocks.insert(0, content.split('---', 2)[1])
    return [yaml.load(block, Loader=UniqueLoader) for block in blocks]


def check_file(item):
    path = root / item['path']
    data = path.read_bytes()
    assert digest(data) == item['candidate_sha256'], str(path)
    old = author.parent / 'author_01' / 'before' / item['path']
    before = old.read_bytes() if old.exists() else b''
    if item['before_sha256'] is not None:
        assert digest(before) == item['before_sha256'], str(old)
        assert bool(b'\r\n' in before) == bool(b'\r\n' in data)
    else:
        assert not old.exists(), 'unexpected before file'
    text = data.decode().replace('\r\n', '\n')
    assert all(line == line.rstrip(' \t') for line in text.splitlines())
    assert data.count(b'\r\n') in (0, data.count(b'\n'))
    parsed[item['path']] = parse_blocks(text)
    links = re.findall(r'(?<!!)\[[^\]]*\]\(([^)]+)\)', text)
    for target in links:
        if '://' not in target and not target.startswith('#'):
            assert (path.parent / target.split('#')[0]).exists(), target
    old_text = before.decode().replace('\r\n', '\n')
    delta = difflib.unified_diff(old_text.splitlines(True), text.splitlines(True),
                                'before/' + item['path'], 'after/' + item['path'])
    diffs.extend(delta)
    return dict(item, yaml_blocks=len(parsed[item['path']]), links=len(links),
                crlf=data.count(b'\r\n'), lf=data.count(b'\n'))


def check_defaults():
    card = parsed['.agents/rules/templates/任务卡模板.md'][1]
    fields = parsed['.agents/rules/templates/任务卡模板.md'][2]
    run = parsed['docs/guides/templates/task_run_record.md'][0]
    qa = parsed['.agents/rules/templates/QA审查报告模板.md'][1]
    policy = parsed['.agents/rules/codex_qa_review.md'][1]
    assignment = card['review_assignments']
    assert set(policy['review_assignments']['reviewer_sessions'][0]) == set(fields['reviewer_session_fields'])
    assert card['status'] == 'Backlog' and card['blocked'] is False
    assert card['scope_status'] == 'unmapped'
    assert card['owner'] is None and card['verification_scope'] is None
    assert card['reviewer'] == [] and assignment['reviewer_sessions'] == []
    assert all(assignment[key] is None for key in assignment if key not in ('not_applicable', 'reviewer_sessions'))
    assert all(value is None for value in card['acceptance'].values())
    assert run['actual_result'] == 'not-executed'
    assert run['commands'] == [] and run['case_results'] == []
    assert run['independent_reviews'] == []
    assert qa['review_status'] == 'pending' and qa['decision'] is None
    assert qa['process_audit'] == qa['result_check'] == 'not-executed'
    assert qa['actual_session'] is None and qa['reviewed_artifacts'] == []
    assert '[x]' not in (root / '.agents/rules/templates/QA审查报告模板.md').read_text()


root = Path.cwd()
out = root / 'docs/evidence/task_template_alignment_20261027/runs/review_02'
author = out.parent / 'author_02'
UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, mapping)
manifest = json.loads((author / 'candidate_manifest.json').read_text())
assert len(manifest) == 7 and len({item['path'] for item in manifest}) == 7
parsed = {}
diffs = []
checks = [check_file(item) for item in manifest]
check_defaults()
delta = ''.join(diffs)
assert delta == (author / 'candidate.patch').read_text(), 'author patch does not match exact 7 candidates'
(out / 'independent_candidate.patch').write_text(delta)
result = {'scope': '7 documentation candidates only; no engineering or HIL acceptance',
          'python': sys.version, 'pyyaml': yaml.__version__, 'checks': checks,
          'candidate_manifest_sha256': digest((author / 'candidate_manifest.json').read_bytes()),
          'author_patch_matches_independent_diff': True,
          'yaml_unique_keys': True, 'blank_defaults_safe': True,
          'reviewer_object_schema_consistent': True, 'relative_markdown_links_exist': True,
          'line_endings_preserved': True, 'trailing_spaces_tabs_absent': True}
print(json.dumps(result, ensure_ascii=False, indent=2))
