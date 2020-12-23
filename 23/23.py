import argparse


# Note: this is probably done more easily with a deque
class Node:
    def __init__(self, value):
        self.data = value
        self.next_node = self
        self.prev_node = self

    def push_right(self, node):
        node.prev_node = self
        node.next_node = self.next_node
        self.next_node.prev_node = node
        self.next_node = node
        return self

    def push_left(self, node):
        node.next_node = self
        node.prev_node = self.prev_node
        self.prev_node.next_node = node
        self.prev_node = node
        return self

    def pop_right(self):
        popped_value = self.next_node.data
        self.next_node = self.next_node.next_node
        self.next_node.prev_node = self
        return popped_value

    def pop_left(self):
        popped_value = self.prev_node.data
        self.prev_node = self.prev_node.prev_node
        self.prev_node.next_node = self
        return popped_value

    def next(self):
        return self.next_node

    def prev(self):
        return self.prev_node

    def value(self):
        return self.data


def main():
    cups = parse_args()

    # Part 1
    final_labels = get_cup_labels(play_cup_game(cups, 100))
    print(f"Cup game labels after 100 turns: {final_labels}")

    # Part 2
    actual_cups = cups + [x + 1 for x in range(len(cups), 1000000)]
    verification_number = calculate_verification_number(play_cup_game(actual_cups, 10000000, print_progress=True))
    print(f"Verification number for actual game: {verification_number}")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file")
    args = parser.parse_args()
    cups = [int(x) for x in open(args.input_file).read().strip()]
    return cups


def play_cup_game(initial_state, num_turns, print_progress=False):
    if print_progress:
        print("Playing cup game...", end='')
    cups = make_linked_list(initial_state)
    lookup_table = make_linked_list_lookup_table(cups, len(initial_state))
    num_cups = len(initial_state)
    for t in range(1, num_turns + 1):
        destination = cups.value() - 1
        picked_up_cups = [cups.pop_right(), cups.pop_right(), cups.pop_right()]
        while destination in picked_up_cups or destination < 1:
            destination -= 1
            if destination < 1:
                destination = num_cups
        destination_node = lookup_table[destination]
        for x in picked_up_cups:
            destination_node = destination_node.push_right(Node(x)).next()
            lookup_table[x] = destination_node
        cups = cups.next()
        if print_progress and t % (num_turns / 100) == 0:
            print(f"\rPlaying cup game ({int(t * 100 / num_turns)}% complete)...\u001b[0K", end='')
    if print_progress:
        print("")
    return make_list_from_linked_list(find_node_for_item(cups, 1))[1:]


def make_linked_list(x):
    it = iter(x)
    current_node = first_node = Node(next(it))
    for value in it:
        current_node = current_node.push_right(Node(value)).next()
    return first_node


def find_node_for_item(node, target):
    first_node = node
    while node.value() != target:
        node = node.next()
        if node == first_node:
            raise Exception("Item was not present")
    return node


def make_list_from_linked_list(node):
    first_node = node
    l = [first_node.value()]
    node = first_node.next()
    while node != first_node:
        l.append(node.value())
        node = node.next()
    return l


def make_linked_list_lookup_table(l, size):
    lookup_table = [0 for _ in range(size + 1)]
    first_node = l
    lookup_table[first_node.value()] = first_node
    node = first_node.next()
    while node != first_node:
        lookup_table[node.value()] = node
        node = node.next()
    return lookup_table


def get_cup_labels(l):
    return "".join(str(x) for x in l)


def calculate_verification_number(cups):
    return cups[0] * cups[1]


if __name__ == "__main__":
    main()
