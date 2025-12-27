FORMAT = """title: {room_number}
description: Go to {room_number}

// PATCH gml_Room_{room_name}_Create 1
{{+achievement}}
"""


ROOM_NAMES = [
    ("rm_bee_001", "Stinky Hole",),
    ("rm_bee_002", "S01"),
    ("rm_bee_003", "S02"),
    ("rm_bee_004", "S03"),
    ("rm_bee_005", "S04"),
    ("rm_bee_006", "S05"),
    ("rm_bee_007", "S06"),
    ("rm_bee_008", "S07"),
    ("rm_bee_009", "S08"),
    ("rm_bee_010", "S09"),
    ("rm_bee_011", "S10"),
    ("rm_bee_012", "S11"),
    ("rm_bee_013", "S12"),
    ("rm_bee_014", "S13"),
    ("rm_misc_0002", "S14"),
    ("rm_bee_015", "S15"),
]



for index, (room_name, room_number) in enumerate(ROOM_NAMES):
    with open(f"achievements/room_s{str(index+1).rjust(2, '0')}", "w") as f:
        f.write(FORMAT.format(
            room_number=room_number,
            room_name=room_name
        ))