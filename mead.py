# Honey  SG ranging between 1.420 g/cm3 and 1.448 g/cm3
import copy
from typing import Self, Final

sg_min_honey = 1.420
sg_max_honey = 1.448
sg_water = 1.0
sg_ethanol = 0.79


class Mead:
    """
    This is a real work in progress, finding a way to display useful information about what a mead may require
    YAN = Yeast assimilable nitrogen
    [Advanced Nutrients in Mead making](https://docs.google.com/document/d/11pW-dC91OupCYKX-zld73ckg9ximXwxbmpLFOqv6JEk/edit)
    [YAN Spreadsheet](https://docs.google.com/spreadsheets/d/1W8Pp52vFx9g-Uk7aq4WK66Kg_TI5nTrI32sBc5fGaPU/edit#gid=0)


    :param self.nitrogen_requirement: required amount of nitrogen in the mead for 1% abv
    """

    def __init__(self, abv: float = None, final_gravity: float = None, start_gravity: float = None,
                 product_weight=5.0, step_feeding=False, step_feed_mix_ratio: float = 1):
        """
        Describes the initial data about a Mead recipe.


        >>> my_mead = Mead(abv=12, final_gravity=1.005, product_weight=4.5)
        >>> my_mead.add_ingredient("Orange", g=250)
        >>> my_mead.add_nitrogen_source("Fermaid K", g=3)
        >>> my_mead.step_feeding_setup(upper_grav_limit=1.100, lower_grav_limit=1.050)
        >>> print(my_mead) # doctest: +NORMALIZE_WHITESPACE
        Mead Calculation for 4.50 litres of product
            Start gravity (required) 1.097
            Final gravity (sweetness) 1.005
            Expected ABV 12.0%
        Ingredients:
            Water 3.980KG 3.980L
            Total Honey 0.675KG 0.472L
            Orange 250g, (2.0 fruit) 234ml 1.067grav
            Honey 675g, 471ml 1.435grav initial honey addition
        Nitrogen requirement (YAN): 314.04ppm * 4.5L = 1413.18mg
            Nitrogen Source: 3.0g @ 100.0ppm = 300.0mg  - Name: Fermaid K - contains inorganic nitrogen
        Current Nitrogen Load: 300.00
        Required Nitrogen Load: 314.04


        :param abv: in percentage points (5% == 5)
        :param final_gravity: preferred sweetness, 1.02 is a middling sweet mead
        :param start_gravity: starting gravity for the mead
        :param product_weight: Volume of final product in Litres
        :param step_feeding: use :class:`Mead.step_feeding_setup()`
        :param step_feed_mix_ratio: ratio of water to honey used in the stop feed to allow for better mixing,
            1.0 would use 1:1 water to honey, 0.0 would use no water, ratio by WEIGHT
        """
        self.nitrogen_requirement = 0

        match (abv is not None, final_gravity is not None, start_gravity is not None):
            case (False, False, False):
                raise Exception("Some Initial data is required")
            case (True, False, True):
                final_gravity = 1.000
            case (False, True, False):
                raise Exception("Either abv or starting gravity will be necessary")
            case (True, True, True):
                raise Exception("If you know all 3 you probably don't need this")
            case (_, _, _):
                pass

        match (abv, final_gravity, start_gravity):
            case (None, final_gravity, start_gravity):
                abv = (start_gravity - final_gravity) * 131
            case (abv, None, start_gravity):
                final_gravity = start_gravity - abv / 131
            case (abv, final_gravity, None):
                start_gravity = final_gravity + abv / 131

        self._step_feed_ = step_feeding
        self.upper_grav_limit = 1.100
        self.lower_grav_limit = 1.050
        self.ingredients = list()

        self.expected_abv = abv
        self.final_gravity = final_gravity
        self.start_gravity = start_gravity

        self.honey_gravity = 1.43

        self.step_feed_ratio = max(0.0, step_feed_mix_ratio)

        self.product_weight = product_weight
        self.kg_water = None
        self.total_kg_honey = None
        self.honey_steps: list[Ingredient] = list()
        self.calculate_ratios()

        self.set_nitrogen_demand_low()
        self.initial_nitrogen: NitrogenSource = nitrogen_source["Honey"].with_quantity(0)
        self.nitrogen_sources: list[NitrogenSource] = list()

    def step_feeding_setup(self, upper_grav_limit: float = None, lower_grav_limit: float = None):
        """
        This function will aim to keep the estimated gravity between the upper and lower bounds for your mead.

        :param upper_grav_limit: defaults to 1.100, will keep previous given limit if called multiple times
        :param lower_grav_limit: defaults to 1.050, will keep previous given limit if called multiple times
        :return:
        """
        self.upper_grav_limit = upper_grav_limit or self.upper_grav_limit
        self.lower_grav_limit = lower_grav_limit or self.lower_grav_limit
        self._step_feed_ = True
        self.honey_steps = list()

        available_water = self.kg_water
        available_honey = self.total_kg_honey
        water_used_for_honey = available_honey * self.step_feed_ratio
        available_honey_water = self.total_kg_honey + water_used_for_honey

        # when using honey & water as step feeding, if step ratio is < 0 it'll not use water
        honey_water_grav = 1 + ((self.honey_gravity - 1) / (1 + self.step_feed_ratio))

        ingredient_gravity_diff, ingredient_vol = self._get_ingredient_vol_grav()
        start_grav = 1 + ingredient_gravity_diff
        volume = self.kg_water + ingredient_vol - water_used_for_honey

        prt_qty = lambda f: f"Honey: {f / (1 + self.step_feed_ratio) * 1 * 1000:.0f}g, " \
                            f"Water: {f / (1 + self.step_feed_ratio) * self.step_feed_ratio * 1000:.0f}g"

        # first feeding
        honey_feed = volume * ((start_grav / self.upper_grav_limit) - 1) / \
                     (1 - (honey_water_grav / self.upper_grav_limit)) * honey_water_grav
        honey_feed = max(min(honey_feed, available_honey_water), 0)
        available_honey_water -= honey_feed

        honey_water_ingredient = Ingredient(f"Honey Water @1:{self.step_feed_ratio}", specific_gravity=honey_water_grav)

        self.honey_steps.append(
            honey_water_ingredient
            .with_quantity(honey_feed * 1000)
            .with_note(f"initial honey addition " + prt_qty(honey_feed))
        )

        step = 0
        # other feedings
        while available_honey_water > 0.00001:
            step += 1
            honey_feed = volume * ((self.lower_grav_limit / self.upper_grav_limit) - 1) / \
                         (1 - (honey_water_grav / self.upper_grav_limit)) * honey_water_grav
            honey_feed = max(min(honey_feed, available_honey_water), 0)
            available_honey_water -= honey_feed
            self.honey_steps.append(
                honey_water_ingredient
                .with_quantity(honey_feed * 1000)
                .with_note(f"Step {step} added at {self.lower_grav_limit:.3f}grav " + prt_qty(honey_feed))
            )

    def kg_honey_(self) -> float:
        """ returns the total honey weight in kilos based on step feeding items """
        return sum([a.weight() for a in self.honey_steps])

    def _get_ingredient_vol_grav(self) -> (float, float):
        """
        :return: ingredient_gravity_diff, ingredient_volume
        """
        ingredient_gravity_diff = 0
        ingredient_vol = 0
        for i in self.ingredients:
            i_vol = i.volume() / 1000 / self.product_weight
            ingredient_vol += i_vol
            ingredient_gravity_diff += i_vol * i.specific_gravity
        return ingredient_gravity_diff, ingredient_vol

    def calculate_ratios(self):
        """
        estimate the required amounts of honey and water to add to the base ingredients.
        Can give negative honey amounts if ingredients already have more sugar than the yeast will need.
        :return: None
        """
        ingredient_gravity_diff, ingredient_vol = self._get_ingredient_vol_grav()

        start_grav = self.start_gravity - ingredient_gravity_diff

        parts_water = (1 - ((start_grav - 1) / (self.honey_gravity - 1)))
        parts_honey = (((start_grav - 1) / (self.honey_gravity - 1)) * self.honey_gravity)

        self.kg_water = parts_water * (self.product_weight - ingredient_vol)
        self.total_kg_honey = parts_honey * (self.product_weight - ingredient_vol)
        self.initial_nitrogen: NitrogenSource = NitrogenSource.get("Honey").with_quantity(self.total_kg_honey * 1000)
        if self._step_feed_:
            self.step_feeding_setup()
        else:
            self.honey_steps = [Ingredient.get("Honey").with_quantity(self.total_kg_honey * 1000)]

    def add_ingredient(self, name: str, g: float = None, kg: float = None, qty_per_litre=False):
        """
        Add a single ingredient, can give wight in grans, kilograms, or both (summed)

        if :arg:`qty_per_litre` is `True` the given weight will be divided by the overall litre of the product

        :param kg: Quantity in Kilograms to be added
        :param g: Quantity in grams to be added
        :param name: Name as shown in [ingredients] dictionary
        :param qty_per_litre: use quantity on a per-litre basis
        :return:
        """

        match (g, kg):
            case (None, None):
                raise Exception("Adding an ingredient requires an amount to be added")
            case (x, None):
                quantity = x
            case (None, x):
                quantity = x * 1000
            case (x, y):
                quantity = x + y * 1000
            case _:
                return

        if name not in ingredients:
            raise IngredientNotImplemented(f"Item {name} not in Ingredients")
        if qty_per_litre:
            quantity = quantity * self.product_weight

        item = Ingredient.get(name).with_quantity(quantity)

        self.ingredients.append(item)

    def __repr__(self) -> str:
        self.calculate_ratios()

        out = f"Mead Calculation for {self.product_weight:.2f} litres of product"
        out += f"\n\tStart gravity (required) {self.start_gravity:.3f} "
        out += f"\n\tFinal gravity (sweetness) {self.final_gravity:.3f} "
        out += f"\n\tExpected ABV {self.expected_abv:.1f}% \n"
        out += f"Ingredients: "
        out += f"\n\tWater {self.kg_water:.3f}KG {self.kg_water:.3f}L \n"
        if self._step_feed_:
            out += f"\tTotal Honey {self.total_kg_honey:.3f}KG {self.total_kg_honey / self.honey_gravity:.3f}L\n"
        out += "".join([i.__str__() for i in self.ingredients])
        out += "".join([i.__str__() for i in self.honey_steps])
        out += f"Nitrogen requirement (YAN): {self.nitrogen_requirement * self._get_brix_():.2f}ppm * " \
               f"{self.product_weight}L = " \
               f"{self.nitrogen_requirement * self._get_brix_() * self.product_weight:.2f}mg\n"

        out += "".join([i.__str__() for i in self.nitrogen_sources])
        total_required_nitrogen = self._get_brix_() * self.nitrogen_requirement
        out += f"Current Nitrogen Load: {self.sum_nitrogen_load():.2f} \n" \
               f"Required Nitrogen Load: {total_required_nitrogen:.2f}\n"
        fermaid_k_use = sum([s.current_dose for s in self.nitrogen_sources if s.name == "Fermaid K"], 0)
        if fermaid_k_use > 0.5 * self.product_weight:
            out += f"Warning: Possibly using too much Fermaid K {fermaid_k_use / self.product_weight:.1f}g, " \
                   "US Law would recommend less than 0.5g/L\n"

        return out

    __str__ = __repr__

    def sum_nitrogen_load(self) -> float:
        """:return: total Nitrogen given in mg"""
        current_nitrogen = self.initial_nitrogen.use_source()

        for n in self.nitrogen_sources:
            current_nitrogen += n.use_source()
        return current_nitrogen

    def _get_brix_(self) -> float:
        """
        Note, brix calculation is not fantastic above 40°Bx,
        for current use cases (nitrogen load estimation) it doesn't matter much.
        :return: brix based on gravity
        """
        brix = (((182.4601 * self.start_gravity - 775.6821)
                 * self.start_gravity + 1262.7794)
                * self.start_gravity - 669.5622)
        return brix

    def calculate_nitrogen_expectations(self):
        """ Estimates the required nitrogen load based on the final abv of the mead and the yeast nitrogen demand """
        total_required_nitrogen = self._get_brix_() * self.nitrogen_requirement
        current_nitrogen = self.sum_nitrogen_load()
        print(f"required: {total_required_nitrogen:.2f}ppm current: {current_nitrogen:.2f}ppm")

    def add_nitrogen_source(self, source: str, g: float):
        """ Adds a source of nitrogen to the brew,
        :param source: Name of the nitrogen source, must be implemented in  :class:`NitrogenSource`
        """
        if source not in nitrogen_source:
            raise NitrogenSourceNotImplemented(f"Item {source} not in nitrogen_sources")

        item = nitrogen_source[source].with_quantity(g)
        self.nitrogen_sources.append(item)

    def set_nitrogen_demand_low(self):
        """Low nitrogen-demand: 7.5 ppm YAN per 1 °Brix.
        [Nutrient Data](https://www.piwine.com/media/pdf/yeast-selection-chart.pdf)"""
        self.nitrogen_requirement = 7.5 / 0.55

    def set_nitrogen_demand_medium(self):
        """Medium nitrogen-demand: 9 ppm YAN per 1 °Brix.
        [Nutrient Data](https://www.piwine.com/media/pdf/yeast-selection-chart.pdf)"""
        self.nitrogen_requirement = 9 / 0.55

    def set_nitrogen_demand_high(self):
        """High nitrogen-demand: 12.5 ppm YAN per 1 °Brix.
        [Nutrient Data](https://www.piwine.com/media/pdf/yeast-selection-chart.pdf)"""
        self.nitrogen_requirement = 12.5 / 0.55

    # noinspection SpellCheckingInspection
    class SNA:
        """
        SNA Options

        :var TOSNA: TOSNA schedule, similar to [meadmaderight.com](https://www.meadmaderight.com/tosna-calculator)
        :var Balathustrius: Balathustrius scheduler from [google docs](https://docs.google.com/spreadsheets/d/15VQe9BLk6TkLF5Fod7ghlRLIaRJJ07kQbPPMygu5Tyk/edit?gid=0#gid=0)
        :var phase_3: simple 3 phase additons of Fermaid O over the first 72 Hours
        """

        TOSNA: Final[str] = "TOSNA"  #
        Balathustrius: Final[str] = "Balathustrius"
        phase_3: Final[str] = "phase_3"
        phase_4: Final[str] = "phase_4"
        Bray_Denard_liquid: Final[str] = "Bray Denard Liquid"
        Bray_Denard_dry: Final[str] = "Bray Denard Dry"

    def staggered_nutrient_additions(self, preset: str = ""):
        """
        Automatic SNA (Staggered Nutrient Addition), or nutrient scheduler
        DO THIS LAST, it'll create useless results if other parts are modified after this

        most of these processes were taken from [r/mead/wiki](https://new.reddit.com/r/mead/wiki/process/nutrient_schedules/)

        :param preset: Options can be found in [Mead.SNA]
        :return:
        """
        n2_total = self._get_brix_() * self.nitrogen_requirement
        if preset.casefold() == self.SNA.TOSNA.casefold():
            print(f"Using {self.SNA.TOSNA} staggered nutrient additions")
            go_ferm = NitrogenSource.get("Go Ferm").with_quantity(0.3)
            ferm_k_grams = (n2_total - go_ferm.use_source()) / NitrogenSource.get("Fermaid K").nitrogen_ppm
            self.nitrogen_sources = [
                go_ferm,
                NitrogenSource.get("Fermaid K").with_quantity(ferm_k_grams / 4).with_note("24 Hours post pitch"),
                NitrogenSource.get("Fermaid K").with_quantity(ferm_k_grams / 4).with_note("48 Hours post pitch"),
                NitrogenSource.get("Fermaid K").with_quantity(ferm_k_grams / 4).with_note("72 Hours post pitch"),
                NitrogenSource.get("Fermaid K").with_quantity(ferm_k_grams / 4)
                .with_note("7 days post pitch or 1/3 sugar break"),
            ]
        elif preset.casefold() == self.SNA.Balathustrius.casefold():
            print(f"Using {self.SNA.Balathustrius} staggered nutrient additions")
            raise NotImplementedError("Sorry, haven't gotten around to this yet, I'd like to though")
        elif preset.casefold() == self.SNA.phase_3.casefold():
            print(f"Using {self.SNA.phase_3} staggered nutrient additions")
            ferm_o_grams = n2_total / NitrogenSource.get("Fermaid O").nitrogen_ppm
            self.nitrogen_sources = [
                NitrogenSource.get("Fermaid O").with_quantity(ferm_o_grams / 3).with_note("At  pitch"),
                NitrogenSource.get("Fermaid O").with_quantity(ferm_o_grams / 3).with_note("3 Days post pitch"),
                NitrogenSource.get("Fermaid O").with_quantity(ferm_o_grams / 3).with_note("7 Days post pitch"),
            ]
        elif preset.casefold() == self.SNA.phase_4.casefold():
            print(f"Using {self.SNA.phase_4} staggered nutrient additions")
            ferm_o_grams = n2_total / NitrogenSource.get("Fermaid O").nitrogen_ppm
            self.nitrogen_sources = [
                NitrogenSource.get("Fermaid O").with_quantity(ferm_o_grams / 4).with_note("At  pitch"),
                NitrogenSource.get("Fermaid O").with_quantity(ferm_o_grams / 4).with_note("1 Day post  pitch"),
                NitrogenSource.get("Fermaid O").with_quantity(ferm_o_grams / 4).with_note("3 Days post pitch"),
                NitrogenSource.get("Fermaid O").with_quantity(ferm_o_grams / 4).with_note("7 Days post pitch"),
            ]

        elif preset.casefold() == self.SNA.Bray_Denard_liquid.casefold() or \
                preset.casefold() == self.SNA.Bray_Denard_dry.casefold():
            print(f"Using {self.SNA.Bray_Denard_liquid} staggered nutrient additions")
            grav_arg = (self.upper_grav_limit if self._step_feed_ else self.start_gravity)

            self.nitrogen_sources = []
            self.nitrogen_sources.append(NitrogenSource.get("Potassium Carbonate")
                                         .with_quantity(0.4 * self.product_weight).with_note("Add at pitch"))
            if preset.casefold() == self.SNA.Bray_Denard_dry.casefold():
                self.nitrogen_sources.append(
                    NitrogenSource.get("Fermaid K")
                    .with_quantity(0.378 * self.product_weight).with_note("Add at pitch"))

            if grav_arg <= 1.090:
                self.nitrogen_sources.append(NitrogenSource.get("Fermaid O")
                                             .with_quantity(0.32 * self.product_weight).with_note("Add at pitch"))
                return

            ferm_o_grams = next(
                (a[1] for a in [(1.100, 0.32), (1.110, 0.40), (1.120, 0.52), (1.130, 0.56), (1.140, 0.64),
                                (1.150, 0.72)] if a[0] - 0.01 >= grav_arg), 0.72) * self.product_weight

            self.nitrogen_sources.append(NitrogenSource.get("Fermaid O")
                                         .with_quantity(ferm_o_grams / 3).with_note("At pitch"))
            self.nitrogen_sources.append(NitrogenSource.get("Fermaid O")
                                         .with_quantity(ferm_o_grams / 3).with_note("48 Hours post pitch"))
            self.nitrogen_sources.append(NitrogenSource.get("Fermaid O")
                                         .with_quantity(ferm_o_grams / 3).with_note("96 Hours post pitch"))
        else:
            raise UserWarning("That has not been implemented")

    sna = staggered_nutrient_additions


