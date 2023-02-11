import base64

# Hex Functions:


def hex2b64(hex_str: str) -> bytes:
    """Converts a hex string to a base64 string"""
    return base64.b64encode(bytes.fromhex(hex_str))


def hex2bytes(hex_str: str) -> bytes:
    """Converts a hex string to a byte string"""
    return bytes.fromhex(hex_str)


# Int Functions:


def int2byte(integer: int) -> bytes:
    """Convert a single byte integer (0, 255) to a byte"""
    assert 0 <= integer <= 255, "The integer must be between 0 and 255"
    return integer.to_bytes(1, "little")


def bigint2bytes(bigint: int) -> bytes:
    """Converts a big integer to a byte string. This function treats the
    byteorder as a little-endian."""
    return bigint.to_bytes((bigint.bit_length() + 7) // 8, "little")


# String Functions:


def string2bytes(string: str) -> bytes:
    """Converts a string encoded with utf-8 to a byte string"""
    return bytes(string, "utf-8")


def string2dict(string: str, equal_sign: str = "=", break_sign: str = "&") -> dict:
    """Converts a string of the form `key1=value1&key2=value2&...` to a dictionary"""
    kv_store = {}
    for kv_pair in string.split(break_sign):
        k, v = kv_pair.split(equal_sign)
        kv_store[k] = v

    return kv_store


# Bytes Functions:


def bytes2blocks(byte_string: bytes, blocksize: int) -> list[bytes]:
    """Splits a byte string into blocks of length `blocksize`"""
    assert (
        len(byte_string) % blocksize == 0
    ), "The byte string must be a multiple of the blocksize"

    return [
        byte_string[i : i + blocksize] for i in range(0, len(byte_string), blocksize)
    ]


# Block Functions:


def blocks2bytes(blocks: list[bytes]) -> bytes:
    """Converts a list of byte blocks to a single byte string"""
    return b"".join(blocks)
