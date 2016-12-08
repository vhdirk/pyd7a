import unittest

from d7a.phy.channel_header import ChannelHeader, ChannelCoding, ChannelClass, ChannelBand


class TestChannelHeader(unittest.TestCase):
  def test_validation_ok(self):
    ch = ChannelHeader(channel_coding=ChannelCoding.PN9,
                       channel_class=ChannelClass.NORMAL_RATE,
                       channel_band=ChannelBand.BAND_433)

  def test_validation_channel_coding(self):
    def bad():
      ch = ChannelHeader(channel_coding="wrong",
                         channel_class=ChannelClass.NORMAL_RATE,
                         channel_band=ChannelBand.BAND_433)

    self.assertRaises(ValueError, bad)

  def test_validation_channel_class(self):
    def bad():
      ch = ChannelHeader(channel_coding=ChannelCoding.PN9,
                         channel_class="wrong",
                         channel_band=ChannelBand.BAND_433)

    self.assertRaises(ValueError, bad)

  def test_validation_channel_band(self):
    def bad():
      ch = ChannelHeader(channel_coding=ChannelCoding.PN9,
                         channel_class=ChannelClass.NORMAL_RATE,
                         channel_band="wrong")

    self.assertRaises(ValueError, bad)


  # TODO test byte generation