#!/usr/bin/env python3
from threading import Lock
from flask import Flask, render_template, session, request, \
    copy_current_request_context, send_from_directory
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect

import subprocess
from datetime import datetime
import serial
import json
import yaml


ser = serial.Serial('/dev/ttyUSB0', 19200, timeout=1)
ser.setRTS(False)
ser.setDTR(False)
ser.read_all()
# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
async_mode = "eventlet"

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()

uvsa_dict = {}


def background_serial_reader_thread():
    # pass
    """Example of how to send server generated events to clients."""
    last_pub = 0
    uvsa_key=['msg_id', 'version', 'card', 'deadman1', 'deadman2', 'auto', 'pir1', 'pir2', 'pir3', 'pir4', 'mag1',
              'mag2', 'lamp_byte', 'horometro', 'buzzer', 'operationMode', 'tiempoRestante', 'mask_byte', 'count_down']

    decoded_data = []

    while True:
        try:
            ser_data = ser.readline().decode('utf8')[:-2]
            print(ser_data)
        except UnicodeDecodeError:
            pass

        try:
            decoded_data = ser_data.split(":")[1][1:-2].split(',')
        except IndexError:
            print("index error")


        if len(uvsa_key) == len(decoded_data): #El primer paquete despues de inicializar tiene basura... por eso se filtra aqui
            for i in range(len(uvsa_key)):
                try:
                    uvsa_dict[uvsa_key[i]] = int(decoded_data[i])
                except:
                    if decoded_data[i] == 'true':
                        uvsa_dict[uvsa_key[i]] = 1
                    else:
                        if decoded_data[i] == 'false':
                            uvsa_dict[uvsa_key[i]] = 0
                        else:
                            uvsa_dict[uvsa_key[i]] = decoded_data[i][1:-1]

            uvsa_dict['date'] = str(datetime.date(datetime.now()))
            uvsa_dict['time'] = str(datetime.time(datetime.now())).split('.')[0]
            #Decodificar lamparas
            uvsa_dict['lamp1'] = uvsa_dict['lamp_byte'] & 0b00000001
            uvsa_dict['lamp2'] = uvsa_dict['lamp_byte'] & 0b00000010
            uvsa_dict['lamp3'] = uvsa_dict['lamp_byte'] & 0b00000100
            uvsa_dict['lamp4'] = uvsa_dict['lamp_byte'] & 0b00001000
            uvsa_dict['lamp5'] = uvsa_dict['lamp_byte'] & 0b00010000
            uvsa_dict['lamp6'] = uvsa_dict['lamp_byte'] & 0b00100000
            uvsa_dict['lampDeadman'] = uvsa_dict['lamp_byte'] & 0b01000000
            uvsa_dict['lampAuto'] = uvsa_dict['lamp_byte'] & 0b10000000

            #  ToDo Un Horometro de verdad
            socketio.sleep(0.02)
            pub = int(float(uvsa_dict['msg_id'])/100)
            if pub != last_pub:
                last_pub = pub
                socketio.emit('my_response', uvsa_dict)


@app.route('/')
def index():
    print("client connected")
    return render_template('index.html')


@app.route('/diagnostico')
def diagnostico():
    return render_template('diagnostico.html')


@app.route('/logs')
def logs():
    return render_template('logs.html')


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
    fabricacion_dict = {'serialNumber':data['Serial'], 'modelo':data['Model']}
    socketio.emit('info_fabricacion', fabricacion_dict)


@socketio.on('connect')
def test_connect():
    print("client connected")
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_serial_reader_thread)
    emit('my_response', {'data': 'Connected', 'count': 0})


@socketio.on('startButton')
def start_button(msg):
    #print("start Button", json.dumps(msg))
    ser.write((json.dumps(msg) + '\r\n').encode())


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
    mask_byte = {}
    mask_byte['buzzer'] = uvsa_dict['mask_byte'] & 0b00000001
    mask_byte['lamp_1'] = uvsa_dict['mask_byte'] & 0b00000010
    mask_byte['lamp_2'] = uvsa_dict['mask_byte'] & 0b00000100
    mask_byte['lamp_3'] = uvsa_dict['mask_byte'] & 0b00001000
    mask_byte['lamp_4'] = uvsa_dict['mask_byte'] & 0b00010000
    mask_byte['lamp_5'] = uvsa_dict['mask_byte'] & 0b00100000
    mask_byte['lamp_6'] = uvsa_dict['mask_byte'] & 0b01000000
    emit('set_toggle_status', mask_byte)


if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0')
