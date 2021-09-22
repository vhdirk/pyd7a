#
# Copyright (c) 2015-2019 University of Antwerp, Aloxy NV.
#
# This file is part of pyd7a
# (see https://github.com/Sub-IoT/pyd7a).
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

# author: Christophe VG <contact@christophe.vg>
# class implementation of responses
from bitstring import ConstBitStream

from d7a.alp.operands.file_header import FileHeaderOperand
from d7a.alp.operations.operation import Operation

from d7a.alp.operands.file        import Data
from d7a.alp.operands.offset import Offset
from d7a.system_files.system_file_ids import SystemFileIds
from d7a.system_files.system_files import SystemFiles


class ReturnFileData(Operation):
  def __init__(self, *args, **kwargs):
    self.systemfile_type = None
    self.file_data_parsed = None
    self.op     = 32
    self.operand_class = Data
    super(ReturnFileData, self).__init__(*args, **kwargs)
    self.try_parse_system_file()

  def try_parse_system_file(self):
    # when reading a known system files we store the parsed data and filename
    try:
      systemfile_type = SystemFiles().files[SystemFileIds(self.operand.offset.id)]
    except:
      return
    # if the file size is between allocated and original length, try to parse it
    if (systemfile_type is not None) and (systemfile_type.length >= self.operand.length.value):
      self.systemfile_type = systemfile_type
      try:
        self.file_data_parsed = systemfile_type.parse(ConstBitStream(bytearray(self.operand.data)), self.operand.offset.offset.value, self.operand.length.value)
      except:
        self.systemfile_type = None
        self.file_data_parsed = None


class ReturnFileHeader(Operation):
  def __init__(self, *args, **kwargs):
    self.op     = 33
    self.operand_class = FileHeaderOperand
    super(ReturnFileHeader, self).__init__(*args, **kwargs)
