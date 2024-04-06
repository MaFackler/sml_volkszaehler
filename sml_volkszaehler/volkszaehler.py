from typing import NamedTuple

class MeterValue(NamedTuple):
    value: int
    scaler: float
    unit: str

    def __str__(self):
        if isinstance(self.value, bytes):
            res = str(self.value)
        else:
            res = str(round(self.value * self.scaler, 2))
            if self.unit:
                res += " " + self.unit
        return res
            


_UNIT_MAP = {
    b"\x62\x1e": "Wh",
    b"\x62\x1b": "W",
}


_SCALER_MAP = {
    b"\x52\xff": 0.1,
    b"\x52\x00": 1,
    b"\x52\x01": 0,
}

_CRC_TABLE_X25 = [
	0x0000, 0x1189, 0x2312, 0x329B, 0x4624, 0x57AD,	0x6536, 0x74BF,
	0x8C48, 0x9DC1, 0xAF5A, 0xBED3, 0xCA6C, 0xDBE5, 0xE97E, 0xF8F7,
	0x1081, 0x0108,	0x3393, 0x221A, 0x56A5, 0x472C, 0x75B7, 0x643E,
	0x9CC9, 0x8D40, 0xBFDB, 0xAE52, 0xDAED, 0xCB64,	0xF9FF, 0xE876,
	0x2102, 0x308B, 0x0210, 0x1399,	0x6726, 0x76AF, 0x4434, 0x55BD,
	0xAD4A, 0xBCC3,	0x8E58, 0x9FD1, 0xEB6E, 0xFAE7, 0xC87C, 0xD9F5,
	0x3183, 0x200A, 0x1291, 0x0318, 0x77A7, 0x662E,	0x54B5, 0x453C,
	0xBDCB, 0xAC42, 0x9ED9, 0x8F50,	0xFBEF, 0xEA66, 0xD8FD, 0xC974,
	0x4204, 0x538D,	0x6116, 0x709F, 0x0420, 0x15A9, 0x2732, 0x36BB,
	0xCE4C, 0xDFC5, 0xED5E, 0xFCD7, 0x8868, 0x99E1,	0xAB7A, 0xBAF3,
	0x5285, 0x430C, 0x7197, 0x601E,	0x14A1, 0x0528, 0x37B3, 0x263A,
	0xDECD, 0xCF44,	0xFDDF, 0xEC56, 0x98E9, 0x8960, 0xBBFB, 0xAA72,
	0x6306, 0x728F, 0x4014, 0x519D, 0x2522, 0x34AB,	0x0630, 0x17B9,
	0xEF4E, 0xFEC7, 0xCC5C, 0xDDD5,	0xA96A, 0xB8E3, 0x8A78, 0x9BF1,
	0x7387, 0x620E,	0x5095, 0x411C, 0x35A3, 0x242A, 0x16B1, 0x0738,
	0xFFCF, 0xEE46, 0xDCDD, 0xCD54, 0xB9EB, 0xA862,	0x9AF9, 0x8B70,
	0x8408, 0x9581, 0xA71A, 0xB693,	0xC22C, 0xD3A5, 0xE13E, 0xF0B7,
	0x0840, 0x19C9,	0x2B52, 0x3ADB, 0x4E64, 0x5FED, 0x6D76, 0x7CFF,
	0x9489, 0x8500, 0xB79B, 0xA612, 0xD2AD, 0xC324,	0xF1BF, 0xE036,
	0x18C1, 0x0948, 0x3BD3, 0x2A5A,	0x5EE5, 0x4F6C, 0x7DF7, 0x6C7E,
	0xA50A, 0xB483,	0x8618, 0x9791, 0xE32E, 0xF2A7, 0xC03C, 0xD1B5,
	0x2942, 0x38CB, 0x0A50, 0x1BD9, 0x6F66, 0x7EEF,	0x4C74, 0x5DFD,
	0xB58B, 0xA402, 0x9699, 0x8710,	0xF3AF, 0xE226, 0xD0BD, 0xC134,
	0x39C3, 0x284A,	0x1AD1, 0x0B58, 0x7FE7, 0x6E6E, 0x5CF5, 0x4D7C,
	0xC60C, 0xD785, 0xE51E, 0xF497, 0x8028, 0x91A1,	0xA33A, 0xB2B3,
	0x4A44, 0x5BCD, 0x6956, 0x78DF,	0x0C60, 0x1DE9, 0x2F72, 0x3EFB,
	0xD68D, 0xC704,	0xF59F, 0xE416, 0x90A9, 0x8120, 0xB3BB, 0xA232,
	0x5AC5, 0x4B4C, 0x79D7, 0x685E, 0x1CE1, 0x0D68,	0x3FF3, 0x2E7A,
	0xE70E, 0xF687, 0xC41C, 0xD595,	0xA12A, 0xB0A3, 0x8238, 0x93B1,
	0x6B46, 0x7ACF,	0x4854, 0x59DD, 0x2D62, 0x3CEB, 0x0E70, 0x1FF9,
	0xF78F, 0xE606, 0xD49D, 0xC514, 0xB1AB, 0xA022,	0x92B9, 0x8330,
	0x7BC7, 0x6A4E, 0x58D5, 0x495C,	0x3DE3, 0x2C6A, 0x1EF1, 0x0F78
]


def _crc_value(buf: bytes):
	res = 0xffff
	for byte in buf:
		res = _CRC_TABLE_X25[(byte ^ res) & 0xff] ^ (res >> 8 & 0xff)
	res ^= 0xffff
	return res


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
    b = int.to_bytes(message[0], 1, byteorder="big")
    as_int: int = int.from_bytes(b, byteorder="big")
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
    found = False

    message = bytearray()
    while message[-4:] != bytearray(b'\x1b\x1b\x1b\x1b'):
        message += bytearray(stream.read(1))
    version = stream.read(4)  # Version
    found = version == b"\x01\x01\x01\x01"
    message += version
    return message[-8:], version

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
        res.append(bytes([b for b in message[0:b]]))
        return message[b:]
        
def _iter_flat(l: list):
    for ele in l:
        if isinstance(ele, list):
            yield from _iter_flat(ele)
        else:
            yield ele


def get_values_from_stream(stream):
    message, version = _read_msg_start(stream)
    _read_until_end(stream, message)
    payload = message[8:-8]
    sml_lists = []
    # TODO: checksum of indiviudal list
    while len(payload) > 0:
        payload = _parse_list(payload, sml_lists)

    sml_lists = [x for x in sml_lists if len(x) == 6]
    values_msg = sml_lists[1]
    res = {}
    for name, status, _, unit, scaler, value, signature in values_msg[3][1][4]:
        obis = ".".join(map(str, name[3:6]))
        unit = _UNIT_MAP.get(unit, None)
        scaler = _SCALER_MAP.get(scaler, 1)
        if unit:
            value = int.from_bytes(value[1:], byteorder="big", signed=True)
        res[obis] = MeterValue(value=value, scaler=scaler, unit=unit)

    crc_values = values_msg[4]
    assert values_msg[5] == b"\x00", str(values_msg[-1])

    value = int.from_bytes(message[-2:], byteorder="little")
    if value != _crc_value(message[0:-2]):
        res = None

    return res
