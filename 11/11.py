import argparse


EMPTY_SEAT = "L"
OCCUPIED_SEAT = "#"
FLOOR = "."
DIRECTIONS = {(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)}


def main():
    seat_map = parse_args()

    # Part 1
    final_occupied_seat_count = count_occupied_seats(get_last_seat_map_iteration(seat_map))
    print(f"Number of occupied seats at final iteration: {final_occupied_seat_count}")

    # Part 2
    updated_final_occupied_seat_count_los = count_occupied_seats(get_last_seat_map_iteration(seat_map, count_visible_occupied_seats, 5))
    print(f"Number of occupied seats based on updated rules: {updated_final_occupied_seat_count_los}")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file")
    args = parser.parse_args()
    seat_map = [l.strip() for l in open(args.input_file)]
    return seat_map


def count_adjacent_occupied_seats(seat_map, x, y):
    counted_seats = 0
    for neighbour_y in range(max(0, y - 1), min(y + 2, len(seat_map))):
        for neighbour_x in range(max(0, x - 1), min(x + 2, len(seat_map[neighbour_y]))):
            if (neighbour_x != x or neighbour_y != y) and seat_map[neighbour_y][neighbour_x] == OCCUPIED_SEAT:
                counted_seats = counted_seats + 1
    return counted_seats


def count_visible_occupied_seats(seat_map, x, y):
    counted_seats = 0
    for dx, dy in DIRECTIONS:
        visible_x = x + dx
        visible_y = y + dy
        while 0 <= visible_y < len(seat_map) and 0 <= visible_x < len(seat_map[visible_y]):
            if seat_map[visible_y][visible_x] == OCCUPIED_SEAT:
                counted_seats = counted_seats + 1
                break
            if seat_map[visible_y][visible_x] == EMPTY_SEAT:
                break
            visible_x = visible_x + dx
            visible_y = visible_y + dy
    return counted_seats


def next_seat_map_iteration(seat_map, count_occupied_seats_func, occupied_seats_count_threshold):
    new_seat_map = []
    for y in range(len(seat_map)):
        new_row = []
        for x in range(len(seat_map[y])):
            old_seat_value = seat_map[y][x]
            new_seat_value = old_seat_value
            num_occupied_neighbours = count_occupied_seats_func(seat_map, x, y)
            if old_seat_value == EMPTY_SEAT and num_occupied_neighbours == 0:
                new_seat_value = OCCUPIED_SEAT
            if old_seat_value == OCCUPIED_SEAT and num_occupied_neighbours >= occupied_seats_count_threshold:
                new_seat_value = EMPTY_SEAT
            new_row.append(new_seat_value)
        new_seat_map.append(new_row)
    return new_seat_map


def get_last_seat_map_iteration(seat_map, count_occupied_seats_func=count_adjacent_occupied_seats, occupied_seats_count_threshold=4):
    next_seat_map = seat_map
    last_seat_map = []
    while not check_seat_maps_equal(last_seat_map, next_seat_map):
        last_seat_map = next_seat_map
        next_seat_map = next_seat_map_iteration(next_seat_map, count_occupied_seats_func, occupied_seats_count_threshold)
    return next_seat_map


def check_seat_maps_equal(lhs, rhs):
    if len(lhs) != len(rhs):
        return False
    for y in range(len(lhs)):
        if len(lhs[y]) != len(rhs[y]):
            return False
        for x in range(len(lhs[y])):
            if lhs[y][x] != rhs[y][x]:
                return False
    return True


def count_occupied_seats(seat_map):
    return sum(sum(1 for s in row if s == OCCUPIED_SEAT) for row in seat_map)


def print_seat_map(seat_map):
    print("\n".join("".join(s for s in row) for row in seat_map))


if __name__ == "__main__":
    main()
