import itertools

from compression.coders.huffman import CodeTree


def test_building_codes_with_code_tree():
    chars = itertools.chain([0] * 25, [1] * 20, [2] * 15, [3, 4, 5, 6] * 10)
    tree = CodeTree.from_chars(chars=chars)
    assert len(tree.codes) == 8
    assert [tree.codes[key] for key in range(7)] == [
        (1, 0),
        (1, 1, 1),
        (1, 1, 0),
        (0, 1, 1, 1),
        (0, 0, 0),
        (0, 0, 1),
        (0, 1, 0),
    ]
    assert tree.codes[257] == (0, 1, 1, 0)
