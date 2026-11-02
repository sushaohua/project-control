import hashlib, json, re
from pathlib import Path
root = Path.cwd()
base = root / 'project-control/docs/evidence/twin_task_alignment_20261029/runs/author_01'
manifest_path = base / 'candidate_manifest.json'
manifest_bytes = manifest_path.read_bytes()
manifest = json.loads(manifest_bytes)
missing = []
mismatch = []
verified = {}
for rel, expected in manifest.items():
    path = root / rel
    if not path.is_file():
        missing.append(rel)
        continue
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    verified[rel] = {'expected_sha256': expected, 'actual_sha256': actual}
    if actual != expected:
        mismatch.append({'path': rel, 'expected': expected, 'actual': actual})
inventory = json.loads((base / 'input_inventory.json').read_text())
def yaml_scalar(path, field):
    match = re.search(r'^' + re.escape(field) + r':\s*(.*?)\s*$', path.read_text(), re.M)
    return None if match is None else match.group(1)
status_drift = []
blocked_drift = []
done_hash_drift = []
for card_id, item in inventory.items():
    path = root / item['path']
    if not path.is_file():
        status_drift.append({'id': card_id, 'reason': 'missing'})
        continue
    current_status = yaml_scalar(path, 'status')
    current_blocked = yaml_scalar(path, 'blocked')
    if current_status != item['status']:
        status_drift.append({'id': card_id, 'before': item['status'], 'current': current_status})
    expected_blocked = str(item['blocked']).lower()
    if current_blocked != expected_blocked:
        blocked_drift.append({'id': card_id, 'before': expected_blocked, 'current': current_blocked})
    if item['status'] == 'Done':
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != item['sha256']:
            done_hash_drift.append({'id': card_id, 'expected': item['sha256'], 'actual': actual})
twin_paths = sorted((root / 'project-control/.agents/kanban/microtasks/vmware_soc_twin').glob('TWIN-*.md'))
twin_checks = []
for path in twin_paths:
    twin_checks.append({'id': yaml_scalar(path, 'id'), 'status': yaml_scalar(path, 'status'), 'blocked': yaml_scalar(path, 'blocked'), 'owner': yaml_scalar(path, 'owner'), 'lease': yaml_scalar(path, 'lease')})
coverage = json.loads((root / 'project-control/docs/evidence/twin_task_alignment_20261029/task_coverage.json').read_text())
result = {
    'candidate_manifest_sha256': hashlib.sha256(manifest_bytes).hexdigest(),
    'manifest_entries': len(manifest),
    'missing': missing,
    'hash_mismatches': mismatch,
    'input_card_count': len(inventory),
    'status_drift': status_drift,
    'blocked_drift': blocked_drift,
    'done_hash_drift': done_hash_drift,
    'twin_card_count': len(twin_checks),
    'twin_cards': twin_checks,
    'coverage_count': len(coverage),
    'coverage_status_counts': {},
    'consistency_errors': json.loads((base / 'consistency.json').read_text()).get('errors', []),
    'new_broken_links': json.loads((base / 'consistency.json').read_text()).get('new_broken_links', [])
}
for item in coverage.values():
    result['coverage_status_counts'][item['status']] = result['coverage_status_counts'].get(item['status'], 0) + 1
outdir = root / 'project-control/docs/evidence/twin_task_alignment_20261029/runs/qa_01'
(outdir / 'reviewed_file_hashes.json').write_text(json.dumps(verified, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(result, ensure_ascii=False, indent=2))
failed = bool(missing or mismatch or status_drift or blocked_drift or done_hash_drift or len(twin_checks) != 16 or any(item['status'] != 'Backlog' or item['blocked'] != 'false' or item['owner'] != 'null' or item['lease'] != 'null' for item in twin_checks) or len(coverage) != 102 or result['consistency_errors'] or result['new_broken_links'])
raise SystemExit(1 if failed else 0)
