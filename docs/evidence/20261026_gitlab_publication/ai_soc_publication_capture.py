import datetime
import json
import os
from pathlib import Path
import subprocess
import sys

run_dir = Path('/tmp/ai_soc_gitlab_publication_run_path').read_text().strip()
label, cwd, *command = sys.argv[1:]
started = datetime.datetime.now().astimezone().isoformat()
result = subprocess.run(command, cwd=cwd, capture_output=True, text=True)
token = os.environ.get('GITLAB_TOKEN', '')
def redact(value):
    return value.replace(token, '[REDACTED]') if token else value
record = dict(started_at=started, finished_at=datetime.datetime.now().astimezone().isoformat(), cwd=cwd, command=command, exit_code=result.returncode, stdout=redact(result.stdout), stderr=redact(result.stderr))
Path(run_dir, label+'.json').write_text(json.dumps(record, ensure_ascii=False, indent=2)+'\n')
print(redact(result.stdout), end='')
print(redact(result.stderr), end='', file=sys.stderr)
print('EVIDENCE '+str(Path(run_dir,label+'.json'))+' EXIT '+str(result.returncode), flush=True)
sys.exit(result.returncode)
