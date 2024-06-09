import fuzzywuzzy.process

from mead import Mead, NitrogenSource, Ingredient
from mead import NitrogenSourceNotImplemented, IngredientNotImplemented


def make_mead_base() -> Mead:
    print("Mead Creation started.\n")
    print("two of Alcohol, Original Gravity or Final gravity will need to be quantified: \n")
    print("Selector: A: ABV, O: Original Gravity, F: Final Gravity")
    selector_aof = [None, None, None]

    while selector_aof.count(None) > 1:
        sel = input("Choose Selector: ")
        if len(sel) == 0:
            print("no valid input found")
            continue
        match sel.lower().strip()[0]:
            case 'a':
                arg = single_float_selector("Select ABV, range 0-40:", 0, 40)
                if arg is not None:
                    selector_aof[0] = arg
            case 'o':
                arg = single_float_selector("Select Original Gravity, range 1.0 - 1.45:", 1, 1.45)
                if arg is not None:
                    selector_aof[1] = arg
            case 'f':
                arg = single_float_selector("Select Final Gravity, range 0.9 - 1.45:", 0.9, 1.45)
                if arg is not None:
                    selector_aof[2] = arg
            case _:
                print("No valid selector chosen")
                continue
    weight = None
    while weight is None:
        weight = single_float_selector("Select final weight (volume) must be greater than 0:", 0, None)

    mead = Mead(*selector_aof, product_weight=weight)
    print(f"Mead Created: ABV = {mead.expected_abv:.1f}, "
          f"Original Gravity = {mead.final_gravity:.3f}, "
          f"Final Gravity = {mead.start_gravity:.3f}")
    return mead


def mead_creator():
    mead = make_mead_base()

    print("Additions can be made here:")
    while True:
        arg = input("Options - I: Ingredient, N: Nitrogen source, E: End and print mead:")
        if len(arg) == 0:
            print("no valid input found")
            continue
        match arg.lower().strip()[0]:
            case 'e':
                break
            case 'i':
                mead = add_ingredient(mead)
            case 'n':
                mead = add_nitrogen(mead)
            case _:
                print("No valid input found")
    print(mead)


def ask_for_bool(question: str) -> bool:
    bl = input(question)
    bl = bl.lower()[0]
    if bl == 'y':
        return True
    return False


def add_ingredient(mead: Mead) -> Mead:
    ingredient_list = Ingredient.get_source_list()
    print("Choose Ingredient, use '.' to exit,  use '?' to print ingredient list: ")
    while True:
        i = input()
        if i[0] == '?':
            sl = ', '.join(ingredient_list)
            print(f"Ingredient options: {sl}")
            continue
        elif i[0] == '.':
            break

        try:
            best_match: tuple[str, int] | None = fuzzywuzzy.process.extractOne(query=i, choices=ingredient_list)
            match best_match:
                case None:
                    print("No match, try again")
                    continue
                case (x, n) if n < 75:
                    if ask_for_bool(f"Did you mean: {x}? (y/n)"):
                        ing = x
                    else:
                        continue
                case (x, n) if n >= 75:
                    ing = x
                case _:
                    print("that didn't work, you shouldn't be here")
                    continue

            qty = single_float_selector("Add Quantity in KG (total):", 0, None)
            if qty is None:
                continue
            print(f"Adding: {qty}kg of {ing}")
            mead.add_ingredient(ing, kg=qty)
            break
        except IngredientNotImplemented as _ie:
            print("No ingredient by that name has been found")

    return mead


def add_nitrogen(mead: Mead) -> Mead:
    nitrogen_list = NitrogenSource.get_source_list()
    print("Choose Nitrogen, use '.' to exit, use '?' to print nitrogen source list: ")
    while True:
        i = input()
        if i[0] == '?':
            sl = ', '.join(nitrogen_list)
            print(f"Nitrogen options: {sl}")
            continue
        elif i[0] == '.':
            break
        try:
            best_match: tuple[str, int] | None = fuzzywuzzy.process.extractOne(query=i, choices=nitrogen_list)
            match best_match:
                case None:
                    print("No match, try again")
                    continue
                case (x, n) if n < 75:
                    if ask_for_bool(f"Did you mean: {x}? (y/n)"):
                        nt = x
                    else:
                        continue
                case (x, n) if n >= 75:
                    nt = x
                case _:
                    print("that didn't work, you shouldn't be here")
                    continue

            qty = single_float_selector("Add Quantity in grams(total):", 0, None)
            if qty is None:
                continue
            print(f"Adding: {qty}g of {nt}")
            mead.add_nitrogen_source(nt, qty)
            break
        except NitrogenSourceNotImplemented as _ne:
            print("we got an unexpected error .. No nitrogen source by that name has been found")

    return mead


def single_float_selector(text: str, range_min: None | float, range_max: None | float) -> float | None:
    var = input(text)
    var = var.strip()
    try:
        var = float(var)
        if (range_min is not None and var < range_min) or (range_max is not None and var > range_max):
            print("Value outside of range")
            return None
        return var
    except ValueError:
        print("Error, input not valid")
        return None


if __name__ == '__main__':
    mead_creator()
