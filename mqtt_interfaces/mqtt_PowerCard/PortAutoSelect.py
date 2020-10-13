#!/usr/bin/env python3
import serial.tools.list_ports
import serial
import time
import paho.mqtt.client as paho
import logging


class ManagePowercard():
    def __init__(self, device_serial_number, device_baudrate=19200, mqtt_broker='localhost', mqtt_port=1883):
        # Serial port
        self.FTDI_SERIAL_NUMBER = device_serial_number
        self.baudrate = device_baudrate
        self.device = ""
        # mqtt
        self.broker = mqtt_broker
        self.port = mqtt_port
        # Aux
        self.log = logging.getLogger("PowerCard_class")

    def on_publish(self):  # create function for callback
        pass

    def run(self):
        mqtt_client = paho.Client("powerCard_serial")  # create client object
        # mqtt_client.on_publish = on_publish  #assign function to callback --example if needed--
        mqtt_client.connect(self.broker, self.port)

        while True:
            while self.device == "":
                ports = list(serial.tools.list_ports.comports())
                for p in ports:
                    if p.serial_number == self.FTDI_SERIAL_NUMBER:
                        self.device = p.device
            print(self.device)
            time.sleep(2)  # Tiempo para que el puerto este listo
            try:
                ser = serial.Serial(self.device, self.baudrate)
                ser.close()  # In case the port is already open this closes it.
                ser.open()  # Reopen the port.
                string = ""

                while ser.isOpen():
                    buffer = ser.read()
                    if (buffer != b'\n') and (buffer != b'\r'):
                        string += buffer.decode('utf8')
                    if buffer == b'\r':
                        # print(string)
                        mqtt_client.publish("uvsa/card", string)
                        string = ""
            except Exception as e:
                self.log.error(e)
                self.device = ""
                ser.close()


if __name__ == '__main__':
    log = logging.getLogger("PowerCard_main")
    device_serial_number = "AG0JU7H6" # "A105ABMO"
    cardReader = ManagePowercard(device_serial_number, device_baudrate=19200, mqtt_broker='localhost', mqtt_port=1883)
    try:
        cardReader.run()
    except Exception as e:
        log.error(e)
