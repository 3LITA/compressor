import typing

from compression import config


def transform(source: typing.List[int]) -> typing.Iterator[int]:
    alphabet = list(range(config.ALPHABET_LENGTH))

    for char in source:
        index = alphabet.index(char)
        alphabet.insert(0, alphabet.pop(index))
        yield index


def restore(transformed: typing.Iterator[int]) -> typing.Iterator[int]:
    alphabet = list(range(config.ALPHABET_LENGTH))

    for index in transformed:
        char = alphabet[index]
        alphabet.insert(0, alphabet.pop(index))
        yield char
