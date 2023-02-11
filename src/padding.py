from .convert import int2byte


def apply_pkcs_7(byte_string: bytes, blocksize: int) -> bytes:
    """Applies PKCS#7 padding to a byte string with a block size of `blocksize` bytes"""
    pad_len = blocksize - len(byte_string) % blocksize
    for _ in range(pad_len):
        byte_string += int2byte(pad_len)

    return byte_string


def remove_pkcs_7(byte_string: bytes) -> bytes:
    """Removes PKCS#7 padding from a byte string. Will raise an error if the padding is invalid."""
    pad_len = byte_string[-1]
    pad_bytes = byte_string[-pad_len:]

    # Padding must all be equal to the length of the padding
    if not all(byte == pad_len for byte in pad_bytes):
        raise ValueError("Invalid PKCS#7 padding")

    return byte_string[:-pad_len]
