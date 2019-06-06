import struct

from d7a.support.schema import Validatable, Types
from d7a.system_files.file import File
from d7a.system_files.system_file_ids import SystemFileIds
from d7a.alp.interface import InterfaceType
from d7a.alp.operands.interface_configuration import InterfaceConfiguration


class InterfaceConfigurationFile(File, Validatable):

  SCHEMA = [{
    "interface_configuration": Types.OBJECT(InterfaceConfiguration)
  }]

  def __init__(self, interface_configuration=InterfaceConfiguration(interface_id=InterfaceType.D7ASP, interface_configuration=None), file_id=0x1D):
    self.interface_configuration = interface_configuration
    if interface_configuration.interface_id == InterfaceType.D7ASP:
      File.__init__(self, file_id, 13)
    elif interface_configuration.interface_id == InterfaceType.LORAWAN_OTAA:
      File.__init__(self, file_id, 36)
    elif interface_configuration.interface_id == InterfaceType.LORAWAN_ABP:
      File.__init__(self, file_id, 44)
    Validatable.__init__(self)

  def __iter__(self):
    for byte in self.interface_configuration:
      yield byte

  def __str__(self):
    return "interface_configuration = {}".format(self.interface_configuration)
