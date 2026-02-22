FORMAT = """title: {title}
description: Create a total of {number} tiles from the effect of a certain statue

// PATCH gml_Object_obj_boulder_Step_0 830
if obj_inventory.tile_maker_counter >= {number}
{{+achievement}}

// PATCH gml_Object_obj_boulder_Step_0 925
if obj_inventory.tile_maker_counter >= {number}
{{+achievement}}
"""

NUMBERS = [
    5, 10, 20, 30, 40, 50, 
    75, 100, 200, 250
]

TITLES = {
    "Professional tiler": 250
}

for number in NUMBERS:
    with open(f"achievements/tile_maker_{str(number).rjust(len(str(max(NUMBERS))), '0')}", "w") as f:
        f.write(FORMAT.format(
            number=number,  
            title=TITLES.get(number, f"Tile layer ({number}/{max(NUMBERS)})")
        ))
