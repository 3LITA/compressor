import pathlib
import typing

from compress import processors, streamers
from compress.coders import huffman

from . import _base


ALGORITHM_NAME = 'bwt'


class Compressor(_base.BaseCompressor):
    algorithm = ALGORITHM_NAME

    def __init__(
        self, input_filepath: pathlib.Path, output_filepath: pathlib.Path
    ) -> None:
        super().__init__(input_filepath=input_filepath, output_filepath=output_filepath)
        self._preprocessed = list(self._preprocess())
        self._encoder = huffman.Encoder.from_chars(chars=list(self._preprocessed))

    def _preprocess(self) -> typing.Iterator[int]:
        block = list(streamers.char_input_stream(filepath=self._input_filepath))
        bwt = processors.burrows_wheeler.BurrowsWheelerTransformer(
            block=block
        ).transform()
        mtf = processors.move_to_front.transform(source=bwt)
        return mtf

    def compress(self) -> None:
        with streamers.BitOutputStream(
            output_filename=self._output_filepath
        ) as output_stream:
            for bit in self._encoder.header:
                output_stream.write(bit=bit)
            for bits in self._encoder.encode(stream=self._preprocessed):
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
        with streamers.BitInputStream(
            input_filename=self._input_filepath
        ) as input_stream:
            last_column = list(
                processors.move_to_front.restore(
                    self._decoder.decode(stream=input_stream.read_no_eof())
                )
            )
        bw = processors.burrows_wheeler.BurrowsWheelerRestorer(last_column=last_column)
        with open(self._output_filepath, 'wb') as output_stream:
            output_stream.write(bytes(bw.restore()[:-1]))
