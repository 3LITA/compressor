import abc
import pathlib


class _FileReaderMixin(abc.ABC):
    @property
    @abc.abstractmethod
    def algorithm(self) -> str:
        ...

    def __init__(self, text: str) -> None:
        self._text = text

    @classmethod
    def from_file(cls, filepath: pathlib.Path) -> '_FileReaderMixin':
        with open(filepath, 'r') as source_file:
            text = source_file.read()
        return cls(text=text)

    def to_file(self, filepath: pathlib.Path) -> None:
        with open(filepath, 'w') as output_file:
            output_file.write(self._act())

    @abc.abstractmethod
    def _act(self) -> str:
        ...


class BaseEncoder(_FileReaderMixin):
    def _act(self) -> str:
        return self.encode()

    @abc.abstractmethod
    def encode(self) -> str:
        ...


class BaseDecoder(_FileReaderMixin):
    def _act(self) -> str:
        return self.decode()

    @abc.abstractmethod
    def decode(self) -> str:
        ...
