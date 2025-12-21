FORMAT = """title: {title}
description: Walk a total of {steps} step{plural}

// PATCH gml_Object_obj_player_Step_0 547
if ds_list_find_value(obj_inventory.ds_rcrds, 1) >= {steps}
    {{+achievement}}
// PATCH gml_Object_obj_player_Step_0 567
if ds_list_find_value(obj_inventory.ds_rcrds, 1) >= {steps}
    {{+achievement}}
// PATCH gml_Object_obj_player_Step_0 580
if ds_list_find_value(obj_inventory.ds_rcrds, 1) >= {steps}
    {{+achievement}}
// PATCH gml_Object_obj_player_Step_0 593
if ds_list_find_value(obj_inventory.ds_rcrds, 1) >= {steps}
    {{+achievement}}
// PATCH gml_Object_obj_player_Step_0 606
if ds_list_find_value(obj_inventory.ds_rcrds, 1) >= {steps}
    {{+achievement}}
// PATCH gml_Object_obj_player_Step_0 629
if ds_list_find_value(obj_inventory.ds_rcrds, 1) >= {steps}
    {{+achievement}}
// PATCH gml_Object_obj_player_Step_0 669
if ds_list_find_value(obj_inventory.ds_rcrds, 1) >= {steps}
    {{+achievement}}
// PATCH gml_Object_obj_player_Step_0 746
if ds_list_find_value(obj_inventory.ds_rcrds, 1) >= {steps}
    {{+achievement}}
"""

STEPS_LIMIT = [
    1, 10, 25, 50, 100, 250, 500, 
    1_000, 2_000, 3_000, 4_000, 5_000,
    10_000, 20_000, 30_000, 40_000, 50_000,
    100_000
]

TITLES = {
    1: "Baby step",
    1_000: "I love walking",
    10_000: "Healthy runner",
    100_000: "Marathon runner",
}

for nb_steps in STEPS_LIMIT:
    with open(f"achievements/steps_{nb_steps}", "w") as f:
        f.write(FORMAT.format(
            steps=nb_steps, 
            plural="s" if nb_steps > 1 else "", 
            title=TITLES.get(nb_steps, f"{nb_steps} steps!")
        ))
