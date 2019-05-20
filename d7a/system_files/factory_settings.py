import struct

from d7a.support.schema import Validatable, Types
from d7a.system_files.file import File
from d7a.system_files.system_file_ids import SystemFileIds


class FactorySettingsFile(File, Validatable):

  SCHEMA = [{
    "gain": Types.INTEGER(min=-128, max=127),
    "rx_bw_low_rate": Types.INTEGER(min=0, max=0xFFFFFFFF),
    "rx_bw_normal_rate": Types.INTEGER(min=0, max=0xFFFFFFFF),
    "rx_bw_high_rate": Types.INTEGER(min=0, max=0xFFFFFFFF)
  }]

  def __init__(self, gain=0, rx_bw_low_rate=10468, rx_bw_normal_rate=78646, rx_bw_high_rate=125868):
    self.gain = gain
    self.rx_bw_low_rate = rx_bw_low_rate
    self.rx_bw_normal_rate = rx_bw_normal_rate
    self.rx_bw_high_rate = rx_bw_high_rate
    File.__init__(self, SystemFileIds.FACTORY_SETTINGS, 0x0D)
    Validatable.__init__(self)

  @staticmethod
  def parse(s):
    gain = s.read("int:8")
    rx_bw_low_rate = s.read("uint:32")
    rx_bw_normal_rate = s.read("uint:32")
    rx_bw_high_rate = s.read("uint:32")

    return FactorySettingsFile(gain=gain, rx_bw_low_rate=rx_bw_low_rate, rx_bw_normal_rate=rx_bw_normal_rate, rx_bw_high_rate=rx_bw_high_rate)

  def __iter__(self):
    yield self.gain
    for byte in bytearray(struct.pack(">I",self.rx_bw_low_rate)):
      yield byte
    for byte in bytearray(struct.pack(">I",self.rx_bw_normal_rate)):
      yield byte
    for byte in bytearray(struct.pack(">I",self.rx_bw_high_rate)):
      yield byte

  def __str__(self):
    return "gain={}, rx_bw_low_rate={}, rx_bw_normal_rate={}, rx_bw_high_rate={}".format(self.gain, hex(self.rx_bw_low_rate), hex(self.rx_bw_normal_rate), hex(self.rx_bw_high_rate))
