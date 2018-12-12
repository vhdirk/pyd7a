from enum import Enum


class InterfaceType(Enum):
  HOST = 0x00
  SERIAL = 0x01
  LORAWAN_ABP = 0x02
  LORAWAN_OTAA = 0x03
  D7ASP = 0xD7