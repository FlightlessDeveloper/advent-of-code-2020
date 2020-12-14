import argparse
from collections import namedtuple


NUM_BITS = 36
MachineState = namedtuple("MachineState", ["mask", "memory_addresses"])
MaskChange = namedtuple("MaskChange", ["mask"])
WriteToMemory = namedtuple("WriteToMemory", ["address", "value"])


def main():
    instructions = parse_args()

    # Part 1
    sum_of_memory = sum_memory_values(run_until_end(instructions).memory_addresses)
    print(f"Sum of all memory address values: {sum_of_memory}")

    # Part 2
    # Note: example 1 takes a long time to complete with this implementation, but the actual input is fast enough
    sum_of_memory_with_floating_bits = sum_memory_values(run_until_end(instructions, floating_address_bits=True).memory_addresses)
    print(f"Sum of all memory address values (with floating address bits): {sum_of_memory_with_floating_bits}")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file")
    args = parser.parse_args()
    instructions = [parse_instruction(l.strip()) for l in open(args.input_file)]
    return instructions


def parse_instruction(s):
    instruction, value = s.split(" = ")
    if instruction == "mask":
        return MaskChange(value)
    elif instruction[:3] == "mem":
        return WriteToMemory(int(instruction[4:-1]), int(value))
    else:
        raise Exception(f"Unknown instruction when parsing: {instruction}")


def run_until_end(instructions, floating_address_bits=False):
    mask = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    memory_addresses = {}
    for i in instructions:
        if isinstance(i, MaskChange):
            mask = i.mask
        elif isinstance(i, WriteToMemory):
            if not floating_address_bits:
                memory_addresses[i.address] = binary_list_to_int(apply_mask(int_to_binary_list(i.value), mask))
            else:
                masked_addresses = [binary_list_to_int(x) for x in apply_mask_floating(int_to_binary_list(i.address), mask)]
                for a in masked_addresses:
                    memory_addresses[a] = i.value
        else:
            raise Exception(f"Unknown instruction when running program: {i}")
    return MachineState(mask, memory_addresses)


def apply_mask(x, mask):
    if len(x) != len(mask):
        raise Exception(f"Mask must match length of number to mask")
    def apply_mask_digit(digit, mask_char):
        if mask_char == "0":
            return 0
        elif mask_char == "1":
            return 1
        elif mask_char == "X":
            return digit
        else:
            raise Exception(f"Unknown mask character {mask_char}")
    return [apply_mask_digit(x[i], mask[i]) for i in range(len(x))]


def apply_mask_floating(x, mask):
    if len(x) != len(mask):
        raise Exception(f"Mask must match length of number to mask")
    if len(x) == 0:
        return [[]]
    elif mask[0] == "0":
        return [[x[0]] + l for l in apply_mask_floating(x[1:], mask[1:])]
    elif mask[0] == "1":
        return [[1] + l for l in apply_mask_floating(x[1:], mask[1:])]
    elif mask[0] == "X":
        remaining_lists = apply_mask_floating(x[1:], mask[1:])
        return [[1] + l for l in remaining_lists] + [[0] + l for l in remaining_lists]
    else:
        raise Exception(f"Unknown mask character {mask[0]}")


def int_to_binary_list(x):
    return [(x >> i) % 2 for i in reversed(range(NUM_BITS))]


def binary_list_to_int(l):
    return sum(x * 2 ** pow for x, pow in zip(reversed(l), range(len(l))))


def sum_memory_values(m):
    return sum(m[i] for i in m)


if __name__ == "__main__":
    main()
