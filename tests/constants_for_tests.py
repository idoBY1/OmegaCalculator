from src.calculatorLogic import defined_operators, expression_formatter, operator, solver

def_ops = defined_operators.OmegaDefinedOperators()
postfix_formatter = expression_formatter.InfixToPostfixFormatter(def_ops)
postfix_solver = solver.PostfixSolver()
ops = def_ops.get_operators_dict()

# get the different '-' types
sub = def_ops._get_overloaded_by_class('-', operator.Subtraction)
minus = def_ops._get_overloaded_by_class('-', operator.Minus)
sign = def_ops._get_overloaded_by_class('-', operator.NegativeSign)