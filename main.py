#!/usr/bin/env python3
# from threading import Lock
from flask import Flask, render_template, make_response
from flask_socketio import SocketIO, emit
from flask_mqtt import Mqtt
import subprocess
import math
from datetime import datetime
import json
import yaml
import logManager

#FRAM - Horometro
import board
import busio
import digitalio
import adafruit_fram

with open('/home/uv/uvsa_user/uvsa_config.yaml') as f:
    uvsa_config = yaml.load(f, Loader=yaml.FullLoader)

app = Flask(__name__)
app.config['MQTT_BROKER_URL'] = uvsa_config['mqtt_server']['broker']
app.config['MQTT_BROKER_PORT'] = uvsa_config['mqtt_server']['port']
# app.config['MQTT_USERNAME'] = ''
# app.config['MQTT_PASSWORD'] = ''
app.config['MQTT_REFRESH_TIME'] = 0.2  # refresh time in seconds
mqtt = Mqtt(app)
# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
socketio = SocketIO(app, async_mode="threading")
mqtt.subscribe('uvsa/#')

class WebApp:
    """

    """

    def __init__(self, cardTopic, scannerTopic):
        """

        """
        # Control Globals
        self.log_entry = []
        self.uvsa_dict = {}
        self.Ubicacion = "tst"
        self.HoraInicio = 0
        self.lastCall = 0
        self.ExposureTime = 0
        self.cardTopic = cardTopic
        self.scannerTopic = scannerTopic
        self.last_modo_operacion = 3 # Manera natural de iniciar el Operation Mode

        ## Create a FRAM object.
        spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
        cs = digitalio.DigitalInOut(board.D5)
        self.fram = adafruit_fram.FRAM_SPI(spi, cs)
        # Leer el fram
        hex0 = "{:02x}".format(int.from_bytes(self.fram[0], byteorder='big'))
        hex1 = "{:02x}".format(int.from_bytes(self.fram[2], byteorder='big'))
        hex2 = "{:02x}".format(int.from_bytes(self.fram[4], byteorder='big'))
        hex3 = "{:02x}".format(int.from_bytes(self.fram[6], byteorder='big'))
        # convertir a entero
        full_hex_str = hex3 + hex2 + hex1 + hex0
        segundos = int(full_hex_str, 16)
        # Convertir a horas
        self.horometro = segundos

    def on_message(self, message):
        if message.topic == self.cardTopic:
            self.on_card_message(message.payload.decode("utf-8"))

    def on_card_message(self, message):
        """Example of how to send server generated events to clients."""
        last_pub = 0
        uvsa_key=['msg_id', 'version', 'card', 'deadman1', 'deadman2', 'auto', 'pir1', 'pir2', 'pir3', 'pir4', 'mag1',
                  'mag2', 'lamp_byte', 'horometro', 'buzzer', 'operationMode', 'tiempoRestante', 'mask_byte', 'count_down',
                  'state_machine_status', 'total_time']
        decoded_data = []
        try:
            decoded_data = message.split(":")[1][1:-2].split(',')

        except IndexError:
            print("index error")

        if len(uvsa_key) == len(decoded_data): #El primer paquete despues de inicializar tiene basura... por eso se filtra aqui
            for i in range(len(uvsa_key)):
                try:
                    self.uvsa_dict[uvsa_key[i]] = int(decoded_data[i])
                except ValueError:
                    if decoded_data[i] == 'true':
                        self.uvsa_dict[uvsa_key[i]] = 1
                    else:
                        if decoded_data[i] == 'false':
                            self.uvsa_dict[uvsa_key[i]] = 0
                        else:
                            self.uvsa_dict[uvsa_key[i]] = decoded_data[i][1:-1]
            today = str(datetime.date(datetime.now())).split("-")
            self.uvsa_dict['date'] = today[2] + "/" + today[1] + "/" + today[0] # dd-mm-yyy
            self.uvsa_dict['time'] = str(datetime.time(datetime.now())).split('.')[0]
            #Decodificar lamparas
            self.uvsa_dict['lamp1'] = self.uvsa_dict['lamp_byte'] & 0b00000001
            self.uvsa_dict['lamp2'] = self.uvsa_dict['lamp_byte'] & 0b00000010
            self.uvsa_dict['lamp3'] = self.uvsa_dict['lamp_byte'] & 0b00000100
            self.uvsa_dict['lamp4'] = self.uvsa_dict['lamp_byte'] & 0b00001000
            self.uvsa_dict['lamp5'] = self.uvsa_dict['lamp_byte'] & 0b00010000
            self.uvsa_dict['lamp6'] = self.uvsa_dict['lamp_byte'] & 0b00100000
            self.uvsa_dict['lampDeadman'] = self.uvsa_dict['lamp_byte'] & 0b01000000
            self.uvsa_dict['lampAuto'] = self.uvsa_dict['lamp_byte'] & 0b10000000
            # Checa si es necesario guardar la ultima rutina de sanitizacion en la bitacora
            self.last_modo_operacion = self.create_log(self.uvsa_dict['operationMode'])
            #  ToDo Un Horometro de verdad
            self.uvsa_dict['horometro'] = self.horometro

            #print(self.uvsa_dict)
            pub = int(float(self.uvsa_dict['msg_id'])/100)
            if pub != last_pub:
                last_pub = pub
                socketio.emit('my_response', self.uvsa_dict, broadcast=True)
                socketio.sleep(0.02)

    def incrementa_horometro(self):
        """

        """
        if math.floor(self.ExposureTime) > 0: #para estar seguros que no es la primera iteracion -primeros 10 seg -
            # Leer el fram
            hex0 = "{:02x}".format(int.from_bytes(self.fram[0], byteorder='big'))
            hex1 = "{:02x}".format(int.from_bytes(self.fram[2], byteorder='big'))
            hex2 = "{:02x}".format(int.from_bytes(self.fram[4], byteorder='big'))
            hex3 = "{:02x}".format(int.from_bytes(self.fram[6], byteorder='big'))

            # convertir a entero
            full_hex_str = hex3 + hex2 + hex1 + hex0
            segundos = int(full_hex_str, 16)

            # Agregar 10 segundos
            segundos += 10

            # Reconvertir a hex
            full_hex = "{:08x}".format(segundos)
            hex0 = full_hex[-2:]
            hex1 = full_hex[-4:-2]
            hex2 = full_hex[-6:-4]
            hex3 = full_hex[:-6]

            # Guardar el tiempo en la Fram
            self.fram[0] = int(hex0, 16)
            self.fram[2] = int(hex1, 16)
            self.fram[4] = int(hex2, 16)
            self.fram[6] = int(hex3, 16)
            # Verificacion
            # Leer el fram
            hex0 = "{:02x}".format(int.from_bytes(self.fram[0], byteorder='big'))
            hex1 = "{:02x}".format(int.from_bytes(self.fram[2], byteorder='big'))
            hex2 = "{:02x}".format(int.from_bytes(self.fram[4], byteorder='big'))
            hex3 = "{:02x}".format(int.from_bytes(self.fram[6], byteorder='big'))
            # convertir a entero
            full_hex_str = hex3 + hex2 + hex1 + hex0
            segundos = int(full_hex_str, 16)
            # Convertir a horas
            self.horometro = segundos

    def create_log(self, modo_operacion):
        """
        :param modo_operacion:
        :type modo_operacion:
        :param last_modo_operacion:
        :type last_modo_operacion:
        :return:
        :rtype:
        """

        if (modo_operacion == 1) and (self.last_modo_operacion == 2):
            self.HoraInicio = datetime.now()
            self.lastCall = self.HoraInicio
            self.ExposureTime = 0
            self.log_entry = [self.uvsa_dict['date'], self.uvsa_dict['time'], "0", self.Ubicacion]

        if (modo_operacion == 3) and (self.last_modo_operacion == 1):
            if self.ExposureTime > 0:
                self.log_entry[2] = str(math.floor(self.ExposureTime))
                logManager.add_new_entry(self.log_entry)
                self.log_entry = []
            socketio.emit('reload_log', broadcast=True)

        try:
            if self.lastCall == self.HoraInicio and self.uvsa_dict['state_machine_status'] == 2:
                self.lastCall = datetime.now()

            if self.lastCall != self.HoraInicio:
                now = datetime.now()
                delta_time = now - self.lastCall
                self.lastCall = now
                if self.uvsa_dict['state_machine_status'] == 2:
                    self.ExposureTime += delta_time.total_seconds()
                    if (self.ExposureTime % 10) < 0.2: # 0.2 Segundos ya que la frec del mesaje es de 5hz. Asi solo toma 1 msg cada 10 seg
                        self.incrementa_horometro()
        except NameError:
            pass
        return modo_operacion

