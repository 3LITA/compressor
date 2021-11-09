from compress import processors

from . import _base


ALGORITHM_NAME = 'bwt'
PROCESSORS = (processors.burrows_wheeler, processors.move_to_front)


class Encoder(_base.HuffmanEncoder):
    algorithm = ALGORITHM_NAME

    _PREPROCESSORS = (
        processors.burrows_wheeler.transform,
        processors.move_to_front.transform,
    )


class Decoder(_base.HuffmanDecoder):
    algorithm = ALGORITHM_NAME

    _POSTPROCESSORS = (
        processors.move_to_front.restore,
        processors.burrows_wheeler.restore,
    )
