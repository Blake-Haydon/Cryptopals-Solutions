from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import secrets
from helper_functions import xor_bytes, has_repeated_blocks
from padding import apply_pkcs_7


def encryption_oracle(plaintext: bytes) -> bytes:
    """Encrypts a `plaintext` with AES-128 in either ECB or CBC mode. The plaintext is padded with PKCS#7 padding
    and a random prefix and suffix are added to the plaintext. The key and IV are chosen at random. The function
    returns a tuple of the mode used and the cyphertext."""

    key = secrets.token_bytes(16)  # for AES-128
    iv = secrets.token_bytes(16)  # for AES-128

    before_bytes = secrets.token_bytes(secrets.choice([5, 6, 7, 8, 9, 10]))
    after_bytes = secrets.token_bytes(secrets.choice([5, 6, 7, 8, 9, 10]))

    modified_plaintext = apply_pkcs_7(before_bytes + plaintext + after_bytes, 16)

    if secrets.choice([True, False]):
        return ("ECB", aes128_ecb_encrypt(modified_plaintext, key))
    else:
        return ("CBC", aes128_cbc_encrypt(modified_plaintext, key, iv))


def is_ecb_mode(cyphertext: bytes) -> bool:
    """Will currently only check for repeating blocks of 16 bytes to determine if the plaintext was encrypted
    using ECB mode"""
    return has_repeated_blocks(cyphertext, 16)  # 16 bytes in an AES block


def aes128_ecb_encrypt(plaintext: bytes, key: bytes) -> bytes:
    """Encrypts a byte string with AES-128 in ECB mode"""

    assert len(key) == 16, "The key must be 16 bytes long"
    assert len(plaintext) % 16 == 0, "The byte string must be a multiple of 16 bytes"

    encryptor = Cipher(
        algorithm=algorithms.AES128(key),
        mode=modes.ECB(),
    ).encryptor()
    return encryptor.update(plaintext) + encryptor.finalize()


def aes128_ecb_decrypt(byte_string: bytes, key: bytes) -> bytes:
    """Decrypts a byte string with AES-128 in ECB mode"""

    assert len(key) == 16, "The key must be 16 bytes long"
    assert len(byte_string) % 16 == 0, "The byte string must be a multiple of 16 bytes"

    decryptor = Cipher(
        algorithm=algorithms.AES128(key),
        mode=modes.ECB(),
    ).decryptor()
    return decryptor.update(byte_string) + decryptor.finalize()


def aes128_cbc_encrypt(byte_string: bytes, key: bytes, iv: bytes) -> bytes:
    """Encrypts a byte string with AES-128 in CBC mode"""

    assert len(key) == 16, "The key must be 16 bytes long"
    assert len(byte_string) % 16 == 0, "The byte string must be a multiple of 16 bytes"

    cyphertext = b""
    prev_cyphertext = iv
    for i in range(0, len(byte_string), 16):
        plaintext = byte_string[i : i + 16]
        prev_cyphertext = aes128_ecb_encrypt(
            xor_bytes(prev_cyphertext, plaintext),
            key,
        )
        cyphertext += prev_cyphertext

    return cyphertext


def aes128_cbc_decrypt(byte_string: bytes, key: bytes, iv: bytes) -> bytes:
    """Decrypts a byte string with AES-128 in CBC mode"""

    assert len(key) == 16, "The key must be 16 bytes long"
    assert len(byte_string) % 16 == 0, "The byte string must be a multiple of 16 bytes"

    plaintext = b""
    curr_cyphertext = byte_string[0:16]
    prev_cyphertext = iv
    for i in range(16, len(byte_string) + 1, 16):
        plaintext += xor_bytes(
            prev_cyphertext,
            aes128_ecb_decrypt(curr_cyphertext, key),
        )
        prev_cyphertext = curr_cyphertext
        curr_cyphertext = byte_string[i : i + 16]

    return plaintext
