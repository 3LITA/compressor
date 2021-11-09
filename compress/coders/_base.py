import abc
import collections
import pathlib
import typing


class _FileReaderMixin(abc.ABC):
    _PREPROCESSORS: tuple[typing.Callable[[str], str], ...] = tuple()
    _POSTPROCESSORS: tuple[typing.Callable[[str], str], ...] = tuple()

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
            text = cls._preprocess(text=text)
        return cls(text=text)

    @classmethod
    def _preprocess(cls, text: str) -> str:
        for preprocessor in cls._PREPROCESSORS:
            text = preprocessor(text)
        return text

    def to_file(self, filepath: pathlib.Path) -> None:
        with open(filepath, 'w') as output_file:
            output_file.write(self._postprocess(self._act()))

    @classmethod
    def _postprocess(cls, text: str) -> str:
        for postprocessor in cls._POSTPROCESSORS:
            text = postprocessor(text)
        return text

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


class HuffmanAlgorithm:
    MAP_TEXT_SPLITTER = '__'
    MAP_ITEMS_SPLITTER = '||'
    KEY_VALUE_SPLITTER = '::'


class HuffmanEncoder(BaseEncoder, HuffmanAlgorithm):
    _letters_map: dict[str, str] = {}

    def encode(self) -> str:
        self._construct_letters_map()
        serialized_map = self._serialize_letters_map()
        encoded = ''.join([self._letters_map[letter] for letter in self._text])
        return f'{serialized_map}{self.MAP_TEXT_SPLITTER}{encoded}'

    def _serialize_letters_map(self) -> str:
        return self.MAP_ITEMS_SPLITTER.join(
            [
                f'{letter}{self.KEY_VALUE_SPLITTER}{code}'
                for letter, code in self._letters_map.items()
            ]
        )

    def _construct_letters_map(self) -> None:
        letter_occurrences: typing.Counter[str] = collections.Counter()
        for letter in self._text:
            letter_occurrences[letter] += 1

        total_letters = len(self._text)
        letter_probabilities = {
            letter: occurrences / total_letters
            for letter, occurrences in letter_occurrences.items()
        }
        self._letters_map = self._build_codes(probabilities=letter_probabilities)

    @classmethod
    def _build_codes(cls, probabilities: dict[str, float]) -> dict[str, str]:
        letters_map: typing.DefaultDict[str, str] = collections.defaultdict(str)

        while probabilities:
            word_1, word_2 = cls._find_two_words_with_least_probability(probabilities)

            probabilities[word_1 + word_2] = probabilities.pop(
                word_1
            ) + probabilities.pop(word_2)
            for letter in word_1:
                letters_map[letter] = '0' + letters_map[letter]
            for letter in word_2:
                letters_map[letter] = '1' + letters_map[letter]
            if len(probabilities) == 1:
                break

        return letters_map

    @staticmethod
    def _find_two_words_with_least_probability(
        letter_probabilites: dict[str, float]
    ) -> list[str]:
        return sorted(letter_probabilites, key=lambda i: letter_probabilites[i])[:2]


class HuffmanDecoder(BaseDecoder, HuffmanAlgorithm):
    def decode(self) -> str:
        serialized_map, encoded_text = self._text.split(self.MAP_TEXT_SPLITTER)

        codes_map: dict[str, str] = {}
        for map_item in serialized_map.split(self.MAP_ITEMS_SPLITTER):
            letter, code = map_item.split(self.KEY_VALUE_SPLITTER)
            codes_map[code] = letter

        decoded_text = ''
        code = ''
        for code_part in encoded_text:
            code += code_part
            letter = codes_map.get(code, '')
            if not letter:
                continue
            decoded_text += letter
            code = ''

        return decoded_text
