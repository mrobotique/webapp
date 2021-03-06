#!/usr/bin/env python3
from threading import Lock
from flask import Flask, render_template, session, request, \
    copy_current_request_context
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect

from datetime import datetime
import serial
import json


ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)

# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
async_mode = "eventlet"

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()


def background_serial_reader_thread():
    """Example of how to send server generated events to clients."""
    last_pub = 0
    uvsa_key=['msg_id', 'version', 'card', 'deadman1', 'deadman2', 'auto', 'pir1', 'pir2', 'pir3', 'pir4', 'mag1',
              'mag2', 'lamp1', 'lamp2', 'lamp3', 'lamp4', 'lamp5', 'lamp6', 'lampDeadman', 'lampAuto', 'buzzer',
              'operationMode', 'tiempoRestante']
    uvsa_dict = {}

    while True:
        ser_data = ser.readline().decode('utf8')[:-2]
        decoded_data = ser_data.split(":")[1][1:-2].split(',')
        if len(uvsa_key) == len(decoded_data): #El primer paquete despues de inicializar tiene basura... por eso se filtra aqui
            for i in range(len(uvsa_key)):
                try:
                    uvsa_dict[uvsa_key[i]] = int(decoded_data[i])
                except:
                    if decoded_data[i] == 'true':
                        uvsa_dict[uvsa_key[i]] = 1
                    else:
                        if decoded_data[i] == 'false':
                            uvsa_dict[uvsa_key[i]]  = 0
                        else:
                            uvsa_dict[uvsa_key[i]] = decoded_data[i][1:-1]
        uvsa_dict['date'] = str(datetime.date(datetime.now()))
        uvsa_dict['time'] = str(datetime.time(datetime.now())).split('.')[0]
        uvsa_dict['pir1'] = 1

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


@socketio.on('connect')
def test_connect():
    print("client connected")
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_serial_reader_thread)
    emit('my_response', {'data': 'Connected', 'count': 0})


@socketio.on('myButton')
def test_button():
    print("myButton")

@socketio.on('startButton')
def start_button(msg):
    print("start Button", msg)

@socketio.on('stopButton')
def stop_button():
    print("stopButton")


@socketio.on('myText')
def test_button(msg):
    print("myText: ", type(msg), msg, msg['data'])


if __name__ == '__main__':

    socketio.run(app, debug=True, host='0.0.0.0')
