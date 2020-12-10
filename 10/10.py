import argparse
from functools import reduce


def main():
    adaptor_joltages = parse_args()

    # Part 1
    adaptor_chain_rating = get_adaptor_chain_rating(adaptor_joltages)
    print(f"Adaptor chain rating: {adaptor_chain_rating}")

    # Part 2
    num_valid_joltage_chains = count_valid_adaptor_chains(adaptor_joltages)
    # NOTE: None of the examples or input seem to include a jolt difference of 2
    print(f"Number of valid chains: {num_valid_joltage_chains}")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file")
    args = parser.parse_args()
    adaptor_joltages = [int(l) for l in open(args.input_file)]
    return [0] + adaptor_joltages + [max(adaptor_joltages) + 3]


def make_adaptor_chain(joltages):
    return sorted(joltages)


def get_adaptor_chain_rating(joltages):
    joltage_diffs = get_adaptor_chain_diffs(make_adaptor_chain(joltages))
    return sum(1 for j in joltage_diffs if j == 1) * sum(1 for j in joltage_diffs if j == 3)


def get_adaptor_chain_diffs(joltages):
    adaptor_chain_diffs = []
    last_joltage = joltages[0]
    for joltage in joltages[1:]:
        joltage_diff = joltage - last_joltage
        if not 1 <= joltage_diff <= 3:
            raise Exception("Joltage diff not between 1 and 3")
        adaptor_chain_diffs.append(joltage_diff)
        last_joltage = joltage
    return adaptor_chain_diffs


def count_valid_adaptor_chains(joltages):
    # 3 is always mandatory
    # 2 is mandatory if not preceded or followed by a 1
    # 1 may or may not be mandatory
    joltage_diffs = get_adaptor_chain_diffs(make_adaptor_chain(joltages))
    split_joltage_diffs = []
    split_start_index = 0
    for i in range(len(joltage_diffs)):
        diff = joltage_diffs[i]
        prev_diff = joltage_diffs[i - 1] if i > 0 else 1
        next_diff = joltage_diffs[i + 1] if i < len(joltage_diffs) - 1 else 1
        if diff == 3 or (prev_diff != 1 and diff == 2 and next_diff != 1):
            split_joltage_diffs.append(joltage_diffs[split_start_index:i])
            split_start_index = i + 1
    split_joltage_diffs.append(joltage_diffs[split_start_index:])
    return reduce(lambda val, l: count_valid_diff_chains_brute_force(l) * val, split_joltage_diffs, 1)


def count_valid_diff_chains_brute_force(diffs):
    if len(diffs) < 2:
        return 1
    new_diff_if_head_skipped = diffs[0] + diffs[1]
    if new_diff_if_head_skipped > 3:
        return count_valid_diff_chains_brute_force(diffs[1:])
    return count_valid_diff_chains_brute_force(diffs[1:]) + count_valid_diff_chains_brute_force([new_diff_if_head_skipped] + diffs[2:])


if __name__ == "__main__":
    main()
