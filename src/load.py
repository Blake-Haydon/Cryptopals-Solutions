import base64


def file_as_bytes(filename: str, remove_newlines=False) -> bytes:
    """Loads a file encoded as `utf-8` as bytes"""

    if remove_newlines:
        with open(filename, "r") as f:
            text = f.read().replace("\n", "")
            return bytes(text, "utf-8")

    else:
        with open(filename, "rb") as f:
            return f.read()


def file_as_b64(filename: str, remove_newlines=False) -> bytes:
    """Loads a file a file encoded with base64 into bytes"""
    return base64.b64decode(file_as_bytes(filename, remove_newlines))
