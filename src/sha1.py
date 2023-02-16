import hashlib


def digest(b: bytes) -> bytes:
    """Computes the SHA-1 digest of a byte string `b`"""
    return hashlib.sha1(b).digest()


def mac(key: bytes, msg: bytes):
    """Computes the SHA-1 MAC of a message `msg` using a key `key`"""
    return digest(key + msg)
