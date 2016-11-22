#!/usr/bin/env python
import argparse

import eventlet
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

from modem.modem import Modem

app = Flask(__name__)
socketio = SocketIO(app)
eventlet.monkey_patch()
modem = None


@app.route('/')
def index():
  return render_template('index.html')


@socketio.on('execute_raw_alp')
def on_execute_raw_alp(data):
  alp_hex_string = data['raw_alp'].replace(" ", "").strip()
  modem.send_command(bytearray(alp_hex_string.decode("hex")))


@socketio.on('connect')
def on_connect():
  print("modem: " + str(modem.uid))
  emit('module_info', {'uid': str(modem.uid)}, broadcast=True)


@socketio.on('disconnect')
def on_disconnect():
  print('Client disconnected', request.sid)


def command_received_callback(cmd):
  print("cmd received: {}".format(cmd))
  with app.test_request_context('/'):
    socketio.emit("received_alp_command", {'cmd': str(cmd) }, broadcast=True)
    print("broadcasted recv command")

if __name__ == '__main__':
  argparser = argparse.ArgumentParser()
  argparser.add_argument("-d", "--device", help="serial device /dev file modem",
                         default="/dev/ttyUSB0")
  argparser.add_argument("-r", "--rate", help="baudrate for serial device", type=int, default=115200)
  config = argparser.parse_args()

  modem = Modem(config.device, config.rate, command_received_callback)
  modem.start_reading()
  socketio.run(app, debug=False)