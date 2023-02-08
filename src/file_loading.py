import base64


def load_file_as_bytes(
    filename: str,
    remove_newlines=False,
    load_as_list=False,
) -> bytes:
    """Loads a file as a byte array"""

    # TODO: maybe remove this if not important
    if load_as_list and remove_newlines:
        with open(filename, "r") as f:
            return [bytes(line.replace("\n", ""), "utf-8") for line in f.readlines()]

    if remove_newlines:
        with open(filename, "r") as f:
            text = f.read().replace("\n", "")
            return bytes(text, "utf-8")

    if load_as_list:
        with open(filename, "r") as f:
            return [bytes(line, "utf-8") for line in f.readlines()]

    else:
        with open(filename, "rb") as f:
            return f.read()


def load_file_as_b64(
    filename: str,
    remove_newlines=False,
    load_as_list=False,
) -> bytes:
    return base64.b64decode(
        load_file_as_bytes(
            filename,
            remove_newlines,
            load_as_list,
        )
    )
