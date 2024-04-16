from pytest import mark

from api.v1.tools.source import extension_from_source
from api.v1.tools.color import (
    convert_colors_to_EFT,
    getColorName,
)


@mark.parametrize(
    'given, expected',
    [
        ('test.jpg', '.jpg'),
        ('test', ''),
        (
            'https://github.com/datable-be/AI4C_ContentAnalysis/blob/da9995b6a2a2795bb2d2cce0695417efc5b674f3/scripts/color-detector/examples/39355scr_0ed48a9fe99bfe5_e183b86fc24d9855178e546b5f96c28a.jpg?raw=true',
            '.jpg',
        ),
    ],
)
def test_sanitize_filename(given: str, expected: str) -> None:
    assert extension_from_source(given) == expected


def test_getColorName():
    assert getColorName((255, 0, 0)) == 'red'
    assert getColorName((0, 255, 0)) == 'green'


def test_convert_colors_to_EFT():
    input_colors = [
        ((255, 0, 0), 10),  # Red color with 10 pixels
        ((0, 255, 0), 20),  # Green color with 20 pixels
        # Add more color tuples as needed
    ]

    result = convert_colors_to_EFT(input_colors)

    assert result == [('red', 10), ('green', 20)]
