from d7a.system_files.dll_config import DllConfigFile
from d7a.system_files.firmware_version import FirmwareVersionFile
from d7a.system_files.system_file_ids import SystemFileIds
from d7a.system_files.uid import UidFile


class SystemFiles:
  files = {
    SystemFileIds.UID: UidFile(),
    SystemFileIds.FIRMWARE_VERSION: FirmwareVersionFile(),
    SystemFileIds.DLL_CONFIG: DllConfigFile(),
  }

  def get_all_system_files(self):
    return self.files