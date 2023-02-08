from .convert import int2bytes, bytes2blocks


# English letter probabilities from https://en.wikipedia.org/wiki/Letter_frequency
# The probabilities are in percent (%)
# letter_probs = {
#     "A": 8.2,
#     "B": 1.5,
#     "C": 2.8,
#     "D": 4.3,
#     "E": 13,
#     "F": 2.2,
#     "G": 2,
#     "H": 6.1,
#     "I": 7,
#     "J": 0.15,
#     "K": 0.77,
#     "L": 4,
#     "M": 2.4,
#     "N": 6.7,
#     "O": 7.5,
#     "P": 1.9,
#     "Q": 0.095,
#     "R": 6,
#     "S": 6.3,
#     "T": 9.1,
#     "U": 2.8,
#     "V": 0.98,
#     "W": 2.4,
#     "X": 0.15,
#     "Y": 2,
#     "Z": 0.074,
# }


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


def xor_bytes(a: bytes, b: bytes) -> bytes:
    """XORs bytes `a` and `b` (`a ^ b`)"""
    assert len(a) == len(b), "The two byte arrays must have the same length"

    xor_bytes = b""
    for i in range(len(a)):
        xor_bytes += int2bytes(a[i] ^ b[i])

    return xor_bytes


def repeat_key(sk: bytes, length: int):
    """Expands a secret key `sk` to a byte array of length `length`"""
    expanded_sk = bytes()
    for i in range(length):
        expanded_sk += int2bytes(sk[i % len(sk)])

    return expanded_sk


def repeating_key_xor(a: bytes, sk: bytes) -> bytes:
    """Encrypts a byte array `a` with a repeating key `sk`"""
    return xor_bytes(a, repeat_key(sk, len(a)))


def xor_hex_strings(a: str, b: str) -> bytes:
    return xor_bytes(bytes.fromhex(a), bytes.fromhex(b))


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
