import pytest

from decrypt import decrypt


@pytest.mark.parametrize(
    "input_text, shift_key, result",
    [
        ("ithicitmicudgcujc", 15, "test text for fun"),
        ("YUSKtXGTJUStZKDZ", 6, "SOME RANDOM TEXT"),
    ],
)
def test_decrypt_good(input_text: str, shift_key: int, result: str):
    assert decrypt(input_text=input_text, key=shift_key) == result


@pytest.mark.parametrize(
    "input_text, shift_key",
    [
        ("I LOVE UKRAINE", "t")
    ],
)
def test_decrypt_bad(
        input_text: str,
        shift_key: int,
):
    with pytest.raises(TypeError):
        decrypt(input_text=input_text, key=shift_key)
