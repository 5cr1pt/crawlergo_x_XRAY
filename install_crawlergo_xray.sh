#!/usr/bin/env bash
# download latest xray, crawlergo for linux and move into specific folder
wget https://github.com/0Kee-Team/crawlergo/releases/latest/download/crawlergo_linux_amd64.zip
wget https://github.com/chaitin/xray/releases/latest/download/xray_linux_amd64.zip
unzip crawlergo_linux_amd64.zip
unzip xray_linux_amd64.zip
rm -rf crawlergo_linux_amd64.zip
rm -rf xray_linux_amd64.zip
mv crawlergo ./crawlergo/
mv xray_linux_amd64 ./xray/