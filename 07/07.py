import argparse
from collections import namedtuple


Rule = namedtuple("Rule", ["colour", "requirements"])
BagQuantity = namedtuple("BagQuantity", ["colour", "quantity"])


def main():
    rules = parse_args()

    # Part 1
    bags_containing_gold = find_all_eventual_parent_colours({"shiny gold"}, rules)
    print(f"Number of bag colours eventually containing gold: {len(bags_containing_gold)}")

    # Part 2
    total_bags_needed = calculate_total_bags_needed("shiny gold", rules)
    print(f"Total bags needed: {total_bags_needed}")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file")
    args = parser.parse_args()
    rules = [parse_rule(l) for l in open(args.input_file)]
    return rules


def parse_rule(s):
    raw_parent_colour_string, raw_requirements_string = s.split(" contain ")
    parent_colour = raw_parent_colour_string.split(" bag")[0]
    if raw_requirements_string.strip() == "no other bags.":
        requirements = []
    else:
        requirements = [BagQuantity(r.split(" bag")[0][2:], int(r[0])) for r in raw_requirements_string.split(", ")]
    return Rule(parent_colour, requirements)


def find_all_eventual_parent_colours(target_colours, rules, answer_colours=set()):
    if len(target_colours) == 0:
        return answer_colours
    else:
        new_answers = set()
        for colour in target_colours:
            new_answers = new_answers.union(c for c in find_valid_parent_colours(colour, rules) if c not in answer_colours)
        return find_all_eventual_parent_colours(new_answers, rules, answer_colours.union(new_answers))


def find_valid_parent_colours(colour, rules):
    return {r.colour for r in rules if colour in map(lambda req: req.colour, r.requirements)}


def calculate_total_bags_needed(colour, rules):
    requirements = next(r for r in rules if r.colour == colour).requirements
    return sum(req.quantity + req.quantity * calculate_total_bags_needed(req.colour, rules) for req in requirements)


def rule_to_string(r):
    return f"{r.colour}: {', '.join([f'{req.quantity} {req.colour}' for req in r.requirements]) if len(r.requirements) > 0 else 'nothing'}"


if __name__ == "__main__":
    main()