class NitrogenSource:
    nitrogen_source_dict: dict[str, Self] = dict()

    def __init__(self, name: str, *, nitrogen_ppm=0.0, parts_nitrogen_pct=0.0, note=""):
        """
        Conversion note: g/hl == mg/L == ppm

        :param name: name of the source, used to getting the source when used
        :type parts_nitrogen_pct: float :param nitrogen_pct: nitrogen that is accessible to the yeast by percent weight
        :type nitrogen_ppm: float :param nitrogen_ppm: nitrogen that is accessible to the yeast
        """
        self.name = name
        self.nitrogen_ppm: float = nitrogen_ppm if nitrogen_ppm else parts_nitrogen_pct * 1000

        self.current_dose = 0
        self.note = note
        self.nitrogen_source_dict[name] = self

    @classmethod
    def get(cls, item: str) -> Self:
        return cls.nitrogen_source_dict[item]

    def requested_quantity(self, required_ppm, litres):
        """
        :type required_ppm: float :param required_ppm: how much nitrogen is needed from this source per litre
        :type litres: float :param litres: how many litres is the batch
        :return: float
        """
        grams = required_ppm / self.nitrogen_ppm * litres
        return grams

    def with_quantity(self, grams) -> Self:
        """ Creates duplicate of :class:`self` with a given quantity to use"""
        new = copy.deepcopy(self)
        new.current_dose = grams
        return new

    def with_note(self, note) -> Self:
        new = copy.deepcopy(self)
        new.note = note
        return new

    def use_source(self):
        if self.current_dose == 0:
            raise Exception("dose must be set before use")

        return self.nitrogen_ppm * self.current_dose

    def __repr__(self) -> str:
        out = f"\tNitrogen Source: {self.current_dose:.1f}g @ {self.nitrogen_ppm:.1f}ppm " \
              f"= {self.nitrogen_ppm * self.current_dose:.1f}mg " \
              f" - Name: {self.name}{' - ' if len(self.note) > 1 else ''}{self.note}\n"
        return out

    __str__ = __repr__

    @staticmethod
    def get_source_list() -> list[str]:
        ls = list(NitrogenSource.nitrogen_source_dict.keys())
        ls.sort()
        return ls


