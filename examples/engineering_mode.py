#!/usr/bin/env python

import argparse
import os
from time import sleep
import sys
import logging

from d7a.alp.command import Command
from d7a.alp.interface import InterfaceType
from d7a.d7anp.addressee import Addressee, IdType
from d7a.sp.configuration import Configuration
from d7a.sp.qos import QoS, ResponseMode
from d7a.system_files.uid import UidFile
from d7a.system_files.engineering_mode import EngineeringModeFile
from d7a.system_files.system_file_ids import SystemFileIds
from d7a.phy.channel_header import ChannelHeader,ChannelCoding,ChannelClass,ChannelBand
from modem.modem import Modem

# This example can be used with a node running the gateway app included in OSS-7, which is connect using the supplied serial device.
# It will query the sensor file (file 0x40) from other nodes running sensor_pull, using adhoc synchronization and print the results.
from util.logger import configure_default_logger

waiting_for_requests = 0

def received_command_callback(cmd):
  global waiting_for_requests
  logging.info(cmd)
  if cmd.execution_completed:
    waiting_for_requests -= 1
    if waiting_for_requests <= 0:
      os._exit(0)

argparser = argparse.ArgumentParser()
argparser.add_argument("-d", "--device", help="serial device /dev file modem",
                            default="/dev/ttyUSB0")
argparser.add_argument("-r", "--rate", help="baudrate for serial device", type=int, default=115200)
argparser.add_argument("-v", "--verbose", help="verbose", default=False, action="store_true")
config = argparser.parse_args()

configure_default_logger(config.verbose)

modem = Modem(config.device, config.rate, unsolicited_response_received_callback=received_command_callback)
modem.connect()
logging.info("Executing query...")

emFile = EngineeringModeFile(mode=1, flags=0, timeout=10, channel_header=ChannelHeader(ChannelCoding.PN9,ChannelClass.NORMAL_RATE,ChannelBand.BAND_868), center_freq_index=0, eirp= 0)
print(emFile)

waiting_for_requests += 1
modem.execute_command_async(
  # alp_command=Command.create_with_write_file_action_system_file(
  #   file=emFile,
  #   interface_type=InterfaceType.HOST
  # )
  alp_command=Command.create_with_write_file_action(
    file_id=5,
    data=list(emFile),
    interface_type=InterfaceType.HOST
  )
)


try:
  while True:
    sleep(5)
except KeyboardInterrupt:
  sys.exit(0)
