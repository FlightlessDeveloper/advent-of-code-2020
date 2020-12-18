import argparse
from collections import namedtuple


Expression = namedtuple("Expression", ["terms"])
Add = namedtuple("Add", [])
Multiply = namedtuple("Multiply", [])
Value = namedtuple("Value", ["value"])


def main():
    expressions = parse_args()

    # Part 1
    # print("\n".join(str(evaluate_terms(e.terms)) for e in expressions))
    sum_of_expressions = sum(evaluate_terms(e.terms) for e in expressions)
    print(f"Sum of expressions: {sum_of_expressions}")

    # Part 2
    # print("\n".join(str(evaluate_terms(e.terms, prioritise_addition=True)) for e in expressions))
    sum_of_expressions_new_rules = sum(evaluate_terms(e.terms, prioritise_addition=True) for e in expressions)
    print(f"Sum of expressions (new rules): {sum_of_expressions_new_rules}")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file")
    args = parser.parse_args()
    expressions = [Expression(parse_terms(e)) for e in open(args.input_file)]
    return expressions


def parse_terms(expression_string):
    first_open_bracket_index = expression_string.find("(")
    if first_open_bracket_index > -1:
        bracket_level = 1
        closing_bracket_index = None
        for i in range(first_open_bracket_index + 1, len(expression_string)):
            if expression_string[i] == "(":
                bracket_level += 1
            elif expression_string[i] == ")":
                bracket_level -= 1
                if bracket_level == 0:
                    closing_bracket_index = i
                    break
        if closing_bracket_index is None:
            raise Exception(f"Could not find matching close bracket in string '{expression_string}'")
        nested_expression = Expression(parse_terms(expression_string[first_open_bracket_index + 1:closing_bracket_index]))
        return parse_terms(expression_string[:first_open_bracket_index]) \
               + [nested_expression] \
               + parse_terms(expression_string[closing_bracket_index + 1:])
    else:
        return [Add() if t == "+" else Multiply() if t == "*" else Value(int(t))
                for t in expression_string.strip().split(" ") if len(t) > 0]


def evaluate_terms(terms, prioritise_addition=False):
    if len(terms) == 1:
        term = terms[0]
        if isinstance(term, Value):
            return term.value
        if isinstance(term, Expression):
            return evaluate_terms(term.terms, prioritise_addition)
        raise Exception(f"Invalid single term: {terms}")
    elif len(terms) > 2:
        operator_index = 1
        if prioritise_addition:
            for i in range(3, len(terms), 2):
                if isinstance(terms[i], Add):
                    operator_index = i
                    break
        operator = terms[operator_index]
        lhs_value = evaluate_terms([terms[operator_index - 1]], prioritise_addition)
        rhs_value = evaluate_terms([terms[operator_index + 1]], prioritise_addition)
        if isinstance(operator, Add):
            return evaluate_terms(terms[:operator_index - 1] + [Value(lhs_value + rhs_value)] + terms[operator_index + 2:], prioritise_addition)
        elif isinstance(operator, Multiply):
            return evaluate_terms(terms[:operator_index - 1] + [Value(lhs_value * rhs_value)] + terms[operator_index + 2:], prioritise_addition)
        raise Exception(f"Invalid operator: {operator}")
    raise Exception(f"Invalid terms: {terms}")


if __name__ == "__main__":
    main()
