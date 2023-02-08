import numpy as np
from .conversions import int2bytes


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
        dist += bin(a[i] ^ b[i]).count("1")

    return dist


def xor_bytes(a: bytes, b: bytes) -> bytes:
    bytes_0 = np.frombuffer(a, dtype="uint8")
    bytes_1 = np.frombuffer(b, dtype="uint8")
    assert (
        bytes_0.shape == bytes_1.shape
    ), "The two byte arrays must have the same shape"
    return (bytes_0 ^ bytes_1).tobytes()


def repeat_key(sk: bytes, length: int):
    """Expands a secret key `sk` to a byte array of length `length`"""
    expanded_sk = bytes()
    for i in range(length):
        expanded_sk += int2bytes(sk[i % len(sk)])

    return expanded_sk


def single_byte_xor(a: bytes, sk: int) -> bytes:
    """Encrypts a byte array `a` with a single byte secret key `sk`"""
    return xor_bytes(a, repeat_key(sk, len(a)))


def repeating_key_xor(a: bytes, sk: bytes) -> bytes:
    """Encrypts a byte array `a` with a repeating key `sk`"""
    return xor_bytes(a, repeat_key(sk, len(a)))


def xor_hex_strings(a: str, b: str) -> bytes:
    return xor_bytes(bytes.fromhex(a), bytes.fromhex(b))


def output_repeated_block(byte_string: bytes, block_size: int) -> bytes:
    """Returns the first repeated block in a byte string"""
    # TODO: this is a naive implementation and can be improved
    for i in range(0, len(byte_string), block_size):
        for j in range(0, len(byte_string), block_size):
            # The same block will always match itself so skip
            if i == j:
                continue

            # Compare the blocks and if they match return true
            a = byte_string[i : i + block_size]
            b = byte_string[j : j + block_size]
            if a == b:
                return a

    return None


def find_block(byte_string: bytes, search_block: bytes, block_size: int) -> int | None:
    """Finds the index of a block in a byte string"""
    for i in range(0, len(byte_string), block_size):
        if byte_string[i : i + block_size] == search_block:
            return i

    return None


def has_repeated_blocks(byte_string: bytes, block_size: int) -> bool:
    if output_repeated_block(byte_string, block_size):
        return True

    return False
