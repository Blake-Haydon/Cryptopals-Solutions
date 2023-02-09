from .helper_functions import repeat_key
from .convert import int2bytes


def xor_bytes(a: bytes, b: bytes) -> bytes:
    """XORs bytes `a` and `b` (`a ^ b`)"""
    assert len(a) == len(b), "The two byte arrays must have the same length"

    xor_bytes = b""
    for i in range(len(a)):
        xor_bytes += int2bytes(a[i] ^ b[i])

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


def single_byte_encrypt(plaintext: bytes, key: bytes):
    """Encrypts a plaintext with a single byte XOR key"""
    assert len(key) == 1, "Key must be a single byte"
    return repeating_key_encrypt(plaintext, key)


def single_byte_decrypt(cyphertext: bytes, key: bytes):
    """Decrypts a cyphertext encrypted with a single byte XOR key"""
    assert len(key) == 1, "Key must be a single byte"
    return repeating_key_decrypt(cyphertext, key)
