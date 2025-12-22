FORMAT = """title: {title}
description: Spawn a total of {number} shades with copy tiles

// PATCH gml_Object_obj_enemy_cr_Create_0 1
if obj_inventory.copy_floor_counter >= {number}
    {{+achievement}}

// PATCH gml_Object_obj_enemy_cr_segment_Create_0 1
if obj_inventory.copy_floor_counter >= {number}
    {{+achievement}}
"""

NUMBERS = [
    10, 20, 30, 40, 50, 
    100, 200, 300, 400, 500,
    1_000,
]

TITLES = {
    1_000: "Shadowbringer"
}

for number in NUMBERS:
    with open(f"achievements/tiles_copy_floor_{number}", "w") as f:
        f.write(FORMAT.format(
            number=number,  
            title=TITLES.get(number, f"*Bwooop* ({number}/{max(NUMBERS)})")
        ))
