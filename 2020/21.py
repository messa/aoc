from operator import itemgetter
from pprint import pprint
import re

foods = []

for line in open('21_input.txt').read().splitlines():
    ingredients, allergens = re.match(r'^(.+) \(contains (.+)\)$', line).groups()
    ingredients = ingredients.split()
    allergens = allergens.split(', ')
    foods.append((ingredients, allergens))

possible_allergen_ingredients = {}

for ingredients, allergens in foods:
    for a in allergens:
        possible_allergen_ingredients[a] = set(ingredients)

for ingredients, allergens in foods:
    for allergen in allergens:
        possible_allergen_ingredients[allergen] &= set(ingredients)
        if len(possible_allergen_ingredients[allergen]) == 1:
            ingredient, = possible_allergen_ingredients[allergen]
            # allergen ingredient was detected, remove from other allergen candidates:
            for other_allergen in possible_allergen_ingredients:
                if other_allergen != allergen:
                    possible_allergen_ingredients[other_allergen].discard(ingredient)

pprint(possible_allergen_ingredients)

ingredient_allergen = {}
for allergen, possible_ingredients in possible_allergen_ingredients.items():
    assert len(possible_ingredients) == 1
    ingredient, = possible_ingredients
    assert ingredient not in ingredient_allergen
    ingredient_allergen[ingredient] = allergen

safe_ingredient_occurrences = 0

for ingredients, allergens in foods:
    for ingredient in ingredients:
        if ingredient not in ingredient_allergen.keys():
            safe_ingredient_occurrences += 1

print('safe_ingredient_occurrences:', safe_ingredient_occurrences)

canonical_list = ','.join(ingredient for ingredient, allergen in sorted(ingredient_allergen.items(), key=itemgetter(1)))

print('canonical_list:', canonical_list)
