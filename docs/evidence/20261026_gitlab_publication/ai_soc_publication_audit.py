"""Read-only comparison of a real GitLab restore with its publishing workspace."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import urllib.parse

source, restored = (Path(arg).resolve() for arg in sys.argv[1:3])
sys.path.insert(0, str(source / 'tools'))
import workspace as w

def git(path, *args):
    return w.git(path, *args).stdout.strip()

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

manifest = w.load_manifest(source)
assert json.loads((restored / 'workspace.json').read_text()) == manifest
expected_root = w.root_git(source, 'rev-parse', 'HEAD').stdout.strip()
assert git(restored, 'rev-parse', 'HEAD') == expected_root
assert not git(restored, 'status', '--porcelain=v1')
assert git(restored, 'branch', '--show-current') == manifest['workspace_project']['branch']
assert git(restored, 'rev-parse', 'HEAD^{tree}') == w.root_git(source, 'rev-parse', 'HEAD^{tree}').stdout.strip()
states = w.verify(restored, manifest)
api = w.GitLab(manifest['gitlab_url'])
entry = manifest['workspace_project']
targets = [dict(path=entry['path'], branch=entry['branch'], commit=expected_root), *manifest['repositories']]
remote = []
for target in targets:
    project = api.request('/projects/' + urllib.parse.quote(entry['namespace'] + '/' + target['path'], safe=''))
    branch = api.request('/projects/' + str(project['id']) + '/repository/branches/' + urllib.parse.quote(target['branch'], safe=''))
    actual = branch['commit']['id']
    assert actual == target['commit'], (target['path'], actual, target['commit'])
    remote.append(dict(project=project['web_url'], branch=target['branch'], commit=actual, visibility=project['visibility']))
    if target['path'] != entry['path']:
        assert git(restored / target['path'], 'rev-parse', 'HEAD^{tree}') == git(source / target['path'], 'rev-parse', 'HEAD^{tree}')

agents = restored / '.agents'
assert agents.is_symlink() and os.readlink(agents) == 'project-control/.agents'
assert agents.resolve() == (restored / 'project-control/.agents').resolve()
rule_files = [name for name in w.git(source / 'project-control', 'ls-files', '-z', '.agents').stdout.split('\0') if name]
hashes = {}
for name in rule_files:
    assert sha(source / 'project-control' / name) == sha(restored / 'project-control' / name), name
    hashes[name] = sha(restored / 'project-control' / name)
task = restored / 'project-control/.agents/kanban/microtasks/minimc_v2/V2-P01D.md'
assert re.search(r'^status: InProgress$', task.read_text(), re.MULTILINE)
for name in ('AGENTS.md', 'README.md', 'WORKSPACE.md', 'workspace.json', 'tools/workspace.py'):
    assert sha(source / name) == sha(restored / name), name
print(json.dumps(dict(source=str(source), restored=str(restored), root_commit=expected_root, states=states, remote=remote, canonical_agents_link=os.readlink(agents), canonical_agents_file_count=len(hashes), canonical_agents_sha256=hashes, V2_P01D='InProgress', result='server publication and restore match; no engineering acceptance'), ensure_ascii=False, indent=2))
