import argparse


EXPENSE_VERIFICATION_NUMBER = 2020


# Note: This solution will fail if one of the inputs is exactly half / one third of the verification number
def main():
    expense_report = parse_input()

    # Part One
    verify_expense_report_pair(expense_report)

    # Part Two
    verify_expense_report_triple(expense_report)


def parse_input():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file")
    args = parser.parse_args()
    expense_report = [int(x) for x in open(args.input_file)]
    return expense_report


def verify_expense_report_pair(expense_report):
    x, y = find_pair_with_total(expense_report, expense_report, EXPENSE_VERIFICATION_NUMBER)
    if x is None or y is None:
        print(f"Could not find pair that adds to {EXPENSE_VERIFICATION_NUMBER}")
        return None
    else:
        print(f"{x} + {y} = {EXPENSE_VERIFICATION_NUMBER}")
        verification_code = x * y
        print(f"{x} * {y} = {verification_code}")
        return verification_code


def find_pair_with_total(lhs, rhs, target):
    for x in lhs:
        for y in rhs:
            if x + y == target:
                return x, y
    return None, None


def verify_expense_report_triple(expense_report):
    x, y, z = find_triple_with_total(expense_report, expense_report, expense_report, EXPENSE_VERIFICATION_NUMBER)
    if x is None or y is None or z is None:
        print(f"Could not find triple that adds to {EXPENSE_VERIFICATION_NUMBER}")
        return None
    else:
        print(f"{x} + {y} + {z} = {EXPENSE_VERIFICATION_NUMBER}")
        verification_code = x * y * z
        print(f"{x} * {y} * {z} = {verification_code}")
        return verification_code


def find_triple_with_total(list_a, list_b, list_c, target):
    for x in list_a:
        for y in list_b:
            for z in list_c:
                if x + y + z == target:
                    return x, y, z
    return None, None, None


if __name__ == "__main__":
    main()
