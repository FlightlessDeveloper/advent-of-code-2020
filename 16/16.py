import argparse
from collections import namedtuple
from functools import reduce


InputData = namedtuple("InputData", ["constraints", "my_ticket", "nearby_tickets"])
Constraint = namedtuple("Constraint", ["field_name", "ranges"])
Range = namedtuple("Range", ["min", "max"])


def main():
    input_data = parse_args()

    # Part 1
    error_rate, valid_tickets = verify_tickets(input_data)
    print(f"Ticket scanning error rate: {error_rate}")

    # Part 2
    valid_tickets.append(input_data.my_ticket)
    indices_for_fields = get_indices_for_fields(input_data.constraints, valid_tickets)
    departure_verification_code = get_departure_verification_code(input_data.my_ticket, indices_for_fields)
    print(f"Departure verification code: {departure_verification_code}")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file")
    args = parser.parse_args()
    input_data = parse_input_file(open(args.input_file).read())
    return input_data


def parse_input_file(lines):
    raw_constraints_lines, raw_my_ticket_lines, raw_nearby_ticket_lines = lines.split("\n\n")
    constraints = parse_constraints_lines(raw_constraints_lines)
    my_ticket = [int(x) for x in raw_my_ticket_lines.split('\n')[1].split(',')]
    nearby_tickets = [[int(x) for x in l.split(',')] for l in raw_nearby_ticket_lines.split('\n')[1:] if len(l) > 0]
    return InputData(constraints, my_ticket, nearby_tickets)


def parse_constraints_lines(constraints_string):
    constraints = []
    for l in constraints_string.split("\n"):
        field_name, raw_ranges = l.split(": ")
        ranges = []
        for range_string in raw_ranges.split(" or "):
            min_string, max_string = range_string.split("-")
            ranges.append(Range(int(min_string), int(max_string)))
        constraints.append(Constraint(field_name, ranges))
    return constraints


def verify_tickets(input_data):
    error_rate = 0
    valid_tickets = []
    for ticket in input_data.nearby_tickets:
        ticket_is_valid = True
        for value in ticket:
            value_is_valid = False
            for constraint in input_data.constraints:
                if verify_value_in_ranges(value, constraint.ranges):
                    value_is_valid = True
                    break
            if not value_is_valid:
                error_rate += value
                ticket_is_valid = False
        if ticket_is_valid:
            valid_tickets.append(ticket)
    return error_rate, valid_tickets


def verify_value_in_ranges(v, ranges):
    for range in ranges:
        if range.min <= v <= range.max:
            return True
    return False


def get_indices_for_fields(constraints, tickets):
    possible_field_names_by_index = [set(c.field_name for c in constraints) for _ in tickets[0]]
    for t in tickets:
        for i, v in enumerate(t):
            invalid_field_names = set()
            for f in possible_field_names_by_index[i]:
                c = next(c for c in constraints if c.field_name == f)
                if not verify_value_in_ranges(v, c.ranges):
                    invalid_field_names.add(f)
            for f in invalid_field_names:
                possible_field_names_by_index[i].remove(f)
    return get_single_index_for_fields(possible_field_names_by_index, set(c.field_name for c in constraints))


def get_single_index_for_fields(possible_field_names_by_index, field_names):
    remaining_fields = set(field_names)
    remaining_indices = set(range(len(possible_field_names_by_index)))
    index_by_field_name = {}
    while len(remaining_fields) > 0:
        found_fields = set()
        found_indices = set()

        for field_name in remaining_fields:
            possible_indices = {i for i in remaining_indices if field_name in possible_field_names_by_index[i]}
            if len(possible_indices) == 1:
                index = next(iter(possible_indices))
                index_by_field_name[field_name] = index
                found_fields.add(field_name)
                found_indices.add(index)

        for index in remaining_indices:
            possible_field_names_for_i = {f for f in possible_field_names_by_index[index] if f in remaining_fields}
            if len(possible_field_names_for_i) == 1:
                field_name = next(iter(possible_field_names_for_i))
                index_by_field_name[field_name] = index
                found_fields.add(field_name)
                found_indices.add(index)

        for field_name in found_fields:
            remaining_fields.remove(field_name)
        for i in found_indices:
            remaining_indices.remove(i)
    return index_by_field_name


def get_departure_verification_code(ticket, ids_for_fields):
    departure_fields = {f for f in ids_for_fields if f.split(" ")[0] == "departure"}
    return reduce(lambda x, y: x * y, (ticket[ids_for_fields[f]] for f in departure_fields), 1)


if __name__ == "__main__":
    main()
