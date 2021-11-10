import collections
import heapq
import pathlib
import typing

from compress import config, helpers


class Node:
    pass


# An internal node in a code tree. It has two nodes as children.
class InternalNode(Node):
    def __init__(self, left: Node, right: Node) -> None:
        if not isinstance(left, Node) or not isinstance(right, Node):
            raise TypeError()
        self.left = left
        self.right = right


# A leaf node in a code tree. It has a char value.
class Leaf(Node):
    def __init__(self, char: int) -> None:
        if char < 0:
            raise ValueError("Symbol value must be non-negative")
        self.char = char


class CodeTree:
    def __init__(self, root: Node, codes: dict[int, tuple[int, ...]]) -> None:
        self.root = root
        self.codes = codes

    @classmethod
    def from_root(cls, root: Node) -> 'CodeTree':
        def build_code_list(node: Node, prefix: tuple[int, ...]) -> None:
            if isinstance(node, InternalNode):
                build_code_list(node.left, prefix + (0,))
                build_code_list(node.right, prefix + (1,))
                return
            if isinstance(node, Leaf):
                if codes.get(node.char):
                    raise ValueError("Symbol has more than one code")
                codes[node.char] = prefix
                return
            raise TypeError("Illegal node type")

        codes: dict[int, tuple[int, ...]] = {}
        build_code_list(node=root, prefix=tuple())

        return cls(root=root, codes=codes)

    @classmethod
    def from_filepath(cls, filepath: pathlib.Path) -> 'CodeTree':
        frequencies = collections.Counter(helpers.char_input_stream(filepath=filepath))
        frequencies[config.EOF_CHAR] += 1
        return cls.from_frequencies(frequencies=frequencies)

    @classmethod
    def from_frequencies(cls, frequencies: typing.Counter[int]) -> 'CodeTree':
        pqueue: list[tuple[int, int, Node]] = []

        for char, frequency in frequencies.items():
            heapq.heappush(pqueue, (frequency, char, Leaf(char=char)))

        if len(pqueue) < 2:
            cls._fill_up_to_2(pqueue=pqueue, exclude_chars=list(frequencies.keys()))

        while len(pqueue) > 1:
            left = heapq.heappop(pqueue)
            right = heapq.heappop(pqueue)
            parent = (
                left[0] + right[0],
                min(left[1], right[1]),
                InternalNode(left=left[2], right=right[2]),
            )
            heapq.heappush(pqueue, parent)

        return CodeTree.from_root(root=pqueue[0][2])

    @staticmethod
    def _fill_up_to_2(
        pqueue: list[tuple[int, int, Node]], exclude_chars: list[int]
    ) -> None:
        for char in range(config.ALPHABET_LENGTH):
            if char not in exclude_chars:
                heapq.heappush(pqueue, (0, char, Leaf(char)))
            if len(pqueue) >= 2:
                return


class CanonicalCode:
    def __init__(self, code_lengths: list[int]) -> None:
        self.code_lengths = code_lengths

    @classmethod
    def from_code_tree(cls, code_tree: CodeTree) -> 'CanonicalCode':
        # TODO: why not just [len(code_tree.codes.get(char, 0) for char in code_tree.codes]
        def build_code_lengths(node: Node, depth: int) -> None:
            if isinstance(node, Leaf):
                code_lengths[node.char] = depth
                return
            if isinstance(node, InternalNode):
                build_code_lengths(node.left, depth + 1)
                build_code_lengths(node.right, depth + 1)
                return
            raise TypeError("Illegal node type")

        code_lengths = [0] * config.ALPHABET_LENGTH
        build_code_lengths(node=code_tree.root, depth=0)

        return cls(code_lengths=code_lengths)

    # TODO: maybe make this method CodeTree.canonize
    def to_code_tree(self) -> CodeTree:
        nodes: list[Node] = []

        for i in range(max(self.code_lengths), -1, -1):
            assert len(nodes) % 2 == 0
            new_nodes: list[Node] = []

            if i > 0:
                for char, code_length in enumerate(self.code_lengths):
                    if code_length == i:
                        new_nodes.append(Leaf(char=char))

            for j in range(0, len(nodes), 2):
                new_nodes.append(InternalNode(left=nodes[j], right=nodes[j + 1]))

            nodes = new_nodes

        return CodeTree.from_root(root=nodes[0])
