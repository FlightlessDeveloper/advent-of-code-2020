import argparse


def main():
    answers = parse_args()

    # Part One
    answers_counts_total = sum(len(x) for x in answers)
    print(f"Total: {answers_counts_total}")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file")
    args = parser.parse_args()
    return parse_answers(s.strip() for s in open(args.input_file))


def parse_answers(lines):
    current_answer_set = set()
    answer_sets = []
    for l in lines:
        if len(l) >= 1:
            for c in l:
                current_answer_set.add(c)
        else:
            answer_sets.append(current_answer_set)
            current_answer_set = set()
    answer_sets.append(current_answer_set)
    return answer_sets


if __name__ == "__main__":
    main()
