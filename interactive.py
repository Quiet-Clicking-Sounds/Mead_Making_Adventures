from mead import Mead, NitrogenSourceNotImplemented, IngredientNotImplemented


def interactive():
    """

    :return:
    """
    abv: float | None = None
    start_grav: float | None = None
    end_grav: float | None = None
    print("Mead Maker")
    allowed_inputs = ('abv', 'start', 'end')
    print(f"Setup, input one of {allowed_inputs} followed by a number to set. ")
    while True:
        arg = input()
        arg0, arg1 = arg.lower().split(" ", 1)

        match arg.lower().split(" ", 1):
            case ['abv', x]:
                abv = float(x)
            case ['start', x]:
                start_grav = float(x)
            case ['end', x]:
                end_grav = float(x)
            case [a, x]:
                print(f"command '{a}' not recognised use one of {allowed_inputs} followed by a number")
        if sum([1 for a in (abv, + start_grav, end_grav) if a is not None]) == 2:
            break
    mead = Mead(abv, end_grav, start_grav)

    while True:
        arg = input()

        match arg.lower().split(" ", 1):
            case _:
                pass


def make_mead_base() -> Mead:
    print("Mead Creation starte.\n")
    print("two of Alcohol, Original Gravity or Final gravity will need to be quantified: \n")
    print("Selector: A: ABV, O: Original Gravity, F: Final Gravity")
    selector_aof = [None, None, None]

    while selector_aof.count(None) == 1:
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
        arg = input("Options - I: Ingredient, N: Nitrogen source, E: End and print mead")
        if len(arg) == 0:
            print("no valid input found")
            continue
        match arg.lower().strip()[0]:
            case 'e': break
            case 'i': mead = add_ingredient(mead)
            case 'n': mead = add_nitrogen(mead)
            case _ : print("No valid input found")
    print(mead)

def add_ingredient(mead: Mead) -> Mead:
    try:
        pass
    except IngredientNotImplemented as _ie:
        print("No ingredient by that name has been found")
    finally:
        return mead

def add_nitrogen(mead: Mead) -> Mead:
    arg = input("123")
    try:
        pass
    except NitrogenSourceNotImplemented as _ne:
        print("No nitrogen source by that name has been found")
    finally:
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
