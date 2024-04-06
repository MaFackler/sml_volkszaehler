import io
import pytest
from binascii import hexlify
data = """
1b 1b 1b 1b
01 01 01 01
76
  01
  01
  01
  01
  01
  01
76
  01
  62 00
  62 00
  72
    01
    77
      01
      01
      01
      01
      73
        77
          07 81 81 01 08 01 ff
          01
          01
          62 1e
          52 ff
          56 00 15 2b f1 77
          01
        77
          07 81 81 01 08 02 ff
          01
          01
          62 1e
          52 ff
          56 00 01 b5 96 26
          01
        77
          07 81 81 10 07 00 ff
          01
          01
          62 1e
          52 ff
          55 ff ff fe 67
          01
      01
      00
  01
  00
76
  01
  01
  01
  01
  01
  81 01 ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff
1b 1b 1b 1b
1a 00
"""


from sml_volkszaehler import get_values_from_stream, MeterValue
from sml_volkszaehler.volkszaehler import _crc_value


@pytest.fixture
def socket():
    res = bytearray()
    global data
    data = data.replace("\n", " ")
    for byte in data.split(" "):
        if byte:
            res += bytearray.fromhex(byte)
    value = _crc_value(res)
    res += int.to_bytes(value, length=2, byteorder="little")
    yield io.BytesIO(bytes(res))


def test_parsing(socket):
    res = get_values_from_stream(socket)

    assert res["1.8.1"].value == 355201399
    assert res["1.8.1"].scaler == 0.1
    assert res["1.8.1"].unit == "Wh"

    assert res["1.8.2"].value == 28677670
    assert res["1.8.2"].scaler == 0.1
    assert res["1.8.2"].unit == "Wh"

    assert res["16.7.0"].value == -409
    assert res["16.7.0"].scaler == 0.1
    assert res["16.7.0"].unit == "Wh"


def test_crc_check():
    value = b"123456789"
    res = _crc_value(value)
    assert res == 36974


