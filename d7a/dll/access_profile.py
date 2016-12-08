from enum import Enum

from d7a.phy.subband import Subband
from d7a.support.schema           import Validatable, Types
from d7a.types.ct import CT


class CsmaCaMode(Enum):
  UNC = 0
  AIND = 1
  RAIND = 2
  RIGD = 3


class AccessProfile(Validatable):

  # TODO update to D7AP v1.1
  SCHEMA = [{
    "scan_type_is_foreground": Types.BOOLEAN(),
    "csma_ca_mode": Types.ENUM(CsmaCaMode),
    "number_of_subbands": Types.INTEGER(min=0, max=8),
    "subnet": Types.BYTE(),
    "scan_automation_period": Types.OBJECT(CT),
    "subbands": Types.LIST(Subband, minlength=1)
  }]

  def __init__(self, scan_type_is_foreground, csma_ca_mode, subnet, scan_automation_period, subbands):
    self.scan_type_is_foreground = scan_type_is_foreground
    self.csma_ca_mode = csma_ca_mode
    self.subnet = subnet
    self.scan_automation_period = scan_automation_period
    self.subbands = subbands
    super(AccessProfile, self).__init__()

  @property
  def number_of_subbands(self):
    return len(self.subbands)

  def __iter__(self):
    control = self.scan_type_is_foreground << 7
    control += self.csma_ca_mode.value << 6
    control += self.number_of_subbands
    yield control
    yield self.subnet
    for byte in self.scan_automation_period: yield byte
    # skip Tc, this is already removed in oss7 as intermediate change towards v1.1
    yield 0 # RFU
    for subband in self.subbands:
      for byte in subband:
        yield byte