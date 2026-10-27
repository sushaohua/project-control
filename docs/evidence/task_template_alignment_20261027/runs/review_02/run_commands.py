from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import subprocess


def run_one(index, command):
    started = datetime.now(timezone.utc).isoformat()
    result = subprocess.run(command, cwd=str(root), capture_output=True)
    ended = datetime.now(timezone.utc).isoformat()
    prefix = output / ('command_%02d' % index)
    stdout = prefix.with_suffix('.stdout.log')
    stderr = prefix.with_suffix('.stderr.log')
    stdout.write_bytes(result.stdout)
    stderr.write_bytes(result.stderr)
    return {'command': command, 'cwd': str(root), 'started': started, 'ended': ended,
            'exit_code': result.returncode, 'stdout_path': str(stdout.relative_to(root)),
            'stderr_path': str(stderr.relative_to(root)),
            'stdout_sha256': hashlib.sha256(result.stdout).hexdigest(),
            'stderr_sha256': hashlib.sha256(result.stderr).hexdigest()}


root = Path.cwd()
output = root / 'docs/evidence/task_template_alignment_20261027/runs/review_02'
author = output.parent / 'author_02'
paths = [item['path'] for item in json.loads((author / 'candidate_manifest.json').read_text())]
commands = [
    ['python3', '-B', str(output / 'independent_checks.py')],
    ['git', '-c', 'core.whitespace=blank-at-eol,blank-at-eof,space-before-tab,cr-at-eol',
     'diff', '--check', '--'] + paths,
    ['cat', '../AGENTS.md', 'manifest.yaml', '.agents/rules/codex_qa_review.md'],
    ['cat'] + paths,
    ['sed', '-n', '68,96p', 'tools/check_task_graph.py'],
    ['sed', '-n', '80,119p', '.agents/rules/04_公共看板与读写协议.md'],
    ['sed', '-n', '124,155p;176,181p',
     'docs/specs/ap_mc_formal_protocol_v2_0_multidevice_routing_draft_20261015.md'],
]
records = [run_one(index, command) for index, command in enumerate(commands, 1)]
(output / 'commands.json').write_text(json.dumps(records, ensure_ascii=False, indent=2) + '\n')
print(json.dumps([{'command_number': index, 'exit_code': item['exit_code']}
                  for index, item in enumerate(records, 1)], indent=2))
