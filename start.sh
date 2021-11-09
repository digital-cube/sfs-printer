#!/bin/sh

echo -n -e '\x1b\x69\x55\x41\x00\x00' > /dev/usb/lp0

cd /home/pi/sfs-printer/
.venv/bin/python worker.py prod > /tmp/sfs-printer-worker.log
