from typing import List, Any

import pytest

from src.calculatorLogic import calc_errors
from tests.constants_for_tests import ops, postfix_solver, sub, minus, sign


class TestPostfixSolver:

    @pytest.mark.parametrize(
        "expression, correct_answer",
        [
            ([1.0, 2.0, ops["+"]], 3.0),
            ([4.0, 7.0, 1.0, ops["*"], ops["+"]], 11.0),
            ([8.0, 3.0, 5.0, ops["*"], ops["+"]], 23.0),
            ([12.0, 9.0, sub, 4.0, ops["+"]], 7.0),
            ([6.0, 2.0, ops["*"], 10.0, ops["+"]], 22.0),
            ([2.0, 7.0, ops["+"], 3.0, sub], 6.0),
            ([4.0, 3.0, ops["^"], 6.0, ops["*"]], 384.0),
            ([2.0, 9.0, 2.0, ops["^"], ops["*"]], 162.0),
            ([15.0, 4.0, ops["%"]], 3.0),
            ([9.0, 3.0, ops["$"]], 9.0),
            ([1.0, 8.0, ops["&"]], 1.0),
            ([6.0, 4.0, ops["@"]], 5.0),
            ([7.0, ops["~"]], -7.0),
            ([5.0, ops["!"]], 120.0),
            ([3.0, minus], -3.0),
            ([5.0, 4.0, ops["+"], ops["("]], 9.0),
            ([1.2, 7.3, ops["+"], ops["("], 0.8, ops["*"]], 6.8),
            ([3.0, 8.0, 2.0, ops["*"], ops["("], ops["+"], ops["("]], 19.0),
            ([7.0, 1.0, ops["+"], ops["("], 9.0, 2.0, sub, ops["("], ops["*"]], 56.0),
            ([4.0, 5.0, ops["+"], ops["("], 2.0, ops["*"], ops["("]], 18.0),
            ([2.7, 6.0, ops["+"], ops["("], minus], -8.7),
            ([3.0, 4.0, sign, ops["+"]], -1.0),
            ([9.4, minus, 2.21, ops["+"]], -7.19),
            ([5.0, minus, ops["("], minus], 5.0),
            ([1.0, minus, minus], 1.0),
            ([8.0, ops["#"]], 8.0),
            ([4.0, 3.0, ops["#"], ops["+"]], 7.0),
            ([6.0, ops["#"], minus], -6.0),
            ([11.0, 2.0, ops["~"], ops["+"]], 9.0),
            ([13.0, ops["!"], ops["#"]], 27.0),
            ([2.0, 6.0, ops["+"], ops["("], ops["!"]], 40320.0),
            ([5.8, 3.0, ops["!"], ops["+"], ops["("]], 11.8),
            ([11.0, 6.0, ops["$"], 2.0, ops["&"], 9.0, ops["@"]], 5.5),
            ([12.0, 8.0, ops["$"], ops["("], 3.0, 7.0, ops["@"], ops["("], ops["&"]], 5.0)
        ]
    )
    def test_solve(self, expression: List[Any], correct_answer: float):
        assert postfix_solver.solve(expression) == correct_answer

    @pytest.mark.parametrize(
        "expression, expected_exception",
        [
            ([1.3, 346.264], calc_errors.SolvingError),
            ([1.0, ops["+"]], calc_errors.SolvingError),
            ([ops["*"], 2.0], calc_errors.SolvingError),
            ([ops["!"], 5.0], calc_errors.SolvingError),
            ([5.0, ops["~"], 4.0], calc_errors.SolvingError),
            ([1.0, 2.0, ops["+"], 3.0, 4.0], calc_errors.SolvingError),
            ([1.0, 0.0, ops["/"]], calc_errors.CalculationError),
            ([-1.0, 0.5, ops["^"]], calc_errors.CalculationError),
            ([0.0, -1.0, ops["^"]], calc_errors.CalculationError),
            ([0.0, 0.0, ops["^"]], calc_errors.CalculationError),
            ([5.0, 0.0, ops["%"]], calc_errors.CalculationError),
            ([-3.0, ops["!"]], calc_errors.CalculationError),
            ([3.2, ops["!"]], calc_errors.CalculationError),
            ([-5.0, ops["#"]], calc_errors.CalculationError),
            ([ops["("]], calc_errors.SolvingError),
            ([ops["+"], 1.0, 2.0], calc_errors.SolvingError),
            ([1.0, 2.0, "a"], calc_errors.SolvingError),
            ([1000000.0, ops["!"], ops["#"]], calc_errors.CalculationError),
            ([1.0, 3.0, ops['/'], ops['('], ops["#"]], calc_errors.CalculationError),
            ([1000.0, 10000.0, ops['^']], calc_errors.CalculationError),
            ([-1000.0, 10000.0, ops['^']], calc_errors.CalculationError),
            ([234.534, 3.7, ops['~']], calc_errors.SolvingError)
        ]
    )
    def test_solve_raises(self, expression: List[Any], expected_exception):
        with pytest.raises(expected_exception):
            postfix_solver.solve(expression)