# crawlergo_x_XRAY

360 0Kee-Team 的 crawlergo动态爬虫 结合 长亭XRAY扫描器的被动扫描功能 (其它被动扫描器同理)

https://github.com/0Kee-Team/crawlergo

https://github.com/chaitin/xray

## 20200829
![OS Type](https://img.shields.io/badge/OS--Type-Kali-blue)
![Python3](https://img.shields.io/badge/Python-v3-blue)
![Webhook](https://img.shields.io/badge/Webhook-Slack-brightgreen)

```
1. 添加下载 crawlergo 和 xray 最新 release 的脚本
2. 添加安装 chrome 和 chromedriver 的脚本（仅支持基于 Debian 的 Linux 发行版
3. 修改 webhook 为推送到 slack webhook app
```

### 操作步骤

```bash
# 安装依赖
$ python3 -m pip install -r requirements.txt  # 安装 requests, flask, simplejson
$ sudo apt-get install ca-certificates    # 安装 ca-certificates
```

- 使用 `install_chrome_chromedriver.sh` 安装 chrome 和 chromedriver
- 使用 `install_crawlergo_xray.sh` 下载最新版 crawlergo 和 xray 到相应的文件夹
- 在 Slack 中添加 [Incoming WebHooks](https://slack.com/apps/A0F7XDUAZ-incoming-webhooks) app; 配置 webhook.py 中的 slack_webhook_url 并启动 webhook.py

```bash
# 默认 webhook 端口为 5000
$ python3 webhook.py
```
- 进入 xray 文件夹 `./xray`；运行 xray 可执行文件生成证书和初始配置文件，并退出

```bash
$ cd ./xray
$ ./xray_linux_amd64 genca
```
- 将证书添加到系统信任证书

```bash
$ sudo cp ca.crt /usr/local/share/ca-certificates
$ sudo update-ca-certificates
```
- 自定义 xray 的配置文件 `config.yaml`
- 启动 xray 并推送到 webhook

```bash
# 默认 xray 监听端口为 7777; 默认推送到 webhook 的 5000 端口
$ ./xray_linux_amd64 webscan --listen 127.0.0.1:7777 --webhook-output http://127.0.0.1:5000/webhook --html-output xray_result.html
```
- 开启新的终端；将目标网址放在 `targets.txt` 文件中；启动 crawlergo

```bash
# 默认 chromedriver 路径为 /usr/local/bin/chromedriver
$ python3 crawlergo_launcher.py # 可选择指定目标文件作为参数，如无指定，默认当前目录下的 targets.txt
```

![slack alert](https://raw.githubusercontent.com/5cr1pt/crawlergo_x_XRAY/master/img/slack_webhook.jpg)

> 参考：
https://github.com/undefinedsec/crawlergo-to-xray

## 20190115更新，launcher_new.py使用crawlergo提供的方法推送请求给xray

crawlergo默认推送方法有个不足就是无法与爬虫过程异步进行。使用launcher.py可以异步节省时间。

注：若运行出现权限不足，请删除crawlergo空文件夹。

## 如遇到报错注意将64位的crawlergo.exe和launcher.py还有targets.txt放在一个目录，将crawlergo目录删除

## 20190113更新，增加容错，解决访问不了的网站爬虫卡死。

## 介绍

一直想找一个小巧强大的爬虫配合xray的被动扫描使用,曾经有过自己写爬虫的想法,奈何自己太菜写一半感觉还没有awvs的爬虫好用

360 0Kee-Teem最近公开了他们自己产品中使用的动态爬虫模块,经过一番摸索发现正合我意,就写了这个脚本

由于该爬虫并未开放代理功能并且有一些从页面抓取的链接不会访问,所以我采用的官方推荐的方法,爬取完成后解析输出的json再使用python的request库去逐个访问

大概逻辑为:

![image](https://raw.githubusercontent.com/timwhitez/crawlergo_x_XRAY/master/img/5.png)

爬取和请求的过程使用了多线程和队列使得请求不会阻塞下一个页面的爬取

## 用法

#### 1. 下载xray最新的release, 下载crawlergo最新的release

注意,是下载编译好的文件而不是git clone它的库

#### 2. 把launcher.py和targets.txt放在crawlergo.exe同目录下


#### 3. 配置好并启动xray被动扫描(脚本默认配置为127.0.0.1:7777)若修改端口请同时修改launcher.py文件中的proxies

![image](https://raw.githubusercontent.com/timwhitez/crawlergo_x_XRAY/master/img/0.png)

配置参数详见XRAY官方文档

![image](https://raw.githubusercontent.com/timwhitez/crawlergo_x_XRAY/master/img/1.png)

#### 4. 配置好launcher.py的cmd变量中的crawlergo爬虫配置(主要是chrome路径改为本地路径), 默认为:

./crawlergo -c C:\Program Files (x86)\Google\Chrome\Application\chrome.exe -t 20 -f smart --fuzz-path --output-mode json target

![image](https://raw.githubusercontent.com/timwhitez/crawlergo_x_XRAY/master/img/4.png)

配置参数详见crawlergo官方文档

#### 5. 把目标url写进targets.txt,一行一个url

![image](https://raw.githubusercontent.com/timwhitez/crawlergo_x_XRAY/master/img/3.png)

#### 6. 用python3运行launcher.py ( XRAY被动扫描为启动的状态 )

#### 7. 生成的sub_domains.txt为爬虫爬到的子域名, crawl_result.txt为爬虫爬到的url


