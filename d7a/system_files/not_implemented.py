import struct

from d7a.support.schema import Validatable, Types
from d7a.system_files.file import File
from d7a.system_files.system_file_ids import SystemFileIds


class NotImplementedFile(File):
  def __init__(self, file_id, length=0):
    self.length = length
    File.__init__(self, file_id, length)

  def __iter__(self):
    for i in range(self.length):
      yield 0
