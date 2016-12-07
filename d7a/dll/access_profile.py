from d7a.support.schema           import Validatable, Types
from d7a.types.ct import CT


class CsmaCaMode(object):
  UNC = 0
  AIND = 1
  RAIND = 2
  RIGD = 3
  ALL   = [ UNC, AIND, RAIND, RIGD ]

  @staticmethod
  def SCHEMA():
    return { "type": "integer", "allowed" : CsmaCaMode.ALL }

class AccessProfile(Validatable):

  # TODO update to D7AP v1.1
  SCHEMA = [{
    "scan_type_is_foreground": Types.BOOLEAN(),
    "csma_ca_mode": Types.INTEGER([CsmaCaMode.ALL]),
    "number_of_subbands": Types.INTEGER(min=0, max=8),
    "subnet": Types.BYTE(),
    "scan_automation_period": Types.OBJECT(CT),
    "transmission_timeout_period": Types.BYTE(), # TODO part of addressee now
    "control": Types.OBJECT(Control),
    "target_address": Types.BYTES(), # TODO max size?
    "d7anp_frame": Types.OBJECT(D7anpFrame), # TODO assuming foreground frames for now
    "crc16"  : Types.BITS(16) # TODO does not work, look into this later {'validator': validate_crc }
  }]

  def __init__(self, length, subnet, control, target_address, d7anp_frame, crc16):
    self.length = length
    self.subnet = subnet
    self.control = control
    self.target_address = target_address
    self.d7anp_frame = d7anp_frame
    self.crc16 = crc16
    # TODO validate CRC

    super(Frame, self).__init__()

  # def validate_crc(self, value, error):
  #   raw_data = []
  #   raw_data.append(self.length)
  #   raw_data.append(self.subnet)
  #   raw_data.append(self.control)
  #   raw_data.append(self.target_address)
  #   raw_data.append(self.payload)
  #   crc = CRCCCITT().calculate(raw_data)

  def __iter__(self):
    yield self.length
    yield self.subnet
    for byte in self.control: yield byte
    for byte in self.target_address: yield byte
    for byte in self.d7anp_frame: yield byte
    yield self.crc16