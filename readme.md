# Mead Making Adventures

Making mead with a buddy, The following and included files are a compilation of information about what we've done.

This is not a guide, no really it's essentially a checklist of stuff we might or might not have brought and or done.

## Recipes We've Started

- [#1 Standard Mead](Recipe%20List%2F%231%20Standard.md)
- [#2 Elderflower Mead](Recipe%20List%2F%232%20Elderflower.md)

## Yeasts I'd like to use

- [12% Gervin Yeast](https://brew2bottle.co.uk/collections/wine-yeast/products/gervin-yeasts?variant=15349934620787)
- [11% Wyeast sweet mead ](https://www.themaltmiller.co.uk/product/wyeast-4184-sweet-mead/?v=79cba1185463)
- [5-10%er WLP90 San-diego](https://www.themaltmiller.co.uk/product/wlp090-san-diego-super-yeast/?v=79cba1185463)
-
    - [wpl90 calculator](https://yeastman.com/calculator)
- [17% dry mead Wyeast ](https://www.themaltmiller.co.uk/product/wyeast-4021-dry-white-sparkling/?v=79cba1185463)

[more yeast ideas](https://new.reddit.com/r/mead/comments/96o93j/what_yeast_is_best_to_use/)

[Some Yeast Nutrient Requirements](https://www.piwine.com/media/pdf/yeast-selection-chart.pdf)

## Yeast Nutrients

which we should probably use

- Fermat K (Vitamins and yeast hulls)
- DAP (Diamonium Phosphate)


- Don't use these again, not enough information about usage available for them
    - [mangrove jacks beer nutrient](https://www.themaltmiller.co.uk/product/mangrove-jacks-beer-nutrient-15g/?v=79cba1185463)
    - [mangrove jacks wine nutrient](https://www.themaltmiller.co.uk/product/mangrove-jacks-wine-nutrient-23-5g/?v=79cba1185463)

## Fermentation Enders

potassium meta-bisulfate is used to stop the fermentation
[potassium metabisulphate / campden tabs](https://www.themaltmiller.co.uk/product/sodium-metabisulphite-100g-campden/?v=79cba1185463)
possible to ignore this if yeast only works to x% alc? (this is only a good idea for higher % meads)

[Polyfloral Honey](https://www.honeymakers.co.uk/products/polyfloral-honey-bucket-33lb) from the local area will be used
in all the planned meads, because we brought 15 kilos of it

Fermentation will be done in 1 Gallon / 5 litre demijohns, with bubbler airlocks

## The Python bit

As is my habit when faced with any amount of maths, I've made a python script.

At first this script was small, and rather ungainly it's now gone through a few iterations where I've made it more
modifiable; there are now two ways to run the script.

### mead.py

first option is the open [mead.py](/mead.py) and modify anything within the `if __name__ == '__main__':` portion of the
script (or import as shown below),this should allow fast re-running and simple modification for anyone who knows a
little python. I hope the way I've structured the python file will make things self-explanatory, and the current
demonstration version will make usage simple.

Below I've shown the inputs and outputs for a 16% Dragonfruit mead (note I've not made this, it's just to show how the
program will work)

```python
from mead import Mead

if __name__ == '__main__':
    print()
    mead = Mead(16, 1.005, product_weight=5, step_feeding=True)
    mead.add_ingredient("Dragon Fruit", g=500)
    mead.set_nitrogen_demand_medium()
    mead.add_nitrogen_source("Fermaid K", 1.5)
    mead.add_nitrogen_source("Fermaid O", 1.5)
    print(mead)
```

And the commandline output will look like this:

```text
Mead Calculation for 5.00 litres of product
	Start gravity (required) 1.127 
	Final gravity (sweetness) 1.005 
	Expected ABV 16.0% 
Ingredients: 
	Water 4.478KG 4.478L 
	Total Honey 0.626KG 0.438L
	Dragon Fruit 500g, 473ml 1.058grav 
	Honey 221g, 154ml 1.435grav initial honey addition
	Honey 405g, 283ml 1.435grav Step 1 added at 1.050grav
Nitrogen requirement (YAN): 484.08ppm * 5L = 2420.39mg
	Nitrogen Source: 1.5g @ 100.0ppm = 150.0mg  - Name: Fermaid K - contains inorganic nitrogen
	Nitrogen Source: 1.5g @ 40.0ppm = 60.0mg  - Name: Fermaid O - add last
Current Nitrogen Load: 210.00 
Required Nitrogen Load: 484.08
```

### interactive.py

The second option is [interactive.py](/interactive.py) which is an interactive wrapper around mead.py, this will ask
the user questions about how they wish to construct a mead; I've used Fuzzy matching for any text input to hopefully
make entering information much less arduous.

### User modification of mead.py

I have yet to add all the ingredients and nitrogen sources I would like to this script, I plan to add a more appropriate
data source for both ingredients and nitrogen sources, currently they are added in python itself.

To include your own source ingredient or nitrogen you will need to add the following lines:

```python 
from mead import *

Ingredient(
    'Ingredient Name',  # The name of your new ingredient
    sugar_per_100g=12.4,  # shown on most common food labels [This is the important one]
    grams_per_ml=0.95,  # can be found via Google [estimates are acceptable] 
    water_ml_per_gram=0.955  # how much is water [estimates are acceptable]
)

NitrogenSource(
    "Fermaid K",  # the name of the nitrogen source
    nitrogen_ppm=100,  # this is equivalent to g/hl 
    parts_nitrogen_pct=0.007,  # can be used in place of nitrogen_ppm, as some suppliers show this not ppm 
    note="contains inorganic nitrogen"  # Optional note will be shown in final print, useful for reminders
)

```

## Acids

- Tartaric Acid
    - Found in: grapes and few other fruits,
- Malic Acid
    - Found in: Green Apples
- Citric Acid
    - Found in: Citrus fruits
- Sorbic Acid
    - used to preserve sweet wines
        - > In the European Union, the amount of sorbic acid that can be added is limited — no more than 200 mg/L. Most
          humans
          have a detection threshold of 135 mg/L, with some having a sensitivity to detect its presence at 50
          mg/L. <sup>[wiki](https://en.wikipedia.org/wiki/Acids_in_wine#Sorbic)</sup>

### seemingly random notes

- Chlorophyll induces bitterness in mead

### Planned Meads

The long list of things that might taste nice, or might just be interesting enough to try, they'll move above
once we've attempted to make them

- Wild Violet
    - requires a lot, 10 cups of violet petals per gallon
    - Contains [Anthocyanin](https://en.wikipedia.org/wiki/Anthocyanin) which causes the pigmentation
    - [buying option](https://www.pollyspetals.co.uk/product/edible-freeze-dried-natural-violet-viola-flower-heads-cake-decoration-cocktail-garnish-food-grade-culinary-uk-grown-dried/)
- [black crowberry](https://en.wikipedia.org/wiki/Empetrum_nigrum)
    - Contains [Anthocyanin](https://en.wikipedia.org/wiki/Anthocyanin) which causes the pigmentation
    - [buying option](https://www.rawliving.co.uk/products/dried-crowberry-powder-100g-islensk-hollusta?variant=40752788504715&currency=GBP&utm_medium=product_sync&utm_source=google&utm_content=sag_organic&utm_campaign=sag_organic&srsltid=AfmBOoq5-gKRgPIGt0PBj5e7dJsq6QzE_oIChfAFNiQ3wZKotVNOKsK0314)
- Lemon & Lavender
- Blood orange
- Lime and Chilli
- Strawberry and elderflower
- Raspberry
- Rhubarb
- Cocao nibs
- Lemon and ginger
- Dandelion
- Mint
- Blackberry
- Ginger
- Apple and cinnamon
- Rose hip / blossom
    - Make a rose hip tea
- Mulberries
- Wineberry
    - Find some dried ones?
- Nettle mead
- Turmeric mead
- Carrot & Parsnip
- turnip & beetroot
- Beetroot
- Horseradish
- Honeysuckle
- Aniseed
- Pumpkin
- Persimmon
- Gooseberry
- Greengage (like plumbs)
- Passion fruit
- Pomegranate
- [Fortified Mojito](Planned%20Recipe%20List/Fortified%20Mojito.md)
- [Sex on the beach](Planned%20Recipe%20List/Sex%20on%20the%20beach.md)
    - the usual cocktail consists of
        - 4 cl Vodka
        - 2 cl Peach schnapps
        - 4 cl Orange juice
        - 4 cl Cranberry juice
    - converting to base pt by weight, n
        - Peach 1pt
            - normal peach mead looks to be around 25% peach to 75% honey
            - how strong is the peach flavour of peach schnapps? probably less strong than peaches themselves
        - Orange
            - 1 orange (31 grams) per litre of fluid
        - Cranberry 2pt
            - 1.3kg of cranberries per gal ? that seems excessive
        - thoughts on quantities: per 5 litres of product
            - Peach 500g
            - Orange 100g
            - Cranberry 250g
