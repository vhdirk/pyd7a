import unittest

from bitstring import ConstBitStream

from d7a.phy.channel_header import ChannelHeader, ChannelCoding, ChannelClass, ChannelBand
from d7a.phy.subband import Subband


class TestSubband(unittest.TestCase):
  valid_channel_header = ChannelHeader(channel_band=ChannelBand.BAND_433,
                                       channel_class=ChannelClass.NORMAL_RATE,
                                       channel_coding=ChannelCoding.PN9)

  def test_validation_ok(self):
    sb = Subband(channel_header=self.valid_channel_header,
                 channel_index_start=0,
                 channel_index_end=0,
                 eirp=10,
                 ccao=86)

  def test_validation_channel_header(self):
    def bad(): sb = Subband(channel_header=None,
                            channel_index_start=0,
                            channel_index_end=0,
                            eirp=10,
                            ccao=86)
    self.assertRaises(ValueError, bad)

  def test_validation_channel_index_start(self):
    def bad(): sb = Subband(channel_header=self.valid_channel_header,
                            channel_index_start=-10,
                            channel_index_end=0,
                            eirp=10,
                            ccao=86)
    self.assertRaises(ValueError, bad)


  def test_validation_channel_index_end(self):
    def bad(): sb = Subband(channel_header=self.valid_channel_header,
                            channel_index_start=0,
                            channel_index_end=-10,
                            eirp=10,
                            ccao=86)
    self.assertRaises(ValueError, bad)

  def test_validation_eirp(self):
    def bad(): sb = Subband(channel_header=self.valid_channel_header,
                            channel_index_start=0,
                            channel_index_end=0,
                            eirp=200,
                            ccao=86)
    self.assertRaises(ValueError, bad)


  def test_validation_cca(self):
    def bad(): sb = Subband(channel_header=self.valid_channel_header,
                            channel_index_start=0,
                            channel_index_end=0,
                            eirp=10,
                            ccao=-10)
    self.assertRaises(ValueError, bad)

  def test_byte_generation(self):
    expected = list(bytearray(self.valid_channel_header)) + [
      0, 0, # channel index start
      16, 0, # channel index end
      10, # eirp
      86 # ccao
    ]
    sb = Subband(channel_header=self.valid_channel_header,
                 channel_index_start=0,
                 channel_index_end=16,
                 eirp=10,
                 ccao=86)
    bytes = bytearray(sb)
    for i in xrange(len(bytes)):
      self.assertEqual(expected[i], bytes[i])

    self.assertEqual(len(expected), len(bytes))

  def test_parse(self):
    bytes = list(bytearray(self.valid_channel_header)) + [
      0, 0,  # channel index start
      16, 0,  # channel index end
      10,  # eirp
      86  # ccao
    ]

    sb = Subband.parse(ConstBitStream(bytes=bytes))
    self.assertEqual(sb.channel_header.channel_band, self.valid_channel_header.channel_band)
    self.assertEqual(sb.channel_header.channel_coding, self.valid_channel_header.channel_coding)
    self.assertEqual(sb.channel_header.channel_class, self.valid_channel_header.channel_class)
    self.assertEqual(sb.channel_index_start, 0)
    self.assertEqual(sb.channel_index_end, 16)
    self.assertEqual(sb.eirp, 10)
    self.assertEqual(sb.ccao, 86)