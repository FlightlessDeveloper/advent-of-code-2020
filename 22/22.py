import argparse
from collections import namedtuple


CombatState = namedtuple("CombatState", ["deck_a", "deck_b"])
RecursiveCombatState = namedtuple("RecursiveCombatState", ["depth", "combat_state"])


def main():
    initial_state = parse_args()

    # Part 1
    final_combat_score = get_score_from_game(play_combat(initial_state))
    print(f"Final Score: {final_combat_score}")

    # Part 2
    final_recursive_combat_score = get_score_from_game(play_recursive_combat(initial_state))
    print(f"Final Score for recursive game: {final_recursive_combat_score}")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file")
    args = parser.parse_args()
    initial_state = parse_decks(open(args.input_file).read())
    return initial_state


def parse_decks(s):
    raw_deck_a, raw_deck_b = s.split("\n\nPlayer 2:\n")
    deck_a = [int(x) for x in raw_deck_a.split("\n")[1:] if len(x) > 0]
    deck_b = [int(x) for x in raw_deck_b.split("\n") if len(x) > 0]
    return CombatState(deck_a, deck_b)


def play_combat(initial_state):
    deck_a, deck_b = initial_state
    while len(deck_a) > 0 and len(deck_b) > 0:
        if deck_a[0] > deck_b[0]:
            deck_a = deck_a[1:] + [deck_a[0], deck_b[0]]
            deck_b = deck_b[1:]
        else:
            deck_b = deck_b[1:] + [deck_b[0], deck_a[0]]
            deck_a = deck_a[1:]
        yield CombatState(deck_a, deck_b)


def calculate_final_score(game_state):
    if len(game_state.deck_a) == 0:
        winning_deck = game_state.deck_b
    elif len(game_state.deck_b) == 0:
        winning_deck = game_state.deck_a
    else:
        raise Exception(f"Can't calculate final score because both decks still contain cards")
    return sum(x * (i + 1) for i, x in enumerate(reversed(winning_deck)))


def play_recursive_combat(initial_state, recursion_depth=0, cached_results=None):
    if cached_results is None:
        cached_results = dict()
    yield RecursiveCombatState(recursion_depth, initial_state)
    hashed_initial_state = hash_combat_state(initial_state)
    if hashed_initial_state in cached_results:
        yield RecursiveCombatState(recursion_depth, cached_results[hashed_initial_state])
    else:
        deck_a, deck_b = initial_state
        previous_states = []
        while len(deck_a) > 0 and len(deck_b) > 0:
            if hash_combat_state(CombatState(deck_a, deck_b)) in previous_states:
                winner_is_a = True
            elif deck_a[0] < len(deck_a) and deck_b[0] < len(deck_b):
                sub_game = play_recursive_combat(CombatState(deck_a[1:deck_a[0] + 1], deck_b[1:deck_b[0] + 1]),
                                                 recursion_depth + 1, cached_results)
                last_sub_game_state = None
                for depth, state in sub_game:
                    last_sub_game_state = state
                    yield RecursiveCombatState(depth, last_sub_game_state)
                winner_is_a = len(last_sub_game_state.deck_a) > len(last_sub_game_state.deck_b)
            else:
                winner_is_a = deck_a[0] > deck_b[0]
            previous_states.append(hash_combat_state(CombatState(deck_a, deck_b)))
            if winner_is_a:
                deck_a = deck_a[1:] + [deck_a[0], deck_b[0]]
                deck_b = deck_b[1:]
            else:
                deck_b = deck_b[1:] + [deck_b[0], deck_a[0]]
                deck_a = deck_a[1:]
            new_state = CombatState(deck_a, deck_b)
            cached_results[hashed_initial_state] = new_state
            yield RecursiveCombatState(recursion_depth, new_state)


def hash_combat_state(s):
    return ",".join(str(x) for x in s.deck_a) + "|" + ",".join(str(x) for x in s.deck_b)


def get_score_from_game(game):
    last_state = None
    try:
        while True:
            last_state = next(game)
    except StopIteration:
        if last_state is not None and isinstance(last_state, CombatState):
            return calculate_final_score(last_state)
        if last_state is not None and isinstance(last_state, RecursiveCombatState):
            return calculate_final_score(last_state.combat_state)
        raise Exception(f"Couldn't find last state")


def get_score_from_game_and_print(game, verbose_level=0):
    last_state = None
    recursion_depth = 0
    for state in game:
        recursion_depth_chaned = False
        if isinstance(state, CombatState):
            last_state = state
        if isinstance(state, RecursiveCombatState):
            last_state = state.combat_state
            if recursion_depth != state.depth:
                recursion_depth = state.depth
                recursion_depth_chaned = True
        if verbose_level > 0:
            deck_a_string = ','.join(str(x) for x in last_state.deck_a)
            deck_b_string = ','.join(str(x) for x in last_state.deck_b)
            if (recursion_depth_chaned and verbose_level > 1) or verbose_level > 2:
                print("")
            if verbose_level > 1 or recursion_depth == 0:
                print(f"\r{'> ' * recursion_depth}[{deck_a_string}] [{deck_b_string}]\u001b[0K", end='')
    if verbose_level > 0:
        print("")
    return calculate_final_score(last_state)


if __name__ == "__main__":
    main()
