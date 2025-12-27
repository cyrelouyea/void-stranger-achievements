FORMAT = """title: {room_number}
description: Go to {room_number}

// PATCH gml_Room_{room_name}_Create 1
{{+achievement}}
"""


ROOM_NAMES = [
    ("rm_ex_lev_001", "L01",),
    ("rm_ex_lev_002", "L02",),
    ("rm_ex_lev_003", "L03",),
    ("rm_ex_lev_004", "L04",),
    ("rm_ex_lev_005", "L05",),
    ("rm_ex_lev_006", "L06",),
    ("rm_ex_lev_007", "L07",),
    ("rm_ex_lev_008", "L08",),
]



for index, (room_name, room_number) in enumerate(ROOM_NAMES):
    with open(f"achievements/room_l{str(index+1).rjust(2, '0')}", "w") as f:
        f.write(FORMAT.format(
            room_number=room_number,
            room_name=room_name
        ))