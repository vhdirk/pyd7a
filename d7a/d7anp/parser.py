
from bitstring import ConstBitStream, ReadError

from d7a.d7anp.addressee import IdType, NlsMethod
from d7a.d7anp.frame import Frame
from d7a.d7anp.control import Control
from d7a.d7atp.parser import Parser as D7atpParser
from d7a.types.ct import CT


class Parser(object):

  def parse(self, bitstream, payload_length):
    control = Control.parse(bitstream)
    payload_length -= 1 # substract control

    origin_access_class = bitstream.read("uint:8")
    payload_length -= 1

    assert control.has_hopping == False, "Not implemented yet"
    assert control.nls_method == NlsMethod.NONE, "Not implemented yet"

    if not control.has_no_origin_access_id:
      if control.origin_id_type == IdType.VID:
        origin_access_id = map(ord, bitstream.read("bytes:2"))
        payload_length = payload_length - 2
      elif control.origin_id_type == IdType.UID:
        origin_access_id = map(ord, bitstream.read("bytes:8"))
        payload_length = payload_length - 8
      else:
        assert False
    else:
      origin_access_id = []

    #payload=map(ord,bitstream.read("bytes:" + str(payload_length)))
    d7atp_frame = D7atpParser().parse(bitstream, payload_length)
    return Frame(control=control, origin_access_class=origin_access_class, origin_access_id=origin_access_id, d7atp_frame=d7atp_frame)
