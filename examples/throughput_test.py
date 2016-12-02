import argparse
import time

import sys
from collections import defaultdict

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
    self.argparser.add_argument("-sw", "--serial-transmitter", help="serial device /dev file transmitter node", default=None)
    self.argparser.add_argument("-sr", "--serial-receiver", help="serial device /dev file receiver node", default=None)
    self.argparser.add_argument("-r", "--rate", help="baudrate for serial device", type=int, default=115200)
    self.argparser.add_argument("-uid", "--unicast-uid", help="UID to use for unicast transmission, "
                                                              "when not using receiver "
                                                              "(in hexstring, for example 0xb57000009151d)", default=None)
    self.argparser.add_argument("-to", "--receiver-timeout", help="timeout for the receiver (in seconds)", type=int, default=10)
    self.argparser.add_argument("-v", "--verbose", help="verbose", default=False, action="store_true")
    self.config = self.argparser.parse_args()

    if self.config.serial_transmitter == None and self.config.serial_receiver ==  None:
      self.argparser.error("At least a transmitter or receiver is required.")

    if self.config.serial_receiver == None and self.config.unicast_uid == None:
      self.argparser.error("When running without receiver a --unicast-uid parameter is required.")

    if self.config.serial_transmitter == None:
      self.transmitter_modem = None
      print("Running without transmitter")
    else:
      self.transmitter_modem = Modem(self.config.serial_transmitter, self.config.rate, None, show_logging=self.config.verbose)

    if self.config.serial_receiver == None:
      self.receiver_modem = None
      print("Running without receiver")
    else:
      self.receiver_modem = Modem(self.config.serial_receiver, self.config.rate, self.receiver_cmd_callback, show_logging=self.config.verbose)
      self.receiver_modem.send_command(Command.create_with_write_file_action_system_file(DllConfigFile(active_access_class=2)))
      print("Receiver scanning on Access Class = 2")



  def start(self):
    self.received_commands = defaultdict(list)
    payload = range(self.config.payload_size)

    if self.transmitter_modem != None:

      print("\n==> broadcast, no QoS, transmitter active access class = 0 ====")
      self.transmitter_modem.send_command(Command.create_with_write_file_action_system_file(DllConfigFile(active_access_class=0)))
      interface_configuration = Configuration(
        qos=QoS(resp_mod=QoS.RESP_MODE_NO),
        addressee=Addressee(
          access_class=2,
          id_type=IdType.BCAST
        )
      )

      self.start_transmitting(interface_configuration=interface_configuration, payload=payload)
      self.wait_for_receiver(payload)

      if self.receiver_modem != None:
        addressee_id = self.receiver_modem.uid
      else:
        addressee_id = int(self.config.unicast_uid, 16)

      print("\n==> unicast, with QoS, transmitter active access class = 0")
      interface_configuration = Configuration(
        qos=QoS(resp_mod=QoS.RESP_MODE_ANY),
        addressee=Addressee(
          access_class=2,
          id_type=IdType.UID,
          id=addressee_id
        )
      )

      self.start_transmitting(interface_configuration=interface_configuration, payload=payload)
      self.wait_for_receiver(payload)

      print("\n==> unicast, no QoS, transmitter active access class = 0")
      interface_configuration = Configuration(
        qos=QoS(resp_mod=QoS.RESP_MODE_NO),
        addressee=Addressee(
          access_class=2,
          id_type=IdType.UID,
          id=addressee_id
        )
      )

      self.start_transmitting(interface_configuration=interface_configuration, payload=payload)
      self.wait_for_receiver(payload)
    else:
      # receive only
      self.receiver_modem.start_reading()
      self.wait_for_receiver(payload)

  def start_transmitting(self, interface_configuration, payload):
    print("Running throughput test with payload size {} and interface_configuration {}\n\nrunning ...\n".format(len(payload), interface_configuration))

    if self.receiver_modem != None:
      self.received_commands = defaultdict(list)
      self.receiver_modem.start_reading()

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
      self.transmitter_modem.d7asp_fifo_flush(command)

    end = time.time()
    print("transmitter: sending {} messages completed in: {} s".format(self.config.msg_count, end - start))
    print("transmitter: throughput = {} bps with a payload size of {} bytes".format(
      (self.config.msg_count * self.config.payload_size * 8) / (end - start), self.config.payload_size)
    )

  def wait_for_receiver(self, payload):
    if self.receiver_modem == None:
      print("Running without receiver so we are not waiting for messages to be received ...")
    else:
      start = time.time()
      while len(self.received_commands.values()) < self.config.msg_count and time.time() - start < self.config.receiver_timeout:
        time.sleep(2)
        print("waiting for receiver to finish ...")

      print("finished receiving or timeout")
      self.receiver_modem.cancel_read()
      payload_has_errors = False
      for sender_cmd in self.received_commands.values():
        for cmd in sender_cmd:
          if type(cmd.actions[0].op) != ReturnFileData and cmd.actions[0].operand.data != payload:
            payload_has_errors = True
            print ("receiver: received unexpected command: {}".format(cmd))

      total_recv = sum(len(v) for v in self.received_commands.values())
      if payload_has_errors == False and total_recv == self.config.msg_count:
        print("receiver: OK: received {} messages with correct payload:".format(total_recv))
        for sender, cmds in self.received_commands.items():
          print("\t{}: {}".format(sender, len(cmds)))
      else:
        print("receiver: NOK: received messages {}:".format(total_recv))
        for sender, cmds in self.received_commands.items():
          print("\t{}: {}".format(sender, len(cmds)))

  def receiver_cmd_callback(self, cmd):
    uid = cmd.interface_status.operand.interface_status.addressee.id
    self.received_commands[uid].append(cmd)


if __name__ == "__main__":
  ThroughtPutTest().start()
