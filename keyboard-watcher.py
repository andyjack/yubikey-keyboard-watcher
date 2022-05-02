#!/usr/bin/env python3

from ctypes import cdll, c_int, c_uint, POINTER, Structure
from pyudev import Context, Monitor
from re import match
from subprocess import run
from sys import argv, exit
from time import sleep

class Display(Structure):
    """ an opaque structure """

def usage():
    print("""
Commands:
    monitor - watch udev for usb input device insertions, and remap
    remap   - run all the remap commands once and exit
""")


def monitor():
    context = Context()
    monitor = Monitor.from_netlink(context)
    monitor.filter_by('input')
    monitor.filter_by('usb')
    # polls forever
    for device in iter(monitor.poll, None):
        # Inserting the yubikey generates several 'add' events, but we don't
        # want to remap on every one of them.  So filter out a single one, wait
        # a bit for things to settle, and remap.
        if device.action == 'add' and match(r'.*input\d+$', device.device_path):
            sleep(2)
            remap()


def remap():
    # compose:ralt - right alt is the compose key, e.g. for accented character entry
    run(args='setxkbmap -option compose:ralt', shell=True, check=True)

    # This X11 stuff is to turn off the caps lock *effect*. If it was turned
    # on, and you somehow no longer have a way to send the CAPS LOCK keycode,
    # there's no way to turn off the effect with the keyboard.
    #
    # https://askubuntu.com/a/80301
    X11 = cdll.LoadLibrary("libX11.so.6")
    X11.XOpenDisplay.restype = POINTER(Display)
    display = X11.XOpenDisplay(c_int(0))
    # '2' corresponds to Caps Lock
    X11.XkbLockModifiers(display, c_uint(0x0100), c_uint(2), c_uint(0))
    X11.XCloseDisplay(display)


if len(argv) < 2:
    usage()
    exit(1)

if argv[1] == 'monitor':
    monitor()
elif argv[1] == 'remap':
    remap()
else:
    usage()
    exit(1)
