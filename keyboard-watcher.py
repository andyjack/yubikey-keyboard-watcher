from pyudev import Context, Monitor, MonitorObserver
from re import match
from subprocess import run, PIPE
from time import sleep
from ctypes import cdll, c_uint

context = Context()
monitor = Monitor.from_netlink(context)
monitor.filter_by('input')
monitor.filter_by('usb')

def fix_mappings(device):
    if device.action == 'add' and match(r'.*input\d+$',device.device_path):
        sleep(2)
        run(args='setxkbmap -option ctrl:nocaps', shell=True, check=True)
        run(args='xcape -e Control_L=Escape', shell=True, check=True)
        turn_off_capslock()

def turn_off_capslock():
    # https://askubuntu.com/a/80301
    X11 = cdll.LoadLibrary("libX11.so.6")
    display = X11.XOpenDisplay(None)
    # '2' corresponds to Caps Lock
    X11.XkbLockModifiers(display, c_uint(0x0100), c_uint(2), c_uint(0))
    X11.XCloseDisplay(display)

for device in iter(monitor.poll, None):
    fix_mappings(device)
