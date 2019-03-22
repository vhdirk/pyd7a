#!/usr/bin/env python

import argparse
import os
from time import sleep
import sys
import logging

from d7a.alp.command import Command
from d7a.alp.interface import InterfaceType
from d7a.d7anp.addressee import Addressee, IdType
from d7a.dll.access_profile import AccessProfile
from d7a.dll.sub_profile import SubProfile
from d7a.phy.subband import SubBand
from d7a.sp.configuration import Configuration
from d7a.sp.qos import QoS, ResponseMode
from d7a.system_files.access_profile import AccessProfileFile
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


emFile = EngineeringModeFile(mode=1, flags=0, timeout=10, channel_header=ChannelHeader(ChannelCoding.PN9,ChannelClass.NORMAL_RATE,ChannelBand.BAND_868), center_freq_index=0, eirp=0)
print(emFile)

waiting_for_requests += 1

channel_index = 128
access_profile = AccessProfile(
    channel_header=ChannelHeader(channel_band=ChannelBand.BAND_868,
                               channel_coding=ChannelCoding.FEC_PN9,
                               channel_class=ChannelClass.LO_RATE),
    sub_profiles=[SubProfile(subband_bitmap=0), SubProfile(), SubProfile(),
                  SubProfile()],
    sub_bands=[SubBand(
      channel_index_start=channel_index,
      channel_index_end=channel_index,
      eirp=10,
      cca=86
    )] * 8
  )

modem.execute_command(Command.create_with_write_file_action_system_file(
  file=AccessProfileFile(access_profile=access_profile, access_specifier=0)),
  timeout_seconds=200
)

modem.execute_command(
  alp_command=Command.create_with_write_file_action(
    file_id=5,
    data=list(emFile),
    interface_type=InterfaceType.D7ASP,
    interface_configuration=Configuration(
      qos=QoS(resp_mod=ResponseMode.RESP_MODE_ALL),
      addressee=Addressee(
        access_class=0x01,
        id_type=IdType.NOID
      )
    )
  )
)


try:
  while True:
    sleep(5)
except KeyboardInterrupt:
  sys.exit(0)
