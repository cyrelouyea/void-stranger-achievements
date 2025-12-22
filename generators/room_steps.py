FORMAT = """title: {title}
description: Walk {steps} step{plural} in a single room

// PATCH gml_Object_obj_player_Step_0 547
if ds_grid_get(obj_inventory.ds_player_info, 3, 0) >= {steps}
    {{+achievement}}
// PATCH gml_Object_obj_player_Step_0 567
if ds_grid_get(obj_inventory.ds_player_info, 3, 0) >= {steps}
    {{+achievement}}
// PATCH gml_Object_obj_player_Step_0 580
if ds_grid_get(obj_inventory.ds_player_info, 3, 0) >= {steps}
    {{+achievement}}
// PATCH gml_Object_obj_player_Step_0 593
if ds_grid_get(obj_inventory.ds_player_info, 3, 0) >= {steps}
    {{+achievement}}
// PATCH gml_Object_obj_player_Step_0 606
if ds_grid_get(obj_inventory.ds_player_info, 3, 0) >= {steps}
    {{+achievement}}
// PATCH gml_Object_obj_player_Step_0 629
if ds_grid_get(obj_inventory.ds_player_info, 3, 0) >= {steps}
    {{+achievement}}
// PATCH gml_Object_obj_player_Step_0 669
if ds_grid_get(obj_inventory.ds_player_info, 3, 0) >= {steps}
    {{+achievement}}
// PATCH gml_Object_obj_player_Step_0 746
if ds_grid_get(obj_inventory.ds_player_info, 3, 0) >= {steps}
    {{+achievement}}
"""

STEPS_LIMIT = [
    100, 500,
    1_000, 2_000, 3_000, 4_000, 5_000,
    6_000, 7_000, 8_000, 9_000, 10_000
]

TITLES = {
    1_000: "Walk, then think",
    10_000: "Playtester (S)",
}

for nb_steps in STEPS_LIMIT:
    with open(f"achievements/steps_room_{nb_steps}", "w") as f:
        f.write(FORMAT.format(
            steps=nb_steps, 
            plural="s" if nb_steps > 1 else "", 
            title=TITLES.get(nb_steps, f"S{str(nb_steps).rjust(4, '0')}")
        ))
