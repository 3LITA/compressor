import itertools
import pathlib
import typing

from compression import config

from ..base import BaseEncoder
from . import tree


class Encoder(BaseEncoder):
    def __init__(
        self, code_lengths: typing.List[int], code_tree: tree.CodeTree
    ) -> None:
        self._code_lengths = code_lengths
        self._tree = code_tree

    @classmethod
    def from_filepath(cls, filepath: pathlib.Path) -> 'Encoder':
        code_tree = tree.CodeTree.from_filepath(filepath=filepath)
        return cls._from_code_tree(code_tree=code_tree)

    @classmethod
    def from_chars(cls, chars: typing.Iterable[int]) -> 'Encoder':
        code_tree = tree.CodeTree.from_chars(chars=chars)
        return cls._from_code_tree(code_tree=code_tree)

    @classmethod
    def _from_code_tree(cls, code_tree: tree.CodeTree) -> 'Encoder':
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
    def encode(
        self, stream: typing.Iterable[int]
    ) -> typing.Iterator[typing.Tuple[int, ...]]:
        return itertools.chain(
            (self._tree.codes[char] for char in stream),
            (self._tree.codes[config.EOF_CHAR],),
        )
