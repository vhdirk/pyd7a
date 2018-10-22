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
      use_ota_activation=True,
      request_ack=False,
      app_port=0x01,
      netw_session_key=[ 0xC5, 0x2D, 0x67, 0xA1, 0xEF, 0x93, 0x7C, 0x6F, 0xD7, 0x2C, 0xE9, 0xC7, 0xBB, 0xEB, 0x71, 0xDD ],
      app_session_key=[ 0x7E, 0xC2, 0xD0, 0x2A, 0x96, 0x23, 0xE3, 0x9E, 0x7B, 0xBC, 0x6E, 0x14, 0xC6, 0x4A, 0x5C, 0x33 ],
      dev_addr=0x260113E8,
      netw_id=0x000017,
      device_eui=[ 0x00, 0x93, 0x04, 0x8E, 0xDE, 0x0D, 0x2E, 0xBB ],
      app_eui=[ 0x70, 0xB3, 0xD5, 0x7E, 0xD0, 0x01, 0x38, 0x8B ],
      app_key=[ 0x47, 0xF4, 0x87, 0xF5, 0x9C, 0x22, 0x44, 0xB7, 0x68, 0x2B, 0x5B, 0x37, 0x51, 0x42, 0xDB, 0xAA ]
    )
  ),
  timeout_seconds=100
)

print result
