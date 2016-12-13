import unittest

from bitstring import ConstBitStream

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
    expected = [
      0b10000001, # AP control: FG scan, UNC, 1 subband
      5, # subnet
      0, # scan automation period
      0, # RFU
    ] + list(bytearray(self.valid_subband)) # TODO multiple subbands
    ap = AccessProfile(scan_type_is_foreground=True,
                       csma_ca_mode=CsmaCaMode.UNC,
                       subnet=5,
                       scan_automation_period=CT(0),
                       subbands=[self.valid_subband])

    bytes = bytearray(ap)
    for i in xrange(len(bytes)):
      self.assertEqual(expected[i], bytes[i])

    self.assertEqual(len(expected), len(bytes))

  def test_parse(self):
    bytes = [
       0b10000001,  # AP control: FG scan, UNC, 1 subband
       5,  # subnet
       0,  # scan automation period
       0,  # RFU
     ] + list(bytearray(self.valid_subband))

    ap = AccessProfile.parse(ConstBitStream(bytes=bytes))
    self.assertEqual(ap.scan_type_is_foreground, True)
    self.assertEqual(ap.csma_ca_mode, CsmaCaMode.UNC)
    self.assertEqual(ap.subnet, 5)
    self.assertEqual(ap.scan_automation_period.mant, CT(0).mant)
    self.assertEqual(ap.scan_automation_period.exp, CT(0).exp)
    self.assertEqual(len(ap.subbands), 1)