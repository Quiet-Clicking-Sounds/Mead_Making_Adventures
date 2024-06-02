from mead import Mead, NitrogenSource, Ingredient, NitrogenSourceNotImplemented, IngredientNotImplemented


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

def make_mead_base()->Mead:

def add_ingredient(mead:Mead, arg:str) -> Mead:
    try:
        pass
    except IngredientNotImplemented as _ie:
        print("No ingredient by that name has been found")
    finally:
        return mead
def add_nitrogen(mead:Mead, arg:str) -> Mead:
    arg = input("123")
    try:
        pass
    except NitrogenSourceNotImplemented as _ne:
        print("No nitrogen source by that name has been found")
    finally:
        return mead

if __name__ == '__main__':
