"""先等新快照再做 API 负例；所有料槽请求均为选择、目标0，不发进退丝。"""
import json
import time
from audit_driver import ROOT, request, record


def await_fresh(label):
    """等待本次采样新快照；label 为用例名；返回就绪布尔值，4秒仅为工具等待上限。"""
    before = json.loads(request(label, 'GET', '/api/v1/temperature/snapshot')['body'])
    request(label, 'POST', '/api/v1/temperature/sample', {})
    deadline = time.monotonic() + 4
    while time.monotonic() < deadline:
        time.sleep(.15)
        value = json.loads(request(label, 'GET', '/api/v1/temperature/snapshot')['body'])
        ready = value['generation_id'] > before['generation_id'] and value['system_status'] == 'NORMAL'
        if ready:
            return True
    record(label, 'precondition_failed', {'reason': '未取得本次NORMAL新快照'})
    return False


def slot_baseline():
    """从本轮真实浏览器 POST 提取配置，强制安全 SELECT/目标0；无参数，返回请求字典。"""
    result = None
    for line in (ROOT / 'browser_cdp_raw.jsonl').open():
        event = json.loads(line)
        if event.get('method') != 'Network.requestWillBeSent':
            continue
        req = event['params']['request']
        if req['url'].endswith('/api/v1/filament/slots') and req['method'] == 'POST':
            result = json.loads(req['postData'])
    result.update(action=0, target_temp_deci_c=0, active_slot=1, slot_id=1, total_mixing_weight=10000)
    return result


def main():
    """展开已知公开接口的正常、负向与恢复请求；无入参，无返回值，不启动打印。"""
    base = slot_baseline()
    cases = [('POS', {}), ('NEG-SLOT5', {'active_slot': 5, 'slot_id': 5}), ('NEG-SUM', {'total_mixing_weight': 9999}), ('NEG-ACTION', {'action': -1}), ('REC', {})]
    for label, delta in cases:
        case = 'BASE-19-API-WAIT-' + label
        if await_fresh(case):
            print(label, request(case, 'POST', '/api/v1/filament/slots', dict(base, **delta)), flush=True)
    for name, size in [('invalid.txt', 19), ('empty.gcode', 0), ('valid.gcode', 5)]:
        print(name, request('BASE-09-API-PAIR', 'POST', '/api/v1/jobs/upload', {'name': name, 'size': size}), flush=True)


if __name__ == '__main__':
    main()
