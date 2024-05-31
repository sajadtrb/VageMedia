#!/bin/bash

git pull
git config --global user.email "xy@gmail.com"
git config --global user.name "X Y"
git checkout -b xy-$(openssl rand -hex 6)
pip install --no-cache-dir -r requirements.txt
/etc/init.d/cloudflared start