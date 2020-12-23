import argparse


def main():
    cups = parse_args()

    # Part 1
    final_labels = get_cup_labels(play_cup_game(cups, 100))
    print(f"Cup game labels after 100 turns: {final_labels}")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file")
    args = parser.parse_args()
    cups = [int(x) for x in open(args.input_file).read().strip()]
    return cups


def play_cup_game(initial_state, num_turns):
    cups = list(initial_state)
    for t in range(num_turns):
        picked_up_cups = cups[1:4]
        remaining_cups = cups[4:]
        destination_cup = cups[0] - 1
        while destination_cup not in remaining_cups:
            destination_cup = len(cups) if destination_cup < 1 else destination_cup - 1
        destination_index = remaining_cups.index(destination_cup)
        cups = remaining_cups[:destination_index + 1] + picked_up_cups + remaining_cups[destination_index + 1:] + [cups[0]]
    return cups


def get_cup_labels(l):
    one_index = l.index(1)
    return "".join(str(x) for x in l[one_index + 1:] + l[:one_index])


if __name__ == "__main__":
    main()
