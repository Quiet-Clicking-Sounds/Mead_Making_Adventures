# Honey  SG ranging between 1.420 g/cm3 and 1.448 g/cm3
import copy
from typing import Self

sg_min_honey = 1.420
sg_max_honey = 1.448
sg_water = 1.0
sg_ethanol = 0.79


def hydrometer_temperature_correction(
        measured_gravity: float, measured_temperature: float, calibration_temperature: float = 20):
    cal1 = 0.000134722124 * calibration_temperature
    cal2 = 0.00000204052596 * calibration_temperature ** 2
    cal3 = 0.00000000232820948 - calibration_temperature ** 3
    tmp1 = 0.000134722124 * measured_temperature
    tmp2 = 0.00000204052596 * measured_temperature ** 2
    tmp3 = 0.00000000232820948 * measured_temperature ** 3
    correction_factor = (1.00130346 - cal1 + cal2 - cal3) - (1.00130346 - tmp1 + tmp2 - tmp3)
    return measured_gravity * correction_factor


class Grav:
    def __init__(self, grav: float, temp: float, cal_temp: float = 20.0):
        self.calibration_temperature = cal_temp
        self.measured_gravity = grav
        self.measured_temperature = temp
        self.correct_gravity: float = 0
        self._correction()

    def _correction(self):
        cal1 = 0.000134722124 * self.calibration_temperature
        cal2 = 0.00000204052596 * self.calibration_temperature ** 2
        cal3 = 0.00000000232820948 - self.calibration_temperature ** 3
        tmp1 = 0.000134722124 * self.measured_temperature
        tmp2 = 0.00000204052596 * self.measured_temperature ** 2
        tmp3 = 0.00000000232820948 * self.measured_temperature ** 3
        self.correct_gravity = (1.00130346 - cal1 + cal2 - cal3) - (1.00130346 - tmp1 + tmp2 - tmp3)

    def __call__(self, *args, **kwargs) -> float:
        return self.correct_gravity


class Alcohol:
    def __init__(self, sg: Grav, fg: Grav):
        self.starting_gravity = sg
        self.final_gravity = fg
        self.alcohol_pct = (sg() - fg()) * 131

    def __call__(self) -> float:
        return self.alcohol_pct


def brix_to_grav(brix: float) -> float:
    return brix * 0.044


def grav_to_brix(grav: float) -> float:
    return grav / 0.044


class NitrogenSource:
    def __init__(self, name: str, *, nitrogen_ppm=0.0, parts_nitrogen_pct=0.0):
        """
        Conversion note: g/hl == mg/L == ppm

        :param name:
        :type parts_nitrogen_pct: float :param nitrogen_pct: nitrogen that is accessible to the yeast by percent weight
        :type nitrogen_ppm: float :param nitrogen_ppm: nitrogen that is accessible to the yeast
        """
        self.name = name
        self.nitrogen_ppm: float = nitrogen_ppm if nitrogen_ppm else parts_nitrogen_pct * 1000

        self.current_dose = 0

    def requested_quantity(self, required_ppm, litres):
        """
        :type required_ppm: float :param required_ppm: how much nitrogen is needed from this source per litre
        :type litres: float :param litres: how many litres is the batch
        :return: float
        """
        grams = required_ppm / self.nitrogen_ppm * litres
        return grams

    def with_quantity(self, litres) -> Self:
        new = copy.deepcopy(self)
        new.current_dose = litres
        return new

    def use_source(self):
        if self.current_dose == 0:
            raise Exception("dose must be set before use")
        print(f"Added Nitrogen Source: {self.name}, @{self.nitrogen_ppm:.1f}ppm * {self.current_dose:.1f}grams "
              f"totaling: {self.nitrogen_ppm * self.current_dose:.1f}")
        return self.nitrogen_ppm * self.current_dose


nitrogen_sources = {
    "Mangrove Jack Beer Nutrient": NitrogenSource("Mangrove Jack Beer Nutrient", parts_nitrogen_pct=0.007),
    "Mangrove Jack Wine Nutrient": NitrogenSource("Mangrove Jack Wine Nutrient", parts_nitrogen_pct=0.14),
    "Fermaid O": NitrogenSource("Fermaid O",  nitrogen_ppm=40),
    "Fermaid K": NitrogenSource("Fermaid K",  nitrogen_ppm=100),
    "DAP": NitrogenSource("DAP",  nitrogen_ppm=210),
    "Honey": NitrogenSource("Honey",  nitrogen_ppm=48.2),
}


