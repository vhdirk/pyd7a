import struct

from d7a.support.schema import Validatable, Types
from d7a.system_files.file import File
from d7a.system_files.system_file_ids import SystemFileIds


class FirmwareVersionFile(File, Validatable):

  SCHEMA = [{
    # TODO protocol version major
    # TODO protocol version major
    # custom field, specific to oss7
    "application_name": Types.STRING(maxlength=6),
    "git_sha1": Types.STRING(maxlength=7)
  }]

  def __init__(self, application_name="", git_sha1=""):
    self.application_name = application_name
    self.git_sha1 = git_sha1
    Validatable.__init__(self)
    File.__init__(self, SystemFileIds.FIRMWARE_VERSION, 13)

  @staticmethod
  def parse(s):
    application_name = s.read("bytes:6").decode("ascii")
    git_sha1 = s.read("bytes:7").decode("ascii")
    return FirmwareVersionFile(application_name=application_name, git_sha1=git_sha1)

  def __iter__(self):
    for byte in bytearray(self.application_name.encode("ASCII")):
      yield byte

    for byte in bytearray(self.git_sha1.encode("ASCII")):
      yield byte

