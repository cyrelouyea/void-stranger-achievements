FORMAT = """title: {title}
description: Walk a total of {steps} step{plural}

// PATCH gml_Object_obj_player_Step_0 547
if obj_inventory.step_counter >= {steps}
    {{+achievement}}

// PATCH gml_Object_obj_player_Step_0 567
if obj_inventory.step_counter >= {steps}
    {{+achievement}}

// PATCH gml_Object_obj_player_Step_0 580
if obj_inventory.step_counter >= {steps}
    {{+achievement}}

// PATCH gml_Object_obj_player_Step_0 593
if obj_inventory.step_counter >= {steps}
    {{+achievement}}

// PATCH gml_Object_obj_player_Step_0 606
if obj_inventory.step_counter >= {steps}
    {{+achievement}}

// PATCH gml_Object_obj_player_Step_0 629
if obj_inventory.step_counter >= {steps}
    {{+achievement}}

// PATCH gml_Object_obj_player_Step_0 669
if obj_inventory.step_counter >= {steps}
    {{+achievement}}

// PATCH gml_Object_obj_player_Step_0 746
if obj_inventory.step_counter >= {steps}
    {{+achievement}}
"""

STEPS_LIMIT = [
    1, 10, 25, 50, 100, 250, 500, 
    1_000, 2_000, 3_000, 4_000, 5_000,
    10_000, 20_000, 30_000, 40_000, 42_195,
]

TITLES = {
    1: "Baby step",
    1_000: "I love walking",
    10_000: "Healthy runner",
    42_195: "Marathon runner",
}

for nb_steps in STEPS_LIMIT:
    with open(f"achievements/steps_{str(nb_steps).rjust(len(str(max(STEPS_LIMIT))), '0')}", "w") as f:
        f.write(FORMAT.format(
            steps=nb_steps, 
            plural="s" if nb_steps > 1 else "", 
            title=TITLES.get(nb_steps, f"{nb_steps} steps!")
        ))
