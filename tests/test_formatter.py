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
            (["4", "+", "7", "*", "1"], [4, 7, 1, ops["*"], ops["+"]]),
            (["8", "+", "3", "*", "5"], [8, 3, 5, ops["*"], ops["+"]]),
            (["12", "-", "9", "+", "4"], [12, 9, sub, 4, ops["+"]]),
            (["6", "*", "2", "+", "10"], [6, 2, ops["*"], 10, ops["+"]]),
            (["2", "+", "7", "-", "3"], [2, 7, ops["+"], 3, sub]),
            (["4", "^", "1", "*", "6"], [4, 1, ops["^"], 6, ops["*"]]),
            (["2", "*", "9", "^", "1"], [2, 9, 1, ops["^"], ops["*"]]),
            (["15", "%", "4"], [15, 4, ops["%"]]),
            (["9", "$", "3"], [9, 3, ops["$"]]),
            (["1", "&", "8"], [1, 8, ops["&"]]),
            (["6", "@", "4"], [6, 4, ops["@"]]),
            (["~", "7"], [7, ops["~"]]),
            (["5", "!"], [5, ops["!"]]),
            (["-", "3"], [3, minus]),
            (["(", "5", "+", "4", ")"], [5, 4, ops["+"], ops["("]]),
            (["(", "1.2", "+", "7.3", ")", "*", "0.8"], [1.2, 7.3, ops["+"], ops["("], 0.8, ops["*"]]),
            (["(", "3", "+", "(", "8", "*", "2", ")", ")"], [3, 8, 2, ops["*"], ops["("], ops["+"], ops["("]]),
            (["(", "7", "+", "1", ")", "*", "(", "9", "-", "2", ")"],
             [7, 1, ops["+"], ops["("], 9, 2, sub, ops["("], ops["*"]]),
            (["(", "(", "4", "+", "5", ")", "*", "2", ")"], [4, 5, ops["+"], ops["("], 2, ops["*"], ops["("]]),
            (["-", "(", "2.7", "+", "6", ")"], [2.7, 6, ops["+"], ops["("], minus]),
            (["3", "+", "-", "4"], [3, 4, sign, ops["+"]]),
            (["-", "9.4", "+", "2.21"], [9.4, minus, 2.21, ops["+"]]),
            (["-", "(", "-", "5", ")"], [5, minus, ops["("], minus]),
            (["-", "-", "1"], [1, minus, minus]),
            (["8", "#"], [8, ops["#"]]),
            (["4", "+", "3", "#"], [4, 3, ops["#"], ops["+"]]),
            (["-", "6", "#"], [6, ops["#"], minus]),
            (["11", "+", "~", "2"], [11, 2, ops["~"], ops["+"]]),
            (["13", "!", "#"], [13, ops["!"], ops["#"]]),
            (["(", "2", "+", "6", ")", "!", ], [2, 6, ops["+"], ops["("], ops["!"]]),
            (["(", "5.8", "+", "3", "!", ")", ], [5.8, 3, ops["!"], ops["+"], ops["("]]),
            (["11", "$", "6", "&", "2", "@", "9"], [11, 6, ops["$"], 2, ops["&"], 9, ops["@"]]),
            (["(", "12", "$", "8", ")", "&", "(", "3", "@", "7", ")"],
             [12, 8, ops["$"], ops["("], 3, 7, ops["@"], ops["("], ops["&"]])
        ]
    )
    def test_format_expression(self, expression: List[str], correct_expression: List[Any]):
        assert TestPostfixFormatter.postfix_formatter.format_expression(expression) == correct_expression