class Ingredient:
    ingredient_dictionary: dict[str, Self] = dict()

    def __init__(self, name: str, *, sugar_per_100g=1.0, grams_per_ml=None, specific_gravity=None,
                 water_ml_per_gram=None,
                 per_item_name: str | None = None, per_item_grams: float | None = None):
        """
        grams per ml == sg

        sugar = :class:`Ingredient("Sugar", sugar_per_g=1, specific_gravity = 1.59)`
        honey = :class:`Ingredient("Honey", specific_gravity=1.435)`

        :param name:
        :param sugar_per_100g: for use with ml_per_g where item is not wholly sugar
        :param grams_per_ml: density in g/cm3
        :param specific_gravity: SG == grams per millilitre
        """
        self.name = name
        if specific_gravity is not None:
            self.specific_gravity = specific_gravity
        elif grams_per_ml is not None:
            self.specific_gravity = (grams_per_ml * sugar_per_100g / 100) + 1
        else:
            raise ValueError("No measurable SG")
        self.per_item: tuple[str, float] | None = None
        if per_item_name and per_item_grams:
            self.per_item: tuple[str, float] | None = (per_item_name, per_item_grams)
        self.parts_water_by_weight = water_ml_per_gram
        self.quantity = 0.0
        self.note: str = None
        self.ingredient_dictionary[name] = self

    @classmethod
    def get(cls, item: str) -> Self:
        return cls.ingredient_dictionary[item]

    def with_quantity(self, grams) -> Self:
        new = copy.deepcopy(self)
        new.quantity = grams
        return new

    def with_note(self, note: str) -> Self:
        new = copy.deepcopy(self)
        new.note = note
        return new

    def volume(self) -> float:
        return self.quantity * self.parts_water_by_weight

    def weight(self) -> float:
        return self.quantity

    def __repr__(self) -> str:
        out = f"\t{self.name} {self.quantity:.0f}g, "
        if self.per_item is not None:
            out += f"({self.quantity / self.per_item[1]:0.1f} {self.per_item[0]}) "
        out += f"{self.quantity / self.specific_gravity:.0f}ml " \
               f"{self.specific_gravity:.3f}grav " \
               f"{self.note if self.note is not None else ''}\n"
        return out

    __str__ = __repr__

    @staticmethod
    def get_source_list() -> list[str]:
        ls = list(Ingredient.ingredient_dictionary.keys())
        ls.sort()
        return ls


