import pytest

from compress.processors import burrows_wheeler


@pytest.mark.parametrize(
    'source, expected',
    (
        pytest.param('codespeedy', '       0yoeepdcsed'),
        pytest.param('Albert Shaidullin', '       1tn hlibSalAluierd'),
        pytest.param('mississippi', '       4pssmipissii'),
    ),
)
def test_burrows_wheeler_transformation(source, expected):
    assert burrows_wheeler.transform(source) == expected
    assert burrows_wheeler.restore(expected) == source
