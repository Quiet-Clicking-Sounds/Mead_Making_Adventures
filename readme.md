# Mead Making Adventures

Making mead with a buddy, The following and included files are a compilation of information about what we've done.

This is not a guide, no really it's essentially a checklist of stuff we might or might not have brought and or done.

## Recipes We've Started

[//]: # (- [1_Standard.md]&#40;Recipe%20List/1_Standard.md&#41;)

[//]: # (- [2_Elderflower.md]&#40;Recipe%20List/2_Elderflower.md&#41;)

[//]: # (- [3_Mojito.md]&#40;Recipe%20List/3_Mojito.md&#41;)

[//]: # (- [4_Orange_and_Chilli.md]&#40;Recipe%20List/4_Orange_and_Chilli.md&#41;)

We've been running multiple meads at a time, each row is started on the same day; generally they use a similar amount of
honey and the same yeast, with the differing factor being the taste additions


<table>
    <tr>
        <td><a href="Recipe%20List/1_Standard.md"> 1 Standard.md</a></td>
        <td><a href="Recipe%20List/2_Elderflower.md"> 2 Elderflower.md</a></td>
    </tr>
    <tr>
        <td><img title="1_Standard.png" src="Recipe%20List/1_Standard.png"></td>
        <td><img title="2_Elderflower.png" src="Recipe%20List/2_Elderflower.png"></td>
    </tr>
    <tr>
        <td><a href="Recipe%20List/3_Mojito.md"> 3 Mojito.md</a></td>
        <td><a href="Recipe%20List/4_Orange_and_Chilli.md"> 4 Orange and Chilli.md</a></td>
    </tr>
    <tr>
        <td><img title="3_Mojito.png" src="Recipe%20List/3_Mojito.png"></td>
        <td><img title="4_Orange_and_Chilli.png" src="Recipe%20List/4_Orange_and_Chilli.png"></td>
    </tr>
    <tr>
        <td><a href="Recipe%20List/5_Standard_Base_A.md"> 5 Standard Base A.md</a></td>
        <td><a href="Recipe%20List/5_Standard_Base_B.md"> 5 Standard Base B.md</a></td>
    </tr>
    <tr>
        <td><img title="5_Standard_Base_A.png" src="Recipe%20List/5_Standard_Base_A.png"></td>
        <td><img title="5_Standard_Base_B.png" src="Recipe%20List/5_Standard_Base_B.png"></td>
    </tr>
    <tr>
        <td colspan="2">
        5A and 5B became:<br>
        <a href="Recipe%20List/5_1_Standard_Base_With_Raspberry.md"> 5.1 Standard Base With Raspberry</a><br>
        <a href="Recipe%20List/5_2_Standard_Base_With_Lemon_Lavendar.md"> 5.2 Standard Base With Lemon and Lavendar</a><br>
        <a href="Recipe%20List/5_3_Standard_Base_Plain.md"> 5.3 Standard Base Plain</a><br>
        <a href="Recipe%20List/5_4_Standard_Base_With_Cucumber.md"> 5.4 Standard Base With Cucumber</a><br>
        <a href="Recipe%20List/5_5_Standard_Base_Tails_with_Lemon.md"> 5.5 Standard Base Tails with Lemon</a>
        </td>
    </tr>
</table>

## Yeasts I'd like to use

- [12% Gervin Yeast](https://brew2bottle.co.uk/collections/wine-yeast/products/gervin-yeasts?variant=15349934620787)
- [11% Wyeast sweet mead ](https://www.themaltmiller.co.uk/product/wyeast-4184-sweet-mead/?v=79cba1185463)
- [5-10%er WLP90 San-diego](https://www.themaltmiller.co.uk/product/wlp090-san-diego-super-yeast/?v=79cba1185463)
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
    mead = Mead(18, 1.000, product_weight=4.75, step_feeding=True)
    mead.add_ingredient("Lime", g=100)
    mead.add_ingredient("Mint", g=0.5)
    mead.set_nitrogen_demand_medium()
    mead.staggered_nutrient_additions(mead.SNA.Bray_Denard_dry)
    print(mead)
```

And the commandline output will look like this:

```text
Mead Calculation for 4.75 litres of product
	Start gravity (required) 1.137 
	Final gravity (sweetness) 1.000 
	Expected ABV 18.0% 
Ingredients: 
	Water 3.427KG 3.427L 
	Total Honey 1.865KG 1.304L
	Lime 100g, (1.5 fruit) 98ml 1.016grav 
	Mint 0g, (3.3 leaves) 0ml 1.000grav 
	Honey Water @1:1 1355g, 1115ml 1.215grav initial honey addition Honey: 678g, Water: 678g
	Honey Water @1:1 835g, 688ml 1.215grav Step 1 added at 1.050grav Honey: 418g, Water: 418g
	Honey Water @1:1 835g, 688ml 1.215grav Step 2 added at 1.050grav Honey: 418g, Water: 418g
	Honey Water @1:1 704g, 579ml 1.215grav Step 3 added at 1.050grav Honey: 352g, Water: 352g
Nitrogen requirement (YAN): 519.02ppm * 4.75L = 2465.34mg
	Nitrogen Source: 1.9g @ 0.0ppm = 0.0mg  - Name: Potassium Carbonate - Add at pitch
	Nitrogen Source: 1.8g @ 100.0ppm = 179.6mg  - Name: Fermaid K - Add at pitch
	Nitrogen Source: 0.6g @ 40.0ppm = 25.3mg  - Name: Fermaid O - At pitch
	Nitrogen Source: 0.6g @ 40.0ppm = 25.3mg  - Name: Fermaid O - 48 Hours post pitch
	Nitrogen Source: 0.6g @ 40.0ppm = 25.3mg  - Name: Fermaid O - 96 Hours post pitch
Current Nitrogen Load: 255.55 
Required Nitrogen Load: 519.02
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

### AutoGraph.py

Graphing utility made to add graphics to the RecipeList items; when run it will 'automatically' create or update the
graphs shown in the recipe list.

## Acids

- Tartaric Acid
    - Found in: Grapes
- Malic Acid
    - Found in: Green Apples
    - Probably the go-to for adding acidity to meads, less extreme than using Citric
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

#### The short list

Meads we're planning to start in November 2024; probably aiming to brew to 8-10% with a wine yeast

- Cucumber Mead
    - brewed dry
- Rhubarb Mead
- Root Vegetable Mead
    - Carrot
    - Beetroot
    - Parsnip
    - Extracting the taste of root vegetables could be interesting
        - foremost idea is currently to blend the vegetables after freexing them, then squeeze the juice out,
          finally extracting more taste by making an infusion with the leftover solids
- Lemon and Lavendar
    - Lemon
    - Lavendar (flowers)
    - notes
        - Extracting taste from the lemon, possibly using high proof alcohol to extract the oils in the zest
        -

---

#### The long list

The long list of things that might taste nice, or might just be interesting enough to try, they'll move above
once we've attempted to make them

Berry Meads

- Sea Buck Thorne Berry <sup>[wiki](https://en.wikipedia.org/wiki/Hippophae)</sup>
    - taste: astringent, sour, and oily
    - contains Malic Acid, may be useful to
      use  [malolactic fermentation](https://en.wikipedia.org/wiki/Malolactic_fermentation), winemaking stuff
    - proposed 5grams per litre?
      via [homebrew thread](https://www.homebrewtalk.com/threads/sea-buckthorn-berries.512882/)
    - 37.5g/L for a cider recipe via [omegafruit](https://omegafruit.ca/sea-buckthorn-berry-cider-recipe/)
- Mulberries / [black crowberry](https://en.wikipedia.org/wiki/Empetrum_nigrum)
    - Contains [Anthocyanin](https://en.wikipedia.org/wiki/Anthocyanin) which causes the pigmentation
    - [buying option](https://www.rawliving.co.uk/products/dried-crowberry-powder-100g-islensk-hollusta?variant=40752788504715&currency=GBP&utm_medium=product_sync&utm_source=google&utm_content=sag_organic&utm_campaign=sag_organic&srsltid=AfmBOoq5-gKRgPIGt0PBj5e7dJsq6QzE_oIChfAFNiQ3wZKotVNOKsK0314)

Flower Meads

- Wild Violet
    - requires a lot, 10 cups of violet petals per gallon
    - Contains [Anthocyanin](https://en.wikipedia.org/wiki/Anthocyanin) which causes the pigmentation
    - [buying option](https://www.pollyspetals.co.uk/product/edible-freeze-dried-natural-violet-viola-flower-heads-cake-decoration-cocktail-garnish-food-grade-culinary-uk-grown-dried/)
- orange blossom
- Dandelion
- Honeysuckle
- Rose hip / blossom
    - Make a rose hip tea

Fruit Meads

- Blood orange
- Raspberry
- Blackberry
- Wineberry
    - Find some dried ones?
- Greengage (like plumbs)
- Persimmon
- Gooseberry
- Passion fruit
- Pomegranate

Vegetable Meads

- Rhubarb
- Rhubarb and Raspberry
- Carrot & Parsnip
- turnip & beetroot
- Beetroot
- Horseradish
- Pumpkin

Herbal Meads

- Mint
    - Don't do this as alone, use with other things, possibly lots of herbs mead?
- Aniseed
- Nettle mead

Other Meads:

- Cocao nibs
- Ginger
- Turmeric mead

Multi Meads

- Lemon & Lavender
- Lemon and ginger
- Strawberry and elderflower
- Apple and cinnamon
- Lime and

Cocktail base Meads

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

### even more ideas taken from desert flavourings mostly

The first group of these are from ["The Flavour Thesaurus" by Niki Segnit]

- Chocolate
    - anise, cardamom, chilli, cinnamon, coffee, ginger, mint, nutmeg, rose, thyme
    - all the things, a chocolate mead might be lovely, but it would need to be added in secondary I think
- Coffee
    - cardamom, cinnamon, clove, coriander seed, ginger, rose, vanilla.
    - note: acidity of coffee, should check if that needs to be added in secondary
- Cherry
    - cinnamon, vanilla.
- Watermelon
    - chilli, cinnamon, coriander leaf, mint, rosemary.
        - thought: coriander may pair badly with honey
- Grape
    - anise, rosemary.
- Strawberry
    - anise, cinnamon, mint, vanilla.
- Pineapple
    - anise, chilli, cinnamon, sage, vanilla.
    - smaller idea: anise, sage, vanilla
- Apple
    - anise, cinnamon, rose, sage, vanilla.
- Pear
    - anise, cardamom, cinnamon.
- Banana
    - anise, cinnamon, vanilla.
- Melon
    - anise, mint, rose.
- Apricot
    - cardamom, cinnamon, ginger, rose, rosemary, vanilla.
- Peach
    - clove, vanilla.

## quick list: how much should be added?

- Cinnamon
    - 1stick /
      gallon [from](https://gotmead.com/blog/making-mead/mead_recipes/joes-ancient-orange-clove-and-cinnamon-mead/)
    - 0.2-0.4 sticks / litre [from]https://www.georgetimmermans.com/cinnamon-mead.html
    - notes: [reddit thread](https://new.reddit.com/r/mead/comments/6yakbm/cinnamon_mead_questions/)
- Vanilla
    - 0.14 Pods / litre [from](https://revolutionfermentation.com/en/blogs/fermented-beverages/vanilla-mead-recipe/)
    - 1 bean / 5
      litres  [reddit thread](https://new.reddit.com/r/mead/comments/88jvls/want_to_make_a_vanilla_bean_mead_is_it_best_to/)

## more thoughts

- Chia Seeds / Guam Gum / Xantham Gum
    - could be used in higher proof meads to make them less 'watery'?
    - supposedly use to improve 'mouth feel', but im still not sure how that relates..
    - could be fun to make thickened mead? 
