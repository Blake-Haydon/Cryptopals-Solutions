from .helper_functions import has_repeated_blocks


def is_ecb_mode(oracle: callable, blocksize: int) -> bool:
    """Will only check for repeating blocks to determine if the plaintext was encrypted
    using ECB mode.

    `oracle(input_bytes: bytes) -> bytes`
    """

    # To get 2 blocks of the same plaintext, we need to have at least 2*blocksize bytes of plaintext
    # More realistically, we need 3*blocksize bytes of plaintext as the first block may have only a single byte in
    # it and therefore will have to fill that block before starting the two full blocks
    input_bytes = b"A" * (3 * blocksize)
    cyphertext = oracle(input_bytes)
    return has_repeated_blocks(cyphertext, blocksize)


def determine_blocksize(oracle: callable) -> tuple[int, int]:
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
            blocksize = abs(cyphertext_len[1] - cyphertext_len[0])
            offset = i - 1
            return blocksize, offset

        i += 1


def determine_blocksize_from_error(oracle: callable) -> tuple[int, int]:
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
