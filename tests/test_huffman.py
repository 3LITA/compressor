from compress.coders import huffman


def test_build_codes():
    letters_probabilites = {
        'a': 0.25,
        'b': 0.2,
        'c': 0.15,
        'd': 0.1,
        'e': 0.1,
        'f': 0.1,
        'g': 0.1,
    }
    letters_map = huffman.Encoder._build_codes(letters_probabilites)
    assert letters_map == {
        'a': '10',
        'b': '111',
        'c': '110',
        'd': '000',
        'e': '001',
        'f': '010',
        'g': '011',
    }


def test_find_two_letters_with_least_probability():
    letter_probabilities = {
        'a': 0.25,
        'b': 0.2,
        'c': 0.15,
        'd': 0.1,
        'e': 0.1,
        'f': 0.1,
        'g': 0.1,
    }
    assert huffman.Encoder._find_two_words_with_least_probability(
        letter_probabilities
    ) == ['d', 'e']
