"""记录独立黑盒调查的命令、HTTP 与浏览器原始证据；不构建、刷写或注入故障。"""
import base64
import datetime
import hashlib
import http.client
import json
import pathlib
import subprocess
import time
import urllib.error
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent
HOST = 'sushaohua@192.168.77.134'
DEBUG = pathlib.Path('/mnt/c/Users/EDY/AppData/Local/Temp/aisoc_build_20261105_001')


def record(case, action, data):
    """追加事件；case、action 为标识，data 为客观数据；返回记录，无业务副作用。"""
    event = dict(case_id=case, action_id=action, utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), monotonic_ns=time.monotonic_ns(), data=data)
    with (ROOT / 'action_timeline.jsonl').open('a') as stream:
        stream.write(json.dumps(event, ensure_ascii=False) + '\n')
    return event


def command(name, args, limit=20):
    """执行有界采证命令；name 为文件名，args 为参数列表，limit 为秒；返回进程结果。"""
    start = record('AUDIT', name + '_start', {'argv': args})
    try:
        result = subprocess.run(args, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=limit)
    except subprocess.TimeoutExpired as error:
        (ROOT / (name + '_timeout.log')).write_bytes(error.output or b'')
        record('AUDIT', name + '_timeout', {'limit_seconds': limit})
        raise
    (ROOT / (name + '.log')).write_bytes(result.stdout)
    record('AUDIT', name + '_end', {'exit_code': result.returncode, 'start': start['utc'], 'sha256': hashlib.sha256(result.stdout).hexdigest()})
    return result


def remote(name, script):
    """通过已授权 SSH 采证；name 为证据名，script 为远端命令；返回命令结果。"""
    return command(name, ['ssh', '-o', 'BatchMode=yes', '-o', 'ConnectTimeout=8', HOST, script])


def request(case, method, path, body=None):
    """记录公开 HTTP 交互；case 为用例，method/path 为入口，body 为可选 JSON；返回响应记录。"""
    payload = None if body is None else json.dumps(body).encode()
    start = record(case, 'http_start', {'method': method, 'path': path, 'body': body})
    req = urllib.request.Request('http://192.168.77.134:8080' + path, data=payload, method=method, headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=12) as response:
            result = {'status': response.status, 'headers': dict(response.headers), 'body': response.read().decode(errors='replace')}
    except urllib.error.HTTPError as error:
        try:
            body_bytes = error.read()
            read_error = None
        except http.client.IncompleteRead as incomplete:
            body_bytes = incomplete.partial
            read_error = str(incomplete)
        result = {'status': error.code, 'headers': dict(error.headers), 'body': body_bytes.decode(errors='replace'), 'read_error': read_error}
    except Exception as error:
        result = {'error': str(error)}
    result['elapsed_ms'] = (time.monotonic_ns() - start['monotonic_ns']) / 1000000
    record(case, 'http_end', result)
    return result


def debug_snapshot(label):
    """保存现有受控采集器文件的完整前缀；label 为阶段名；返回字节数及哈希，不争抢 COM。"""
    result = {}
    for node in ['mc', 'th']:
        source = DEBUG / (node + '_debug_raw.log')
        data = source.read_bytes()
        (ROOT / (label + '_' + node + '_debug_raw.log')).write_bytes(data)
        result[node] = {'source': str(source), 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}
    record('AUDIT', 'debug_snapshot_' + label, result)
    return result


def baseline(label):
    """保存阶段运行身份与只读状态；label 为阶段名；返回空值，证据写入本 run。"""
    remote(label + '_runtime', '''date -u +%FT%TZ
hostname
for f in /tmp/aisoc_twin_logs/*.pid; do p=$(cat "$f"); echo "$f $p"; readlink /proc/$p/exe; sha256sum /proc/$p/exe; ps -p "$p" -o pid,lstart,args; tr '\\0' '\\n' < /proc/$p/environ | sed -n '/^AISOC_/p'; done
cat /tmp/aisoc_twin_logs/runtime.env
cd /home/sushaohua/tmp/ai_soc_project/soc-ap
git rev-parse HEAD
git status --porcelain
sha256sum browser_hmi/first_release/index.html browser_hmi/first_release/app.js browser_hmi/first_release/styles.css /tmp/aisoc_twin_logs/web_root/index.html /tmp/aisoc_twin_logs/web_root/app.js /tmp/aisoc_twin_logs/web_root/styles.css
ls -l /dev/serial/by-id/ /dev/ttyUSB0
fuser /dev/ttyUSB0
stty -F /dev/ttyUSB0 -a
pgrep -af '[h]w_sampler.py' || true
''')
    for name in ['forward_service', 'device_manager', 'ui_gateway']:
        remote(label + '_' + name, 'cat /tmp/aisoc_twin_logs/' + name + '.log')
    debug_snapshot(label)
    request('BASE-02', 'GET', '/api/v1/state')
    request('BASE-20', 'GET', '/api/v1/temperature/snapshot')


if __name__ == '__main__':
    baseline('initial')
