import argparse


def main():
    start_time, bus_ids = parse_args()

    # Part 1
    arrival_time, next_bus_id = find_next_bus(start_time, bus_ids)
    wait_time = arrival_time - start_time
    print(f"Waiting {wait_time} minutes for bus #{next_bus_id} ({wait_time * next_bus_id})")

    # Part 2
    contest_timestamp = find_contest_timestamp(bus_ids)
    print(f"Contest winning timestamp: {contest_timestamp}")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file")
    args = parser.parse_args()
    start_time_string, bus_ids_string = open(args.input_file)
    start_time = int(start_time_string.strip())
    bus_ids = [int(x.strip()) if x.strip().isnumeric() else None for x in bus_ids_string.split(",")]
    return start_time, bus_ids


def find_next_bus(start_time, bus_ids, max_time_threshold=999999999):
    for current_time in range(start_time, max_time_threshold):
        for id in bus_ids:
            if id is not None and current_time % id == 0:
                return current_time, id
    raise Exception(f"Max time of {max_time_threshold} elapsed (find_next_bus)")


def find_contest_timestamp(bus_ids):
    ids_with_offsets = sorted(list(filter(lambda x: x[0] is not None, (map(lambda x: (x[1], x[0]), enumerate(bus_ids))))))
    print(ids_with_offsets)
    raise Exception("Use WolframAlpha for this because I couldn't figure out a libary to solve the simultaneous equations")


if __name__ == "__main__":
    main()
