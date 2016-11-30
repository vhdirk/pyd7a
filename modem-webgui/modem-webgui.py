#!/usr/bin/env python
import argparse

import eventlet
import sys
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

from d7a.alp.command import Command
from d7a.system_files.system_files import SystemFiles
from modem.modem import Modem

app = Flask(__name__)
socketio = SocketIO(app)
eventlet.monkey_patch()
modem = None


@app.route('/')
def index():
  return render_template('index.html', systemfiles=SystemFiles().get_all_system_files())


@socketio.on('execute_raw_alp')
def on_execute_raw_alp(data):
  alp_hex_string = data['raw_alp'].replace(" ", "").strip()
  modem.send_command(bytearray(alp_hex_string.decode("hex")))

@socketio.on('read_local_system_file')
def on_read_local_system_file(data):
  print("read local system file")
  modem.send_command(
    Command.create_with_read_file_action_system_file(SystemFiles.files[int(data['file_id'])])
  )

@socketio.on('read_local_file')
def on_read_local_file(data):
  print("read_local_file")
  cmd = Command.create_with_read_file_action(
    file_id=int(data['file_id']),
    offset=int(data['offset']),
    length=int(data['length'])
  )

  modem.send_command(cmd)


@socketio.on('connect')
def on_connect():
  print("modem: " + str(modem.uid))
  emit('module_info', {
    'uid': hex(modem.uid),
    'application_name': modem.firmware_version.application_name,
    'git_sha1': modem.firmware_version.git_sha1
  }, broadcast=True)


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