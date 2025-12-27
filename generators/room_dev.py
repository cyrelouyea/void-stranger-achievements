FORMAT = """title: {room_number}
description: Go to {room_number}

// PATCH gml_Room_{room_name}_Create 1
{{+achievement}}
"""


ROOM_NAMES = [
    ("rm_ee_000", "SE00",),
    ("rm_ee_001", "SE01",),
    ("rm_ee_002", "SE02",),
    ("rm_ee_003", "SE03",),
    ("rm_ee_004", "SE04",),
    ("rm_ee_005", "SE05",),
    ("rm_ee_006", "SE06",),
    ("rm_ee_007", "SE07",),
    ("rm_ee_008", "SE08",),
]



for index, (room_name, room_number) in enumerate(ROOM_NAMES):
    with open(f"achievements/room_se{str(index+1).rjust(2, '0')}", "w") as f:
        f.write(FORMAT.format(
            room_number=room_number,
            room_name=room_name
        ))