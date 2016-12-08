import unittest

from d7a.dll.access_profile import AccessProfile, CsmaCaMode, Subband
from d7a.types.ct import CT


class TestAccessProfile(unittest.TestCase):
  def test_validation_ok(self):
    ap = AccessProfile(scan_type_is_foreground=True,
                       csma_ca_mode=CsmaCaMode.UNC,
                       subnet=0,
                       scan_automation_period=CT(0),
                       subbands=[Subband()])

  def test_validation_scan_type_is_foreground(self):
    def bad():
      ap = AccessProfile(scan_type_is_foreground="wrong",
                       csma_ca_mode=CsmaCaMode.UNC,
                       subnet=0,
                       scan_automation_period=CT(0),
                       subbands=[Subband()])

    self.assertRaises(ValueError, bad)

  def test_validation_csma_ca_mode(self):
    def bad():
      ap = AccessProfile(scan_type_is_foreground=True,
                         csma_ca_mode="wrong",
                         subnet=0,
                         scan_automation_period=CT(0),
                         subbands=[Subband()])

    self.assertRaises(ValueError, bad)

  def test_validation_subnet(self):
    def bad():
      ap = AccessProfile(scan_type_is_foreground=True,
                         csma_ca_mode=CsmaCaMode.UNC,
                         subnet="wrong",
                         scan_automation_period=CT(0),
                         subbands=[Subband()])

    self.assertRaises(ValueError, bad)

  def test_validation_scan_automation_period(self):
    def bad():
      ap = AccessProfile(scan_type_is_foreground=True,
                         csma_ca_mode=CsmaCaMode.UNC,
                         subnet=0,
                         scan_automation_period="wrong",
                         subbands=[])

    self.assertRaises(ValueError, bad)

  def test_validation_no_subband(self):
    def bad():
      ap = AccessProfile(scan_type_is_foreground=True,
                         csma_ca_mode=CsmaCaMode.UNC,
                         subnet=0,
                         scan_automation_period=CT(0),
                         subbands=[])

    self.assertRaises(ValueError, bad)