class NitrogenSourceNotImplemented(Exception):
    pass


class IngredientNotImplemented(Exception):
    pass


# Nitrogen Sources
nitrogen_source = NitrogenSource.nitrogen_source_dict
NitrogenSource("Mangrove Jack Beer Nutrient", parts_nitrogen_pct=0.007)
NitrogenSource("Mangrove Jack Wine Nutrient", parts_nitrogen_pct=0.14)
NitrogenSource("Fermaid O", nitrogen_ppm=40, note="add last")
NitrogenSource("Fermaid K", nitrogen_ppm=100, note="contains inorganic nitrogen")
NitrogenSource("Go Ferm", nitrogen_ppm=10, note="YAN contribution is insignificant, only use for starter")
NitrogenSource("DAP", nitrogen_ppm=210, note="mostly inorganic nitrogen, add early")
NitrogenSource("Honey", nitrogen_ppm=0)
NitrogenSource("Potassium Carbonate", nitrogen_ppm=0, note="Not Nitrogen, still useful")

# Ingredients
ingredients = Ingredient.ingredient_dictionary
Ingredient("Honey", specific_gravity=1.435)
Ingredient("Honey Water", specific_gravity=1.435)
Ingredient("Sugar", specific_gravity=1.59)
Ingredient("Orange", sugar_per_100g=9.35, grams_per_ml=0.72, water_ml_per_gram=0.86,
           per_item_name="fruit", per_item_grams=125)

