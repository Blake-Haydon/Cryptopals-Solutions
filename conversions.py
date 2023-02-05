import base64


def hex2b64(hex_str: str) -> bytes:
    return base64.b64encode(bytes.fromhex(hex_str))


def hex2bytes(hex_str: str) -> bytes:
    return bytes.fromhex(hex_str)


def string2bytes(string: str) -> bytes:
    return bytes(string, "utf-8")


def int2bytes(integer: int) -> bytes:
    """Convert a single byte integer (0, 255) to a byte"""
    assert 0 <= integer <= 255, "The integer must be between 0 and 255"
    return integer.to_bytes(1, "little")
