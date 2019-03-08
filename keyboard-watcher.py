#!/usr/bin/python3

from ctypes import cdll, c_uint
from pyudev import Context, Monitor, MonitorObserver
from re import match
from subprocess import run
from sys import argv, exit
from time import sleep

def usage():
    print("""
Commands:
    monitor - watch udev for usb input device insertions, and remap
    remap   - run all the remap commands once and exit
""")

def fix_mappings():
    run(args='setxkbmap -option ctrl:nocaps', shell=True, check=True)
    run(args='xcape -e Control_L=Escape', shell=True, check=True)

    # https://askubuntu.com/a/80301
    X11 = cdll.LoadLibrary("libX11.so.6")
    display = X11.XOpenDisplay(None)
    # '2' corresponds to Caps Lock
    X11.XkbLockModifiers(display, c_uint(0x0100), c_uint(2), c_uint(0))
    X11.XCloseDisplay(display)

if len(argv) < 2:
    usage()
    exit(1)

if argv[1] == 'monitor':
    context = Context()
    monitor = Monitor.from_netlink(context)
    monitor.filter_by('input')
    monitor.filter_by('usb')
    # polls forever
    for device in iter(monitor.poll, None):
        if device.action == 'add' and match(r'.*input\d+$',device.device_path):
            sleep(2)
            fix_mappings()
elif argv[1] == 'remap':
    fix_mappings()
else:
    usage()
    exit(1)

