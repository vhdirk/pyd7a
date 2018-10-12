import struct

from d7a.support.schema import Validatable, Types


class LoRaWANInterfaceConfiguration(Validatable):

  SCHEMA = [{
    # "use_ota_activation": Types.BOOLEAN(),
    # "request_ack": Types.BOOLEAN(),
    # # TODO first byte is extensible with other fields, for example ADR or SFx
    # "application_port": Types.BYTE(),
    # # TODO assuming ABP for now
    # "netw_session_key": Types.BYTES(),
    # "app_session_key": Types.BYTES(),
    # "dev_addr": Types.BYTES(),
    # "netw_id": Types.BYTES()
  }]

  def __init__(self, use_ota_activation, request_ack, app_port, netw_session_key, app_session_key, dev_addr, netw_id):
    self.use_ota_activation = use_ota_activation
    self.request_ack = request_ack
    self.app_port = app_port
    self.netw_session_key = netw_session_key
    self.app_session_key = app_session_key
    self.dev_addr = dev_addr
    self.netw_id = netw_id
    super(LoRaWANInterfaceConfiguration, self).__init__()

  def __iter__(self):
    byte = 0
    if self.use_ota_activation:
      byte |= 1 << 7
    if self.request_ack:
      byte |= 1 << 6

    yield byte
    yield self.app_port
    for byte in self.netw_session_key:
      yield byte

    for byte in self.app_session_key:
      yield byte

    for byte in self.dev_addr:
      yield byte

    for byte in self.netw_id:
      yield byte

  def __str__(self):
    return str(self.as_dict())

  @staticmethod
  def parse(s):
    use_ota = s.read("bool")
    request_ack = s.read("bool")
    _rfu = s.read("bits:6")
    app_port = s.read("uint:8")
    netw_session_key = s.read("bytes:16")
    app_session_key = s.read("bytes:16")
    dev_addr = s.read("bytes:4")
    netw_id = s.read("bytes:4")
    return LoRaWANInterfaceConfiguration(
      use_ota_activation = use_ota,
      request_ack = request_ack,
      app_port = app_port,
      netw_session_key = netw_session_key,
      app_session_key = app_session_key,
      dev_addr = dev_addr,
      netw_id = netw_id
    )