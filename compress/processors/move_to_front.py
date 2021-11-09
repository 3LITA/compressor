import string


ASCII = string.ascii_letters + string.digits + string.punctuation + string.whitespace


def transform(source: str) -> str:
    alphabet = ASCII

    result = ''
    for char in source:
        index = alphabet.index(char)
        result += f'{index:03d}'
        # TODO: maybe some functool for here?
        alphabet = char + alphabet[:index] + alphabet[index + 1 :]

    return result


def restore(transformed: str) -> str:
    alphabet = ASCII

    restored = ''
    for i in range(0, len(transformed), 3):
        index = int(transformed[i : i + 3])
        char = alphabet[index]
        restored += char
        alphabet = alphabet[index] + alphabet[:index] + alphabet[index + 1 :]

    return restored
