import argparse


def main():
    port_data, preamble_length = parse_args()

    # Part 1
    first_vulnerable_value = find_vulnerable_value(port_data, preamble_length)
    print(f"Value of first vulnerable number: {first_vulnerable_value}")

    # Part 2
    vulnerable_range = find_range_for_sum(port_data, first_vulnerable_value)
    weakness_value = min(vulnerable_range) + max(vulnerable_range)
    print(f"Weakness value: {weakness_value}")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file")
    parser.add_argument("preamble_length")
    args = parser.parse_args()
    port_data = [int(l) for l in open(args.input_file)]
    preamble_length = int(args.preamble_length)
    return port_data, preamble_length


def find_vulnerable_value(port_data, preamble_length):
    for i in range(preamble_length, len(port_data)):
        if port_data[i] not in get_possible_pair_sums(port_data[i - preamble_length:i]):
            return port_data[i]
    return None


def get_possible_pair_sums(l):
    return {l[x] + l[y] for x in range(len(l)) for y in range(x + 1, len(l))}


def find_range_for_sum(port_data, target_sum):
    for first_index in range(len(port_data)):
        current_total = 0
        for i in range(first_index + 1, len(port_data)):
            current_total = current_total + port_data[i]
            if current_total == target_sum:
                return port_data[first_index:i + 1]
            elif current_total > target_sum:
                break
    return None


if __name__ == "__main__":
    main()
