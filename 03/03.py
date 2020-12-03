import argparse
from collections import namedtuple
from functools import reduce

MapVector = namedtuple("MapVector", ["x", "y"])
SPACE = "."
TREE = "#"


def main():
    tree_map = parse_input()
    tree_counts = []
    for s in [MapVector(1, 1), MapVector(3, 1), MapVector(5, 1), MapVector(7, 1), MapVector(1, 2)]:
        tree_count = get_path_for_slope(tree_map, s).count(TREE)
        print(f"{mapVectorToString(s)} -> {tree_count} trees")
        tree_counts.append(tree_count)
    verification_code = reduce(lambda x, y: x * y, tree_counts)
    print(f"Verification Code: {verification_code}")


def parse_input():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file")
    args = parser.parse_args()
    tree_map = [list(filter(lambda c: c in {SPACE, TREE}, x)) for x in open(args.input_file)]
    return tree_map


def get_path_for_slope(tree_map, slope, x_pos=0):
    if len(tree_map) < 1:
        return []
    else:
        first_row = tree_map[0]
        x_pos_bounded = x_pos % len(first_row)
        # Note: This still works if slope.y is bigger than len(tree_map)
        return [first_row[x_pos_bounded]] + get_path_for_slope(tree_map[slope.y:], slope, x_pos + slope.x)


def mapVectorToString(v):
    return f"({v.x}, {v.y})"


if __name__ == "__main__":
    main()
