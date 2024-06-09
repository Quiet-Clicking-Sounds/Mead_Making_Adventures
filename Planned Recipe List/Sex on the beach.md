# Sex on the beach
```text
Mead Calculation for 5.00 litres of product
	Start gravity (required) 1.102 
	Final gravity (sweetness) 1.010 
	Expected ABV 12.0% 
Ingredients: 
	Water 4.271KG 4.271L 
	Peach 100g, 92ml 1.084grav 
	Orange 50g, (0.4 fruit) 47ml 1.067grav 
	Cranberry Raw 75g, 74ml 1.018grav 
	Honey 987g, 687ml 1.435grav 
Nitrogen requirement (YAN): 394.76ppm * 5L = 1973.80mg
	Nitrogen Source: 2.5g @ 100.0ppm = 250.0mg  - Name: Fermaid K - contains inorganic nitrogen
	Nitrogen Source: 3.5g @ 40.0ppm = 140.0mg  - Name: Fermaid O - add last
Current Nitrogen Load: 390.00 
Required Nitrogen Load: 394.76
```




### generator code for this mead
```python
from mead import Mead
mead = Mead(12, 1.010, product_weight=5, step_feeding=False)
mead.add_ingredient("Peach", g=100)
mead.add_ingredient("Orange", g=50)
mead.add_ingredient("Cranberry Raw", g=75)
mead.set_nitrogen_demand_medium()
mead.add_nitrogen_source("Fermaid K", 2.5)
mead.add_nitrogen_source("Fermaid O", 3.5)
```
