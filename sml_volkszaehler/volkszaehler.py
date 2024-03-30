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


def _split_byte(message: bytearray):
    b = int.to_bytes(message[0], 1)
    as_int: int = int.from_bytes(b)
    first = as_int >> 4
    read_next_byte = first >> 3
    second = as_int & 0b00001111
    n = 1
    if read_next_byte:
        b2 = message[1]
        second = (second << 4) + message[1]
        n += 1

    return (first, second, n)


def _read_msg_start(stream):
    message = bytearray()
    while message[-4:] != bytearray(b'\x1b\x1b\x1b\x1b'):
        message += bytearray(stream.read(1))
    version = stream.read(4)  # Version
    assert version == b"\x01\x01\x01\x01"
    message += bytearray(version)
    return message

def _read_until_end(stream, message):
    while message[-5:] != bytearray(b"\x1b\x1b\x1b\x1b\x1a"):
        message += bytearray(stream.read(1))
    message += bytearray(stream.read(3))


def _parse_list(message, res):
    a, b, n = _split_byte(message)
    if a == 7:
        message = message[n:]
        children = []
        for i in range(0, b):
            message = _parse_list(message, children)
        res.append(children)
        return message
    else:
        b = max(b, 1)  # NOTE: 0x00 handling
        assert len(message) >= b, f"{len(message)} vs. {b}"
        res.append(message[0:b])
        return message[b:]
        



def get_values_from_stream(stream):
    message = _read_msg_start(stream)
    _read_until_end(stream, message)

    payload = message[8:-8]
    res = []
    while len(payload) > 0:
        payload = _parse_list(payload, res)
        print("rest payload", payload)

    return res
    values = []
    identifier, length = _split_byte(stream.read(1))
    print(identifier, length)
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

