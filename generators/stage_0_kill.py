FORMAT = """title: {title}
description: {description} 

// PATCH gml_Object_obj_ex_dfenemy_006_Other_11	104
if obj_inventory.stage_0_kill_counter >= {number}
{{+achievement}}

// PATCH gml_Object_obj_ex_levenemy_002_Other_11 64	
if obj_inventory.stage_0_kill_counter >= {number}
{{+achievement}}

// PATCH gml_Object_obj_ex_dfenemy_003_Other_11	69
if obj_inventory.stage_0_kill_counter >= {number}
{{+achievement}}

// PATCH gml_Object_obj_ex_dfenemy_002_Other_11	135
if obj_inventory.stage_0_kill_counter >= {number}
{{+achievement}}

// PATCH gml_Object_obj_ex_dfenemy_001_Other_11	64
if obj_inventory.stage_0_kill_counter >= {number}
{{+achievement}}

// PATCH gml_Object_obj_ex_levenemy_001_Other_11 64
if obj_inventory.stage_0_kill_counter >= {number}
{{+achievement}}

// PATCH gml_Object_obj_ex_lev_extra_Other_11 11
if destroyer_id == 0 && obj_inventory.stage_0_kill_counter >= {number}
    {{+achievement}}

// PATCH gml_Object_obj_ex_dfenemy_005_Other_11	70
if obj_inventory.stage_0_kill_counter >= {number}
{{+achievement}}

// PATCH gml_Object_obj_ex_lev_final_Step_0	104   
if obj_inventory.stage_0_kill_counter >= {number}
{{+achievement}}

// PATCH gml_Object_obj_ex_dfenemy_004_Other_11	74
if obj_inventory.stage_0_kill_counter >= {number}
{{+achievement}}

// PATCH gml_Object_obj_ex_levenemy_003_Other_11 82
if obj_inventory.stage_0_kill_counter >= {number}
{{+achievement}}
"""

NUMBERS = [
    1, 50, 100, 250, 500, 1_000,
    2_000, 3_000, 4_000, 5_000, 10_000
]

TITLES = {
    1: "Pilot fighter",
    10_000: "Endless Struggle",
}

DESCRIPTIONS = {
    1: "Kill an enemy in Stage 0"
}

for number in NUMBERS:
    with open(f"achievements/stage_0_kill_{str(number).rjust(len(str(max(NUMBERS))), '0')}", "w") as f:
        f.write(FORMAT.format(
            number=number,
            title=TITLES.get(number, f"Pilot fighter ({number}/{max(NUMBERS)})"),
            description=DESCRIPTIONS.get(number, f"Kill a total of {number} enemies in Stage 0")
        ))
