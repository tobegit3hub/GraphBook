#!/bin/bash

set -x

cd "$(dirname "$0")"

# Pull latest code
git pull origin main
git submodule update --init

# Update frontend
cd ../../frontend/
npm install
npm run build

# Cleanup old data
cd ../tools/website/
ps aux | grep './server.py' | grep -v "grep" | awk '{print $2}' | xargs kill -9
mysql -uroot -proot < ./drop_database.sql

# Import topics and start
cd ../../python/server/
./import_official_topics.py ./topicland_website.ini
nohup ./server.py ./topicland_website.ini  &
