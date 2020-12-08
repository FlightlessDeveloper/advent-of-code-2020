import argparse
from collections import namedtuple


Instruction = namedtuple("Instruction", ["operation", "argument"])
ProgramState = namedtuple("ProgramState", ["line_num", "accumulator"])
VALID_INSTRUCTIONS = {"acc", "jmp", "nop"}


def main():
    program = parse_args()

    # Part 1
    acc_at_infinite_loop_start = find_acc_at_infinite_loop_start(program)
    print(f"Accumulator at start of infinite loop: {acc_at_infinite_loop_start}")

    # Part 2
    fixed_program = solve_halting_problem(program)
    final_program_state = get_program_states(fixed_program)[-1]
    print(f"Final accumulator in fixed program: {final_program_state.accumulator}")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file")
    args = parser.parse_args()
    program = [parse_instruction(l) for l in open(args.input_file)]
    return program


def parse_instruction(s):
    operation = s[:3]
    if operation not in VALID_INSTRUCTIONS:
        raise Exception(f"Unsupported operation while parsing: '{operation}'")

    argument_sign_string = s[4]
    if argument_sign_string == "+":
        argument_sign = 1
    elif argument_sign_string == "-":
        argument_sign = -1
    else:
        raise Exception(f"Invalid sign on argument: '{argument_sign_string}'")

    unsigned_argument = int(s[5:])
    return Instruction(operation, argument_sign * unsigned_argument)


def run_program(p):
    accumulator = 0
    line_num = 0
    while line_num < len(p):
        instruction = p[line_num]
        if instruction.operation == "acc":
            accumulator = accumulator + instruction.argument
            line_num = line_num + 1
        elif instruction.operation == "jmp":
            line_num = line_num + instruction.argument
        elif instruction.operation == "nop":
            line_num = line_num + 1
        else:
            raise Exception(f"Unsupported operation while running: '{instruction.operation}'")
        yield ProgramState(line_num, accumulator)


def get_program_states(program, max_instruction_count=9999):
    instruction_count = 0
    program_states = []
    program_machine = run_program(program)
    try:
        while instruction_count < max_instruction_count:
            instruction_count = instruction_count + 1
            program_states.append(next(program_machine))
    except StopIteration:
        return program_states
    raise Exception(f"Max instruction count of {max_instruction_count} reached")


def find_acc_at_infinite_loop_start(p):
    program_machine = run_program(p)
    lines_already_run = set()
    accumulator = 0
    next_line = 0
    try:
        while next_line not in lines_already_run:
            lines_already_run.add(next_line)
            next_line, accumulator = next(program_machine)
    except StopIteration:
        return None
    return accumulator


def solve_halting_problem(program):
    for target_index in range(len(program)):
        if program[target_index].operation in {"jmp", "nop"}:
            new_program = flip_operation_at_index(program, target_index)
            if find_acc_at_infinite_loop_start(new_program) is None:
                return new_program
    return None


def flip_operation_at_index(program, index):
    new_program = program.copy()
    instruction = program[index]
    if instruction.operation == "jmp":
        new_operation = "nop"
    elif instruction.operation == "nop":
        new_operation = "jmp"
    else:
        new_operation = instruction.operation
    new_program[index] = Instruction(new_operation, instruction.argument)
    return new_program


if __name__ == "__main__":
    main()
