FORMAT = """title: Another hint ({number})
description: Find the {ordinal} riddle orb

// PATCH gml_Object_obj_npc_riddle_Create_0 87
if room == {room_name} && j_check != 0 && !global.failure && tip_location == 0 && tip_number <= 5
{{+achievement}}"""


ORDINALS = {
    1: "first",
    2: "second",
    3: "third",
    4: "fourth",
    5: "fifth",
    6: "sixth",
    7: "seventh",
    8: "eighth",
}

ROOM_NAMES = [
    "rm_0055",
    "rm_0078",
    "rm_rest_area_6",
    "rm_0204",
    "rm_0251",
]

for index, room_name in enumerate(ROOM_NAMES):
    with open(f"achievements/npc_riddle_{index+1}", "w") as f:
        f.write(FORMAT.format(ordinal=ORDINALS[index+1], room_name=room_name, number=index+1))