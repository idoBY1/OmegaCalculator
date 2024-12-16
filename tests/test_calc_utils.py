import pytest

from src.calculatorLogic import calc_utils


class TestCalcUtils:

    @pytest.mark.parametrize(
        "string, new_string",
        [
            ("a b   c   de", "abcde"),
            ("abc", "abc"),
            ("abc bc  a", "abcbca")
        ]
    )
    def test_delete_whitespace(self, string: str, new_string: str):
        assert calc_utils.delete_whitespace(string) == new_string

    @pytest.mark.parametrize(
        "string, new_string",
        [
            ("a b   c   de", "a b c de"),
            ("abc", "abc"),
            ("abc bc  a", "abc bc a")
        ]
    )
    def test_organize_whitespace(self, string: str, new_string: str):
        assert calc_utils.organize_whitespace(string) == new_string

    @pytest.mark.parametrize(
        "string, result",
        [
            ("1", True),
            ("1.1", True),
            ("12.345", True),
            ("1 2.34", True),
            ("0. 34 1 ", True),
            ("=", False),
            ("34$", False),
            ("^16", False),
            ("je", False),
            ("a", False),
            ("R", False),
            ("d23", False),
            (";:", False)
        ]
    )
    def test_is_float_str(self, string: str, result: bool):
        assert calc_utils.is_float_str(string) == result