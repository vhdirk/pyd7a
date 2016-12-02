import argparse
import time

import sys

from d7a.alp.command import Command
from d7a.alp.interface import InterfaceType
from d7a.d7anp.addressee import Addressee, IdType
from d7a.sp.configuration import Configuration
from d7a.sp.qos import QoS
from modem.modem import Modem
from d7a.alp.operations.responses import ReturnFileData
from d7a.system_files.dll_config import DllConfigFile


class ThroughtPutTest:
  def __init__(self):
    self.argparser = argparse.ArgumentParser(
      fromfile_prefix_chars="@",
      description="Test throughput over 2 serial D7 modems"
    )

    self.argparser.add_argument("-n", "--msg-count", help="number of messages to transmit", type=int, default=10)
    self.argparser.add_argument("-p", "--payload-size", help="number of bytes of (appl level) payload to transmit", type=int, default=50)
    self.argparser.add_argument("-sw", "--serial-writer", help="serial device /dev file writer node", default="/dev/ttyUSB0")
    self.argparser.add_argument("-sr", "--serial-reader", help="serial device /dev file reader node", default=None)
    self.argparser.add_argument("-r", "--rate", help="baudrate for serial device", type=int, default=115200)
    self.argparser.add_argument("-v", "--verbose", help="verbose", default=False, action="store_true")
    self.config = self.argparser.parse_args()

    self.writer_modem = Modem(self.config.serial_writer, self.config.rate, None, show_logging=self.config.verbose)

    if self.config.serial_reader == None:
      self.reader_modem = None
    else:
      self.reader_modem = Modem(self.config.serial_reader, self.config.rate, self.reader_received_cmd_callback, show_logging=self.config.verbose)

  def start(self):
    payload = range(self.config.payload_size)

    print("\n==> broadcast, no QoS, writer active access class = 2 ====")
    self.writer_modem.send_command(Command.create_with_write_file_action_system_file(DllConfigFile(active_access_class=2)))
    interface_configuration = Configuration(
      qos=QoS(resp_mod=QoS.RESP_MODE_NO),
      addressee=Addressee(
        access_class=2,
        id_type=IdType.BCAST
      )
    )

    self.test_throughput(interface_configuration=interface_configuration, payload=payload)

    addressee_id = 0
    if self.reader_modem != None:
      addressee_id = self.reader_modem.uid

    print("\n==> unicast, with QoS, writer active access class = 2")
    interface_configuration = Configuration(
      qos=QoS(resp_mod=QoS.RESP_MODE_ANY),
      addressee=Addressee(
        access_class=2,
        id_type=IdType.UID,
        id=addressee_id
      )
    )

    self.test_throughput(interface_configuration=interface_configuration, payload=payload)

    print("\n==> unicast, no QoS, writer active access class = 2")
    interface_configuration = Configuration(
      qos=QoS(resp_mod=QoS.RESP_MODE_NO),
      addressee=Addressee(
        access_class=2,
        id_type=IdType.UID,
        id=addressee_id
      )
    )

    self.test_throughput(interface_configuration=interface_configuration, payload=payload)

  def test_throughput(self, interface_configuration, payload):
    print("Running throughput test with payload size {} and interface_configuration {}\n\nrunning ...\n".format(len(payload), interface_configuration))
    self.received_commands = []

    if self.reader_modem != None:
      self.reader_modem.start_reading()

    command = Command.create_with_return_file_data_action(
      file_id=0x40,
      data=payload,
      interface_type=InterfaceType.D7ASP,
      interface_configuration=interface_configuration
    )

    start = time.time()

    for i in range(self.config.msg_count):
      sys.stdout.write("{}/{}\r".format(i + 1, self.config.msg_count))
      sys.stdout.flush()
      self.writer_modem.d7asp_fifo_flush(command)

    end = time.time()
    print("writer: sending {} messages completed in: {} s".format(self.config.msg_count, end - start))
    print("writer: throughput = {} bps with a payload size of {} bytes".format(
      (self.config.msg_count * self.config.payload_size * 8) / (end - start), self.config.payload_size)
    )

    if self.reader_modem == None:
      print("Running without receiver so we are not waiting for messages to be received ...")
    else:
      while len(self.received_commands) < self.config.msg_count and time.time() - start < 5:
        time.sleep(0.5)
        print("waiting for reader to finish ...")

      print("finished reading or timeout")
      self.reader_modem.cancel_read()
      payload_has_errors = False
      for cmd in self.received_commands:
        if type(cmd.actions[0].op) != ReturnFileData and cmd.actions[0].operand.data != payload:
          payload_has_errors = True
          print ("reader: received unexpected command: {}".format(cmd))

      if payload_has_errors == False and len(self.received_commands) == self.config.msg_count:
        print("reader: OK: received {} messages with correct payload".format(len(self.received_commands)))
      else:
        print("reader: NOK: received {} messages".format(len(self.received_commands)))

  def reader_received_cmd_callback(self, cmd):
    self.received_commands.append(cmd)


if __name__ == "__main__":
  ThroughtPutTest().start()