class Mead:
    """
    This is a real work in progress, finding a way to display useful information about what a mead may require
    YAN = Yeast assimilable nitrogen
    :param self.nitrogen_requirement: required amount of nitrogen in the mead for 1% abv
    """

    def __init__(self, abv: float, final_gravity: float = 1.000, product_volume=5, honey_gravity=1.43):
        """

        :param abv: in percentage points (5% == 5)
        :param final_gravity: preferred sweetness, 1.02 is a middling sweet mead
        :param honey_gravity: gravity of the honey being used, if known
        """
        self.expected_abv = abv
        self.final_gravity = final_gravity
        self.start_gravity = self.final_gravity + (self.expected_abv / 131)
        self.honey_gravity = 1.43

        self.product_volume = product_volume
        self.kg_water = 1 - ((self.start_gravity - 1) / (self.honey_gravity - 1))
        self.kg_honey = ((self.start_gravity - 1) / (self.honey_gravity - 1)) * self.honey_gravity

        self.nitrogen_requirement = 7.5 / 0.55
        self.initial_nitrogen: NitrogenSource = nitrogen_sources["Honey"].with_quantity(self.kg_honey)
        self.nitrogen_sources: list[NitrogenSource] = list()

    def calculate_nitrogen_expectations(self):
        total_required_nitrogen = self.expected_abv * self.nitrogen_requirement
        current_nitrogen = self.initial_nitrogen.use_source()

        for n in self.nitrogen_sources:
            current_nitrogen += n.use_source()
        print(f"required: {total_required_nitrogen:.2f}ppm current: {current_nitrogen:.2f}ppm")

    def add_nitrogen_source(self, source: NitrogenSource, qty: float):
        self.nitrogen_sources.append(source.with_quantity(qty))

    def set_nitrogen_demand_low(self):
        """Low nitrogen-demand: 7.5 ppm YAN per 1 °Brix."""
        self.nitrogen_requirement = 7.5 / 0.55

    def set_nitrogen_demand_medium(self):
        """Medium nitrogen-demand: 9 ppm YAN per 1 °Brix."""
        self.nitrogen_requirement = 9 / 0.55

    def set_nitrogen_demand_high(self):
        """High nitrogen-demand: 12.5 ppm YAN per 1 °Brix."""
        self.nitrogen_requirement = 12.5 / 0.55


def abv_estimate(original_gravity, final_gravity):
    # predict the final abv of a fermented drink
    return (original_gravity - final_gravity) * 131


def estimate_final_gravity(alcohol_content, original_gravity):
    return original_gravity - (alcohol_content / 131)


def required_original_gravity(alcohol_content, final_gravity):
    return final_gravity + (alcohol_content / 131)


def auto_compute(finished_gravity_pref=1.02, yeast_tolerance_pct=14, end_litres=5, sg_of_honey=1.43):
    magic_number = 135
    # 104 = yeast@14
    sg_drop = yeast_tolerance_pct / magic_number
    sg_start = finished_gravity_pref + sg_drop
    # water in KG
    required_water = 1 - ((sg_start - 1) / (sg_of_honey - 1))
    # honey in KG
    required_honey = (sg_start - 1) / (sg_of_honey - 1) * sg_of_honey

    print(f"\n--- Mead Calculator ---\n"
          f"alcohol content {yeast_tolerance_pct:.0f}%, "
          f"for {end_litres:.2f} litres of product \n"
          f"{required_honey * end_litres:.2f} KG honey, "
          f"{required_water * end_litres:.2f} KG water\n"
          f"SG: {sg_start:.2f}, FG: {finished_gravity_pref:.2f}")
    if sg_start > 1.14:
        print("Alert: Mead over 1.14 SG may stall, add additional sugar content when below 1.09 Grav")


if __name__ == '__main__':
    mead = Mead(5, 1.02)

    mead.add_nitrogen_source(nitrogen_sources["Mangrove Jack Beer Nutrient"], 3.5)
    mead.add_nitrogen_source(nitrogen_sources["Fermaid K"], 2.5)
    mead.calculate_nitrogen_expectations()

    if False:
        auto_compute(yeast_tolerance_pct=6)
        auto_compute()

        # https://brew2bottle.co.uk/collections/wine-yeast/products/gervin-yeasts?variant=15349934620787
        auto_compute(yeast_tolerance_pct=12)
        auto_compute(yeast_tolerance_pct=15)
        auto_compute(yeast_tolerance_pct=18)
        auto_compute(yeast_tolerance_pct=21)

        # sweet mead https://www.themaltmiller.co.uk/product/wyeast-4184-sweet-mead/?v=79cba1185463
        auto_compute(yeast_tolerance_pct=11)
        # 5-10%er https://www.themaltmiller.co.uk/product/wlp090-san-diego-super-yeast/?v=79cba1185463
        # 17% dry mead https://www.themaltmiller.co.uk/product/wyeast-4021-dry-white-sparkling/?v=79cba1185463
