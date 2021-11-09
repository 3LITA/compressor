import collections
import dataclasses
import typing


@dataclasses.dataclass
class Transformation:
    last_column: str
    index: int

    def dump(self) -> str:
        index = f'{self.index:8d}'
        assert len(index) <= 8, "Index overflow!"
        return f'{index}{self.last_column}'

    @classmethod
    def load(cls, raw: str) -> 'Transformation':
        index = int(raw[:8])
        return cls(index=index, last_column=raw[8:])


def transform(source: str) -> str:
    rotations = sorted(_generate_rotations(source=source))
    index = rotations.index(source)
    bwt = _construct_last_column(rotations)
    return Transformation(last_column=bwt, index=index).dump()


def _generate_rotations(source: str) -> typing.Iterator[str]:
    for i in range(len(source)):
        yield f'{source[i:]}{source[:i]}'


def _construct_last_column(rotations: list[str]) -> str:
    return ''.join(rotation[-1] for rotation in rotations)


def restore(raw_transformation: str) -> str:
    transformation = Transformation.load(raw_transformation)
    last_first_map = _build_last_first_map(transformation.last_column)
    return _restore_by_last_first_map(
        index=transformation.index,
        last_first_map=last_first_map,
    )


def _build_last_first_map(last_column: str) -> dict[tuple[str, int], tuple[str, int]]:
    first_column = sorted(last_column)

    enumerated_first_column = _enumerate_letters_in_column(column=first_column)
    enumerated_last_column = _enumerate_letters_in_column(column=last_column)

    return {
        letter_number: enumerated_first_column[i]
        for i, letter_number in enumerate(enumerated_last_column)
    }


def _enumerate_letters_in_column(column: typing.Iterable[str]) -> list[tuple[str, int]]:
    enumerated_letters = []

    counter: typing.Counter[str] = collections.Counter()
    for letter in column:
        counter[letter] += 1
        enumerated_letters.append((letter, counter[letter]))

    return enumerated_letters


def _restore_by_last_first_map(
    index: int,
    last_first_map: dict[tuple[str, int], tuple[str, int]],
) -> str:
    letter = tuple(last_first_map.keys())[index]  # dict preserves insert order

    letters = []
    while last_first_map:
        letter = last_first_map.pop(letter)
        letters.append(letter[0])

    return ''.join(letters)
