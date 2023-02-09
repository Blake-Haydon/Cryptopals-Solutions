import hashlib


def digest(b: bytes) -> bytes:
    """Computes the SHA-256 digest of a byte string `b`"""
    return hashlib.sha256(b).digest()
