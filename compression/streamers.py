import pathlib
import typing


def char_input_stream(filepath: pathlib.Path) -> typing.Iterator[int]:
    with open(filepath, 'rb') as input_stream:
        byte = input_stream.read(1)
        while byte:
            yield byte[0]
            byte = input_stream.read(1)


class BitInputStream:
    _stream: typing.BinaryIO

    def __init__(self, input_filename: pathlib.Path) -> None:
        self._input_filename = input_filename
        self._current_byte = 0
        self._bits_remaining = 0

    def __enter__(self) -> 'BitInputStream':
        self._stream = open(self._input_filename, 'rb')
        return self

    def __exit__(self, *exc: typing.Any) -> None:
        self._stream.close()
        self._current_byte = -1
        self._bits_remaining = 0

    def read(self) -> int:
        if self._current_byte == -1:
            return -1
        if not self._bits_remaining:
            temp = self._stream.read(1)
            if not temp:
                self._current_byte = -1
                return -1

            self._bits_remaining = 8
            self._current_byte = temp[0]
        self._bits_remaining -= 1
        return (self._current_byte >> self._bits_remaining) & 1

    def read_no_eof(self) -> typing.Iterator[int]:
        result = self.read()
        while result != -1:
            yield result
            result = self.read()
        raise EOFError


class BitOutputStream:
    _stream: typing.BinaryIO

    def __init__(self, output_filename: pathlib.Path) -> None:
        self._output_filename = output_filename
        self._current_byte = 0
        self._bits_filled = 0

    def __enter__(self) -> 'BitOutputStream':
        self._stream = open(self._output_filename, 'wb')
        return self

    def __exit__(self, *exc: typing.Any) -> None:
        while self._bits_filled != 0:
            self.write(0)
        self._stream.close()

    def write(self, bit: int) -> None:  # TODO: use bool bit
        self._current_byte = (self._current_byte << 1) | bit
        self._bits_filled += 1

        if self._bits_filled == 8:
            self._flush()

    def _flush(self) -> None:
        content = bytes((self._current_byte,))
        self._stream.write(content)
        self._current_byte = 0
        self._bits_filled = 0
