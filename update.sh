#!/bin/sh
cd /opt/v6helper
./build.py
service nginx reload > /dev/null
