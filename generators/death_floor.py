FORMAT = """title: {title}
description: Activate a total of {number} instant death tiles

// PATCH gml_Object_obj_deathfloor_Step_2 13
if obj_inventory.death_floor_counter >= {number}
    {{+achievement}}

// PATCH gml_Object_obj_deathfloor_Step_2 34
if obj_inventory.death_floor_counter >= {number}
    {{+achievement}}

// PATCH gml_Object_obj_deathfloor_Step_2 66
if obj_inventory.death_floor_counter >= {number}
    {{+achievement}}
"""

NUMBERS = [
    10, 20, 30, 40, 50, 
    100, 200, 300, 400, 500,
    1_000,
]

TITLES = {
    1_000: "Zeus"
}

for number in NUMBERS:
    with open(f"achievements/tiles_death_floor_{number}", "w") as f:
        f.write(FORMAT.format(
            number=number,  
            title=TITLES.get(number, f"*Psssshhh* ({number}/{max(NUMBERS)})")
        ))
