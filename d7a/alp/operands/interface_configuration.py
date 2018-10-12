from d7a.alp.interface import InterfaceType
from d7a.support.schema import Validatable, Types


class InterfaceConfiguration(Validatable):
  SCHEMA = [{
    "interface_id"        : Types.ENUM(InterfaceType),
    "interface_configuration"    : Types.OBJECT(Validatable, nullable=True)
  }]

  def __init__(self, interface_id, interface_configuration=None):
    self.interface_id = interface_id
    self.interface_configuration   = interface_configuration
    super(InterfaceConfiguration, self).__init__()

  def __iter__(self):
    yield self.interface_id.value
    if self.interface_configuration:
      for byte in self.interface_configuration: yield byte

  def __str__(self):
    return "interface-id={}, configuration={}".format(self.interface_id, self.interface_configuration)
