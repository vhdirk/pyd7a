
from bitstring import ConstBitStream, ReadError
from d7a.d7atp.frame import Frame
from d7a.d7atp.control import Control
from d7a.alp.parser import Parser as AlpParser
from d7a.types.ct import CT


class Parser(object):

  def parse(self, bitstream, payload_length):
    control = Control.parse(bitstream)
    payload_length = payload_length - 1 # subtract control byte

    dialog_id = bitstream.read("uint:8")
    payload_length = payload_length - 1

    transaction_id = bitstream.read("uint:8")
    payload_length = payload_length - 1

    target_rx_level_i = None
    if control.has_agc:
      target_rx_level_i = bitstream.read("uint:8")
      payload_length -= 1

    tl = None
    if control.has_tl:
      tl = CT.parse(bitstream)
      payload_length -= 1

    te = None
    if control.has_te:
      te = CT.parse(bitstream)
      payload_length -= 1

    ack_template = None
    if control.is_ack_not_void:
      transaction_id_start = bitstream.read("uint:8")
      payload_length = payload_length - 1
      transaction_id_stop = bitstream.read("uint:8")
      payload_length = payload_length - 1
      assert transaction_id_start == transaction_id, "Other case not implemented yet"
      assert transaction_id_stop == transaction_id, "Other case not implemented yet"
      # TODO ack bitmap (for when transaction_id_start != transaction_id)
      ack_template = [ transaction_id_start, transaction_id_stop ]

    assert control.is_ack_record_requested == False, "Not implemented yet"
    assert control.is_ack_not_void == False, "Not implemented yet"

    alp_command = AlpParser().parse(bitstream, payload_length)

    return Frame(
      control=control,
      dialog_id=dialog_id,
      transaction_id=transaction_id,
      agc_rx_level_i=target_rx_level_i,
      tl=tl,
      te=te,
      ack_template=ack_template,
      alp_command=alp_command
    )