cardTopic = uvsa_config['powerCard']['mqtt_topic']
scannerTopic = uvsa_config['codebarScanner']['mqtt_topic']
my_webapp = WebApp(cardTopic, scannerTopic)


@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    my_webapp.on_message(message)


@app.route('/')
def index():
    print("client connected")
    return render_template('index.html')


@app.route('/diagnostico')
def diagnostico():
    return render_template('diagnostico.html')


@app.route('/logs')
def logs():
    response = make_response(logManager.run_guts())
    return response


@app.route('/ajustes')
def ajustes():
    return render_template('ajustes.html')


@app.route('/ayuda')
def ayuda():
    return render_template('ayuda.html')


@app.route('/acerca')
def acerca():
    return render_template('acerca.html')


@socketio.on('acerca_info')
def acerca_info():
    # ToDo Hacer el archivo YAML para recuperar el numero de serie y el modelo desde el archivo que produccion
    # ToDo debe de llenar.
    with open("/etc/uvsa/model_sn.yaml") as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    fabricacion_dict = {'serialNumber': data['Serial'], 'modelo': data['Model']}
    socketio.emit('info_fabricacion', fabricacion_dict)


@socketio.on('startButton')
def start_button(msg):
    # https://github.com/perrin7/ninjacape-mqtt-bridge/blob/master/ninjaCapeSerialMQTTBridge.py
    mqtt.publish('uvsa/button', (json.dumps(msg) + '\r\n').encode())


