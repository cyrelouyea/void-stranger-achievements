FORMAT = """title: {room_number}
description: Go to trailer room no. 1

// PATCH gml_Room_{room_name}_Create 1
if ds_grid_get(obj_inventory.ds_player_info, 22, 1) != 1000
    {{+achievement}}
"""


ROOM_NAMES = [
    "rm_trailer_001",
    "rm_trailer_002",
    "rm_trailer_003",
    "rm_trailer_004",
    "rm_trailer_005",
    "rm_trailer_006",
    "rm_trailer_007",
    "rm_trailer_008",
    "rm_trailer_009",
    "rm_trailer_010",
    "rm_trailer_012",
    "rm_trailer_013",
    "rm_trailer_014",
    "rm_trailer_015",
    "rm_trailer_016",
    "rm_trailer_017",
    "rm_trailer_018",
    "rm_trailer_019",
    "rm_trailer_020",
    "rm_trailer_021",
    "rm_trailer_022",
    "rm_trailer_023",
    "rm_trailer_024",
    "rm_trailer_025",
    "rm_trailer_026",
    "rm_trailer_027",
    "rm_trailer_028",
    "rm_trailer_011",
]

for index, room_name in enumerate(ROOM_NAMES):
    with open(f"achievements/room_et{str(index+1).rjust(2, '0')}", "w") as f:
        f.write(FORMAT.format(room_number=f"ET{str(index+1).rjust(2, '0')}", room_name=room_name))