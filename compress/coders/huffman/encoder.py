import itertools
import pathlib
import typing

from compress import config

from ..base import BaseEncoder
from . import tree


class Encoder(BaseEncoder):
    def __init__(self, code_lengths: list[int], code_tree: tree.CodeTree) -> None:
        self._code_lengths = code_lengths
        self._tree = code_tree

    @classmethod
    def from_filepath(cls, filepath: pathlib.Path) -> 'Encoder':
        code_tree = tree.CodeTree.from_filepath(filepath=filepath)
        canonical = tree.CanonicalCode.from_code_tree(code_tree=code_tree)
        code_tree = canonical.to_code_tree()
        return cls(code_lengths=canonical.code_lengths, code_tree=code_tree)

    @property
    def header(self) -> typing.Iterator[int]:
        for char in range(config.ALPHABET_LENGTH):
            code_length = self._code_lengths[char]
            for bit in reversed(range(8)):
                yield (code_length >> bit) & 1

    # TODO: return Iterator[bool]
    def encode(self, stream: typing.Iterator[int]) -> typing.Iterator[tuple[int, ...]]:
        return itertools.chain(
            (self._tree.codes[char] for char in stream),
            (self._tree.codes[config.EOF_CHAR],),
        )
