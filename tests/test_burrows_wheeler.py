import pytest

from compression.processors import burrows_wheeler


@pytest.mark.parametrize(
    'source, expected',
    (
        pytest.param(
            [99, 111, 100, 101, 115, 112, 101, 101, 100, 121],
            [256, 111, 101, 101, 112, 100, 99, 115, 101, 100, 121],
        ),
        pytest.param(
            [
                65,
                108,
                98,
                101,
                114,
                116,
                32,
                83,
                104,
                97,
                105,
                100,
                117,
                108,
                108,
                105,
                110,
            ],
            [
                116,
                256,
                32,
                104,
                108,
                105,
                98,
                83,
                97,
                108,
                65,
                108,
                117,
                105,
                101,
                114,
                100,
                110,
            ],
        ),
        pytest.param(
            [109, 105, 115, 115, 105, 115, 115, 105, 112, 112, 105],
            [115, 115, 109, 112, 256, 112, 105, 115, 115, 105, 105, 105],
        ),
    ),
)
def test_burrows_wheeler_transformation(source, expected):
    bwt = burrows_wheeler.BurrowsWheelerTransformer(source).transform()
    print(bwt)
    assert bwt == expected
    # assert burrows_wheeler.restore(expected) == source
