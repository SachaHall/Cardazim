import struct


def unpack_int(data: bytes) -> int:
    return struct.unpack("<I", data)[0]


def pack_int(n: int) -> bytes:
    return struct.pack("<I", n)


def get_str_from_bytes(data: bytes) -> tuple[str, bytes]:
    uint_sz = 4
    name_sz = unpack_int(data[:uint_sz])
    name = data[uint_sz:uint_sz + name_sz].decode('utf-8')
    return name, data[uint_sz+name_sz:]


def encode_str(string: str) -> bytes:
    sz: bytes = pack_int(len(string))
    return sz + string.encode('utf-8')
