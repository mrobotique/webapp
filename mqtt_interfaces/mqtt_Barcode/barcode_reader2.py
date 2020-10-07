from evdev import InputDevice, categorize, ecodes

device = InputDevice("/dev/input/by-id/usb-WIT_Electron_Company_WIT_122-UFS_V7.13-event-kbd"
                     "") # my keyboard
for event in device.read_loop():
    if event.value == ecodes.EV_KEY:
        print(categorize(event))