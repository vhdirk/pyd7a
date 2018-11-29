# parser
# author: Christophe VG <contact@christophe.vg>

# a parser for ALP commands wrapped in serial interface frames

from bitstring                    import ConstBitStream, ReadError
from d7a.alp.parser               import Parser as AlpParser
from d7a.parse_error              import ParseError
import enum
import crc16
import struct
from pprint import pprint

up_counter = 1
down_counter = 1

class MessageType(enum.Enum):
  ALP_DATA = 0X01
  PING_REQUEST = 0X02
  PING_RESPONSE = 0X03
  LOGGING = 0X04

class Parser(object):

  def __init__(self, skip_alp_parsing=False):
    self.buffer = bytearray()
    self.skip_alp_parsing = skip_alp_parsing

  def shift_buffer(self, start):
    self.buffer = self.buffer[start:]
    return self

  def parse(self, msg):
    self.buffer.extend(msg)
    return self.parse_buffer()


#|sync|sync|counter|message type|length|crc1|crc2|
  @staticmethod
  def build_serial_frame(command):
    global up_counter
    buffer = bytearray([ 0xC0, 0])
    alp_command_bytes = bytearray(command)
    buffer.append(up_counter)
    temp = MessageType.ALP_DATA
    buffer.append(temp.value)
    buffer.append(len(alp_command_bytes))
    crc = crc16.crc16xmodem(bytes(alp_command_bytes), 0xffff)
    buffer = buffer + struct.pack(">H", crc)
    buffer = buffer + alp_command_bytes
    up_counter = up_counter + 1
    if up_counter > 255:
      up_counter = 0
    return buffer


  def parse_buffer(self):
    parsed = 0
    cmds   = []
    errors = []

    while True:
      (cmd, info) = self.parse_one_command_from_buffer()
      errors.extend(info["errors"])
      if cmd is None: break
      parsed += info["parsed"]
      cmds.append(cmd)

    info["parsed"] = parsed
    info["errors"] = errors
    return (cmds, info)

  def parse_one_command_from_buffer(self):
    retry       = True    # until we have one or don't have enough
    errors      = []
    cmd         = None
    bits_parsed = 0
    while retry and len(self.buffer) > 0:
      try:
        s           = ConstBitStream(bytes=self.buffer)
        cmd_length  = self.parse_serial_interface_header(s)
        if self.skip_alp_parsing:
          if s.length < cmd_length:
            raise ReadError

          cmd = s.read("bytes:" + str(cmd_length))
        else:
          cmd = AlpParser().parse(s, cmd_length)

        bits_parsed = s.pos
        self.shift_buffer(bits_parsed/8)
        retry = False         # got one, carry on
      except ReadError:       # not enough to read, carry on and wait for more
        retry = False
      except Exception as e: # actual problem with current buffer, need to skip
        errors.append({
          "error"   : e.args[0],
          "buffer"  : " ".join(map(lambda b: format(b, "02x"), self.buffer)),
          "pos"     : s.pos,
          "skipped" : self.skip_bad_buffer_content()
        })

    info = {
      "parsed" : bits_parsed,
      "buffer" : len(self.buffer) * 8,
      "errors" : errors
    }
    return (cmd, info)

  def skip_bad_buffer_content(self):
    # skip until we find 0xc0, which might be a valid starting point
    try:
      self.buffer.pop(0)                      # first might be 0xc0
      pos = self.buffer.index(b'\xc0')
      self.buffer = self.buffer[pos:]
      return pos + 1
    except IndexError:                        # empty buffer
      return 0
    except ValueError:                        # empty buffer, reported by .index
      skipped = len(self.buffer) + 1          # popped first item already
      self.buffer = bytearray()
      return skipped

  # |sync|sync|counter|message type|length|crc1|crc2|
  def parse_serial_interface_header(self, s):
    global down_counter
    b = s.read("uint:8")
    if b != 0xC0:
      raise ParseError("expected 0xC0, found {0}".format(b))
    version = s.read("uint:8")
    if version != 0:
      raise ParseError("Expected version 0, found {0}".format(version))
    counter = s.read("uint:8")
    if counter != down_counter:
      pprint("counters not equal") #TODO consequence?
      down_counter = counter #reset counter
    message_type = s.read("uint:8") #TODO different handler?
    cmd_len = s.read("uint:8")
    crc1 = s.read("uint:8")
    crc2 = s.read("uint:8")
    if len(self.buffer) - s.bytepos < cmd_len:
      raise ReadError("ALP command not complete yet, expected {0} bytes, got {1}".format(cmd_len, s.len - s.bytepos))
    payload = s.peeklist('bytes:b', b=cmd_len)[0]
    crc = crc16.crc16xmodem(bytes(payload), 0xffff)
    crc_calculated = int(bytes(bytearray([crc1, crc2])).encode('hex'), 16)
    down_counter = down_counter + 1
    if down_counter > 255:
      down_counter = 0
    if crc != crc_calculated:
      raise ParseError("CRC is incorrect found {0} and exprected {1}".format(crc, crc_calculated))

    return cmd_len

