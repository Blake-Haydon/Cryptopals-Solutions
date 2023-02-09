from .helper_functions import repeating_key_xor


def single_byte_encrypt(plaintext: bytes, key: bytes):
    """Encrypts a plaintext with a single byte XOR key"""
    assert len(key) == 1, "Key must be a single byte"
    return repeating_key_xor(plaintext, key)


def single_byte_decrypt(cyphertext: bytes, key: bytes):
    """Decrypts a cyphertext encrypted with a single byte XOR key"""
    assert len(key) == 1, "Key must be a single byte"
    return repeating_key_xor(cyphertext, key)
