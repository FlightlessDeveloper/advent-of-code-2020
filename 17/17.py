import argparse
from collections import namedtuple


ACTIVE_CELL = '#'
Point3D = namedtuple("Point", ["x", "y", "z"])
Point4D = namedtuple("Point", ["x", "y", "z", "w"])


def main():
    initial_cube_state = parse_args()

    # Part 1
    conway_cube_sequence = run_conway_cube(initial_cube_state)
    boot_sequence = [next(conway_cube_sequence) for _ in range(6)]
    print(f"Active cells after 6 cycle boot sequence: {len(boot_sequence[-1])}")

    # Part 2
    conway_cube_sequence_4d = run_conway_cube(add_4th_dimension_to_points(initial_cube_state))
    boot_sequence_4d = [next(conway_cube_sequence_4d) for _ in range(6)]
    print(f"Active cells after 6 cycle boot sequence in 4D: {len(boot_sequence_4d[-1])}")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file")
    args = parser.parse_args()
    initial_cube_state = parse_cube_state_layer(open(args.input_file).read())
    return initial_cube_state


def parse_cube_state_layer(s, z=0):
    return {Point3D(x, y, z) for y, l in enumerate(s.split('\n')) for x, c in enumerate(l) if c == ACTIVE_CELL}


def run_conway_cube(initial_state, max_iterations=999999):
    active_points = set(initial_state)
    volatile_points = set()
    for p in active_points:
        volatile_points.add(p)
        for neighbour in get_neighbour_points(p):
            volatile_points.add(neighbour)
    for _ in range(max_iterations):
        new_activated_points = set()
        new_deactivated_points = set()
        for p in volatile_points:
            num_active_neighbours = count_active_neighbours(p, active_points)
            if p in active_points and not (2 <= num_active_neighbours <= 3):
                new_deactivated_points.add(p)
            if p not in active_points and num_active_neighbours == 3:
                new_activated_points.add(p)
        for p in new_activated_points:
            active_points.add(p)
        for p in new_deactivated_points:
            active_points.remove(p)
        volatile_points = set()
        for p in new_activated_points.union(new_deactivated_points):
            volatile_points.add(p)
            for neighbour in get_neighbour_points(p):
                volatile_points.add(neighbour)
        yield active_points


def get_neighbour_points(p):
    if isinstance(p, Point3D):
        return {Point3D(x, y, z)
                for x in range(p.x-1, p.x+2) for y in range(p.y-1, p.y+2) for z in range(p.z-1, p.z+2)
                if not (x == p.x and y == p.y and z == p.z)}
    elif isinstance(p, Point4D):
        return {Point4D(x, y, z, w)
                for x in range(p.x-1, p.x+2) for y in range(p.y-1, p.y+2) for z in range(p.z-1, p.z+2) for w in range(p.w-1, p.w+2)
                if not (x == p.x and y == p.y and z == p.z and w == p.w)}
    else:
        raise Exception(f"get_neighbour_points can only be called with Point3D or Point4D (was called with {p})")


def count_active_neighbours(point, active_points):
    return sum(map(lambda p: 1 if p in active_points else 0, (n for n in get_neighbour_points(point))))


def add_4th_dimension_to_points(points, w=0):
    return {Point4D(p.x, p.y, p.z, w) for p in points}


def print_3d_conway_cube(active_points, min_x=-2, max_x=5, min_y=-2, max_y=7, min_z=-2, max_z=2):
    for z in range(min_z, max_z + 1):
        print(f"Z={z}")
        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                print('#' if Point3D(x, y, z) in active_points else '.', end='')
            print("")
        print("")


if __name__ == "__main__":
    main()
