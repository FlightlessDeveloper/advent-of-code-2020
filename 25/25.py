import argparse


def main():
    card_public_key, door_public_key = parse_args()

    card_loop_size = find_loop_size(card_public_key)
    door_loop_size = find_loop_size(door_public_key)
    encryption_key = get_encryption_key(card_public_key, door_loop_size)
    print(f"Encryption Key: {encryption_key}")


def find_loop_size(public_key):
    for n, v in enumerate(perform_handshake_loops(7)):
        if v == public_key:
            return n
    raise Exception(f"Could not find loop size for public key {public_key}")


def get_encryption_key(public_key, loop_size):
    loops = perform_handshake_loops(public_key)
    for _ in range(loop_size):
        next(loops)
    return next(loops)


def perform_handshake_loops(subject_number, max_loops=999999999):
    value = 1
    yield(value)
    for i in range(max_loops):
        value = value * subject_number
        value = value % 20201227
        yield value


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file")
    args = parser.parse_args()
    card_public_key, door_public_key = [int(x.strip()) for x in open(args.input_file)]
    return card_public_key, door_public_key


if __name__ == "__main__":
    main()
