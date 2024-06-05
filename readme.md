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

As is my habit when faced with any amount of maths, I've made a python script. It's not all that pretty, thrown together
in an afternoon, but it will spit out some useful basic information about the planning stage of mead making, with
estimations of how much honey and water will be needed for the volume of end-product.

standard usage is to edit the script then run it, I'm too lazy to implement a CLI, the output will be as shown
below, depending on data given to it.

Currently, I've been using it to estimate how much honey I need to add for my fermentation to kill itself due to the
yeasts alcohol limit, while keeping some sweetness in the final mead, the calculations look correct, but should be
subject to a reasonable doubt when used; we've been sanity checking with other recipes.
<table>
<tr><td>6% Alcohol tolerance Yeast</td><td>15% Alcohol tolerance Yeast</td></tr>
<tr>
<td>

```
--- Mead Calculator ---
alcohol content 6%, for 5.00 litres of product 
1.07 KG honey, 4.25 KG water
SG: 1.06, FG: 1.02
```

</td>
<td>

```
--- Mead Calculator ---
alcohol content 15%, for 5.00 litres of product 
2.18 KG honey, 3.48 KG water
SG: 1.13, FG: 1.02
```

</td>



</tr>
</table>

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
- Sex on the beach
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
