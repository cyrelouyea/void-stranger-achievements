FORMAT = """title: {room_number}
description: {description}

// PATCH gml_Room_{room_name}_Create 1
{{+achievement}}
"""


ROOM_NAMES = [
    ("rm_e_intermission", "DIS?",),
    ("rm_dis_gate", "The Gate",),
    ("rm_e_001", "D01"),
    ("rm_e_023", "D02"),
    ("rm_e_004", "D03"),
    ("rm_e_002", "D04"),
    ("rm_e_006", "D05"),
    ("rm_e_007", "D06"),
    ("rm_e_018", "D07"),
    ("rm_e_009", "D08"),
    ("rm_e_005", "D09"),
    ("rm_e_010", "D10"),
    ("rm_e_026", "D11"),
    ("rm_e_012", "D12"),
    ("rm_e_019", "D13"),
    ("rm_e_011", "D14"),
    ("rm_e_013", "D15"),
    ("rm_e_017", "D16"),
    ("rm_e_014", "D17"),
    ("rm_e_024", "D18"),
    ("rm_e_015", "D19"),
    ("rm_e_022", "D20"),
    ("rm_e_025", "D21"),
    ("rm_e_020", "D22"),
    ("rm_e_016", "D23"),
    ("rm_e_008", "D24"),
    ("rm_e_003", "D25"),
    ("rm_e_021", "D26"),
    ("rm_e_027", "D27"),
    ("rm_e_000", "D28"),
    ("rm_return_000", "D28.5"),
    ("rm_fb_000", "D29"),
    ("rm_fb_001", "D30"),
    ("rm_test_0005", "D31"),
    ("rm_fb_002", "D32"),
    ("rm_fb_003", "D33"),
    ("rm_fb_004", "D34"),
    ("rm_fb_005", "D35"),
    ("rm_test_0007", "D36"),
    ("rm_fb_006", "D37"),
    ("rm_dis_room_ready", "Heart of DIS")
]



for index, (room_name, room_number) in enumerate(ROOM_NAMES):
    with open(f"achievements/room_d{str(index+1).rjust(2, '0')}", "w") as f:
        f.write(FORMAT.format(
            description=f"Reach {room_number}",
            room_number=room_number,
            room_name=room_name
        ))