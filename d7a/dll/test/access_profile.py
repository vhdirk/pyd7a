import unittest

from d7a.dll.access_profile import AccessProfile, CsmaCaMode, Subband
from d7a.phy.channel_header import ChannelHeader, ChannelBand, ChannelCoding, ChannelClass
from d7a.types.ct import CT


class TestAccessProfile(unittest.TestCase):
  valid_subband = Subband(
    channel_header=ChannelHeader(
      channel_class=ChannelClass.NORMAL_RATE,
      channel_coding=ChannelCoding.PN9,
      channel_band=ChannelBand.BAND_433
    ),
    channel_index_start=0,
    channel_index_end=0,
    ccao=86,
    eirp=10
  )

  def test_validation_ok(self):
    ap = AccessProfile(scan_type_is_foreground=True,
                       csma_ca_mode=CsmaCaMode.UNC,
                       subnet=0,
                       scan_automation_period=CT(0),
                       subbands=[self.valid_subband])

  def test_validation_scan_type_is_foreground(self):
    def bad():
      ap = AccessProfile(scan_type_is_foreground="wrong",
                       csma_ca_mode=CsmaCaMode.UNC,
                       subnet=0,
                       scan_automation_period=CT(0),
                       subbands=[self.valid_subband])

    self.assertRaises(ValueError, bad)

  def test_validation_csma_ca_mode(self):
    def bad():
      ap = AccessProfile(scan_type_is_foreground=True,
                         csma_ca_mode="wrong",
                         subnet=0,
                         scan_automation_period=CT(0),
                         subbands=[self.valid_subband])

    self.assertRaises(ValueError, bad)

  def test_validation_subnet(self):
    def bad():
      ap = AccessProfile(scan_type_is_foreground=True,
                         csma_ca_mode=CsmaCaMode.UNC,
                         subnet="wrong",
                         scan_automation_period=CT(0),
                         subbands=[self.valid_subband])

    self.assertRaises(ValueError, bad)

  def test_validation_scan_automation_period(self):
    def bad():
      ap = AccessProfile(scan_type_is_foreground=True,
                         csma_ca_mode=CsmaCaMode.UNC,
                         subnet=0,
                         scan_automation_period="wrong",
                         subbands=[self.valid_subband])

    self.assertRaises(ValueError, bad)

  def test_validation_no_subband(self):
    def bad():
      ap = AccessProfile(scan_type_is_foreground=True,
                         csma_ca_mode=CsmaCaMode.UNC,
                         subnet=0,
                         scan_automation_period=CT(0),
                         subbands=[])

    self.assertRaises(ValueError, bad)

  def test_byte_generation(self):
    expected = []
    ap = AccessProfile(scan_type_is_foreground=True,
                       csma_ca_mode=CsmaCaMode.UNC,
                       subnet=0,
                       scan_automation_period=CT(0),
                       subbands=[self.valid_subband])

    self.assertEqual(expected, bytearray(ap))