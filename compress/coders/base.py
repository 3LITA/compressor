import abc
import typing


class BaseEncoder(abc.ABC):
    @abc.abstractmethod
    def encode(self, stream: typing.Iterator[int]) -> typing.Iterator[tuple[int, ...]]:
        ...


class BaseDecoder(abc.ABC):
    @abc.abstractmethod
    def decode(self, stream: typing.Iterator[int]) -> typing.Iterator[int]:
        ...
