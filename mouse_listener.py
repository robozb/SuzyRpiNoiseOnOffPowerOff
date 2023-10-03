from evdev import InputDevice, categorize, ecodes, KeyEvent, list_devices
from subprocess import Popen, call
import os
from pyudev import Context

device_path = None

# Listázzuk ki az összes elérhető eszközt
devices = [InputDevice(path) for path in list_devices()]

# Végigmegyünk az eszközök listáján
for device in devices:
    # Megnézzük, hogy az eszköz nevében szerepel-e az "egér" vagy "mouse" szó
    if 'mouse' in device.name.lower() or 'egér' in device.name.lower():
        # Ha igen, kiíratjuk az eszköz elérési útját és nevét
        print(f"Eszköz elérési útja: {device.path}, Eszköz neve: {device.name}")
        device_path=device.path
        # és leállítjuk a keresést
        break



print(device_path)

#device_path='/dev/input/event0'

# A program, amit indítani szeretnél (például egy zenét)
command_to_run = ['/usr/bin/mpg123', '--loop', '-1', '/home/robozb/01-White-Noise-10min.mp3']
command_to_poweroff = ['/usr/sbin/poweroff']


dev = InputDevice(device_path)
process = None

for event in dev.read_loop():
    if event.type == ecodes.EV_KEY:
        key_event = categorize(event)
        if key_event.keystate == KeyEvent.key_down:
            # Bal egérgomb kódja: BTN_LEFT
            if event.code == ecodes.BTN_LEFT:
                if process is None or process.poll() is not None:
                    # Indítsd el a zenét
                    process = Popen(command_to_run)
                else:
                    # Állítsd le a zenét
                    call(['kill', str(process.pid)])
                    process = None
            # Jobb egérgomb kódja: BTN_RIGHT
            elif event.code == ecodes.BTN_RIGHT:
                # Indítsd el a poweroff parancsot
                call(command_to_poweroff)
