FORMAT = """title: Secret crystal #{number}
description: Find and collect the secret crystal #{number}

// PATCH gml_GlobalScript_scr_savetoken 35
if room == {room_name}
    {{+achievement}}
"""

ROOMS = [
    "rm_0025",
    "rm_0043",
    "rm_0067",
    "rm_0107",
    "rm_0128",
    "rm_0151",
    "rm_0185",
    "rm_0223",
]


for number, room_name in enumerate(ROOMS):
    with open(f"achievements/memory_crystals_secret_{number + 1}", "w") as f:
        f.write(FORMAT.format(
            number=number + 1,
            room_name=room_name
        ))
