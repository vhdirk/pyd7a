import struct

from d7a.support.schema import Validatable, Types
from d7a.system_files.file import File
from d7a.system_files.system_file_ids import SystemFileIds


class VidFile(File, Validatable):
  SCHEMA = [{
    "vid": Types.INTEGER(min=0, max=0xFFFF),
    "control": Types.INTEGER(min=0, max=0xFF)
  }]


  def __init__(self, vid=0xFFFF, control=0x00):
    self.vid = vid
    self.control = control
    File.__init__(self, SystemFileIds.VID.value, 3)
    Validatable.__init__(self)

  @staticmethod
  def parse(s):
    vid = s.read("uint:16")
    control = s.read("uint:8")
    return VidFile(vid=vid, control=control)

  def __iter__(self):
    for byte in bytearray(struct.pack(">H", self.vid)):
      yield byte
    yield self.control


  def __str__(self):
    return "vid={}, control={}".format(hex(self.vid), hex(self.control))
