from d7a.alp.operands.file_header import FileHeaderOperand
from d7a.alp.operations.operation import Operation


class CreateNewFile(Operation):
  def __init__(self, *args, **kwargs):
    self.op     = 17
    self.operand_class = FileHeaderOperand
    super(CreateNewFile, self).__init__(*args, **kwargs)



