#!/bin/bash
# 간단 업데이트 스크립트

cd /opt/cafemap
git pull
sudo systemctl restart cafemap
echo "업데이트 완료!"
