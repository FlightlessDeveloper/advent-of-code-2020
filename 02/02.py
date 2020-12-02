import argparse
from collections import namedtuple

PasswordLine = namedtuple("password_line", ["left_int", "right_int", "char", "password"])


def main():
    password_lines = parse_input()

    valid_password_lines_part_one = list(filter(verify_password_line_part_one, password_lines))
    print(f"Part one valid password lines: {len(valid_password_lines_part_one)}")

    valid_password_lines_part_two = list(filter(verify_password_line_part_two, password_lines))
    print(f"Part two valid password lines: {len(valid_password_lines_part_two)}")


def parse_input():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file")
    args = parser.parse_args()
    expense_report = [parse_password_line(x) for x in open(args.input_file)]
    return expense_report


def parse_password_line(s):
    ints_string, char_string, password = s.split(" ")
    char = char_string[0]
    left_int_string, right_int_string = ints_string.split("-")
    left_int = int(left_int_string)
    right_int = int(right_int_string)
    return PasswordLine(left_int, right_int, char, password)


def verify_password_line_part_one(l):
    return l.left_int <= sum(1 if c == l.char else 0 for c in l.password) <= l.right_int


def verify_password_line_part_two(l):
    char_is_on_left = l.password[l.left_int - 1] == l.char
    char_is_on_right = l.password[l.right_int - 1] == l.char
    return (char_is_on_left and not char_is_on_right) or (char_is_on_right and not char_is_on_left)


if __name__ == "__main__":
    main()
