FORMAT_NORMAL = """title: Puzzle master ({room_number})
description: Solve {room_number} with Lillie by taking the stairs and without using the sword, the wings or the upgraded rod.

// PATCH gml_Object_obj_exit_Alarm_0 40
if global.loop == 1 && room == {room_name} && !global.endless_used && !global.sword_used && !global.wings_used
{{+achievement}}"""

FORMAT_NINNIE = """title: Puzzle m-master ({room_number})
description: Solve {room_number} with Lillie by taking the stairs and without using the sword, the wings or the upgraded rod. Y-You can't abandon Ninnie!

// PATCH gml_Object_obj_exit_Alarm_0 40
if global.loop == 1 && room == {room_name} && !global.endless_used && !global.sword_used && !global.wings_used {{
    with (obj_npc_friend) {{
        if friend_state == 1 && f_path_exists {{
            {{+achievement}}
        }}
    }}
}}"""

with open("generators/burdenless_hard.txt", "r") as f:
    text = f.read()

for line in text.splitlines():
    room_data = line.split()

    room_number = room_data[0].strip().rjust(3, "0")
    room_name = room_data[1].strip()
    
    if len(room_data) > 2:
        with_ninnie = room_data[2].strip() == "N"
    else:
        with_ninnie = False

    with open(f"achievements/puzzle_master_b{room_number}", "w") as f:
        if not with_ninnie:
            f.write(FORMAT_NORMAL.format(room_number=f"B{room_number}", room_name=room_name))
        else:
            f.write(FORMAT_NINNIE.format(room_number=f"B{room_number}", room_name=room_name))