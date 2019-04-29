import unittest

from bitstring import ConstBitStream

from d7a.system_files.vid import VidFile

class TestVidFile(unittest.TestCase):

    def test_default_constructor(self):
        c = VidFile()
        self.assertEqual(c.vid, 0xFFFF)
        self.assertEqual(c.control, 0)


    def test_parsing(self):
        file_contents = [
            0x05, 0x03,  # VID
            0x65,        # Control
        ]

        config = VidFile.parse(ConstBitStream(bytes=file_contents))
        self.assertEqual(config.vid, 0x0503)
        self.assertEqual(config.control, 0x65)

    def test_byte_generation(self):
        bytes = bytearray(VidFile())
        self.assertEqual(len(bytes), 3)
        self.assertEqual(bytes[0], 0xFF)
        self.assertEqual(bytes[1], 0xFF)
        self.assertEqual(bytes[2], 0)

        bytes = bytearray(VidFile(vid=0x4536, control=0x12))
        self.assertEqual(len(bytes), 3)
        self.assertEqual(bytes[0], 0x45)
        self.assertEqual(bytes[1], 0x36)
        self.assertEqual(bytes[2], 0x12)
