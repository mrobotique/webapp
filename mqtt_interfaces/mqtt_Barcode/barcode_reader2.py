from evdev import InputDevice, categorize, ecodes
import paho.mqtt.client as paho
import yaml
import time
import os

scancodes = {
    # Scancode: ASCIICode
    0: None, 1: u'ESC', 2: u'1', 3: u'2', 4: u'3', 5: u'4', 6: u'5', 7: u'6', 8: u'7', 9: u'8',
    10: u'9', 11: u'0', 12: u'-', 13: u'=', 14: u'BKSP', 15: u'TAB', 16: u'q', 17: u'w', 18: u'e', 19: u'r',
    20: u't', 21: u'y', 22: u'u', 23: u'i', 24: u'o', 25: u'p', 26: u'[', 27: u']', 28: u'CRLF', 29: u'LCTRL',
    30: u'a', 31: u's', 32: u'd', 33: u'f', 34: u'g', 35: u'h', 36: u'j', 37: u'k', 38: u'l', 39: u';',
    40: u'"', 41: u'`', 42: u'LSHFT', 43: u'\\', 44: u'z', 45: u'x', 46: u'c', 47: u'v', 48: u'b', 49: u'n',
    50: u'm', 51: u',', 52: u'.', 53: u'/', 54: u'RSHFT', 56: u'LALT', 57: u' ', 100: u'RALT'
}

capscodes = {
    0: None, 1: u'ESC', 2: u'!', 3: u'@', 4: u'#', 5: u'$', 6: u'%', 7: u'^', 8: u'&', 9: u'*',
    10: u'(', 11: u')', 12: u'_', 13: u'+', 14: u'BKSP', 15: u'TAB', 16: u'Q', 17: u'W', 18: u'E', 19: u'R',
    20: u'T', 21: u'Y', 22: u'U', 23: u'I', 24: u'O', 25: u'P', 26: u'{', 27: u'}', 28: u'CRLF', 29: u'LCTRL',
    30: u'A', 31: u'S', 32: u'D', 33: u'F', 34: u'G', 35: u'H', 36: u'J', 37: u'K', 38: u'L', 39: u':',
    40: u'\'', 41: u'~', 42: u'LSHFT', 43: u'|', 44: u'Z', 45: u'X', 46: u'C', 47: u'V', 48: u'B', 49: u'N',
    50: u'M', 51: u'<', 52: u'>', 53: u'?', 54: u'RSHFT', 56: u'LALT', 57: u' ', 100: u'RALT'
}


def readBarcode(devicePath):
    dev = InputDevice(devicePath)
    dev.grab()  # grab provides exclusive access to the device

    x = ''
    caps = False

    for event in dev.read_loop():
        if event.type == ecodes.EV_KEY:
            data = categorize(event)  # Save the event temporarily to introspect it
            if data.scancode == 42:
                if data.keystate == 1:
                    caps = True
                if data.keystate == 0:
                    caps = False

            if data.keystate == 1:  # Down events only
                if caps:
                    key_lookup = u'{}'.format(capscodes.get(data.scancode)) or u'UNKNOWN:[{}]'.format(
                        data.scancode)  # Lookup or return UNKNOWN:XX
                else:
                    key_lookup = u'{}'.format(scancodes.get(data.scancode)) or u'UNKNOWN:[{}]'.format(
                        data.scancode)  # Lookup or return UNKNOWN:XX

                if (data.scancode != 42) and (data.scancode != 28):
                    x += key_lookup

                if data.scancode == 28:
                    return x

def main():
    """

    """
    # Carga los parametros de configuracion
    with open('/home/uv/uvsa_user/uvsa_config.yaml') as f:
        uvsa_config = yaml.load(f, Loader=yaml.FullLoader)
    # mqtt server Configuracion y main loop
    mqtt_broker = uvsa_config['mqtt_server']['broker']
    mqtt_port = uvsa_config['mqtt_server']['port']
    mqtt_client = paho.Client("barcode_client")  # create client object
    mqtt_client.connect(mqtt_broker, mqtt_port)
    mqtt_client.loop_start()
    # otros parametros
    devicePath = uvsa_config["codebarScanner"]["device_path"]
    mqtt_topic = uvsa_config["codebarScanner"]["mqtt_topic"]
    error_send = True

    while True:
        while not (os.path.exists(devicePath)):
            time.sleep(1)
            if error_send:
                mqtt_client.publish(mqtt_topic, "NA")
                error_send = False
        error_send = True

        try:
            scannedString = readBarcode(devicePath)
            # print(s)
            mqtt_client.publish(mqtt_topic, scannedString)
            time.sleep(0.1)
        except OSError:
            mqtt_client.publish(mqtt_topic, "NA")
            error_send = False


if __name__ == '__main__':
    main()