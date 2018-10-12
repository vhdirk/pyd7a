import unittest

from bitstring import ConstBitStream

from d7a.alp.interface import InterfaceType
from d7a.alp.operands.interface_configuration import InterfaceConfiguration
from d7a.alp.operands.lorawan_interface_configuration import LoRaWANInterfaceConfiguration
from d7a.alp.operations.forward import Forward
from d7a.sp.configuration import Configuration


class TestForward(unittest.TestCase):
  def test_byte_generation_forward_D7A_iface(self):
    d7asp_config = Configuration()
    forward_action = Forward(
      operand=InterfaceConfiguration(
        interface_id=InterfaceType.D7ASP,
        interface_configuration=d7asp_config
      )
    )

    bytes = bytearray(forward_action)
    self.assertEqual(len(bytes), len(bytearray(d7asp_config)) + 1)
    self.assertEqual(bytes[0], 0xD7)
    self.assertEqual(bytes[1:], bytearray(d7asp_config))
    # TODO configuration

  def test_byte_generation_forward_LoRaWAN_iface(self):
    lorawan_config = LoRaWANInterfaceConfiguration(
      use_ota_activation=False,
      request_ack=False,
      app_port=0x01,
      netw_session_key=[0] * 16,
      app_session_key=[1] * 16,
      dev_addr=[3] * 4,
      netw_id=[4] * 4
    )

    forward_action = Forward(
      operand=InterfaceConfiguration(
        interface_id=InterfaceType.LORAWAN,
        interface_configuration=lorawan_config
      )
    )

    bytes = bytearray(forward_action)
    self.assertEqual(len(bytes), len(bytearray(lorawan_config)) + 1)
    self.assertEqual(bytes[0], 0x02)
    self.assertEqual(bytes[1:], bytearray(lorawan_config))



