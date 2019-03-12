import struct

from d7a.support.schema import Validatable, Types
from d7a.system_files.file import File
from d7a.system_files.system_file_ids import SystemFileIds


class EngineeringModeFile(File, Validatable):

  SCHEMA = [{
    "mode": Types.INTEGER(min=0, max=255),
    "command": Types.INTEGER(min=0, max=0xFFFFFFFFFFFFFFFF)
  }]

  def __init__(self, mode=0, command=0):
    self.mode = mode
    self.command = command
    Validatable.__init__(self)
    File.__init__(self, SystemFileIds.ENGINEERING_MODE, 9)

  @staticmethod
  def parse(s):
    mode = s.read("uint:8")
    command = s.read("uint:64")
    return EngineeringModeFile(mode=mode, command=command)

  def __iter__(self):
    yield self.mode
    for byte in bytearray(struct.pack(">Q", self.command)):
      yield byte

  def __str__(self):
    return "mode={}, command={}".format(hex(self.mode), hex(self.command))