"""使用规定 Windows venv/probe-rs 执行有界 UART 故障；仅写指定 CTRL1，finally 精确恢复。"""
import datetime
import json
import subprocess
import sys
import time
import urllib.error
import urllib.request

PROBE = r'C:\Users\EDY\tools\probe-rs\probe-rs.exe'
IDENTITIES = {
    'TH': ('AT32F423CCT7', '0483:3748:', '0x4001100C', 0x202C),
    'MC': ('AT32F435VGT7', '0483:3748:75003800120000334C41534E', '0x4000440C', 0x201C),
}


def emit(action, data):
    """向受控 stdout 输出时间事件；action 为标识，data 为数据；返回空值。"""
    print(json.dumps({'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'monotonic_ns': time.monotonic_ns(), 'action': action, 'data': data}), flush=True)


def probe(action, value, identity):
    """按 identity 芯片/探针/CTRL1 执行 action 与 value；返回原始输出，失败抛异常。"""
    chip, probe_id, address, expected = identity
    args = [PROBE, action, 'b32', address, str(value), '--chip', chip, '--probe', probe_id, '--format', 'simple-hex'] if action == 'read' else [PROBE, action, 'b32', address, str(value), '--chip', chip, '--probe', probe_id]
    result = subprocess.run(args, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=8)
    output = result.stdout.decode(errors='replace')
    emit('probe_' + action, {'argv': args, 'exit_code': result.returncode, 'output': output})
    if result.returncode:
        raise RuntimeError(output)
    return output.strip()


def http(method, path):
    """采集 method/path 的公开接口；返回响应字典；故障响应也作为原始证据保留。"""
    req = urllib.request.Request('http://192.168.77.134:8080' + path, data=b'{}' if method == 'POST' else None, method=method, headers={'Content-Type': 'application/json'})
    try:
        response = urllib.request.build_opener(urllib.request.ProxyHandler({})).open(req, timeout=8)
    except urllib.error.HTTPError as error:
        response = error
    with response:
        result = {'method': method, 'path': path, 'status': response.code, 'body': response.read().decode(errors='replace')}
    emit('http', result)
    return result


def main():
    """按 CLI 角色执行一次外设故障/恢复；无参数，无返回值，不操作 Flash 或加热。"""
    role = sys.argv[1]
    identity = IDENTITIES[role]
    actual = int(probe('read', 1, identity), 16)
    if actual != identity[3]:
        raise RuntimeError('当前 CTRL1 与本轮已核验正常值不一致，停止注入')
    emit('fault_begin', {'role': role, 'original_ctrl1': actual})
    try:
        probe('write', 0, identity)
        probe('read', 1, identity)
        http('POST', '/api/v1/temperature/sample')
        time.sleep(3)
        http('GET', '/api/v1/temperature/snapshot')
        http('GET', '/api/v1/jobs/status')
        http('POST', '/api/v1/filament/slots')
        time.sleep(2)
    finally:
        probe('write', actual, identity)
        restored = int(probe('read', 1, identity), 16)
        emit('fault_restore', {'role': role, 'matched': restored == actual})
        if restored != actual:
            raise RuntimeError('CTRL1 恢复核验失败')
    http('POST', '/api/v1/temperature/sample')
    time.sleep(1)
    http('GET', '/api/v1/temperature/snapshot')


if __name__ == '__main__':
    main()
