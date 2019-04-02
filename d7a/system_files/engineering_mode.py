import struct

from d7a.support.schema import Validatable, Types
from d7a.system_files.file import File
from d7a.system_files.system_file_ids import SystemFileIds
from d7a.phy.channel_header import ChannelHeader,ChannelCoding,ChannelClass,ChannelBand


class EngineeringModeFile(File, Validatable):

  SCHEMA = [{
    "mode": Types.INTEGER(min=0, max=255),
    "flags": Types.INTEGER(min=0, max=255),
    "timeout": Types.INTEGER(min=0, max=255),
    "channel_header": Types.OBJECT(ChannelHeader),
    "center_freq_index": Types.INTEGER(min=0, max=0xFFFF),
    "eirp": Types.INTEGER(min=-128, max=127)
  }]

  def __init__(self, mode=0, flags=0, timeout=0, channel_header=ChannelHeader(ChannelCoding.PN9,ChannelClass.LO_RATE,ChannelBand.BAND_868), center_freq_index=0, eirp=0):
    self.mode = mode
    self.flags = flags
    self.timeout = timeout
    self.channel_header = channel_header
    self.center_freq_index = center_freq_index
    self.eirp = eirp
    File.__init__(self, SystemFileIds.ENGINEERING_MODE, 9)
    Validatable.__init__(self)

  @staticmethod
  def parse(s):
    mode = s.read("uint:8")
    flags = s.read("uint:8")
    timeout = s.read("uint:8")
    s.read("uint:1")  # RFU
    channel_band_value = s.read("uint:3")
    if (channel_band_value == 0):
      channel_band_value = 3 ## fix schema error if all zeros are read
    channel_band = ChannelBand(channel_band_value)
    channel_class = ChannelClass(s.read("uint:2"))
    channel_coding = ChannelCoding(s.read("uint:2"))

    channel_header = ChannelHeader(channel_coding=channel_coding, channel_class=channel_class, channel_band=channel_band)
    center_freq_index = s.read("uint:16")
    eirp = s.read("int:8")
    s.read("uint:16")  # RFU
    return EngineeringModeFile(mode=mode, flags=flags, timeout=timeout, channel_header=channel_header, center_freq_index=center_freq_index, eirp=eirp)

  def __iter__(self):
    yield self.mode
    yield self.flags
    yield self.timeout
    for byte in self.channel_header:
      yield byte
    for byte in bytearray(struct.pack("<h", self.center_freq_index)): yield byte
    yield self.eirp
    yield 0
    yield 0

  def __str__(self):
    return "mode={}, flags={}, timeout={}, channel_header={{{}}}, center_freq_index={}, eirp={}".format(hex(self.mode), hex(self.flags),self.timeout, self.channel_header, self.center_freq_index, self.eirp)
