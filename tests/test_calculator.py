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
            ("-5!#", -3),
            ("-(10# + 20#)", -3),
            ("((10.5 + 2.5) * 3 - (40 / 5)) ^ 2 + 10", 971),
            ("((100 $ 50 & 75 @ 60) % 10) * 2", 15),
            ("(100$200&150)@((10&5)$20)", 85),
            ("((1 + (2 * (3 + (4 * (5 - (6 / 2)))))) ^ 2 ) #", 16),
            ("(1.1*1.1*1.1*1.1*1.1*1.1*1.1) + (2.1*2.1*2.1*2.1*2.1*2.1)", 87.7148381),
            ("12 * (3 - 1) + 7 / 2 ^ 2  + 11 - 22 * 3 + 4 / 5  ^ 2", -29.09),
            ("~-7 + (3 * 4) / 2 - 10 + 15 - 2 + 1 * 2 ^ 3 / 2", 20),
            ("((10+3)/2*2-(4*1)  + 10) # + 12 / 5 * 6 - 11 + 11", 24.4),
            ("2 ^ 2 + 5 % 2 * (4 + 3) - 9 + 11 - 2 * 3 + 4 / 5 ^ 2", 7.16),
            ("((1 + 2 + 3 ) # + (4 + 5 + 6) #) * 2 + 10 / 2 * 3 - 4 ^ 2 + 1", 24),
            ("10 - (2 * 4) + (15 / 3) & 10 - 2 / 5 * 6  + 11 - 2", 13.6),
            ("23 $ 12 & 15 @ 10 + 2 % 2 + 12 - 4 / 5 * 6 + 10 ", 29.7),
            ("(11 $ 22 & 33 ) @ (44  - 55 / 2 )  + 100 - 2 * 4 + 12 / 6 - 1", 112.25),
            ("((100 + 200 - 100 ) $ ( 50 + 100)) @ 75  + 1 - 2 * 3 + 4/8 - 111", 22),
            ("1 * 2 + 3 ^ 2 - 14 / 2 + 6 % 7 + (12 * 2 / 3) ^ 2", 74),
            ("((2*3)+ (4*5) - 7 % 2  )  $ 8 & 10 @ 11  + 12 - 3 / 4 + 1 * 2", 23.75),
            ("123 * (2 - 1) + 1 / 2 ^ 3  - 4 % 5 + 6 - 13", 112.125),
            ("1 * 2 * 3 / 4 + 5 ^ 2 - 6 + 7 % 8 + 123 - 67 / ~5 * 6 - 11", 219.9),
            ("~-12 + 2 * 4 - 6 / 8 + 10 % 2 + 111 - 22 / 88 * 44 - 86", 33.25),
            ("123 $ 234 & 100 @ 120 + 100 - 200 * 300 + 240 / 600 + 100 - 1 / 2 * 3", -59691.1),
            ("12 - 12 + 12 * 12 / 12 ^ 2  + 12 % 12 + 111 - 10 / 2 * 3 - 1 ", 96),
            ("-(12 + 4) + 7 * 10 / 1 - 4 % 1 + 12 - 12 * 3 / 4 + 1", 58),
            ("~-7 + (3 * 4) / 2 - 10 + 15 - 2 + 1 * 2 ^ 3 / 2 + 11 - 2 * 3 + 4", 29),
            ("15 +6 +9& 3 - 5^3 + 2*6 % 2 + (7*3- 1)", -81)
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
            ("5+ -(6*2)!", CalculationError),
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
    def test_calculate_raises(self, expression: str, expected_exception):
        with pytest.raises(expected_exception):
            test_calculator.calculate(expression)