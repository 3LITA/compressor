import pathlib

from compress import helpers
from compress.coders import huffman

from . import _base


ALGORITHM_NAME = 'huffman'


class Compressor(_base.BaseCompressor):
    algorithm = ALGORITHM_NAME

    def __init__(
        self, input_filepath: pathlib.Path, output_filepath: pathlib.Path
    ) -> None:
        super().__init__(input_filepath=input_filepath, output_filepath=output_filepath)
        self._encoder = huffman.Encoder.from_filepath(filepath=input_filepath)

    def compress(self) -> None:
        with helpers.BitOutputStream(
            output_filename=self._output_filepath
        ) as output_stream:
            for bit in self._encoder.header:
                output_stream.write(bit=bit)
            input_stream = helpers.char_input_stream(filepath=self._input_filepath)
            for bits in self._encoder.encode(stream=input_stream):
                for bit in bits:
                    output_stream.write(bit=bit)


class Decompressor(_base.BaseDecompressor):
    algorithm = ALGORITHM_NAME

    def __init__(
        self, input_filepath: pathlib.Path, output_filepath: pathlib.Path
    ) -> None:
        super().__init__(input_filepath=input_filepath, output_filepath=output_filepath)
        self._decoder = huffman.Decoder.from_filepath(filepath=input_filepath)

    def decompress(self) -> None:
        with helpers.BitInputStream(
            input_filename=self._input_filepath
        ) as input_stream:
            with open(self._output_filepath, 'wb') as output_stream:
                for char in self._decoder.decode(stream=input_stream.read_no_eof()):
                    output_stream.write(bytes((char,)))
