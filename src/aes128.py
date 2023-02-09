from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

from .xor import xor_bytes
from .convert import bytes2blocks, blocks2bytes

AES128_KEY_LENGTH = 16


def ecb_encrypt(plaintext: bytes, key: bytes) -> bytes:
    """Encrypts a byte string with AES-128 in ECB mode
    ```
    C[i] = E_k(P[i])
    ```
    """
    encryptor = Cipher(
        algorithm=algorithms.AES128(key),
        mode=modes.ECB(),
    ).encryptor()
    return encryptor.update(plaintext) + encryptor.finalize()


def ecb_decrypt(cyphertext: bytes, key: bytes) -> bytes:
    """Decrypts a byte string with AES-128 in ECB mode
    ```
    P[i] = D_k(C[i])
    ```
    """
    decryptor = Cipher(
        algorithm=algorithms.AES128(key),
        mode=modes.ECB(),
    ).decryptor()
    return decryptor.update(cyphertext) + decryptor.finalize()


def cbc_encrypt(plaintext: bytes, key: bytes, iv: bytes) -> bytes:
    """Encrypts a byte string with AES-128 in CBC mode
    ```
    C[0] = IV
    C[i] = E_k(P[i] XOR C[i-1])
    ```
    """
    cyphertext_blocks = [iv]
    plaintext_blocks = bytes2blocks(plaintext, AES128_KEY_LENGTH)

    # The first block has index 1 as the 0th block is the IV
    for i in range(1, len(plaintext_blocks)):
        cyphertext_blocks.append(
            ecb_encrypt(
                xor_bytes(
                    plaintext_blocks[i],
                    cyphertext_blocks[i - 1],
                ),
                key,
            )
        )

    # Exclude the IV in the return value as it is not part of the cyphertext
    return blocks2bytes(cyphertext_blocks[1:])


def cbc_decrypt(byte_string: bytes, key: bytes, iv: bytes) -> bytes:
    """Decrypts a byte string with AES-128 in CBC mode
    ```
    C[0] = IV
    P[i] = D_k(C[i]) XOR C[i-1]
    ```
    """
    cyphertext_blocks = [iv] + bytes2blocks(byte_string, AES128_KEY_LENGTH)
    plaintext_blocks = [None]

    # The first block has index 1 as the 0th block is the IV
    for i in range(1, len(cyphertext_blocks)):
        plaintext_blocks.append(
            xor_bytes(
                ecb_decrypt(
                    cyphertext_blocks[i],
                    key,
                ),
                cyphertext_blocks[i - 1],
            )
        )

    return blocks2bytes(plaintext_blocks[1:])
