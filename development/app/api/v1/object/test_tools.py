from pytest import mark

from tools import extension_from_url


@mark.parametrize(
    "given, expected",
    [
        ("test.jpg", "jpg"),
        ("test", ""),
        (
            "https://github.com/datable-be/AI4C_ContentAnalysis/blob/da9995b6a2a2795bb2d2cce0695417efc5b674f3/scripts/color-detector/examples/39355scr_0ed48a9fe99bfe5_e183b86fc24d9855178e546b5f96c28a.jpg?raw=true",
            "jpg",
        ),
    ],
)
def test_sanitize_filename(given: str, expected: str) -> None:
    assert extension_from_url(given) == expected
