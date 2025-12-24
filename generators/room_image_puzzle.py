FORMAT = """title: Gray's memories #{number}
description: Find the jigsaw puzzle #{number} 

// PATCH gml_Room_{room_name}_Create 1
{{+achievement}}
"""

FORMAT_SOLVED = """title: Gray's memories #{number} (Solved)
description: Solve the jigsaw puzzle #{number} 

// PATCH gml_Object_obj_puzzlepieces_Step_0 139
if room == {room_name}
    {{+achievement}}"""

ROOMS = [
    "rm_graysmemories_001",
    "rm_graysmemories_002",
    "rm_graysmemories_003",
    "rm_graysmemories_004",
    "rm_graysmemories_005",
    "rm_graysmemories_006",
]

for index, room_name in enumerate(ROOMS):
    with open(f"achievements/room_graysmemories_{index+1}", "w") as f:
        f.write(FORMAT.format(number=index+1, room_name=room_name))

    with open(f"achievements/graysmemories_solved_{index+1}", "w") as f:
        f.write(FORMAT_SOLVED.format(number=index+1, room_name=room_name))