import unittest

from bitstring import ConstBitStream

from d7a.phy.channel_header import ChannelHeader, ChannelCoding, ChannelClass, ChannelBand
from d7a.phy.channel_id import ChannelID


class TestChannelID(unittest.TestCase):
  def test_byte_generation(self):
    expected = [
      0b00101000,
      16, 0  # channel_id
    ]

    channel_id = ChannelID(
      ChannelHeader(channel_coding=ChannelCoding.PN9, channel_class=ChannelClass.NORMAL_RATE,channel_band=ChannelBand.BAND_433),
      16
    )

    bytes = bytearray(channel_id)
    for i in xrange(len(bytes)):
      self.assertEqual(expected[i], bytes[i])

    self.assertEqual(len(expected), len(bytes))

  def test_parse(self):
    bytes = [
      0b00101000, # header
      16, 0  # channel_id
    ]

    ch = ChannelID.parse(ConstBitStream(bytes=bytes))

    self.assertEqual(ch.channel_header.channel_coding, ChannelCoding.PN9)
    self.assertEqual(ch.channel_header.channel_class, ChannelClass.NORMAL_RATE)
    self.assertEqual(ch.channel_header.channel_band, ChannelBand.BAND_433)
    self.assertEqual(ch.channel_index, 16)

  def test_generate_channel_id_string(self):
    ch = ChannelID(
      channel_header=ChannelHeader(
        channel_class=ChannelClass.NORMAL_RATE,
        channel_coding=ChannelCoding.PN9,
        channel_band=ChannelBand.BAND_433
      ),
      channel_index=16
    )

    self.assertEqual(str(ch), "433NP016")

  def test_parse_channel_id_string(self):
    s = "868LF048"
    expected_ch = ChannelID(
      channel_header=ChannelHeader(
        channel_class=ChannelClass.LO_RATE,
        channel_coding=ChannelCoding.FEC_PN9,
        channel_band=ChannelBand.BAND_868
      ),
      channel_index=48
    )

    ch = ChannelID.from_string(s)
    self.assertEqual(ch.channel_header, expected_ch.channel_header)
    self.assertEqual(ch.channel_index, expected_ch.channel_index)