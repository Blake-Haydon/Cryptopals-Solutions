from .conversions import int2bytes


def apply_pkcs_7(byte_string: bytes, block_size: int) -> bytes:
    """Applies PKCS#7 padding to a byte string with a block size of `block_size` bytes"""
    pad_len = block_size - len(byte_string) % block_size
    for _ in range(pad_len):
        byte_string += int2bytes(pad_len)

    return byte_string


def remove_pkcs_7(byte_string: bytes) -> bytes:
    """Removes PKCS#7 padding from a byte string. Will raise an error if the padding is invalid."""
    pad_len = byte_string[-1]
    pad_bytes = byte_string[-pad_len:]

    # Padding must all be equal to the length of the padding
    if not all(byte == pad_len for byte in pad_bytes):
        raise ValueError("Invalid PKCS#7 padding")

    return byte_string[:-pad_len]
