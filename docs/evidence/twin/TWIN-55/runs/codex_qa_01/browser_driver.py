"""以真实 Chrome CDP 记录可见入口和网络，不改页面存储或调用应用内部函数。"""
import base64
import json
import sys
import time
import urllib.request
import websocket
from audit_driver import ROOT, record


class Browser:
    """封装专用页面 CDP；仅通过公开 DOM 查找与真实输入驱动界面。"""

    def __init__(self):
        """连接专用 Chrome 页；无入参，无返回值；失败抛异常。"""
        pages = json.load(urllib.request.urlopen('http://127.0.0.1:19355/json/list'))
        page = next(item for item in pages if item['type'] == 'page')
        self.socket = websocket.create_connection(page['webSocketDebuggerUrl'], timeout=15, origin='http://localhost:19355')
        self.counter = 0
        self.call('Network.enable')
        self.call('Page.enable')

    def call(self, method, params=None):
        """发送 CDP method 与可选 params；返回响应，过程中追加全部事件。"""
        self.counter += 1
        self.socket.send(json.dumps({'id': self.counter, 'method': method, 'params': params or {}}))
        while True:
            value = json.loads(self.socket.recv())
            with (ROOT / 'browser_cdp_raw.jsonl').open('a') as stream:
                stream.write(json.dumps(value, ensure_ascii=False) + '\n')
            # 页面原生提示框会阻塞后续求值；先保留事件，仅确认无决策含义的 alert。
            if value.get('method') == 'Page.javascriptDialogOpening':
                accepted = value['params']['type'] == 'alert'
                self.socket.send(json.dumps({'id': 1000000, 'method': 'Page.handleJavaScriptDialog', 'params': {'accept': accepted}}))
            if value.get('id') == self.counter:
                if 'error' in value:
                    raise RuntimeError(value['error'])
                return value.get('result', {})

    def evaluate(self, expression):
        """读取 DOM expression 或注入测试用文件；返回可序列化值，不修改应用内部状态。"""
        result = self.call('Runtime.evaluate', {'expression': expression, 'returnByValue': True, 'awaitPromise': True})
        if 'exceptionDetails' in result:
            raise RuntimeError(result['exceptionDetails'])
        return result.get('result', {}).get('value')

    def click(self, selector):
        """定位 DOM selector 后发送鼠标按压和释放；返回空值，无元素时抛异常。"""
        bounds = self.evaluate("(()=>{const e=document.querySelector(" + json.dumps(selector) + ");if(!e)throw Error('missing');e.scrollIntoView();const r=e.getBoundingClientRect();return {x:r.x+r.width/2,y:r.y+r.height/2}})()")
        self.call('Input.dispatchMouseEvent', dict(type='mousePressed', button='left', clickCount=1, **bounds))
        self.call('Input.dispatchMouseEvent', dict(type='mouseReleased', button='left', clickCount=1, **bounds))

    def snapshot(self, label):
        """保存 label 对应截图、DOM 和可见文本；返回文本，不修改业务状态。"""
        time.sleep(1)
        text = self.evaluate('document.body.innerText')
        (ROOT / (label + '.txt')).write_text(text)
        (ROOT / (label + '.html')).write_text(self.evaluate('document.documentElement.outerHTML'))
        shot = self.call('Page.captureScreenshot', {'format': 'png', 'captureBeyondViewport': False})
        (ROOT / (label + '.png')).write_bytes(base64.b64decode(shot['data']))
        return text


def main():
    """按 CLI 参数执行单一浏览器动作；无入参，无返回值；异常保留调用证据。"""
    browser = Browser()
    action, label = sys.argv[1:3]
    record(label, 'browser_' + action, {'arguments': sys.argv[3:]})
    if action == 'navigate':
        browser.call('Page.navigate', {'url': 'http://192.168.77.134:8080/'})
        time.sleep(4)
    elif action == 'click':
        browser.click(sys.argv[3])
    elif action == 'eval':
        print(json.dumps(browser.evaluate(sys.argv[3]), ensure_ascii=False))
    elif action == 'reload':
        browser.call('Page.reload', {'ignoreCache': True})
        time.sleep(3)
    print(browser.snapshot(label))
    browser.socket.close()


if __name__ == '__main__':
    main()
