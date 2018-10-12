from enum import Enum


class InterfaceType(Enum):
  HOST = 0x00
  SERIAL = 0x01
  LORAWAN = 0x02
  D7ASP = 0xD7
