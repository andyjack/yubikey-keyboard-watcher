## What is this

I sometimes have to unplug/replug a yubikey on my linux desktop, but this makes
my keyboard mappings disappear.

```
setxkbmap -option ctrl:nocaps
xcape -e 'Control_L=Escape'
```

I want to monitor udev for device changes, and redo the mappings automatically.

Sometimes my Caps Lock key gets stuck on too!  I'm not sure if this is due to
me futzing around with the above commands manually, but this will simulate a
single Caps_Lock keypress:

`xdotool key Caps_Lock`

## Requirements

`apt install python3-pyudev`

Tested on python 3.6.

<!--
 vim:tw=78
-->
