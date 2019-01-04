import struct

from d7a.support.schema import Validatable, Types
from d7a.system_files.file import File
from d7a.system_files.system_file_ids import SystemFileIds


class SecurityKeyFile(File, Validatable):

  SCHEMA = [{
    "key": Types.BITS(length=128)
  }]

  def __init__(self, key=0):
    self.key = key
    Validatable.__init__(self)
    File.__init__(self, SystemFileIds.NWL_SECURITY_KEY.value, 16)

  @staticmethod
  def parse(s):
    key = s.read("bytes:16")
    return SecurityKeyFile(key)

  def __iter__(self):
    for byte in [(self.key & (0xff << pos * 8)) >> pos * 8 for pos in range(16)]:
      yield byte

  def __str__(self):
    return "key={}".format(self.key)