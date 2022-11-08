#!/bin/sh

cd /home/pi/sfs-printer/
#.venv/bin/python worker.py dev > /tmp/sfs-printer-worker.log
.venv/bin/python worker.py prod > /tmp/sfs-printer-worker.log
