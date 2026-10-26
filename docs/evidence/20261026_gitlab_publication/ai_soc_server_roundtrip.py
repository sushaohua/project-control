"""Clone and restore from the SSH server, then compare exact commits and rules."""
import json
from pathlib import Path
import subprocess
import sys

source = Path(sys.argv[1]).resolve()
destination = Path(sys.argv[2]).resolve()
sys.path.insert(0, str(source / 'tools'))
import workspace as w

commands = [
    (source, ['git', 'clone', '--branch', 'main', 'ssh://git@192.168.77.113:2222/sushaohua/ai-soc-workspace.git', str(destination)]),
    (destination, ['python3', 'tools/workspace.py', 'restore']),
    (destination, ['python3', 'tools/workspace.py', 'verify']),
    (source, ['python3', '/tmp/ai_soc_publication_audit.py', str(source), str(destination)]),
]
for cwd, command in commands:
    print(json.dumps(dict(cwd=str(cwd), command=command)), flush=True)
    result = subprocess.run(command, cwd=cwd, env=w.credential_env(source), capture_output=True, text=True)
    print(w.redact(result.stdout), end='', flush=True)
    print(w.redact(result.stderr), end='', flush=True)
    print('EXIT', result.returncode, flush=True)
    if result.returncode:
        sys.exit(result.returncode)
print('SERVER ROUNDTRIP COMPLETE', flush=True)
