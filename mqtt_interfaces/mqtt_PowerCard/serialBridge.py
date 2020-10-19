#!/usr/bin/env python3
import serial.tools.list_ports
import serial
import time
import paho.mqtt.client as paho
import logging
import threading
import yaml


class ManagePowercard():
    def __init__(self, device_serial_number, baudrate, mqtt_broker, mqtt_port, button_topic):
        # Serial port
        self.FTDI_SERIAL_NUMBER = device_serial_number
        self.baudrate = baudrate
        self.device = ""
        self.ser = None
        # Aux
        self.log = logging.getLogger("PowerCard_class")
        # mqtt
        self.mqtt_client = None
        self.mqtt_broker = mqtt_broker
        self.mqtt_port = mqtt_port
        self.button_topic = button_topic

    def serial_thread(self):
        while True:
            while self.device == "":
                ports = list(serial.tools.list_ports.comports())
                for p in ports:
                    if p.serial_number == self.FTDI_SERIAL_NUMBER:
                        self.device = p.device
            #print(self.device)
            time.sleep(2)  # Tiempo para que el puerto este listo
            try:
                self.ser =serial.Serial(self.device, self.baudrate)
                self.ser.close()  # In case the port is already open this closes it.
                self.ser.open()  # Reopen the port.
                string = ""

                while self.ser.isOpen():
                    buffer = self.ser.read()
                    if (buffer != b'\n') and (buffer != b'\r'):
                        string += buffer.decode('utf8')
                    if buffer == b'\r':
                        # print(string)
                        self.mqtt_client.publish("uvsa/card", string)
                        string = ""
            except Exception as e:
                self.log.error(e)
                self.device = ""
                self.ser.close()

    def on_message(self, client, userdata, message):
        self.ser.write(message.payload)

    def run(self):
        self.mqtt_client = paho.Client("powerCard_serial")  # create client object
        self.mqtt_client.on_message = self.on_message
        self.mqtt_client.connect(self.mqtt_broker, self.mqtt_port)
        self.mqtt_client.subscribe(self.button_topic)
        self.mqtt_client.loop_start()
        serial_thread = threading.Thread(target=self.serial_thread)
        serial_thread.daemon = True
        serial_thread.start()

        while True:  # main thread
            time.sleep(1)


if __name__ == '__main__':
    log = logging.getLogger("PowerCard_main")
    with open('/home/uv/uvsa_user/uvsa_config.yaml') as f:
        uvsa_config = yaml.load(f, Loader=yaml.FullLoader)

    baudrate = uvsa_config['powerCard']['baudrate']
    device_serial_number = uvsa_config['powerCard']['serial_number']
    mqtt_broker = uvsa_config['mqtt_server']['broker']
    mqtt_port = uvsa_config['mqtt_server']['port']
    button_topic = uvsa_config['generic']['mqtt_topic_pageButton']

    cardReader = ManagePowercard(device_serial_number, baudrate, mqtt_broker, mqtt_port, button_topic)
    try:
        cardReader.run()
    except Exception as e:
        log.error(e)