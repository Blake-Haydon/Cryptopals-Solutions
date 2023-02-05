from conversions import int2bytes


def apply_pkcs_7(byte_string: bytes, block_size: int) -> bytes:
    """Applies PKCS#7 padding to a byte string with a block size of `block_size` bytes"""
    pad_len = block_size - len(byte_string) % block_size
    for _ in range(pad_len):
        byte_string += int2bytes(pad_len)

    return byte_string


def remove_pkcs_7(byte_string: bytes) -> bytes:
    """Removes PKCS#7 padding from a byte string"""
    pad_len = byte_string[-1]
    return byte_string[:-pad_len]
