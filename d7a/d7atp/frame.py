
from d7a.support.schema import Validatable, Types
from d7a.d7atp.control import Control
from d7a.types.ct import CT
from d7a.alp.command import Command

class Frame(Validatable):

  SCHEMA = [{
    "control": Types.OBJECT(Control),
    "dialog_id": Types.INTEGER(min=0, max=255),
    "transaction_id": Types.INTEGER(min=0, max=255),
    "agc_rx_level_i": Types.INTEGER(min=0, max=31),
    "tl": Types.OBJECT(CT, nullable=True),
    "te": Types.OBJECT(CT, nullable=True),
    "ack_template": Types.OBJECT(nullable=True), # TODO
    "alp_command": Types.OBJECT(Command)
  }]

  def __init__(self, control, dialog_id, transaction_id, alp_command, agc_rx_level_i=10, tl=None, te=None, ack_template=None):
    if agc_rx_level_i == None:
      agc_rx_level_i = 10

    self.control = control
    self.dialog_id = dialog_id
    self.transaction_id = transaction_id
    self.agc_rx_level_i = agc_rx_level_i
    self.tl = tl
    self.te = te
    self.ack_template = ack_template
    self.alp_command = alp_command
    super(Frame, self).__init__()

  def __iter__(self):
    for byte in self.control: yield byte
    yield self.dialog_id
    yield self.transaction_id
    if self.control.has_agc:
      yield self.agc_rx_level_i

    if self.control.has_tl:
      yield self.tl

    if self.control.has_te:
      yield self.te

    if self.control.is_ack_not_void:
      for byte in self.ack_template: yield byte

    for byte in self.alp_command: yield byte