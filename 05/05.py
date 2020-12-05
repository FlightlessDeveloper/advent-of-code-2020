import argparse
from collections import namedtuple


BoardingPass = namedtuple("Pass", ["row", "col", "id"])
FRONT = "F"
BACK = "B"
LEFT = "L"
RIGHT = "R"
NUM_ROWS = 128
NUM_COLS = 8


def main():
    boarding_passes = parse_args()

    # Part 1
    highest_pass_id = max(map(lambda p: p.id, boarding_passes))
    print(f"Highest pass ID: {highest_pass_id}")

    # Part 2
    my_seat = find_my_seat(boarding_passes)
    print(f"My seat: {my_seat}")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file")
    args = parser.parse_args()
    boarding_passes = [parse_boarding_pass(l.strip()) for l in open(args.input_file)]
    return boarding_passes


def parse_boarding_pass(s):
    row = count_binary(s[:7], FRONT, BACK)
    col = count_binary(s[7:], LEFT, RIGHT)
    return BoardingPass(row, col, get_boarding_pass_id(row, col))


def count_binary(l, zero_char, one_char):
    total = 0
    exp = 0
    for c in reversed(l):
        if c == one_char:
            total = total + 2 ** exp
        elif c != zero_char:
            raise Exception(f"Character {c} was not a valid char for binary counting")
        exp = exp + 1
    return total


def get_boarding_pass_id(row, col):
    return row * 8 + col


def find_my_seat(boarding_passes):
    ids = set(map(lambda p: p.id, boarding_passes))
    missing_passes = find_missing_passes(boarding_passes)
    for p in missing_passes:
        if (p.id - 1 in ids) and (p.id + 1 in ids):
            return p
    raise Exception("Couldn't find my seat!")


def find_missing_passes(passes):
    remaining_seats = {(r, c) for r in range(1, NUM_ROWS - 1) for c in range(NUM_COLS)}
    for p in passes:
        if 0 < p.row < NUM_ROWS:
            remaining_seats.remove((p.row, p.col))
    return [BoardingPass(r, c, get_boarding_pass_id(r, c)) for (r, c) in remaining_seats]


if __name__ == "__main__":
    main()
