import argparse


def main():
    answers = parse_args()

    # Part One
    print(f"Total: {sum(len(x[0]) for x in answers)}")

    # Part Two
    print(f"Total: {sum(len(x[1]) for x in answers)}")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file")
    args = parser.parse_args()
    return parse_answers(s.strip() for s in open(args.input_file))


def parse_answers(lines):
    answer_set_part_one = set()
    answer_set_part_two = set("abcdefghijklmnopqrstuvwxyz")
    answer_sets = []
    for l in lines:
        if len(l) >= 1:
            next_set = set(c for c in l)
            answer_set_part_one = answer_set_part_one.union(next_set)
            answer_set_part_two = answer_set_part_two.intersection(next_set)
        else:
            answer_sets.append((answer_set_part_one, answer_set_part_two))
            answer_set_part_one = set()
            answer_set_part_two = set("abcdefghijklmnopqrstuvwxyz")
    answer_sets.append((answer_set_part_one, answer_set_part_two))
    return answer_sets


if __name__ == "__main__":
    main()
