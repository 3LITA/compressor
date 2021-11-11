import collections
import functools
import typing

from compression import config


class BurrowsWheelerTransformer:
    def __init__(self, block: typing.List[int]) -> None:
        self._block = block + [config.END_OF_BLOCK_CHAR]

    def transform(self) -> typing.List[int]:
        indices = list(range(len(self._block)))
        indices.sort(key=functools.cmp_to_key(self._compare))
        last_column = self._construct_last_column(indices=indices)
        return last_column

    def _compare(self, x: int, y: int) -> int:
        # TODO: remove this duplication
        return self._compare_by_x(x=x, y=y) if x > y else self._compare_by_y(x=x, y=y)

    def _compare_by_x(self, x: int, y: int) -> int:
        while self._block[x] == self._block[y] and x < len(self._block):
            x += 1
            y += 1

        if self._block[x] == self._block[y]:
            return 0
        return -1 if self._block[x] < self._block[y] else 1

    def _compare_by_y(self, x: int, y: int) -> int:
        while self._block[x] == self._block[y] and y < len(self._block):
            x = x + 1
            y = y + 1

        if self._block[x] == self._block[y]:
            return 0
        return -1 if self._block[x] < self._block[y] else 1

    def _construct_last_column(self, indices: typing.List[int]) -> typing.List[int]:
        return [self._block[ix - 1] for ix in indices]


class BurrowsWheelerRestorer:
    def __init__(self, last_column: typing.List[int]) -> None:
        self._last_column = last_column

    def restore(self) -> typing.List[int]:
        last_first_map = self._build_last_first_map()
        target_shift_index = self._last_column.index(config.END_OF_BLOCK_CHAR)
        return self._restore_by_last_first_map(
            index=target_shift_index,
            last_first_map=last_first_map,
        )

    def _build_last_first_map(
        self,
    ) -> typing.Dict[typing.Tuple[int, int], typing.Tuple[int, int]]:
        first_column = sorted(self._last_column)

        enumerated_first_column = self._enumerate_letters_in_column(column=first_column)
        enumerated_last_column = self._enumerate_letters_in_column(
            column=self._last_column
        )

        return {
            char: enumerated_first_column[i]
            for i, char in enumerate(enumerated_last_column)
        }

    @staticmethod
    def _enumerate_letters_in_column(
        column: typing.Iterable[int],
    ) -> typing.List[typing.Tuple[int, int]]:
        enumerated_letters = []

        counter: typing.Counter[int] = collections.Counter()
        for char in column:
            counter[char] += 1
            enumerated_letters.append((char, counter[char]))

        return enumerated_letters

    @staticmethod
    def _restore_by_last_first_map(
        index: int,
        last_first_map: typing.Dict[typing.Tuple[int, int], typing.Tuple[int, int]],
    ) -> typing.List[int]:
        char = tuple(last_first_map.keys())[index]  # dict preserves insert order

        chars = []
        while last_first_map:
            char = last_first_map.pop(char)
            chars.append(char[0])

        return chars
