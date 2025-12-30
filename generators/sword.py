FORMAT = """title: {title}
description: Use the sword a total of {number} times

// PATCH gml_Object_obj_player_Step_0 1247
if obj_inventory.sword_counter >= {number}
    {{+achievement}}

// PATCH gml_Object_obj_npc_gor_Alarm_3 5
if obj_inventory.sword_counter >= {number}
    {{+achievement}}

// PATCH gml_Object_obj_gor_cube_Step_0 24
if obj_inventory.sword_counter >= {number}
    {{+achievement}}
"""

NUMBERS = [
    1, 5, 10, 20, 30, 40, 50,
    100, 200, 300, 400, 500
]

TITLES = {
    1: "En garde!",
    500: "Flash Fencer",
}

for number in NUMBERS:
    with open(f"achievements/sword_{str(number).rjust(len(str(max(NUMBERS))), '0')}", "w") as f:
        f.write(FORMAT.format(
            number=number,
            title=TITLES.get(number, f"En garde! ({number}/{max(NUMBERS)})")
        ))
