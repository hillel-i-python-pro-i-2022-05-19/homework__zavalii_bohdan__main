import pytest

from encrypt import encrypt


@pytest.mark.parametrize(
    "input_text, shift_key, result",
    [
        ("ATTACKATONCE", 9, "JCCJLTJCXWLN"),
        ("I LOVE UKRAINE", 9, "RwUXENwDTAJRWN"),
        ("testing homework", 23, "qbpqfkdkeljbtloh"),
    ],
)
def test_encrypt_good(input_text: str, shift_key: int, result: str):
    assert encrypt(input_text=input_text, key=shift_key) == result


@pytest.mark.parametrize(
    "input_text, shift_key",
    [
        ("I LOVE UKRAINE", "t")
    ],
)
def test_encrypt_type_error(
        input_text: str,
        shift_key: int,
):
    with pytest.raises(TypeError):
        encrypt(input_text=input_text, key=shift_key)


@pytest.mark.parametrize(
    "input_text, shift_key",
    [
        (64, 12)
    ],
)
def test_encrypt_attr_err(
        input_text: str,
        shift_key: int,
):
    with pytest.raises(AttributeError):
        encrypt(input_text=input_text, key=shift_key)
