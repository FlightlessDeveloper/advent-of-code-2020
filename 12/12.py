import argparse
from collections import namedtuple


ShipInstruction = namedtuple("ShipInstruction", ["action", "value"])
ShipState = namedtuple("ShipState", ["x", "y", "direction"])


def main():
    directions = parse_args()

    # Part 1
    final_distance = measure_distance(move_ship(directions))
    print(f"Final distance: {final_distance}")

    # Part 2
    final_distance_waypoint = measure_distance(move_ship_waypoint(directions))
    print(f"Final distance: {final_distance_waypoint}")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file")
    args = parser.parse_args()
    directions = [parse_instruction(l.strip()) for l in open(args.input_file)]
    return directions


def parse_instruction(s):
    return ShipInstruction(s[0], int(s[1:]))


def move_ship(instructions, initial_state=ShipState(0, 0, 90)):
    ship_state = initial_state
    for i in instructions:
        if i.action == "N":
            ship_state = ShipState(ship_state.x, ship_state.y - i.value, ship_state.direction)
        elif i.action == "S":
            ship_state = ShipState(ship_state.x, ship_state.y + i.value, ship_state.direction)
        elif i.action == "E":
            ship_state = ShipState(ship_state.x + i.value, ship_state.y, ship_state.direction)
        elif i.action == "W":
            ship_state = ShipState(ship_state.x - i.value, ship_state.y, ship_state.direction)
        elif i.action == "L":
            ship_state = ShipState(ship_state.x, ship_state.y, (ship_state.direction - i.value) % 360)
        elif i.action == "R":
            ship_state = ShipState(ship_state.x, ship_state.y, (ship_state.direction + i.value) % 360)
        elif i.action == "F":
            if ship_state.direction == 0:
                ship_state = ShipState(ship_state.x, ship_state.y - i.value, ship_state.direction)
            elif ship_state.direction == 90:
                ship_state = ShipState(ship_state.x + i.value, ship_state.y, ship_state.direction)
            elif ship_state.direction == 180:
                ship_state = ShipState(ship_state.x, ship_state.y + i.value, ship_state.direction)
            elif ship_state.direction == 270:
                ship_state = ShipState(ship_state.x - i.value, ship_state.y, ship_state.direction)
            else:
                raise Exception(f"Invalid direction: {ship_state.direction}")
        else:
            raise Exception(f"Invalid action: {i.action}")
    return ship_state


def move_ship_waypoint(instructions, initial_state=ShipState(0, 0, 90), initial_waypoint=ShipState(10, -1, 0)):
    ship_state = initial_state
    waypoint = initial_waypoint
    for i in instructions:
        if i.action == "N":
            waypoint = ShipState(waypoint.x, waypoint.y - i.value, waypoint.direction)
        elif i.action == "S":
            waypoint = ShipState(waypoint.x, waypoint.y + i.value, waypoint.direction)
        elif i.action == "E":
            waypoint = ShipState(waypoint.x + i.value, waypoint.y, waypoint.direction)
        elif i.action == "W":
            waypoint = ShipState(waypoint.x - i.value, waypoint.y, waypoint.direction)
        elif i.action == "L":
            if i.value == 0:
                continue
            elif i.value == 90:
                waypoint = ShipState(waypoint.y, -waypoint.x, waypoint.direction)
            elif i.value == 180:
                waypoint = ShipState(-waypoint.x, -waypoint.y, waypoint.direction)
            elif i.value == 270:
                waypoint = ShipState(-waypoint.y, waypoint.x, waypoint.direction)
            else:
                raise Exception(f"Invalid direction: {ship_state.direction}")
        elif i.action == "R":
            if i.value == 0:
                continue
            elif i.value == 90:
                waypoint = ShipState(-waypoint.y, waypoint.x, waypoint.direction)
            elif i.value == 180:
                waypoint = ShipState(-waypoint.x, -waypoint.y, waypoint.direction)
            elif i.value == 270:
                waypoint = ShipState(waypoint.y, -waypoint.x, waypoint.direction)
            else:
                raise Exception(f"Invalid direction: {ship_state.direction}")
        elif i.action == "F":
            ship_state = ShipState(ship_state.x + i.value * waypoint.x, ship_state.y + i.value * waypoint.y, ship_state.direction)
        else:
            raise Exception(f"Invalid action: {i.action}")
    return ship_state


def measure_distance(lhs, rhs=ShipState(0, 0, 90)):
    return abs(lhs.x - rhs.x) + abs(lhs.y - rhs.y)


if __name__ == "__main__":
    main()
