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


def string2dict(string: str, equal_sign: str = "=", break_sign: str = "&") -> dict:
    """Converts a string of the form `key1=value1&key2=value2&...` to a dictionary"""
    kv_store = {}
    for kv_pair in string.split(break_sign):
        k, v = kv_pair.split(equal_sign)
        kv_store[k] = v

    return kv_store
