#!/bin/sh

ENV=prod
[ $# -eq 1 ] && ENV=$1

cd /home/pi/sfs-printer/
.venv/bin/python worker.py $ENV > /tmp/sfs-printer-worker.log

