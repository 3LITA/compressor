from . import _base


ALGORITHM_NAME = 'huffman'


class Encoder(_base.HuffmanEncoder):
    algorithm = ALGORITHM_NAME


class Decoder(_base.HuffmanDecoder):
    algorithm = ALGORITHM_NAME
