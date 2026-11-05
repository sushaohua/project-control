"""按动作显式采样后调查浏览器文件与配置路径；不启动后台采样或运动作业。"""
import time
from audit_driver import ROOT, record, request
from browser_driver import Browser
from software_checks import fill


def fresh(browser, label):
    """动作前请求一次新采样；browser 为 CDP，label 为标识；返回空值，保存快照。"""
    request(label, 'POST', '/api/v1/temperature/sample', {})
    request(label, 'GET', '/api/v1/temperature/snapshot')
    time.sleep(0.15)
    browser.evaluate('document.readyState')


def upload(browser, name):
    """选择已存档 name 文件；browser 为 CDP；返回空值，不启动打印。"""
    fresh(browser, 'BASE-09-' + name + '-fresh')
    record('BASE-09', 'fresh_file_input', {'filename': name})
    doc = browser.call('DOM.getDocument')
    node = browser.call('DOM.querySelector', {'nodeId': doc['root']['nodeId'], 'selector': '#gcode-file-input'})
    browser.call('DOM.setFileInputFiles', {'nodeId': node['nodeId'], 'files': ['/tmp/twin55_codex_qa_01_fixtures/' + name]})
    time.sleep(0.5)
    browser.snapshot('BASE-09-fresh-' + name)
    print(name, flush=True)


def main():
    """运行安全公开操作；无入参，无返回值，全部动作与网络事件进入证据。"""
    browser = Browser()
    browser.click('#nav-btn-slots')
    browser.click('[data-preset="single-1"]')
    fresh(browser, 'BASE-17-fresh')
    record('BASE-17', 'save_valid', {'weights': [10000, 0, 0, 0]})
    browser.click('#btn-save-slots')
    time.sleep(1)
    browser.snapshot('BASE-17-fresh-save')
    browser.click('#nav-btn-dashboard')
    fresh(browser, 'BASE-08-fresh')
    browser.click('[data-load-model="CalibrationCube.gcode"]')
    time.sleep(0.5)
    browser.snapshot('BASE-08-fresh-cube')
    for name in ['valid.gcode', 'invalid.txt', 'invalid.gcode', 'empty.gcode', 'valid.gcode']:
        upload(browser, name)
    fresh(browser, 'GCODE-M114')
    fill(browser, '#gcode-manual-input', 'M114')
    record('GCODE-M114', 'click_send_query', {'gcode': 'M114'})
    browser.click('#btn-send-gcode')
    time.sleep(6)
    browser.snapshot('GCODE-M114-result')
    browser.socket.close()


if __name__ == '__main__':
    main()
