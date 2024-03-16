import io
import pytest
from binascii import hexlify
data = "TODODATA"

from sml_volkszaehler import get_values_from_stream, MeterValue


@pytest.fixture
def socket():
    res = bytearray()
    for byte in data.split(" "):
        res += bytearray.fromhex(byte)
    yield io.BytesIO(bytes(res))


def test_parsing(socket):
    res = get_values_from_stream(socket)
    assert res["1.8.0"] == MeterValue(value=180, scaler=0.1, unit='Wh')
    assert res["1.8.1"] == MeterValue(value=181, scaler=0.1, unit='Wh')
    assert res["1.8.2"] == MeterValue(value=182, scaler=0.1, unit='Wh')

    assert res["2.8.0"] == MeterValue(value=280, scaler=0.1, unit='Wh')
    assert res["2.8.1"] == MeterValue(value=281, scaler=0.1, unit='Wh')
    assert res["2.8.2"] == MeterValue(value=282, scaler=0.1, unit='Wh')

    assert res["16.7.0"] == MeterValue(value=1670, scaler=1, unit='W')
    assert res["36.7.0"] == MeterValue(value=3670, scaler=1, unit='W')
    assert res["56.7.0"] == MeterValue(value=5670, scaler=1, unit='W')
    assert res["76.7.0"] == MeterValue(value=7670, scaler=1, unit='W')

    assert res["199.130.3"] == MeterValue(value=b"FOO", scaler=1, unit=None)
    assert res["199.130.5"] == MeterValue(value=b"BAR", scaler=1, unit=None)





