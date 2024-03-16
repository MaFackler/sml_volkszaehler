from typing import NamedTuple

class MeterValue(NamedTuple):
    value: int
    scaler: float
    unit: str


_UNIT_MAP = {
    b"\x1e": "Wh",
    b"\x1b": "W",
}


_SCALER_MAP = {
    b"\xff": 0.1,
    b"\x00": 1,
    b"\x01": 0,
}


def _read_value_list_from_stream(stream, length, level=0):
    res = []
    for i in range(0, length):
        identifier, value = _split_byte(stream.read(1))
        if identifier == 7:
            res.append(_read_value_list_from_stream(stream, value, level=level + 1))
        elif value > 0:
            binvalue = stream.read(value - 1)
            res.append(binvalue)
        else:
            res.append(None)
    return res


def _split_byte(b: bytes):
    assert len(b) == 1
    first = int.from_bytes(b) >> 4
    second = int.from_bytes(b) & 0b00001111
    return (first, second)


def _read_msg_start(stream):
    message = []
    while message[-4:] != [b'\x1b', ] * 4:
        message.append(stream.read(1))
    _ = stream.read(4)  # Version


def get_values_from_stream(stream):
    _read_msg_start(stream)
    values = []
    identifier, length = _split_byte(stream.read(1))
    while identifier == 7:
        values.append(_read_value_list_from_stream(stream, length, level=1))
        identifier, length = _split_byte(stream.read(1))

    # TODO: improve access
    # TODO: also parse other values?
    values = values[1][3][1][4]

    res = {}
    for name, status, valTime, unit, scaler, value, signature in values:
        obis = [
            str(name[2]),
            str(name[3]),
            str(name[4])
        ]
        unit = _UNIT_MAP.get(unit, None)
        scaler = _SCALER_MAP.get(scaler, 1)
        if unit:
            value = int.from_bytes(value)
        res[".".join(obis)] = MeterValue(value=value,
                                         scaler=scaler,
                                         unit=unit)

    return res

