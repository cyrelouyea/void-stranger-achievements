FORMAT = """title: {title}
description: {description} 

// PATCH gml_Object_obj_ex_dfenemy_missile_Step_0 64
if obj_inventory.stage_0_hit_counter >= {number}
{{+achievement}}

// PATCH gml_Object_obj_ex_levgiantstar_Step_0 305
if obj_inventory.stage_0_hit_counter >= {number}
{{+achievement}}

// PATCH gml_Object_obj_player_add_Step_0 381
if obj_inventory.stage_0_hit_counter >= {number}
{{+achievement}}

// PATCH gml_Object_obj_player_add_Step_0 933
if obj_inventory.stage_0_hit_counter >= {number}
{{+achievement}}

"""

NUMBERS = [
    1, 5, 10, 20, 30, 40, 
    50, 75, 100, 150, 200,
]

TITLES = {
    1: "Scratched",
    200: "Pain tolerance",
}

DESCRIPTIONS = {
    1: "Get hit in Stage 0"
}

for number in NUMBERS:
    with open(f"achievements/stage_0_hit_{str(number).rjust(len(str(max(NUMBERS))), '0')}", "w") as f:
        f.write(FORMAT.format(
            number=number,
            title=TITLES.get(number, f"Scratched ({number}/{max(NUMBERS)})"),
            description=DESCRIPTIONS.get(number, f"Get hit a total of {number} times in Stage 0")
        ))
