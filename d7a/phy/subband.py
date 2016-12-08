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
