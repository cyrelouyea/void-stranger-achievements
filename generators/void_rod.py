FORMAT = """title: {title}
description: Use the void rod {number} times

// PATCH gml_Object_obj_player_Step_0 114
if ds_list_find_value(obj_inventory.ds_rcrds, 0) >= {number}
    {{+achievement}}
// PATCH gml_Object_obj_player_Step_0 825
if ds_list_find_value(obj_inventory.ds_rcrds, 0) >= {number}
    {{+achievement}}
"""

NUMBERS_LIMIT = [
    5, 10, 25, 50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 
    1_000, 2_000, 3_000, 4_000, 5_000,
    6_000, 7_000, 8_000, 9_000, 10_000
]

for number in NUMBERS_LIMIT:
    with open(f"achievements/void_rod_{number}", "w") as f:
        f.write(FORMAT.format(
            number=number,
            title=f"{number} tiles moved!"
        ))
