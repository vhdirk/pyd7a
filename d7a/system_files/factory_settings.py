import struct

from d7a.support.schema import Validatable, Types
from d7a.system_files.file import File
from d7a.system_files.system_file_ids import SystemFileIds


class FactorySettingsFile(File, Validatable):

  SCHEMA = [{
    "gain": Types.INTEGER(min=-128, max=127),
    "rx_BW_low_rate": Types.INTEGER(min=0, max=31),
    "rx_BW_normal_rate": Types.INTEGER(min=0, max=31),
    "rx_BW_high_rate": Types.INTEGER(min=0, max=31)
  }]

  def __init__(self, gain=0, rx_BW_low_rate=0x14, rx_BW_normal_rate=0x11, rx_BW_high_rate=0x01):
    self.gain = gain
    self.rx_BW_low_rate = rx_BW_low_rate
    self.rx_BW_normal_rate = rx_BW_normal_rate
    self.rx_BW_high_rate = rx_BW_high_rate
    File.__init__(self, SystemFileIds.FACTORY_SETTINGS, 4)
    Validatable.__init__(self)

  @staticmethod
  def parse(s):
    gain = s.read("int:8")
    rx_BW_low_rate = s.read("uint:8")
    rx_BW_normal_rate = s.read("uint:8")
    rx_BW_high_rate = s.read("uint:8")

    return FactorySettingsFile(gain=gain, rx_BW_low_rate=rx_BW_low_rate, rx_BW_normal_rate=rx_BW_normal_rate, rx_BW_high_rate=rx_BW_high_rate)

  def __iter__(self):
    yield self.gain
    yield self.rx_BW_low_rate
    yield self.rx_BW_normal_rate
    yield self.rx_BW_high_rate

  def __str__(self):
    return "gain={}, rx_BW_low_rate={}, rx_BW_normal_rate={}, rx_BW_high_rate={}".format(self.gain, hex(self.rx_BW_low_rate), hex(self.rx_BW_normal_rate), hex(self.rx_BW_high_rate))
