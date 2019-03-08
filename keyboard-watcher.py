from pyudev import Context, Monitor, MonitorObserver
from re import match
from subprocess import run, PIPE
from time import sleep

context = Context()
monitor = Monitor.from_netlink(context)
monitor.filter_by('input')
monitor.filter_by('usb')

def fix_mappings(device):
    if device.action == 'add' and match(r'.*input\d+$',device.device_path):
        sleep(2)
        run(args='setxkbmap -option ctrl:nocaps', shell=True, check=True)
        run(args='xcape -e Control_L=Escape', shell=True, check=True)

for device in iter(monitor.poll, None):
    fix_mappings(device)

