import argparse


def main():
    adaptor_joltages = parse_args()

    # Part 1
    adaptor_chain = make_adaptor_chain(adaptor_joltages + [max(adaptor_joltages) + 3])
    adaptor_chain_rating = get_adaptor_chain_rating(adaptor_chain)
    print(f"Adaptor chain rating: {adaptor_chain_rating}")

    # Part 2
    pass


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file")
    args = parser.parse_args()
    adaptor_joltages = [int(l) for l in open(args.input_file)]
    return adaptor_joltages


def make_adaptor_chain(joltages):
    return sorted(joltages)


def get_adaptor_chain_rating(joltages):
    last_joltage = 0
    joltage_diff_counts = {1:0, 2:0, 3:0}
    for joltage in joltages:
        joltage_diff = joltage - last_joltage
        if not 1 <= joltage_diff <= 3:
            raise Exception("Joltage diff not between 1 and 3")
        joltage_diff_counts[joltage_diff] = joltage_diff_counts[joltage_diff] + 1
        last_joltage = joltage
    return joltage_diff_counts[1] * joltage_diff_counts[3]


if __name__ == "__main__":
    main()
