import argparse


def main():
    instruction_lists = parse_args()

    # Part 1
    black_tiles = turn_over_tiles(instruction_lists)
    print(f"Number of black tiles: {len(black_tiles)}")

    # Part 2
    eventual_black_tiles = run_daily_changes(black_tiles, 100)
    print(f"Number of black tiles after 100 days: {len(eventual_black_tiles)}")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file")
    args = parser.parse_args()
    instruction_lists = [parse_instruction_list(l.strip()) for l in open(args.input_file)]
    return instruction_lists


def parse_instruction_list(l):
    instructions = []
    while len(l) > 0:
        if l.startswith("ne") or l.startswith("nw") or l.startswith("se") or l.startswith("sw"):
            instructions.append(l[:2])
            l = l[2:]
        elif l.startswith("w") or l.startswith("e"):
            instructions.append(l[:1])
            l = l[1:]
        else:
            raise Exception(f"Can't parse instruction string '{l}'")
    return instructions


def turn_over_tiles(instruction_lists):
    black_tiles = set()
    for instructions in instruction_lists:
        pos = (0, 0)
        for instruction in instructions:
            x, y = pos
            if instruction == "ne":
                pos = (x + 1, y - 1)
            elif instruction == "e":
                pos = (x + 2, y)
            elif instruction == "se":
                pos = (x + 1, y + 1)
            elif instruction == "nw":
                pos = (x - 1, y - 1)
            elif instruction == "w":
                pos = (x - 2, y)
            elif instruction == "sw":
                pos = (x - 1, y + 1)
            else:
                raise Exception(f"Instruction '{instruction}' not valid")
        if pos in black_tiles:
            black_tiles.remove(pos)
        else:
            black_tiles.add(pos)
    return black_tiles


def run_daily_changes(initial_black_tiles, num_days):
    black_tiles = set(initial_black_tiles)
    for day in range(num_days):
        new_white_tiles = set()
        new_black_tiles = set()
        volatiles = set() # Pun intended
        for pos in black_tiles:
            volatiles.add(pos)
            for n in get_neighbours(pos):
                volatiles.add(n)
        for pos in volatiles:
            num_black_neighbours = sum(1 if n in black_tiles else 0 for n in get_neighbours(pos))
            if pos in black_tiles:
                if num_black_neighbours == 0 or num_black_neighbours > 2:
                    new_white_tiles.add(pos)
            else:
                if num_black_neighbours == 2:
                    new_black_tiles.add(pos)
        for pos in new_white_tiles:
            if pos in black_tiles:
                black_tiles.remove(pos)
        for pos in new_black_tiles:
            black_tiles.add(pos)
    return black_tiles


def get_neighbours(pos):
    x, y = pos
    return {(x + 1, y - 1), (x + 2, y), (x + 1, y + 1), (x - 1, y - 1), (x - 2, y), (x - 1, y + 1)}


if __name__ == "__main__":
    main()
