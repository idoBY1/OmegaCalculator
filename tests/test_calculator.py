import pytest

from src.calculatorLogic.calc_errors import SolvingError, CalculationError, FormattingError
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
            ("3+~4^5", -1021),
            ("(23+78)*1.5", 151.5),
            ("3*7^(1+4-3)", 147),
            ("6     6 7@ (32*10 )$- 9", 493.5),
            ("0000002 +     00003", 5),
            ("2^4^7", 268435456),
            ("2^(3^3)", 134217728),
            ("4---5+2*-13", -27),
            ("99##", 9),
            ("16^0.5*(3+2$(8&5))", 32), # (16^0.5)*(3+(2$(8&5))) -> (16^0.5)*(3+ (2$5)) -> (16^0.5)*(3+5) -> 4 * 8
            ("159 -2 *3 ^3!@62  #", -4215), # 159-(2*(3^((3!)@(62#)))) -> 159-(2*(3^(6@8))) -> 159-(2*(3^7))
            ("~-5", 5),
            ("~----------2", -2),
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
            ("-(10# + 20#)", -3),
            ("((10.5 + 2.5) * 3 - (40 / 5)) ^ 2 + 10", 971),
            ("((100 $ 50 & 75 @ 60) % 10) * 2", 15),
            ("(100$200&150)@((10&5)$20)", 85),
            ("((1 + (2 * (3 + (4 * (5 - (6 / 2)))))) ^ 2 ) #", 16),
            ("(1.1*1.1*1.1*1.1*1.1*1.1*1.1) + (2.1*2.1*2.1*2.1*2.1*2.1)", 87.7148381)
        ]
    )
    def test_calculate(self, expression: str, correct_answer: float):
        assert test_calculator.calculate(expression) == correct_answer

    @pytest.mark.parametrize(
        "expression, expected_exception",
        [
            ("3^*2", FormattingError),
            ("1--6!#", CalculationError),
            ("~*-3", FormattingError),
            ("3(8+2)", SolvingError),
            ("5(-2", FormattingError),
            ("+4*7", FormattingError),
            ("823*4+6&", FormattingError),
            ("4.23^0.397*6%", FormattingError),
            ("7++", FormattingError),
            ("+8+", FormattingError),
            ("8$(77-)^2", FormattingError),
            ("sdkjfb", FormattingError),
            ("1 + 1 = 2", FormattingError),
            ("", SolvingError),
            ("                       ", SolvingError),
            ("99999999!", CalculationError),
            ("(1/2)!", CalculationError),
            ("(-7)!", CalculationError),
            ("34956^23654", CalculationError),
            ("0^0+6", CalculationError),
            ("5%(3+4-7)", CalculationError),
            ("1 / 0", CalculationError),
            ("(0.1 + (1 / 3))!", CalculationError),
            ("5+-4!", CalculationError),
            ("(-1)^0.5", CalculationError),
            ("0^-1", CalculationError),
            ("(1/9)#", CalculationError),
            ("(12^0.345)#", CalculationError),
            ("8^-2#", CalculationError)
        ]
    )
    def test_calculate_raises(self, expression: str, expected_exception: type[Exception]):
        with pytest.raises(expected_exception):
            test_calculator.calculate(expression)