import struct

from d7a.support.schema import Validatable, Types


class LoRaWANInterfaceConfiguration(Validatable):

  SCHEMA = [{
    # # TODO first byte is extensible with other fields, for example ADR or SFx
    # "use_ota_activation": Types.BOOLEAN(),
    # "request_ack": Types.BOOLEAN(),
    # "application_port": Types.BYTE(),
    # "netw_session_key": Types.BYTES(),
    # "app_session_key": Types.BYTES(),
    # "dev_addr": Types.BYTES(),
    # "netw_id": Types.BYTES(),
    # "device_eui": Types.BYTES(),
    # "app_eui": Types.BYTES(),
    # "app_key": Types.BYTES()
  }]

  def __init__(self, use_ota_activation, request_ack, app_port, netw_session_key, app_session_key, dev_addr, netw_id, device_eui, app_eui, app_key):
    self.use_ota_activation = use_ota_activation
    self.request_ack = request_ack
    self.app_port = app_port
    self.netw_session_key = netw_session_key
    self.app_session_key = app_session_key
    self.dev_addr = dev_addr
    self.netw_id = netw_id
    self.device_eui = device_eui
    self.app_eui = app_eui
    self.app_key = app_key
    super(LoRaWANInterfaceConfiguration, self).__init__()

  def __iter__(self):
    byte = 0
    if self.use_ota_activation:
      byte |= 1
    if self.request_ack:
      byte |= 1 << 1

    yield byte
    yield self.app_port
    if self.use_ota_activation:
      for byte in self.device_eui:
        yield byte

      for byte in self.app_eui:
        yield byte

      for byte in self.app_key:
        yield byte
    else:
      for byte in self.netw_session_key:
        yield byte

      for byte in self.app_session_key:
        yield byte

      for byte in bytearray(struct.pack(">I", self.dev_addr)):
        yield byte

      for byte in bytearray(struct.pack(">I", self.netw_id)):
        yield byte

  def __str__(self):
    return str(self.as_dict())

  @staticmethod
  def parse(s):
    _rfu = s.read("bits:6")
    request_ack = s.read("bool")
    use_ota = s.read("bool")
    app_port = s.read("uint:8")
    if use_ota:
      device_eui = s.read("bytes:8")
      app_eui = s.read("bytes:8")
      app_key = s.read("bytes:16")
      netw_session_key = [0] * 16,
      app_session_key = [1] * 16,
      dev_addr = 1,
      netw_id = 2,
    else:
      netw_session_key = s.read("bytes:16")
      app_session_key = s.read("bytes:16")
      dev_addr = s.read("uint:32")
      netw_id = s.read("uint:32")
      device_eui = [0] * 8,
      app_eui = [0] * 8,
      app_key = [0] * 16
    return LoRaWANInterfaceConfiguration(
      use_ota_activation = use_ota,
      request_ack = request_ack,
      app_port = app_port,
      netw_session_key = netw_session_key,
      app_session_key = app_session_key,
      dev_addr = dev_addr,
      netw_id = netw_id,
      device_eui=device_eui,
      app_eui=app_eui,
      app_key=app_key
    )



