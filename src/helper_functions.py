from .convert import int2byte, bytes2blocks


def hamming_distance(a: bytes, b: bytes) -> int:
    """Calculates the hamming distance between two byte arrays"""
    assert len(a) == len(
        b
    ), "The two byte arrays must have the same length to calculate the hamming distance"

    dist = 0
    for i in range(len(a)):
        # find all different bits and count them
        dist += bin(a[i] ^ b[i]).count("1")

    return dist


def repeat_key(key: bytes, length: int):
    """Expands a secret key to a byte array of a certain length"""
    expanded_sk = bytes()
    for i in range(length):
        expanded_sk += int2byte(key[i % len(key)])

    return expanded_sk


def output_repeated_block(byte_string: bytes, blocksize: int) -> bytes:
    """Returns the first repeated block in a byte string"""
    # TODO: this is a naive implementation and can be improved

    blocks = bytes2blocks(byte_string, blocksize)
    for i in range(len(blocks)):
        for j in range(len(blocks)):
            # The same block will always match itself so skip
            if i == j:
                continue

            if blocks[i] == blocks[j]:
                return blocks[i]

    return None


def find_block(byte_string: bytes, search_block: bytes, blocksize: int) -> int | None:
    """Finds the index of a block in a byte string"""

    blocks = bytes2blocks(byte_string, blocksize)
    for i in range(len(blocks)):
        if blocks[i] == search_block:
            return i

    return None


def has_repeated_blocks(byte_string: bytes, blocksize: int) -> bool:
    if output_repeated_block(byte_string, blocksize):
        return True

    return False
