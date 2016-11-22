#!/usr/bin/env python
import time

from datetime import datetime

import struct
from threading import Thread

import serial

from d7a.alp.operations.responses import ReturnFileData
from d7a.alp.regular_action import RegularAction
from d7a.serial_console_interface.parser import Parser

from d7a.alp.command import Command
from d7a.system_files.uid import UidFile

from d7a.system_files.system_file_ids import SystemFileIds

class Modem:
  def __init__(self, device, baudrate, receive_callback, show_logging=True):
    self.show_logging = show_logging
    self.parser = Parser()
    self.config = {
      "device"   : device,
      "baudrate" : baudrate
    }

    connected = self._connect_serial_modem()
    if connected:
      print("connected to {}, node UID {}".format(self.config["device"], hex(self.uid)))
    else:
      raise ModemConnectionError

    self.read_async_active = False
    self.receive_callback = receive_callback

  def _connect_serial_modem(self):
    self.dev = serial.Serial(
      port     = self.config["device"],
      baudrate = self.config["baudrate"],
      timeout  = 0.5,
    )

    self.send_command(Command.create_with_read_file_action_system_file(UidFile()))

    # read thread not yet running here, read sync
    start_time = datetime.now()
    timeout = False
    while not timeout:
      commands, info = self.read()
      for command in commands:
        for action in command.actions:
          if type(action) is RegularAction \
              and type(action.operation) is ReturnFileData \
              and action.operand.offset.id == SystemFileIds.UID:
            self.uid = struct.unpack(">Q", bytearray(action.operand.data))[0]
            return True

      if (datetime.now() - start_time).total_seconds() > 2:
        timeout = True
        self.log("Timed out reading node information")

    return False


  def log(self, *msg):
    if self.show_logging: print " ".join(map(str, msg))

  def send_command(self, alp_command):
    data = self.parser.build_serial_frame(alp_command)
    self.dev.write(data)
    self.dev.flush()
    self.log("Sending command of size", len(data))

  def d7asp_fifo_flush(self, alp_command):
    self.send_command(alp_command)
    flush_done = False
    should_restart_async_read = False
    if self.read_async_active:
      self.log("stopping read thread")
      should_restart_async_read = True
      self.read_async_active = False
      self.read_thread.shutdown = True
      self.read_thread.join()
      self.log("read thread stopped")

    start_time = datetime.now()
    timeout = False
    self.log("flush start of command with tag {}".format(alp_command.tag_id))
    while not flush_done and not timeout:
      data_received = self.dev.read()
      if len(data_received) > 0:
        (cmds, info) = self.parser.parse(data_received)

        for cmd in cmds:
          if cmd.tag_id == alp_command.tag_id:
            flush_done = True
            if cmd.completed_with_error:
              self.log("Flushing cmd with tag {} done, with error".format(cmd.tag_id))
            else:
              self.log("Flushing cmd with tag {} done, without error".format(cmd.tag_id))
            break

        for error in info["errors"]:
          error["buffer"] = " ".join(["0x{:02x}".format(ord(b)) for b in error["buffer"]])
          print error

      if (datetime.now() - start_time).total_seconds() > 2:
        timeout = True
        self.log("Flush timed out, skipping")

    if should_restart_async_read:
      self.start_reading()

  def read(self):
    try:
      data = self.dev.read_all()
    except serial.SerialException:
      time.sleep(5)
      self.setup_serial_device()
      data = ""
    return self.parser.parse(data)

  def cancel_read(self):
    if self.read_async_active:
      self.read_async_active = False
      self.read_thread.shutdown = True
      self.read_thread.join()

  def start_reading(self):
    self.read_async_active = True
    self.read_thread = Thread(target=self.read_async)
    self.read_thread.daemon = True
    self.read_thread.start()

  def read_async(self):
    self.log("starting read thread")

    while self.read_async_active:
      data_received = self.dev.read()
      if len(data_received) > 0:
        (cmds, info) = self.parser.parse(data_received)
        for error in info["errors"]:
          error["buffer"] = " ".join(["0x{:02x}".format(ord(b)) for b in error["buffer"]])
          print error

        for cmd in cmds:
          if self.receive_callback != None:
            self.receive_callback(cmd)

    self.log("end read thread")


class ModemConnectionError(Exception):
  pass