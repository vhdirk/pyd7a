#!/usr/bin/env python

import argparse
import os

import logging

from d7a.alp.command import Command
from d7a.alp.interface import InterfaceType
from d7a.alp.operands.lorawan_interface_configuration import LoRaWANInterfaceConfiguration

from modem.modem import Modem

# This example can be used with a node running the mode app included in OSS-7, which is connect using the supplied serial device.
# It will send a LoRaWAN message print the result.
from util.logger import configure_default_logger


def received_command_callback(cmd):
  logging.info(cmd)
  if cmd.execution_completed:
    os._exit(0)

argparser = argparse.ArgumentParser()
argparser.add_argument("-d", "--device", help="serial device /dev file modem",
                            default="/dev/ttyUSB0")
argparser.add_argument("-r", "--rate", help="baudrate for serial device", type=int, default=115200)
argparser.add_argument("-v", "--verbose", help="verbose", default=False, action="store_true")
config = argparser.parse_args()

configure_default_logger(config.verbose)

modem = Modem(config.device, config.rate, )
modem.connect()
logging.info("Executing query...")
result = modem.execute_command(
  alp_command=Command.create_with_read_file_action(
    file_id=0x40,
    length=8,
    interface_type=InterfaceType.LORAWAN,
    interface_configuration=LoRaWANInterfaceConfiguration(
      use_ota_activation=False,
      request_ack=False,
      app_port=0x01,
      netw_session_key=[0] * 16,
      app_session_key=[1] * 16,
      dev_addr=[3] * 4,
      netw_id=[4] * 4
    )
  ),
  timeout_seconds=100
)

print result
