from src import calculator
from src.calculatorLogic import defined_operators, expression_formatter, operator, solver

test_calculator = calculator.Calculator()

def_ops = test_calculator.defined_operators
postfix_formatter = test_calculator.formatter
postfix_solver = test_calculator.solver
ops = def_ops.get_operators_dict()

# get the different '-' types
sub = def_ops._get_overloaded_by_class('-', operator.Subtraction)
minus = def_ops._get_overloaded_by_class('-', operator.Minus)
sign = def_ops._get_overloaded_by_class('-', operator.NegativeSign)