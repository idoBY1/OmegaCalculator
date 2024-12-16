from typing import List, Any

import pytest

from src.calculatorLogic import expression_formatter, defined_operators, operator


class TestPostfixFormatter:
    def_ops = defined_operators.OmegaDefinedOperators()
    postfix_formatter = expression_formatter.InfixToPostfixFormatter(def_ops)
    ops = def_ops.get_operators_dict()

    # get the different '-' types
    sub = def_ops._get_overloaded_by_class('-', operator.Subtraction)
    minus = def_ops._get_overloaded_by_class('-', operator.Minus)
    sign = def_ops._get_overloaded_by_class('-', operator.NegativeSign)

    @pytest.mark.parametrize(
        "expression, correct_expression",
        [
            ("1+2", ["1", "+", "2"]),
            ("1 +2", ["1", "+", "2"]),
            ("1+ 2", ["1", "+", "2"]),
            ("1 + 2", ["1", "+", "2"]),
            ("123+321", ["123", "+", "321"]),
            ("1 2 3", ["123"]),
            ("12func", ["12", "func"]),
            ("12func12", ["12", "func12"]),
            ("12func 12", ["12", "func", "12"]),
            ("12fu nc 12", ["12", "fu", "nc", "12"]),
            ("!!!", ["!", "!", "!"]),
            ("*/ $ -#", ["*", "/", "$", "-", "#"]),
            ("1+2*5-21", ["1", "+", "2", "*", "5", "-", "21"]),
            ("1+ 2*  5-   2 1", ["1", "+", "2", "*", "5", "-", "21"]),
            ("()))(", ["(", ")", ")", ")", "("]),
            ("2453 + gsddfv1&&   %23", ["2453", "+", "gsddfv1", "&", "&", "%", "23"]),
        ]
    )
    def test_extract_symbols(self, expression: str, correct_expression: List[str]):
        assert TestPostfixFormatter.postfix_formatter.extract_symbols(expression) == correct_expression

    @pytest.mark.parametrize(
        "expression, correct_expression",
        [
            (["1", "+", "2"], [1, 2, ops["+"]]),
            (["43", "+", "5", "*", "8"], [43, 5, 8, ops["*"], ops["+"]])
        ]
    )
    def test_format_expression(self, expression: List[str], correct_expression: List[Any]):
        assert TestPostfixFormatter.postfix_formatter.format_expression(expression) == correct_expression