import secrets


def gen_keypair(p: int, g: int) -> tuple[int, int]:
    """Generate a keypair for Diffie-Hellman.

    Args:
        `p`: Prime number
        `g`: Generator

    Returns:
        `(private_key, public_key)`: The private and public keypair
    """

    private_key = secrets.randbelow(p)
    public_key = pow(g, private_key, p)
    return private_key, public_key


def shared_secret(p: int, public_key: int, private_key: int) -> int:
    """Generate the shared secret.

    Args:
        `p`: Prime number
        `public_key`: Public key
        `private_key`: Private key

    Returns:
        `shared_secret`: The shared integer secret between the multiple parties
    """

    shared_secret = pow(public_key, private_key, p)
    return shared_secret
