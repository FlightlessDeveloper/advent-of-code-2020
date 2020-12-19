import argparse
from collections import namedtuple


RuleCharacter = namedtuple("RuleCharacter", ["char"])
RuleSequence = namedtuple("RuleSequence", ["rules"])
RuleOneOf = namedtuple("RuleOneOf", ["rules"])
RuleRepeat = namedtuple("RuleRepeat", ["rule"])
RuleRepeatBoth = namedtuple("RuleRepeatBoth", ["left_rule", "right_rule"])


def main():
    rules, messages = parse_args()

    print("Part 1:")
    computed_rules = compute_rules(rules)
    num_valid_messages = count_valid_messages(messages, computed_rules[0])
    print(f"Number of valid messages: {num_valid_messages}\n")

    print("Part 2:")
    computed_rules_with_advanced_rules = compute_rules(rules, advanced_rules=True)
    num_valid_messages_with_advanced_rules = count_valid_messages(messages, computed_rules_with_advanced_rules[0], print_progress=True)
    print(f"Number of valid messages: {num_valid_messages_with_advanced_rules}\n")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file")
    args = parser.parse_args()
    rules, messages = open(args.input_file).read().split("\n\n")
    return parse_rules(rules.strip().split("\n")), messages.strip().split("\n")


def parse_rules(rule_strings):
    rules = dict()
    for rule in rule_strings:
        index_string, sub_rules = rule.split(": ")
        if sub_rules.startswith('"'):
            rules[int(index_string)] = sub_rules[1:-1]
        else:
            rules[int(index_string)] = [[int(x) for x in s.split(" ")] for s in sub_rules.split(" | ")]
    return rules


def compute_rules(rules, advanced_rules=False):
    computed_rules = dict((i, RuleCharacter(rules[i])) for i in rules if isinstance(rules[i], str))
    uncomputed_rule_indices = set(i for i in rules).difference(iter(computed_rules))
    while len(uncomputed_rule_indices) > 0:
        computable_rules = list(filter(lambda i: all(x in computed_rules or x == i for l in rules[i] for x in l),
                                       uncomputed_rule_indices))
        for rule_index in computable_rules:
            if advanced_rules and rule_index == 8:
                computed_rule = RuleSequence([computed_rules[42], RuleRepeat(computed_rules[42])])
            elif advanced_rules and rule_index == 11:
                computed_rule = RuleSequence([computed_rules[42], RuleRepeatBoth(computed_rules[42], computed_rules[31]), computed_rules[31]])
            else:
                computed_rule = RuleOneOf([RuleSequence([computed_rules[x] for x in l]) for l in rules[rule_index]])
                while (isinstance(computed_rule, RuleOneOf) or isinstance(computed_rule, RuleSequence))\
                        and len(computed_rule.rules) == 1:
                    computed_rule = computed_rule.rules[0]
            computed_rules[rule_index] = computed_rule
            uncomputed_rule_indices.remove(rule_index)
    return computed_rules


def is_valid_message(message, rule):
    for s in match_message_to_rule(message, rule):
        if len(s) == 0:
            return True
    return False


def match_message_to_rule(message, rule):
    if len(message) == 0:
        return ''
    if isinstance(rule, RuleCharacter):
        if message.startswith(rule.char):
            return [message[1:]]
        else:
            return []
    if isinstance(rule, RuleSequence):
        new_messages = match_message_to_rule(message, rule.rules[0])
        next_rules = rule.rules[1:]
        if len(next_rules) == 0:
            return new_messages
        else:
            return [s for m in new_messages for s in match_message_to_rule(m, RuleSequence(next_rules))]
    if isinstance(rule, RuleOneOf):
        return [s for r in rule.rules for s in match_message_to_rule(message, r)]
    if isinstance(rule, RuleRepeat):
        new_messages = [message]
        valid_messages = []
        while len(new_messages) > 0:
            valid_messages += new_messages
            new_messages = [s for m in new_messages for s in match_message_to_rule(m, rule.rule)]
        return valid_messages
    if isinstance(rule, RuleRepeatBoth):
        valid_messages = [message]
        for num_loops in range(300):
            new_messages = [message]
            for i in range(num_loops):
                new_messages = [s for m in new_messages for s in match_message_to_rule(m, rule.left_rule)]
            if len(new_messages) > 1:
                # If we can't reduce by left_rule i times, then we won't be able to for any n>i either
                break
            for i in range(num_loops):
                new_messages = [s for m in new_messages for s in match_message_to_rule(m, rule.right_rule)]
            valid_messages += new_messages
        return valid_messages
    else:
        raise Exception(f"Invalid rule: {rule}")


def count_valid_messages(messages, rule, print_progress=False):
    count = 0
    num_messages = len(messages)
    for i, m in enumerate(messages):
        if print_progress:
            print(f"\rChecking message {i + 1} of {num_messages} ({count} valid so far)\t[{m}]\u001b[0K", end='')
        if is_valid_message(m, rule):
            count += 1
    if print_progress:
            print(f"\rChecked {num_messages} messages ({count} valid)\u001b[0K")
    return count


if __name__ == "__main__":
    main()
