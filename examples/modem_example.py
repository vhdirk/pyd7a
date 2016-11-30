#!/usr/bin/env python

import argparse

from d7a.alp.command import Command
from d7a.alp.interface import InterfaceType
from d7a.d7anp.addressee import Addressee, IdType
from d7a.sp.configuration import Configuration
from d7a.sp.qos import QoS
from d7a.system_files.uid import UidFile
from modem.modem import Modem


def received_command_callback(cmd):
  print cmd

argparser = argparse.ArgumentParser()
argparser.add_argument("-d", "--device", help="serial device /dev file modem",
                            default="/dev/ttyUSB0")
argparser.add_argument("-r", "--rate", help="baudrate for serial device", type=int, default=115200)
config = argparser.parse_args()

modem = Modem(config.device, config.rate, receive_callback=received_command_callback)
modem.start_reading()

modem.d7asp_fifo_flush(
  alp_command=Command.create_with_read_file_action_system_file(
    file=UidFile(),
    interface_type=InterfaceType.D7ASP,
    interface_configuration=Configuration(
      qos=QoS(resp_mod=QoS.RESP_MODE_ALL),
      addressee=Addressee(
        access_class=0,
        id_type=IdType.BCAST
      )
    )
  )
)

while True:
  pass
