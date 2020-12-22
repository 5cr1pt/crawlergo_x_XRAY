# encoding='utf-8'
from flask import Flask, request
import logging
import datetime
import requests
import sys
import telebot
from configparser import ConfigParser

app = Flask(__name__)


def pushToTelegram(token, chatid, plugin, vuln_type, content, create_time):
    """
    docstring
    """
    text = '\n'.join(['*'+plugin+' - '+vuln_type+'*',
                      '_'+create_time+'_', content])
    bot = telebot.TeleBot(token, parse_mode='markdown')
    bot.send_message(chatid, text+'\n')


def pushToSlack(webhook_url, plugin, vuln_type, content, create_time):
    resp = requests.post(webhook_url,
                         json={"attachments": [
                             {
                                 # fallbck 值不会显示
                                 "fallback": "xray-alert",
                                 # 引用的首行，小字
                                 "text": "_"+create_time+"_",
                                 # 引用的标题
                                 "pretext": vuln_type,
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


def pushNotification(plugin, vuln_type, content, create_time):
    """
    docstring
    """
    cfg = ConfigParser()
    cfg.read('config.ini')
    platform = cfg.get('platform', 'name')
    if platform == 'slack':
        webhook_url = cfg.get('slack', 'webhook_url')
        pushToSlack(webhook_url, plugin,
                    vuln_type, content, create_time)
    elif platform == 'telegram':
        token = cfg.get('telegram', 'token')
        chatid = cfg.get('telegram', 'chatid')
        pushToTelegram(token, chatid, plugin, vuln_type, content, create_time)
    else:
        print('ERROR, Notification Platform Not Supported.')
        sys.exit()


@app.route('/webhook', methods=['POST'])
def xray_webhook():
    vuln = request.json
    # 过滤掉 https://chaitin.github.io/xray/#/api/statistic 的数据
    if "vuln_class" not in vuln:
        return "ok"
    create_time = str(datetime.datetime.fromtimestamp(
        vuln["create_time"]/1000))
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
        vuln_request = vuln["detail"]["request"].strip(
        ) or vuln["detail"]["request1"].strip()
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
        pushNotification(plugin, vuln_type, content, create_time)
    except Exception as e:
        logging.exception(e)
    return 'ok'


if __name__ == '__main__':
    app.run()
