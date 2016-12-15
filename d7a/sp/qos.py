# qos
# author: Christophe VG <contact@christophe.vg>

# class implementation of qos parameters
from enum import Enum

from d7a.support.schema import Validatable, Types

class ResponseMode(Enum):
  RESP_MODE_NO = 0
  RESP_MODE_ALL = 1
  RESP_MODE_ANY = 2
  RESP_MODE_NO_RPT = 4
  RESP_MODE_ON_ERROR = 5
  RESP_MODE_PREFERRED = 6

class QoS(Validatable):
  SCHEMA = [{
    "nls": Types.BOOLEAN(),
    "stop_on_err": Types.BOOLEAN(),
    "record" : Types.BOOLEAN(),
    "resp_mod"     : Types.ENUM(ResponseMode)
  }]
  
  def __init__(self, nls=False, resp_mod=ResponseMode.RESP_MODE_NO, stop_on_err=False, record=False):
    self.nls          = nls
    self.resp_mod     = resp_mod
    self.stop_on_err  = stop_on_err
    self.record       = record
    super(QoS, self).__init__()

  def __iter__(self):
    byte = 0
    if self.nls: byte |= 1 << 7
    if self.stop_on_err: byte |= 1 << 6
    if self.record: byte |= 1 << 5
    # rfu
    byte += self.resp_mod.value
    yield byte

  @staticmethod
  def parse(s):
    nls = s.read("bool")
    stop_on_error = s.read("bool")
    record = s.read("bool")
    _ = s.read("uint:2") # RFU
    resp_mode = ResponseMode(int(s.read("uint:3")))
    return QoS(nls=nls, stop_on_err=stop_on_error, record=record, resp_mod=resp_mode)

  def __str__(self):
    return str(self.as_dict())