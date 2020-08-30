# encoding='utf-8'
import requests
import datetime
import logging
from flask import Flask, request

# 自定义 slack webhook app 的 URL
slack_webhook_url = ''

app = Flask(__name__)


def pushToSlack(plugin,vuln_class,content,create_time):
    resp = requests.post(slack_webhook_url,
        json={"attachments": [
            {
                # fallbck 值不会显示
                "fallback": "xray-alert",
                # 引用的首行，小字
                "text": create_time,
                # 引用的标题
                "pretext": vuln_class,
                # 引用标签的颜色
                "color": "danger",
                "fields": [{
                    # 对引用的概括
                    "title": plugin,
                    # 引用消息的内容部分
                    "value": content,
                    # 是否自动缩略
                    "short": "false"
                    }]
            }
        ]})
    if resp.text != 'ok':
        raise ValueError("push to slack failed, %s" % resp.text)


@app.route('/webhook', methods=['POST'])
def xray_webhook():
    vuln = request.json
    # 过滤掉 https://chaitin.github.io/xray/#/api/statistic 的数据
    if "vuln_class" not in vuln:
        return "ok"
    create_time = str(datetime.datetime.fromtimestamp(vuln["create_time"]/1000))
    vuln_url = vuln["target"]["url"]
    plugin = vuln["plugin"]
    vuln_type = vuln["vuln_class"] or "default"
    try:
        vuln_position = vuln["detail"]["param"]["key"]
        vuln_payload = '`'+vuln["detail"]["payload"]+'`'
    except:
        vuln_position = ''
        vuln_payload = ''
    try:
        vuln_request = vuln["detail"]["request"].strip() or vuln["detail"]["request1"].strip()
    except:
        vuln_request = ''
    if vuln_position:
        content = """
Target: {url}
Position: {position}
Payload: {payload}
```
{request}
```
""".format(url=vuln_url, position=vuln_position, payload=vuln_payload, request=vuln_request)
    elif vuln_request:
        content = """
Target: {url}
```
{request}
```
""".format(url=vuln_url, request=vuln_request)
    else:
        content = """
Target: {url}
""".format(url=vuln_url)
    try:
        pushToSlack(plugin,vuln_type,content,create_time)
    except Exception as e:
        logging.exception(e)
    return 'ok'


if __name__ == '__main__':
    app.run()