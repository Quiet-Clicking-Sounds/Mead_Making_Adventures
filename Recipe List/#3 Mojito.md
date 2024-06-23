Dom's Mint and Lime pre Mojito

```
Mead Calculation for 4.75 litres of product
	Start gravity (required) 1.137 
	Final gravity (sweetness) 1.000 
	Expected ABV 18.0% 
Ingredients: 
	Water 3.427KG 3.427L 
	Total Honey 1.865KG 1.304L
	Lime 100g, (1.5 fruit) 98ml 1.016grav 
	Mint 1g, (4.0 leaves) 1ml 1.000grav 
	Honey 1211g, 844ml 1.435grav initial honey addition
	Honey 654g, 455ml 1.435grav Step 1 added at 1.050grav
Nitrogen requirement (YAN): 519.02ppm * 4.75L = 2465.34mg
	Nitrogen Source: 2.5g @ 100.0ppm = 250.0mg  - Name: Fermaid K - contains inorganic nitrogen
	Nitrogen Source: 3.0g @ 40.0ppm = 120.0mg  - Name: Fermaid O - add last
	Nitrogen Source: 3.0g @ 40.0ppm = 120.0mg  - Name: Fermaid O - add last
Current Nitrogen Load: 490.00 
Required Nitrogen Load: 519.02
```

``` python
    print()
    mead = Mead(18, 1.000, product_weight=4.75, step_feeding=True)
    mead.add_ingredient("Lime", g=100)
    mead.add_ingredient("Mint", 0.15*4)
    mead.set_nitrogen_demand_medium()
    mead.add_nitrogen_source("Fermaid K", 2.5)
    mead.add_nitrogen_source("Fermaid O", 3.0)
    mead.add_nitrogen_source("Fermaid O", 3.0)
    print(mead)
```
