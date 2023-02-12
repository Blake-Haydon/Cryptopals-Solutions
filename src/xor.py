from .helper_functions import repeat_key
from .convert import int2byte
from .analysis import score_string


def xor_bytes(a: bytes, b: bytes) -> bytes:
    """XORs bytes `a` and `b` (`a ^ b`)"""
    assert len(a) == len(b), "The two byte arrays must have the same length"

    xor_bytes = b""
    for i in range(len(a)):
        xor_bytes += int2byte(a[i] ^ b[i])

    return xor_bytes


def xor_hex_strings(a: str, b: str) -> bytes:
    """XORs hex strings `a` and `b` (`a ^ b`)"""
    return xor_bytes(bytes.fromhex(a), bytes.fromhex(b))


def repeating_key_encrypt(plaintext: bytes, key: bytes) -> bytes:
    """Encrypts a plaintext with a repeating XOR key"""
    repeated_key = repeat_key(key, len(plaintext))
    return xor_bytes(plaintext, repeated_key)


def repeating_key_decrypt(cyphertext: bytes, key: bytes) -> bytes:
    """Decrypts a cyphertext with a repeating XOR key"""
    repeated_key = repeat_key(key, len(cyphertext))
    return xor_bytes(cyphertext, repeated_key)


def repeating_key_break(cyphertext: bytes, key_size: int) -> tuple[str, bytes]:
    zero_key = b"\x00" * key_size
    best_keys = []
    for j in range(key_size):
        best_score = 0
        best_key = zero_key
        for i in range(256):
            key = zero_key[:j] + int2byte(i) + zero_key[j + 1 :]
            plaintext = repeating_key_decrypt(cyphertext, key)
            plaintext = plaintext.decode("ascii", errors="ignore")

            # Keep track of best key for that specific character
            score = score_string(plaintext)
            if score > best_score:
                best_score = score
                best_key = key

        # Add the best key for that specific character to the list of keys
        best_keys.append(best_key)

    # XOR the best keys together to get the real key
    key = zero_key
    for i in range(len(best_keys)):
        key = xor_bytes(best_keys[i], key)

    plaintext = repeating_key_decrypt(cyphertext, key)
    return plaintext, key


def single_byte_encrypt(plaintext: bytes, key: bytes):
    """Encrypts a plaintext with a single byte XOR key"""
    assert len(key) == 1, "Key must be a single byte"
    return repeating_key_encrypt(plaintext, key)


def single_byte_decrypt(cyphertext: bytes, key: bytes):
    """Decrypts a cyphertext encrypted with a single byte XOR key"""
    assert len(key) == 1, "Key must be a single byte"
    return repeating_key_decrypt(cyphertext, key)


def single_byte_break(cyphertext: bytes) -> tuple[str, bytes]:
    """Breaks a cyphertext encrypted with a single byte XOR key"""
    best_score = 0
    best_plaintext = ""
    best_key = b""
    for i in range(256):
        key = int2byte(i)
        plaintext = single_byte_decrypt(cyphertext, key)
        plaintext = plaintext.decode("ascii", "ignore")
        score = score_string(plaintext)

        # Keep track of most likely plaintext
        if score > best_score:
            best_score = score
            best_plaintext = plaintext
            best_key = key

    return best_plaintext, best_key