@socketio.on('set_dateTime')
def set_datetime(msg):
    """
    :param msg: Diccionario que contiene la hora y la fecha msg = {'fecha':str, 'hora':str}
    :type: dict
    :return: None
    """
    myDateTime = msg['fecha'] + " " + msg['hora'] + ":00.000"
    proc = subprocess.Popen(['sudo', 'date', '--set='+myDateTime], stdout=subprocess.PIPE)
    msg = str(proc.communicate()[0], 'utf-8')
    proc = subprocess.Popen(['sudo', 'hwclock', '-w'], stdout=subprocess.PIPE)
    emit('setDateResponse', msg)


@socketio.on('request_toggle_status')
def set_toggle_status():
    mask_byte = {'buzzer': my_webapp.uvsa_dict['mask_byte'] & 0b00000001,
                 'lamp_1': my_webapp.uvsa_dict['mask_byte'] & 0b00000010,
                 'lamp_2': my_webapp.uvsa_dict['mask_byte'] & 0b00000100,
                 'lamp_3': my_webapp.uvsa_dict['mask_byte'] & 0b00001000,
                 'lamp_4': my_webapp.uvsa_dict['mask_byte'] & 0b00010000,
                 'lamp_5': my_webapp.uvsa_dict['mask_byte'] & 0b00100000,
                 'lamp_6': my_webapp.uvsa_dict['mask_byte'] & 0b01000000}
    emit('set_toggle_status', mask_byte)


@socketio.on('delete_entries')
def delete_entries(entries_list):
    logManager.del_rows(entries_list)
    emit('reload_log', broadcast=True)


@socketio.on('delete_file')
def delete_file():
    logManager.del_log()
    emit('reload_log', broadcast=True)


if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', use_reloader=False)
