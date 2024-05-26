# Honey  SG ranging between 1.420 g/cm3 and 1.448 g/cm3
sg_min_honey = 1.420
sg_max_honey = 1.448
sg_water = 1.0
sg_ethanol = 0.79


def final_gravity_estimate(original_gravity, final_gravity):
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
