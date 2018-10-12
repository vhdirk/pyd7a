import binascii
import pprint
import unittest

from bitstring import ConstBitStream

from d7a.alp.operands.lorawan_interface_configuration import LoRaWANInterfaceConfiguration


class TestLoRaWANInterfaceConfiguration(unittest.TestCase):
  def test_byte_generation(self):
    lorawan_config = LoRaWANInterfaceConfiguration(
      use_ota_activation=False,
      request_ack=True,
      app_port=0x01,
      netw_session_key=[0] * 16,
      app_session_key=[1] * 16,
      dev_addr=1,
      netw_id=2
    )


    bytes = bytearray(lorawan_config)
    self.assertEqual(len(bytes), 42)
    self.assertEqual(bytes[0], 1 << 1) # control byte
    self.assertEqual(bytes[1], 0x01) # app port
    self.assertEqual(bytes[2:18], bytearray([0] * 16))  # netw session key
    self.assertEqual(bytes[18:34], bytearray([1] * 16))  # app session key
    self.assertEqual(bytes[34:38], bytearray('\x00\x00\x00\x01'))  # dev addr
    self.assertEqual(bytes[38:], bytearray('\x00\x00\x00\x02'))  # netw id


  def test_parsing(self):
    bytes = [
      1 << 1,  # control byte
      2  # app port
    ]

    bytes.extend([0] * 16) # netw session key
    bytes.extend([1] * 16) # app session key
    bytes.extend([0, 0, 0, 1]) # dev addr
    bytes.extend([0, 0, 0, 2])  # netw id

    config = LoRaWANInterfaceConfiguration.parse(ConstBitStream(bytes=bytes))
    self.assertEqual(type(config), LoRaWANInterfaceConfiguration)
    self.assertEqual(config.use_ota_activation, False)
    self.assertEqual(config.request_ack, True)
    self.assertEqual(config.app_port, 2)
    self.assertEqual(config.netw_session_key, bytearray([0] * 16))
    self.assertEqual(config.app_session_key, bytearray([1] * 16))
    self.assertEqual(config.dev_addr, 1)
    self.assertEqual(config.netw_id, 2)

