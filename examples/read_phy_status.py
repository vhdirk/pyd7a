#!/usr/bin/env python
#
# Copyright (c) 2015-2019 University of Antwerp, Aloxy NV.
#
# This file is part of pyd7a
# (see https://github.com/MOSAIC-LoPoW/pyd7a).
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#

import argparse
import sys
import logging

from d7a.alp.command import Command
from d7a.system_files.phy_status import PhyStatusFile

from modem.modem import Modem

from util.logger import configure_default_logger


def received_command_callback(cmd):
  logging.info(cmd)
  if cmd.execution_completed:
      sys.exit(0)

argparser = argparse.ArgumentParser()
argparser.add_argument("-d", "--device", help="serial device /dev file modem",
                            default="/dev/ttyUSB0")
argparser.add_argument("-r", "--rate", help="baudrate for serial device", type=int, default=115200)
argparser.add_argument("-v", "--verbose", help="verbose", default=False, action="store_true")
argparser.add_argument("-l", "--length", help="length of scanned channels. If this is not right, it will still show data but not parse it", default=1, type=int)
config = argparser.parse_args()
configure_default_logger(config.verbose)

modem = Modem(config.device, config.rate, unsolicited_response_received_callback=received_command_callback)
modem.connect()

answers = modem.execute_command(
  alp_command=Command.create_with_read_file_action_system_file(
    file=PhyStatusFile(channel_status_list_length=config.length)
  )
)

for answer in answers:
  logging.info("answer is {}".format(answer.__str__()))


