import pytest

from src.calculatorLogic.calc_errors import SolvingError, CalculationError
from tests.constants_for_tests import test_calculator


class TestCalculator:

    @pytest.mark.parametrize(
        "expression, correct_answer",
        [
            ("1+2", 3),
            ("3-2", 1),
            ("2*3", 6),
            ("7 / 2", 3.5),
            ("5^3", 125),
            ("7%4", 3),
            ("321$123", 321),
            ("9999&11", 11),
            ("2@8", 5),
            ("~31", -31),
            ("9!", 362880),
            ("81.24#", 15),
            ("2+4*3", 14),
            ("-8+6/3", -6),
            ("3+-3", 0),
            ("-5!", -120),
            ("20-4!", -4),
            ("(23+78)*1.5", 151.5),
            ("3*7^(1+4-3)", 147),
            ("6     6 7@ (32*10 )$- 9", 493.5),
            ("2^4^7", 268435456),
            ("2^(3^3)", 134217728),
            ("4---5+2*-13", -27),
            ("99##", 9),
            ("16^0.5*(3+2$(8&5))", 32), # (16^0.5)*(3+(2$(8&5))) -> (16^0.5)*(3+ (2$5)) -> (16^0.5)*(3+5) -> 4 * 8
            ("159 -2 *3 ^3!@62  #", -4215), # 159-(2*(3^((3!)@(62#)))) -> 159-(2*(3^(6@8))) -> 159-(2*(3^7))
            ("~-5", 5),
            ("10 % 3 * 2", 2),
            ("-(2 + 3)", -5),
            ("5 + -(2 * 3)", -1),
            ("5 % 2 * (7 - 3)", 4),
            ("4! - 2! * 3", 18),
            ("10 $ 20 & 15 @ 22", 18.5),
            ("10 $ 20 & 22 @ 15", 17.5),
            ("4# + 7# + 12#", 14),
            ("2#*5+1#", 11),
            ("12345# * 2", 30),
            ("-123#", -6),
            ("-(10# + 20#)", -3)
        ]
    )
    def test_calculate(self, expression: str, correct_answer: float):
        assert test_calculator.calculate(expression) == correct_answer

    @pytest.mark.parametrize(
        "expression, expected_exception",
        [
            ("", SolvingError),
            ("1--6!#", CalculationError)
        ]
    )
    def test_calculate_raises(self, expression: str, expected_exception: type[Exception]):
        with pytest.raises(expected_exception):
            test_calculator.calculate(expression)