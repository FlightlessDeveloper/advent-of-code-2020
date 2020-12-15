import argparse


PART_ONE_TURN_COUNT = 2020
PART_TWO_TURN_COUNT = 30000000


def main():
    starting_numbers = parse_args()

    memory_game = play_memory_game(starting_numbers, PART_TWO_TURN_COUNT)
    numbers_spoken = [next(memory_game) for _ in range(PART_TWO_TURN_COUNT)]

    print(f"2020th number: {numbers_spoken[PART_ONE_TURN_COUNT - 1]}")
    print(f"30000000th number: {numbers_spoken[PART_TWO_TURN_COUNT - 1]}")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file")
    args = parser.parse_args()
    starting_numbers = [int(x) for x in next(open(args.input_file)).strip().split(",")]
    return starting_numbers


def play_memory_game(starting_numbers, num_total_turns=None):
    turn_number = 1
    last_time_spoken = {}
    next_number = starting_numbers[0]
    while num_total_turns is None or turn_number <= num_total_turns:
        yield next_number
        previous_number = next_number
        if turn_number < len(starting_numbers):
            next_number = starting_numbers[turn_number]
        else:
            next_number = turn_number - last_time_spoken[next_number] if next_number in last_time_spoken else 0
        last_time_spoken[previous_number] = turn_number
        turn_number += 1
        if num_total_turns is not None and turn_number % (num_total_turns / 10) == 0:
            print(f"{100 * turn_number // num_total_turns}% complete", end='\n' if turn_number == num_total_turns else '\r')


if __name__ == "__main__":
    main()
