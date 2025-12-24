FORMAT = """title: {title}
description: Use the void rod {number} times in a single room

// PATCH gml_Object_obj_player_Step_0 1144
if ds_grid_get(obj_inventory.ds_player_info, 3, 1) >= {number}
    {{+achievement}}
// PATCH gml_Object_obj_player_Step_0 825
if ds_grid_get(obj_inventory.ds_player_info, 3, 1) >= {number}
    {{+achievement}}
"""

VOID_LIMIT = [
    100, 1_000, 10_000
]

TITLES = {
    10_000: "Playtester (V)",
}

for nb_void in VOID_LIMIT:
    with open(f"achievements/void_rod_room_{nb_void}", "w") as f:
        f.write(FORMAT.format(
            number=nb_void, 
            title=TITLES.get(nb_void, f"V{str(nb_void).rjust(4, '0')}")
        ))
