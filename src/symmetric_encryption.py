from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from .helper_functions import xor_bytes, has_repeated_blocks


def is_ecb_mode(oracle: callable, block_size: int) -> bool:
    """Will only check for repeating blocks to determine if the plaintext was encrypted
    using ECB mode.

    `oracle(input_bytes: bytes) -> bytes`
    """

    # To get 2 blocks of the same plaintext, we need to have at least 2*blocksize bytes of plaintext
    # More realistically, we need 3*blocksize bytes of plaintext as the first block may have only a single byte in
    # it and therefore will have to fill that block before starting the two full blocks
    input_bytes = b"A" * (3 * block_size)
    cyphertext = oracle(input_bytes)
    return has_repeated_blocks(cyphertext, block_size)


def determine_block_size(oracle: callable) -> tuple[int, int]:
    """Determines the block length of the encryption oracle by feeding it a byte string of increasing length
    and checking how the output changes. The function must not error for this function to work correctly.

    `oracle(input_bytes: bytes) -> bytes`

    Returns the block length of the encryption oracle and the offset needed for no padding.
    """

    cyphertext_len = set()
    i = 0
    while True:
        # Add the length of the cyphertext to the set (repeated lengths will be ignored)
        cyphertext = oracle(b"A" * i)
        cyphertext_len.add(len(cyphertext))

        # When there are two different lengths, the block length is the difference between them
        if len(cyphertext_len) == 2:
            cyphertext_len = list(cyphertext_len)  # convert set to list
            block_size = abs(cyphertext_len[1] - cyphertext_len[0])
            offset = i - 1
            return block_size, offset

        i += 1


def determine_block_size_from_error(oracle: callable) -> tuple[int, int]:
    """Determines the block length of the encryption oracle by feeding it a byte string of increasing length
    and checking when it does not error out. The function must error for this function to work correctly.

    `oracle(input_bytes: bytes) -> bytes`

    Returns the block length of the encryption oracle and the offset needed for no padding.
    """

    non_error_i = []
    i = 0
    while True:
        try:
            oracle(b"A" * i)
            non_error_i.append(i)
        except Exception:
            pass

        if len(non_error_i) == 2:
            block_length = non_error_i[1] - non_error_i[0]
            offset = non_error_i[0]
            return block_length, offset

        i += 1


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