Ingredient("Lemon", sugar_per_100g=2.52, grams_per_ml=0.95, water_ml_per_gram=0.923,
           per_item_name="fruit", per_item_grams=85)  # g/ml estimated
Ingredient("Lime", sugar_per_100g=1.69, grams_per_ml=0.95, water_ml_per_gram=0.883,
           per_item_name="fruit", per_item_grams=67)  # g/ml estimated

Ingredient("Peach", sugar_per_100g=8.39, grams_per_ml=0.998, water_ml_per_gram=0.89)
Ingredient("Cranberry Raw", sugar_per_100g=4.27, grams_per_ml=0.42, water_ml_per_gram=.873)
Ingredient("Cranberry Dried", sugar_per_100g=72.56, grams_per_ml=0.51, water_ml_per_gram=.157)
Ingredient("Beetroot", sugar_per_100g=6.76, grams_per_ml=0.57, water_ml_per_gram=.876)
Ingredient("Pumpkin", sugar_per_100g=2.76, grams_per_ml=0.68, water_ml_per_gram=.916)
Ingredient("Dragon Fruit", sugar_per_100g=9.75, grams_per_ml=0.59, water_ml_per_gram=.84)

Ingredient("Mint", sugar_per_100g=0, grams_per_ml=0.856, water_ml_per_gram=0.1,
           per_item_name="leaves", per_item_grams=0.15)

if __name__ == '__main__':
    print()
    mead = Mead(18, 1.000, product_weight=4.75, step_feeding=True)
    mead.add_ingredient("Lime", g=100)
    mead.add_ingredient("Mint", g=0.5)
    mead.set_nitrogen_demand_medium()
    mead.staggered_nutrient_additions(mead.SNA.Bray_Denard_dry)
    # mead.add_nitrogen_source("Fermaid K", 2.5)
    # mead.add_nitrogen_source("Fermaid O", 3.0)
    # mead.add_nitrogen_source("Fermaid O", 3.0)

    print(mead)
