import argparse
from collections import namedtuple
from functools import reduce

FoodItem = namedtuple("FoodItem", ["ingredients", "allergens"])


def main():
    food_items = parse_args()

    # Part 1
    ingredients_for_allergens = find_potential_ingredients_for_allergens(food_items)
    safe_ingredient_count = count_safe_ingredients(food_items, ingredients_for_allergens)
    print(f"Number of times safe ingredients appear: {safe_ingredient_count}")

    # Part 2
    canonical_dangerous_ingredient_list = make_canonical_dangerous_ingredient_list(ingredients_for_allergens)
    print(f"Canonical dangerous ingredient list: {canonical_dangerous_ingredient_list}")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file")
    args = parser.parse_args()
    food_items = [parse_food_item(s) for s in open(args.input_file)]
    return food_items


def parse_food_item(s):
    ingredients_string, allergens_string = s.split(" (contains ")
    return FoodItem(set(ingredients_string.split(" ")), set(allergens_string[:-2].split(", ")))


def find_potential_ingredients_for_allergens(food_items):
    foods_by_allergen = dict()
    for food in food_items:
        for allergen in food.allergens:
            if allergen in foods_by_allergen:
                foods_by_allergen[allergen].append(food.ingredients)
            else:
                foods_by_allergen[allergen] = [food.ingredients]
    ingredients_for_allergens = dict((allergen, reduce((lambda a, b: a & b), ingredient_lists))
                                     for allergen, ingredient_lists in foods_by_allergen.items())
    altered_ingredients_for_allergens = True
    while altered_ingredients_for_allergens:
        allergens_with_one_ingredient = set(a for a, i in ingredients_for_allergens.items() if len(i) == 1)
        altered_ingredients_for_allergens = False
        for identified_allergen in allergens_with_one_ingredient:
            identified_ingredient = next(iter(ingredients_for_allergens[identified_allergen]))
            for allergen in ingredients_for_allergens:
                if allergen != identified_allergen and identified_ingredient in ingredients_for_allergens[allergen]:
                    ingredients_for_allergens[allergen].remove(identified_ingredient)
                    altered_ingredients_for_allergens = True
    return ingredients_for_allergens


def count_safe_ingredients(food_items, ingregients_for_allergens):
    safe_ingredients = reduce((lambda a, b: a | b), (f.ingredients for f in food_items))\
                       - reduce((lambda a, b: a | b), ingregients_for_allergens.values())
    return sum(sum(1 if i in safe_ingredients else 0 for i in f.ingredients) for f in food_items)


def make_canonical_dangerous_ingredient_list(ingredients_for_allergens):
    return ",".join(map(lambda x: ",".join(x[1]), sorted(ingredients_for_allergens.items(), key=lambda x: x[0])))


if __name__ == "__main__":
    main()
