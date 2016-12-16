import struct

from d7a.phy.channel_header import ChannelHeader
from d7a.support.schema import Validatable, Types


class Subband(Validatable):
  # TODO update to D7AP v1.1

  SCHEMA = [{
    "channel_header": Types.OBJECT(ChannelHeader),
    "channel_index_start": Types.INTEGER(min=0, max=0xFFFF),
    "channel_index_end": Types.INTEGER(min=0, max=0xFFFF),
    "eirp": Types.INTEGER(min=-128, max=127),
    "ccao": Types.INTEGER(min=0, max=128),
  }]

  def __init__(self, channel_header, channel_index_start, channel_index_end, eirp, ccao):
    self.channel_header= channel_header
    self.channel_index_start = channel_index_start
    self.channel_index_end = channel_index_end
    self.eirp = eirp
    self.ccao = ccao
    super(Subband, self).__init__()

  def __iter__(self):
    for byte in self.channel_header: yield byte
    for byte in bytearray(struct.pack("<h", self.channel_index_start)): yield byte
    for byte in bytearray(struct.pack("<h", self.channel_index_end)): yield byte
    yield self.eirp
    yield self.ccao

  @staticmethod
  def parse(s):
    channel_header = ChannelHeader.parse(s)
    channel_index_start = struct.unpack("<h", s.read("bytes:2"))[0]
    channel_index_end = struct.unpack("<h", s.read("bytes:2"))[0]
    eirp = s.read("uint:8")
    ccao = s.read("uint:8")

    return Subband(channel_header=channel_header,
                   channel_index_start=channel_index_start,
                   channel_index_end=channel_index_end,
                   eirp=eirp,
                   ccao=ccao)

  def __str__(self):
    return "channel_header={}, channel_index_start={}, channel_index_end={}, eirp={}, ccao={}".format(
      self.channel_header,
      self.channel_index_start,
      self.channel_index_end,
      self.eirp,
      self.ccao
    )