FORMAT = """title: {title}
description: Detonate a total of {number} bomb tiles

// PATCH gml_Object_obj_explofloor_vanish_Create_0 10
if obj_inventory.bomb_floor_counter >= {number}
    {{+achievement}}
"""

NUMBERS = [
    10, 20, 30, 40, 50, 
    100, 200, 300, 400, 500,
    1_000,
]

TITLES = {
    1_000: "Living detonator"
}

for number in NUMBERS:
    with open(f"achievements/tiles_bomb_floor_{number}", "w") as f:
        f.write(FORMAT.format(
            number=number,  
            title=TITLES.get(number, f"*Kaboom* ({number}/{max(NUMBERS)})")
        ))
