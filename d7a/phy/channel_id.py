import struct

from d7a.phy.channel_header import ChannelHeader
from d7a.support.schema import Validatable, Types


class ChannelID(Validatable):
  
  SCHEMA = [{
    "channel_header": Types.OBJECT(ChannelHeader),
    "channel_index": Types.INTEGER(min=0, max=0xFFFF),
  }]

  def __init__(self, channel_header, channel_index):
    self.channel_header = channel_header
    self.channel_index = channel_index
    super(ChannelID, self).__init__()

  def __iter__(self):
    for byte in self.channel_header: yield byte
    for byte in bytearray(struct.pack("<h", self.channel_index)): yield byte


  @staticmethod
  def parse(s):
    channel_header = ChannelHeader.parse(s)
    channel_index = s.read("uint:16")
    return ChannelID(channel_header=channel_header, channel_index=channel_index)

  def __str__(self):
    return "{0}{1:0>3}".format(self.channel_header, self.channel_index)

  @staticmethod
  def from_string(s):
      channel_header = ChannelHeader.from_string(s[0:5])
      channel_index = int(s[5:8])
      return ChannelID(channel_header=channel_header, channel_index=channel_index)