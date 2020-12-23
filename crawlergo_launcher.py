#!/usr/bin/python3
# coding: utf-8
import sys
import simplejson
import threading
import subprocess
import requests
import warnings
warnings.filterwarnings(action='ignore')

# 自定义 chromedriver 路径
chromedriver = "/usr/local/bin/chromedriver"


def opt2File2(subdomains):
	try:
		f = open('sub_domains.txt','a')
		f.write(subdomains + '\n')
	finally:
		f.close()


def main(data1):
	target = data1
	cmd = ["./crawlergo", "-c", chromedriver, "--custom-headers", "{\"User-Agent\": \"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.0 Safari/537.36\"}", "-t", "5","--fuzz-path", "--robots-path", "--push-to-proxy", "http://127.0.0.1:7777/", "--push-pool-max", "999","--output-mode", "json" , target]
	rsp = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	output, error = rsp.communicate()
	try:
		result = simplejson.loads(output.decode().split("--[Mission Complete]--")[1])
	except:
		return
	req_list = result["req_list"]
	sub_domain = result["sub_domain_list"]
	print(data1)
	print("[crawl ok]")
	for subd in sub_domain:
		# 略过空白行
		if subd.strip():
			opt2File2(subd)
	print("[scanning]")


if __name__ == '__main__':
	try:
		file = open(sys.argv[1])
	except:
		file = open("targets.txt")
	for text in file.readlines():
		data1 = text.strip('\n')
		main(data1)
