import pathlib
import typing

from compression import config, streamers

from ..base import BaseDecoder
from . import tree


class Decoder(BaseDecoder):
    def __init__(self, code_tree: tree.CodeTree) -> None:
        self._code_tree = code_tree

    @classmethod
    def from_filepath(cls, filepath: pathlib.Path) -> 'Decoder':
        code_lengths = cls._read_header(filepath=filepath)
        canonical = tree.CanonicalCode(code_lengths=code_lengths)
        code_tree = canonical.to_code_tree()
        return cls(code_tree=code_tree)

    @staticmethod
    def _read_header(filepath: pathlib.Path) -> typing.List[int]:
        def read_int(n: int) -> int:
            result = 0
            for _ in range(n):
                result = (result << 1) | next(input_stream.read_no_eof())
            return result

        with streamers.BitInputStream(input_filename=filepath) as input_stream:
            return [read_int(config.BYTE_LENGTH) for _ in range(config.ALPHABET_LENGTH)]

    def decode(self, stream: typing.Iterator[int]) -> typing.Iterator[int]:
        self._skip_header(stream=stream)

        current_node = typing.cast(tree.InternalNode, self._code_tree.root)
        for bit in stream:
            if bit:
                next_node = current_node.right
            else:
                next_node = current_node.left
            if isinstance(next_node, tree.InternalNode):
                current_node = next_node
                continue
            if isinstance(next_node, tree.Leaf):
                if next_node.char == config.EOF_CHAR:
                    return
                yield next_node.char
                current_node = typing.cast(tree.InternalNode, self._code_tree.root)
                continue
            raise TypeError("Illegal node type")

    def _skip_header(self, stream: typing.Iterator[int]) -> None:
        for _ in range(config.ALPHABET_LENGTH):
            for _ in range(config.BYTE_LENGTH):
                next(stream)
