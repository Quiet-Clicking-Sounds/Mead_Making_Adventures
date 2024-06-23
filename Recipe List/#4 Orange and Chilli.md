Rob's Chilli and Orange Mead

```
Mead Calculation for 4.75 litres of product
	Start gravity (required) 1.132 
	Final gravity (sweetness) 1.010 
	Expected ABV 16.0% 
Ingredients: 
	Water 3.788KG 3.788L 
	Total Honey 1.312KG 0.917L
	Orange 250g, (2.0 fruit) 234ml 1.067grav 
	Red Chillis 75g Grav = N/A
	Honey 859g, 598ml 1.435grav initial honey addition
	Honey 453g, 316ml 1.435grav Step 1 added at 1.050grav
Nitrogen requirement (YAN): 501.16ppm * 4.75L = 2380.52mg
	Nitrogen Source: 2.5g @ 100.0ppm = 250.0mg  - Name: Fermaid K - contains inorganic nitrogen
	Nitrogen Source: 3.0g @ 40.0ppm = 120.0mg  - Name: Fermaid O - add last
	Nitrogen Source: 3.0g @ 40.0ppm = 120.0mg  - Name: Fermaid O - add last
Current Nitrogen Load: 490.00 
Required Nitrogen Load: 501.16

```


``` python
    print()
    mead = Mead(16, 1.010, product_weight=4.75, step_feeding=True)
    mead.add_ingredient("Orange", g=250)
    mead.set_nitrogen_demand_medium()
    mead.add_nitrogen_source("Fermaid K", 2.5)
    mead.add_nitrogen_source("Fermaid O", 3.0)
    mead.add_nitrogen_source("Fermaid O", 3.0)
    print(mead)
```
