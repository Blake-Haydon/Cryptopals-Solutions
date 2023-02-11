import hashlib


def digest(b: bytes) -> bytes:
    """Computes the SHA-1 digest of a byte string `b`"""
    return hashlib.sha1(b).digest()
