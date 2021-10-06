import collections
import sys
import typing


MAP_TEXT_SPLITTER = '__'
MAP_ITEMS_SPLITTER = '||'
KEY_VALUE_SPLITTER = '::'


class Encoder:
    def __init__(self, text: str) -> None:
        self._text = text
        self._letters_map: dict[str, str] = {}

    @classmethod
    def from_filepath(cls, filepath: str) -> 'Encoder':
        with open(filepath, 'r') as input_file:
            text = input_file.read()
        return Encoder(text=text)

    def encode_to_filepath(self, filepath: str) -> None:
        encoded = self.encode()
        with open(filepath, 'w') as output_file:
            output_file.write(encoded)

    def encode(self) -> str:
        self._construct_letters_map()
        serialized_map = self._serialize_letters_map()
        encoded = ''.join([self._letters_map[letter] for letter in self._text])
        return f'{serialized_map}{MAP_TEXT_SPLITTER}{encoded}'

    def _serialize_letters_map(self) -> str:
        return MAP_ITEMS_SPLITTER.join(
            [
                f'{letter}{KEY_VALUE_SPLITTER}{code}'
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


class Decoder:
    def __init__(self, text: str) -> None:
        self._text = text

    @classmethod
    def from_filepath(cls, filepath: str) -> 'Decoder':
        with open(filepath, 'r') as encoded_file:
            text = encoded_file.read()
        return cls(text=text)

    def decode_to_filepath(self, filepath: str) -> None:
        decoded_text = self.decode()
        with open(filepath, 'w') as output_file:
            output_file.write(decoded_text)

    def decode(self) -> str:
        serialized_map, encoded_text = self._text.split(MAP_TEXT_SPLITTER)

        codes_map: dict[str, str] = {}
        for map_item in serialized_map.split(MAP_ITEMS_SPLITTER):
            letter, code = map_item.split(KEY_VALUE_SPLITTER)
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


def main() -> None:
    action = sys.argv[1]
    filepath = sys.argv[2]

    if action == 'e':
        encoder = Encoder.from_filepath(filepath=filepath)
        encoder.encode_to_filepath(filepath=f'{filepath}.huff')
    elif action == 'd':
        decoder = Decoder.from_filepath(filepath=filepath)
        decoder.decode_to_filepath(filepath=f'{filepath}.decoded')


if __name__ == '__main__':
    main()
