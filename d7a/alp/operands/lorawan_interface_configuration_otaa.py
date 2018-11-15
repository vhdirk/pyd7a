import struct

from d7a.support.schema import Validatable, Types


class LoRaWANInterfaceConfigurationOTAA(Validatable):

  SCHEMA = [{
    # # TODO first byte is extensible with other fields, for example ADR or SFx
    # "request_ack": Types.BOOLEAN(),
    # "application_port": Types.BYTE(),
    # "device_eui": Types.BYTES(),
    # "app_eui": Types.BYTES(),
    # "app_key": Types.BYTES()
  }]

  def __init__(self, request_ack, app_port, device_eui, app_eui, app_key):
    self.request_ack = request_ack
    self.app_port = app_port
    self.device_eui = device_eui
    self.app_eui = app_eui
    self.app_key = app_key
    super(LoRaWANInterfaceConfigurationOTAA, self).__init__()

  def __iter__(self):
    byte = 0
    if self.request_ack:
      byte |= 1 << 1

    yield byte
    yield self.app_port

    for byte in self.device_eui:
      yield byte

    for byte in self.app_eui:
      yield byte

    for byte in self.app_key:
      yield byte


  def __str__(self):
    return str(self.as_dict())

  @staticmethod
  def parse(s):
    _rfu = s.read("bits:6")
    request_ack = s.read("bool")
    _rfu = s.read("bits:1")
    app_port = s.read("uint:8")

    device_eui = s.read("bytes:8")
    app_eui = s.read("bytes:8")
    app_key = s.read("bytes:16")

    return LoRaWANInterfaceConfigurationOTAA(
      request_ack=request_ack,
      app_port=app_port,
      device_eui=device_eui,
      app_eui=app_eui,
      app_key=app_key
    )



