# action
# author: Christophe VG <contact@christophe.vg>

# class implementation of action parameters

# D7A ALP Action 
#
# ALP Control   1 Byte
#   b7    GROUP Group this action with the next one (see 11.4.3)
#   b6    RESP  Return ALP Error Template
#   b5-b0 OP    Operation describing the action
# ALP Operand   N Bytes
from bitstring import ConstBitStream

from d7a.alp.operations.requests import ReadFileData
from d7a.alp.operations.responses import ReturnFileData
from d7a.support.schema           import Validatable, Types

from d7a.alp.operations.operation import Operation
from d7a.alp.operations.nop       import NoOperation
from d7a.system_files.system_file_ids import SystemFileIds
from d7a.system_files.system_files import SystemFiles


class Action(Validatable):

  SCHEMA = [{
    "op"       : Types.BITS(6),
    "operation": Types.OBJECT(Operation),
    "operand"  : Types.OBJECT(nullable=True)  # there is no Operand base-class
  }]

  def __init__(self, operation=NoOperation()):
    self.operation = operation
    super(Action, self).__init__()

  @property
  def op(self):
    return self.operation.op

  @property
  def operand(self):
    return self.operation.operand

  def __str__(self):
    if isinstance(self.operation, ReturnFileData):
      # when reading a known system files we output the parsed data
      try:
        systemfile_type = SystemFiles().get_all_system_files()[SystemFileIds(self.operand.offset.id)]
        if systemfile_type is not None and systemfile_type.length == self.operand.length:
          systemfile_content = systemfile_type.parse(ConstBitStream(bytearray(self.operand.data)))
          return "{} content: {}".format(systemfile_type.__class__.__name__, systemfile_content)
      except:
        pass # not a SystemFile, do nothing
    elif isinstance(self.operation, ReadFileData):
      return "Read file {}".format(self.operand.offset.id)

    return "{}".format(type(self.operation).__name__)

  def __repr__(self):
    return "op={}, operand={}({})".format(type(self.operation).__name__, type(self.operand).__name__, self.operand)
