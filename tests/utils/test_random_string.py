import pytest

from src.utils.random_string import generate_random_string


class TestRandomString:
    def test_generates_correct_length(self):
        string = generate_random_string(10)  # 🚧

        assert len(string) == 10  # 🧪

    def test_throws_if_not_int(self):
        with pytest.raises(TypeError):  # 🧪
            _ = generate_random_string("this ain't valid")  # type: ignore  # 🚧

    def test_negative_length(self):
        string = generate_random_string(-1)  # 🚧

        assert string == ""  # 🧪
