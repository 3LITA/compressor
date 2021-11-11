import abc
import pathlib


class _BaseAlgorithm:
    def __init__(
        self, input_filepath: pathlib.Path, output_filepath: pathlib.Path
    ) -> None:
        self._input_filepath = input_filepath
        self._output_filepath = output_filepath


class BaseCompressor(_BaseAlgorithm, abc.ABC):
    @abc.abstractmethod
    def compress(self) -> None:
        ...


class BaseDecompressor(_BaseAlgorithm, abc.ABC):
    @abc.abstractmethod
    def decompress(self) -> None:
        ...
