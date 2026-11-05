"""执行不触发运动或加热的浏览器调查；断言依据 BASE 草案，工具尚未经非作者复核。"""
import json
import time
from audit_driver import ROOT, record, remote
from browser_driver import Browser


def step(browser, label, selector, delay=1):
    """点击 selector 并保存 label 证据；browser 为连接，delay 为等待秒数；返回空值。"""
    record(label, 'click', {'selector': selector})
    browser.click(selector)
    time.sleep(delay)
    browser.snapshot(label)
    print(label, flush=True)


def fill(browser, selector, value):
    """用真实键盘输入 value；browser 为连接，selector 为输入框；返回空值。"""
    browser.click(selector)
    browser.call('Input.dispatchKeyEvent', {'type': 'keyDown', 'key': 'a', 'code': 'KeyA', 'modifiers': 2, 'windowsVirtualKeyCode': 65})
    browser.call('Input.dispatchKeyEvent', {'type': 'keyUp', 'key': 'a', 'code': 'KeyA', 'modifiers': 2, 'windowsVirtualKeyCode': 65})
    browser.call('Input.insertText', {'text': value})


def uploads(browser):
    """通过真实文件控件调查四个无执行副作用的输入；browser 为连接；返回空值。"""
    files = {'valid.gcode': 'M114\n', 'invalid.txt': 'This is not G-code\n', 'invalid.gcode': 'This is not G-code\n', 'empty.gcode': ''}
    remote('upload_fixture_create', "python3 - <<'PY'\nimport pathlib,json\np=pathlib.Path('/tmp/twin55_codex_qa_01_fixtures');p.mkdir(exist_ok=True)\nfor name,data in json.loads(" + repr(json.dumps(files)) + ").items(): (p/name).write_text(data)\nPY")
    for name, data in files.items():
        (ROOT / name).write_text(data)
        record('BASE-09', 'file_input', {'filename': name, 'contents': data})
        document = browser.call('DOM.getDocument')
        node = browser.call('DOM.querySelector', {'nodeId': document['root']['nodeId'], 'selector': '#gcode-file-input'})
        browser.call('DOM.setFileInputFiles', {'nodeId': node['nodeId'], 'files': ['/tmp/twin55_codex_qa_01_fixtures/' + name]})
        time.sleep(2)
        browser.snapshot('BASE-09-' + name)
        print('upload', name, flush=True)


def main():
    """运行界面独立调查并保留恢复动作；无入参，无返回值，不触发固件业务动作。"""
    browser = Browser()
    step(browser, 'BASE-03-english', '#btn-lang-toggle')
    browser.call('Page.reload', {'ignoreCache': True})
    time.sleep(3)
    browser.snapshot('BASE-03-reload-english')
    step(browser, 'BASE-03-chinese-recovery', '#btn-lang-toggle')
    step(browser, 'BASE-03-theme', '#btn-theme-toggle')
    browser.call('Page.reload')
    time.sleep(3)
    browser.snapshot('BASE-03-reload-theme')
    step(browser, 'BASE-03-theme-recovery', '#btn-theme-toggle')
    step(browser, 'BASE-17-slots', '#nav-btn-slots')
    for preset in ['single-1', 'dual-50', 'quad-25']:
        step(browser, 'BASE-18-' + preset, '[data-preset="' + preset + '"]')
    fill(browser, '#slot-weight-0', '-1')
    browser.snapshot('BASE-19-negative-weight')
    step(browser, 'BASE-19-save-negative', '#btn-save-slots')
    step(browser, 'BASE-19-valid-recovery', '[data-preset="single-1"]')
    step(browser, 'BASE-17-save-valid', '#btn-save-slots', 2)
    step(browser, 'BASE-08-dashboard', '#nav-btn-dashboard')
    step(browser, 'BASE-08-cube', '[data-load-model="CalibrationCube.gcode"]', 2)
    uploads(browser)
    step(browser, 'BASE-22-network', '#nav-btn-network')
    step(browser, 'BASE-23-health', '#nav-btn-hms')
    browser.socket.close()


if __name__ == '__main__':
    main()
