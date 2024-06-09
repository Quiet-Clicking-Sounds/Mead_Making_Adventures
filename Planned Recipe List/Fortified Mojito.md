# Fortified Mojito Mead
```python
from mead import Mead
mead = Mead(18, 1.018, product_weight=5, step_feeding=True)
mead.add_ingredient("Lime", g=320)
mead.add_ingredient("Mint", g=1.5)
mead.set_nitrogen_demand_medium()
mead.add_nitrogen_source("Fermaid K", 4)
mead.add_nitrogen_source("Fermaid O", 2)
mead.add_nitrogen_source("Fermaid O", 2)
```
```text
Mead Calculation for 5.00 litres of product
	Start gravity (required) 1.155 
	Final gravity (sweetness) 1.018 
	Expected ABV 18.0% 
Ingredients: 
	Water 3.817KG 3.817L 
	Total Honey 1.610KG 1.126L
	Lime 320g, 4.8 fruit 315ml 1.016grav 
	Mint 2g, 10.0 leaves 2ml 1.000grav 
	Honey 714g, 498ml 1.435grav initial honey addition
	Honey 839g, 585ml 1.435grav Step 1 added at 1.050grav
	Honey 57g, 40ml 1.435grav Step 2 added at 1.050grav
Nitrogen requirement (YAN): 579.02ppm * 5L = 2895.09mg
	Nitrogen Source: 4.0g @ 100.0ppm = 400.0mg  - Name: Fermaid K - contains inorganic nitrogen
	Nitrogen Source: 2.0g @ 40.0ppm = 80.0mg  - Name: Fermaid O - add last
	Nitrogen Source: 2.0g @ 40.0ppm = 80.0mg  - Name: Fermaid O - add last
Current Nitrogen Load: 560.00 
Required Nitrogen Load: 579.02

Final additions Rum to 24% ABV
```
