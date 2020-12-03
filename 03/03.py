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


def get_path_for_slope(tree_map, slope, start_point=MapVector(0, 0)):
    x = start_point.x
    y = start_point.y
    slope_path = []
    while y < len(tree_map):
        x = x % len(tree_map[y])
        slope_path.append(tree_map[y][x])
        y = y + slope.y
        x = x + slope.x
    return slope_path


def mapVectorToString(v):
    return f"({v.x}, {v.y})"


if __name__ == "__main__":
    main()
