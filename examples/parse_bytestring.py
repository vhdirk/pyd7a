import fileinput

from d7a.serial_console_interface.parser import Parser

parser = Parser()
for hexstring in fileinput.input():
  hexstring = hexstring.strip().replace(' ', '')
  cmds, info = parser.parse(bytearray(hexstring.decode("hex")))
  for cmd in cmds:
    print cmd

  print info