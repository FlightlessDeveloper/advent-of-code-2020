import argparse
from functools import reduce

EXPENSE_VERIFICATION_NUMBER = 2020


def main():
    expense_report = parse_input()
    print(f"Part 1:")
    verify_expense_report(expense_report, 2)
    print(f"\nPart 2:")
    verify_expense_report(expense_report, 3)


def parse_input():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file")
    args = parser.parse_args()
    expense_report = [int(x) for x in open(args.input_file)]
    return expense_report


def verify_expense_report(expense_report, num_entries):
    for t in get_unique_tuples(expense_report, num_entries):
        if sum(t) == EXPENSE_VERIFICATION_NUMBER:
            verification_code = reduce((lambda x, y: x * y), t)
            print(f"{' + '.join(str(x) for x in t)} = {EXPENSE_VERIFICATION_NUMBER}")
            print(f"{' * '.join(str(x) for x in t)} = {verification_code}")
            return verification_code
    print(f"Could not find a solution for {num_entries} entries.")
    return None


def get_unique_tuples(l, tuple_length):
    ls = set(l)
    unique_tuples = [(x,) for x in ls]
    for i in range(tuple_length - 1):
        unique_tuples = [t + (x,) for t in unique_tuples for x in ls if x not in t]
    return unique_tuples


if __name__ == "__main__":
    main()
