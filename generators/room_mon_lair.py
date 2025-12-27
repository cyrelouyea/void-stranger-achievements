FORMAT = """title: {room_number}
description: Go to {room_number}

// PATCH gml_Room_{room_name}_Create 1
{{+achievement}}
"""


ROOM_NAMES = [
    ("rm_mon_001", "Secret Lair",),
    ("rm_mon_002", "M01",),
    ("rm_mon_003", "M02",),
    ("rm_mon_004", "M03",),
    ("rm_mon_005", "M04",),
    ("rm_mon_006", "M05",),
    ("rm_mon_007", "M06",),
    ("rm_mon_008", "M07",),
    ("rm_mon_009", "M08",),
    ("rm_mon_010", "M09",),
    ("rm_mon_011", "M10",),
    ("rm_mon_012", "M11",),
    ("rm_mon_013", "M12",),
    ("rm_mon_014", "M13",),
    ("rm_mon_015", "M14",),
    ("rm_test_0006", "M15",),
    ("rm_mon_016", "M16",),
]



for index, (room_name, room_number) in enumerate(ROOM_NAMES):
    with open(f"achievements/room_m{str(index+1).rjust(2, '0')}", "w") as f:
        f.write(FORMAT.format(
            room_number=room_number,
            room_name=room_name
        ))