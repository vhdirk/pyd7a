import argparse
import threading
import time

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
    self.argparser.add_argument("-sr", "--serial-reader", help="serial device /dev file reader node", default="/dev/ttyUSB1")
    self.argparser.add_argument("-r", "--rate", help="baudrate for serial device", type=int, default=115200)
    self.config = self.argparser.parse_args()

    self.writer_modem = Modem(self.config.serial_writer, self.config.rate)
    #self.reader_modem = Modem(self.config.serial_reader, self.config.rate)

  def start(self):
    print("\n==> broadcast, no QoS, writer active access class = 2 ====")
    self.writer_modem.send_command(Command.create_with_write_file_action_system_file(DllConfigFile(active_access_class=2)))
    payload = range(self.config.payload_size)
    interface_configuration = Configuration(
      qos=QoS(resp_mod=QoS.RESP_MODE_NO),
      addressee=Addressee(
        access_class=2,
        id_type=IdType.BCAST
      )
    )

    self.test_throughput(interface_configuration=interface_configuration, payload=payload)

    print("\n==> broadcast, no QoS, writer active access class = 5")
    self.writer_modem.send_command(Command.create_with_write_file_action_system_file(DllConfigFile(active_access_class=5)))
    #self.test_throughput(interface_configuration=interface_configuration, payload=payload)

    # print("\n==> unicast, no QoS, writer active access class = 5")
    # interface_configuration = Configuration(
    #   qos=QoS(resp_mod=QoS.RESP_MODE_NO),
    #   addressee=Addressee(
    #     access_class=2,
    #     id_type=IdType.UID,
    #     id=self.reader_modem.uid
    #   )
    # )

    #self.test_throughput(interface_configuration=interface_configuration, payload=payload)

  def test_throughput(self, interface_configuration, payload):
    print("Running throughput test with payload size {} and interface_configuration {}".format(len(payload), interface_configuration))
    self.received_commands = []
    self.reading_done_event = threading.Event()
    self.reading_done_event.clear()
    self.stop_reading_thread = False
    reader_thread = threading.Thread(target=self.run_reader)
    #reader_thread.start()

    command = Command.create_with_return_file_data_action(
      file_id=0x40,
      data=payload,
      interface_type=InterfaceType.D7ASP,
      interface_configuration=interface_configuration
    )

    start = time.time()

    # command = Command.create_with_return_file_data_action(
    #   file_id=0x40,
    #   data=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    #   interface_type=InterfaceType.D7ASP,
    #   interface_configuration=Configuration(
    #     qos=QoS(resp_mod=QoS.RESP_MODE_ANY),
    #     addressee=Addressee(
    #       access_class=2,
    #       id_type=IdType.UID,
    #       id=0x000b570000078eb7
    #     )
    #   )
    # )


    for i in range(self.config.msg_count):
      self.writer_modem.d7asp_fifo_flush(command)

    end = time.time()
    print("writer: sending {} messages completed in: {} s".format(self.config.msg_count, end - start))
    print("writer: throughput = {} bps with a payload size of {} bytes".format(
      (self.config.msg_count * self.config.payload_size * 8) / (end - start), self.config.payload_size)
    )

    reading_timeout = 5
    success = self.reading_done_event.wait(reading_timeout)
    if not success:
      self.stop_reading_thread = True
      print("reading timeout after {} s".format(reading_timeout))

    payload_has_errors = False
    for cmd in self.received_commands:
      if type(cmd.actions[0].op) != ReturnFileData and cmd.actions[0].operand.data != payload:
        payload_has_errors = True
        print ("reader: received unexpected command: {}".format(cmd))

    if payload_has_errors == False and len(self.received_commands) == self.config.msg_count:
      print("reader: OK: received {} messages with correct payload".format(len(self.received_commands)))
    else:
      print("reader: NOK: received {} messages".format(len(self.received_commands)))

  def run_reader(self):
    for cmd in self.reader_modem.read_async():
      if self.stop_reading_thread:
        return

      self.received_commands.append(cmd)
      if len(self.received_commands) == self.config.msg_count:
        self.reader_modem.cancel_read()
        self.reading_done_event.set()



if __name__ == "__main__":
  ThroughtPutTest().start()
